"""SQLite による進捗の永続化：習熟度・解答履歴・Leitner・問題統計。"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from .models import DIFFICULTY_WEIGHT

# Leitner の箱ごとの再出題間隔（秒）
LEITNER_INTERVALS = {1: 0, 2: 1 * 86400, 3: 2 * 86400, 4: 4 * 86400, 5: 8 * 86400}
INITIAL_MASTERY = 50.0


class Store:
    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS mastery (
                scope TEXT PRIMARY KEY,
                score REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS attempt (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT NOT NULL,
                correct INTEGER NOT NULL,
                chosen TEXT NOT NULL,
                ts REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS leitner (
                question_id TEXT PRIMARY KEY,
                box INTEGER NOT NULL,
                due_ts REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS question_stat (
                question_id TEXT PRIMARY KEY,
                seen INTEGER NOT NULL DEFAULT 0,
                correct INTEGER NOT NULL DEFAULT 0,
                wrong_labels TEXT NOT NULL DEFAULT '{}'
            );
            """
        )
        # 既存DBの移行：誤答原因（自己申告）列を後付けする
        cols = {r["name"] for r in self.conn.execute("PRAGMA table_info(attempt)").fetchall()}
        if "cause" not in cols:
            self.conn.execute("ALTER TABLE attempt ADD COLUMN cause TEXT")
        self.conn.commit()

    # ---- 習熟度 ----
    def get_mastery(self, scope: str) -> float:
        row = self.conn.execute("SELECT score FROM mastery WHERE scope=?", (scope,)).fetchone()
        return row["score"] if row else INITIAL_MASTERY

    def all_mastery(self) -> dict[str, float]:
        rows = self.conn.execute("SELECT scope, score FROM mastery").fetchall()
        return {r["scope"]: r["score"] for r in rows}

    def _set_mastery(self, scope: str, score: float) -> None:
        score = max(0.0, min(100.0, score))
        self.conn.execute(
            "INSERT INTO mastery(scope, score) VALUES(?,?) "
            "ON CONFLICT(scope) DO UPDATE SET score=excluded.score",
            (scope, score),
        )

    # ---- 解答記録 ----
    def record_answer(self, question, chosen: set[str], correct: bool, k: float = 0.3) -> int:
        """解答を記録し、作成した attempt の id を返す（誤答原因の後付け記録に使う）。

        `chosen` は選択ラベル集合。空集合は呼び出し側（QuizScreen）で弾く前提。
        """
        now = time.time()
        cur = self.conn.execute(
            "INSERT INTO attempt(question_id, correct, chosen, ts) VALUES(?,?,?,?)",
            (question.id, int(correct), json.dumps(sorted(chosen)), now),
        )
        attempt_id = cur.lastrowid
        assert attempt_id is not None  # AUTOINCREMENT の INSERT 直後は必ず採番される

        # 習熟度更新（難易度で重み付け）
        w = DIFFICULTY_WEIGHT.get(question.difficulty, 1.0)
        for scope in question.scopes():
            s = self.get_mastery(scope)
            if correct:
                s += (100 - s) * k * w
            else:
                s -= s * k * (2 - w)  # easy(w=0.6)→係数1.4で減点大、hard(w=1.4)→係数0.6
            self._set_mastery(scope, s)

        # Leitner 更新
        box = self.get_box(question.id)
        if correct:
            box = min(5, box + 1)
        else:
            box = 1
        self.conn.execute(
            "INSERT INTO leitner(question_id, box, due_ts) VALUES(?,?,?) "
            "ON CONFLICT(question_id) DO UPDATE SET box=excluded.box, due_ts=excluded.due_ts",
            (question.id, box, now + LEITNER_INTERVALS[box]),
        )

        # 問題統計（誤選択肢分析）
        row = self.conn.execute(
            "SELECT seen, correct, wrong_labels FROM question_stat WHERE question_id=?",
            (question.id,),
        ).fetchone()
        seen, cor, wrong = (row["seen"], row["correct"], json.loads(row["wrong_labels"])) if row else (0, 0, {})
        seen += 1
        cor += int(correct)
        if not correct:
            for lbl in chosen - question.correct_labels:
                wrong[lbl] = wrong.get(lbl, 0) + 1
        self.conn.execute(
            "INSERT INTO question_stat(question_id, seen, correct, wrong_labels) VALUES(?,?,?,?) "
            "ON CONFLICT(question_id) DO UPDATE SET seen=excluded.seen, correct=excluded.correct, "
            "wrong_labels=excluded.wrong_labels",
            (question.id, seen, cor, json.dumps(wrong)),
        )
        self.conn.commit()
        return attempt_id

    def set_cause(self, attempt_id: int, cause: str) -> None:
        """直近の解答（attempt）に誤答原因の自己申告を紐づける。"""
        self.conn.execute("UPDATE attempt SET cause=? WHERE id=?", (cause, attempt_id))
        self.conn.commit()

    def wrong_questions(self) -> list[dict]:
        """問題ごとの最新解答が「誤答」のものを、新しい順に返す。

        各要素: {question_id, chosen(list[str]), cause(str|None), ts(float)}。
        最新が正解の問題は「克服済み」とみなして除外する。
        """
        rows = self.conn.execute(
            """
            SELECT a.question_id, a.correct, a.chosen, a.cause, a.ts
            FROM attempt a
            JOIN (SELECT question_id, MAX(id) AS mid FROM attempt GROUP BY question_id) last
              ON a.id = last.mid
            WHERE a.correct = 0
            ORDER BY a.ts DESC
            """
        ).fetchall()
        return [
            {
                "question_id": r["question_id"],
                "chosen": json.loads(r["chosen"]),
                "cause": r["cause"],
                "ts": r["ts"],
            }
            for r in rows
        ]

    def cause_counts(self) -> dict[str, int]:
        """誤答の自己申告原因の集計（cause が記録された解答のみ）。"""
        rows = self.conn.execute(
            "SELECT cause, COUNT(*) AS c FROM attempt "
            "WHERE correct = 0 AND cause IS NOT NULL GROUP BY cause"
        ).fetchall()
        return {r["cause"]: r["c"] for r in rows}

    # ---- Leitner ----
    def get_box(self, question_id: str) -> int:
        row = self.conn.execute(
            "SELECT box FROM leitner WHERE question_id=?", (question_id,)
        ).fetchone()
        return row["box"] if row else 1

    def get_due(self, question_id: str) -> float:
        row = self.conn.execute(
            "SELECT due_ts FROM leitner WHERE question_id=?", (question_id,)
        ).fetchone()
        return row["due_ts"] if row else 0.0

    def all_due(self) -> dict[str, float]:
        """全問題の due_ts を1クエリで取得（適応選択の N+1 回避用）。"""
        rows = self.conn.execute("SELECT question_id, due_ts FROM leitner").fetchall()
        return {r["question_id"]: r["due_ts"] for r in rows}

    # ---- 統計 ----
    def question_stats(self) -> dict[str, dict]:
        rows = self.conn.execute(
            "SELECT question_id, seen, correct, wrong_labels FROM question_stat"
        ).fetchall()
        return {
            r["question_id"]: {
                "seen": r["seen"],
                "correct": r["correct"],
                "wrong_labels": json.loads(r["wrong_labels"]),
            }
            for r in rows
        }

    def total_attempts(self) -> int:
        return self.conn.execute("SELECT COUNT(*) AS c FROM attempt").fetchone()["c"]

    def close(self) -> None:
        self.conn.close()
