"""TUI を起動せずにパーサ・エンジン・ストアを検証するスモークテスト。

実行: python -m aws_quiz.selftest
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from .engine import (
    build_mock_exam,
    recommend_fundamental,
    select_adaptive,
    select_fundamentals_review,
    select_weak,
)
from .parser import load_all_questions
from .store import Store
from .sync import check_sync

SERVICES_ROOT = Path(__file__).resolve().parents[2] / "services"


def main() -> int:
    print(f"services root: {SERVICES_ROOT}")
    questions = load_all_questions(SERVICES_ROOT)
    print(f"パース済み問題数: {len(questions)}")
    assert questions, "問題が1問もパースされていません。questions.md を確認してください。"

    # 形式検証
    problems = []
    for q in questions:
        if not q.options:
            problems.append(f"{q.id}: 選択肢なし")
        if not q.correct_labels:
            problems.append(f"{q.id}: 正解が未指定")
        if q.qtype == "single" and len(q.correct_labels) != 1:
            problems.append(f"{q.id}: single なのに正解が {len(q.correct_labels)} 個")
        if q.qtype == "multi" and len(q.correct_labels) < 2:
            problems.append(f"{q.id}: multi なのに正解が {len(q.correct_labels)} 個")
        if not q.stem:
            problems.append(f"{q.id}: 設問文が空")
    if problems:
        print("⚠ 形式エラー:")
        for p in problems:
            print("   -", p)
    else:
        print("✅ 形式チェック OK")

    # サービス別集計
    by_svc: dict[str, int] = {}
    for q in questions:
        by_svc[q.service] = by_svc.get(q.service, 0) + 1
    print("サービス別:", by_svc)

    # 同期チェック
    sync = check_sync(SERVICES_ROOT)
    stale = [s.service for s in sync if s.stale]
    print(f"同期: 対象 {len(sync)} / 要見直し {stale or 'なし'}")

    # エンジン＋ストアを一時DBで検証
    with tempfile.TemporaryDirectory() as d:
        store = Store(Path(d) / "t.db")
        adaptive = select_adaptive(store, questions, 5)
        print(f"適応選択: {[q.id for q in adaptive]}")
        # 解答をシミュレート（最初の問題を正解、次を誤答）
        q0 = adaptive[0]
        store.record_answer(q0, q0.correct_labels, True)
        q1 = adaptive[1]
        wrong = {o.label for o in q1.options if not o.correct}
        attempt_id = store.record_answer(q1, {next(iter(wrong))} if wrong else set(), False)
        print(f"習熟度: {store.all_mastery()}")

        # 誤答深掘り：原因記録・誤答抽出・原因集計・基礎推薦の検証
        store.set_cause(attempt_id, "confusion")
        wrong_qs = store.wrong_questions()
        assert any(
            w["question_id"] == q1.id and w["cause"] == "confusion" for w in wrong_qs
        ), "誤答原因(cause)が wrong_questions に反映されない"
        assert store.cause_counts().get("confusion", 0) >= 1, "原因集計が反映されない"
        # 空 pool では空リストを返す（フォールスルー安全性）
        assert select_fundamentals_review(store, [], wrong_qs, 5) == [], "空poolは空を返すべき"
        svc_q = next((q for q in questions if q.service not in {
            "ip-addressing-subnetting", "routing-bgp", "dns", "transport-tcp-udp",
            "tls-and-vpn-crypto", "osi-and-encapsulation", "nat-and-load-balancing-concepts",
        } and any(t in q.tags for t in ("bgp", "dns", "tls", "nat", "cidr", "mtu"))), None)
        if svc_q:
            print(f"基礎推薦サンプル: {svc_q.id} -> {recommend_fundamental(svc_q, store)}")
        fund_review = select_fundamentals_review(store, questions, wrong_qs, 5)
        print(f"弱点の基礎復習: {[q.id for q in fund_review]}")
        weak = select_weak(store, questions, 5)
        print(f"苦手選択: {[q.id for q in weak]}")
        mock = build_mock_exam(questions, 10)
        print(f"模擬試験(10問)分野: {sorted(q.domain for q in mock)}")
        store.close()

    print("\n✅ セルフテスト完了")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
