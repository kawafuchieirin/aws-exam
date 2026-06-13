"""適応出題エンジン：習熟度＋Leitner＋難易度適合度で出題順を決める。"""
from __future__ import annotations

import random
import time

from .models import DOMAINS, TAG_TO_FUNDAMENTAL, Option, Question
from .store import INITIAL_MASTERY, Store

# 優先度の重み（SPEC 4.4）
W_DUE = 2.0       # Leitner 復習期限
W_WEAK = 1.5      # 苦手領域
W_FIT = 1.0       # 難易度適合
W_FRESH = 0.5     # 鮮度
STALE_PENALTY = 0.5

_DIFF_LEVEL = {"easy": 25.0, "medium": 55.0, "hard": 80.0}


def _priority(
    q: Question,
    now: float,
    mastery: dict[str, float],
    stats: dict[str, dict],
    due_map: dict[str, float],
) -> float:
    """事前取得した状態（mastery/stats/due）から優先度を計算する（DBアクセスなし）。"""
    # 復習期限：due を過ぎているほど高い
    due = due_map.get(q.id, 0.0)
    overdue = 0.0
    if due and due <= now:
        overdue = min(1.0, (now - due) / (3 * 86400) + 0.3)

    # 苦手：サービス＋タグの平均習熟度が低いほど高い
    scopes = q.scopes()
    avg_m = sum(mastery.get(s, INITIAL_MASTERY) for s in scopes) / len(scopes)
    weak = 1 - avg_m / 100

    # 難易度適合：目標は「習熟度に少し背伸びした難易度」。差が小さいほど高得点
    target = mastery.get(f"service:{q.service}", INITIAL_MASTERY)
    fit = 1 - abs(_DIFF_LEVEL.get(q.difficulty, 55.0) - (target + 15)) / 100
    fit = max(0.0, fit)

    # 鮮度：未出題ほど高い
    stat = stats.get(q.id)
    fresh = 1.0 if not stat else 1 / (1 + stat["seen"])

    score = W_DUE * overdue + W_WEAK * weak + W_FIT * fit + W_FRESH * fresh
    if q.stale:
        score -= STALE_PENALTY
    # 同点ばらし
    return score + random.uniform(0, 0.05)


def select_adaptive(store: Store, pool: list[Question], n: int) -> list[Question]:
    # 状態を1回ずつ取得してループ内の N+1 クエリを回避
    now = time.time()
    mastery = store.all_mastery()
    stats = store.question_stats()
    due_map = store.all_due()
    ranked = sorted(
        pool, key=lambda q: _priority(q, now, mastery, stats, due_map), reverse=True
    )
    return ranked[:n]


def confusion_patterns(
    qmap: dict[str, Question],
    stats: dict[str, dict],
    top_n: int = 8,
    only_ids: set[str] | None = None,
) -> list[tuple[int, Question, Option]]:
    """誤選択肢分析：問題ごとに最も選ばれた誤答選択肢を回数降順で返す。

    only_ids を渡すとその問題に限定する（誤答深掘り用）。None なら全問題（統計画面用）。
    """
    items = stats.items() if only_ids is None else [
        (qid, stats[qid]) for qid in only_ids if qid in stats
    ]
    out: list[tuple[int, Question, Option]] = []
    for qid, st in items:
        q = qmap.get(qid)
        if not q or not st["wrong_labels"]:
            continue
        label, cnt = max(st["wrong_labels"].items(), key=lambda kv: kv[1])
        opt = next((o for o in q.options if o.label == label), None)
        if opt:
            out.append((cnt, q, opt))
    out.sort(key=lambda x: x[0], reverse=True)
    return out[:top_n]


def select_weak(store: Store, pool: list[Question], n: int, weak_count: int = 5) -> list[Question]:
    """習熟度の低い scope 下位 weak_count に該当する問題に絞って適応選択。"""
    mastery = store.all_mastery()
    if not mastery:
        return select_adaptive(store, pool, n)
    weak_scopes = {
        s for s, _ in sorted(mastery.items(), key=lambda kv: kv[1])[:weak_count]
    }
    filtered = [q for q in pool if set(q.scopes()) & weak_scopes]
    if not filtered:
        filtered = pool
    return select_adaptive(store, filtered, n)


def select_by_filter(
    store: Store,
    pool: list[Question],
    n: int,
    service: str | None = None,
    domain: int | None = None,
) -> list[Question]:
    filtered = pool
    if service:
        filtered = [q for q in filtered if q.service == service]
    if domain:
        filtered = [q for q in filtered if q.domain == domain]
    return select_adaptive(store, filtered or pool, n)


def select_review(store: Store, pool: list[Question], n: int) -> list[Question]:
    """過去に間違えた問題（box==1 かつ正答率の低い問題）を優先。"""
    stats = store.question_stats()

    def wrongness(q: Question) -> float:
        st = stats.get(q.id)
        if not st or st["seen"] == 0:
            return -1.0
        return 1 - st["correct"] / st["seen"]

    candidates = [q for q in pool if wrongness(q) > 0]
    candidates.sort(key=wrongness, reverse=True)
    return candidates[:n]


def recommend_fundamental(q: Question, store: Store) -> tuple[str, str, float] | None:
    """誤答した問題のタグから「最も弱い概念」を選び、復習すべき基礎トピックを返す。

    戻り値: (基礎トピックの service 名, 弱点タグ, そのタグの習熟度) または None。
    自分自身が基礎トピックの問題なら推薦しない（既に基礎を解いている）。
    """
    if q.domain == 0:  # 基礎トピック（fundamentals）自体には推薦しない
        return None
    candidates = [(t, store.get_mastery(f"tag:{t}")) for t in q.tags if t in TAG_TO_FUNDAMENTAL]
    if not candidates:
        return None
    tag, mastery = min(candidates, key=lambda tm: tm[1])  # 最も習熟度が低い概念
    return TAG_TO_FUNDAMENTAL[tag], tag, mastery


def select_fundamentals_review(
    store: Store, pool: list[Question], wrong: list[dict], n: int = 10
) -> list[Question]:
    """誤答群から推薦される基礎トピックに絞って復習問題を選ぶ。"""
    qmap = {q.id: q for q in pool}
    topics: set[str] = set()
    for w in wrong:
        q = qmap.get(w["question_id"])
        if not q:
            continue
        rec = recommend_fundamental(q, store)
        if rec:
            topics.add(rec[0])
    if not topics:
        return []
    candidates = [q for q in pool if q.service in topics]
    return select_adaptive(store, candidates, n)


def build_mock_exam(pool: list[Question], total: int = 65) -> list[Question]:
    """本番配点（分野別%）に応じて問題を配分した模擬試験セットを組む。"""
    by_domain: dict[int, list[Question]] = {d: [] for d in DOMAINS}
    for q in pool:
        by_domain.setdefault(q.domain, []).append(q)

    exam: list[Question] = []
    for d, (_, weight) in DOMAINS.items():
        k = round(total * weight / 100)
        bucket = by_domain.get(d, [])
        random.shuffle(bucket)
        exam.extend(bucket[:k])
    random.shuffle(exam)
    return exam[:total]
