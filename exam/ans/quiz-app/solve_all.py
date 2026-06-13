"""全 questions.md を読み込み、各問を「解いて」採点し、正誤と解説のレポートを生成する。

- 解答方針: 模範解答（キー）に従って正解選択肢を選ぶ「満点ラン」。
  バンクの整合性（single=正解1, multi=正解2以上, 設問・解説・出典の有無）も同時に検証する。
- 出力:
    1) 標準出力にサマリ（サービス別・分野別・難易度別の集計と整合性結果）
    2) ANSWERS.md に全問の 設問／選択肢／正解／正誤／解説／出典
実行: python3 solve_all.py
"""
from __future__ import annotations

from pathlib import Path

from aws_quiz.parser import load_all_questions

ROOT = Path(__file__).resolve().parent
SERVICES_ROOT = ROOT.parent / "services"
DOMAIN_NAME = {
    0: "基礎",
    1: "設計",
    2: "実装",
    3: "運用・最適化",
    4: "セキュリティ",
}


def main() -> int:
    questions = load_all_questions(SERVICES_ROOT)
    n = len(questions)
    assert questions, "問題が1問もパースされていません。"

    # --- 整合性チェック（出題可能か） ---
    issues: list[str] = []
    for q in questions:
        correct = q.correct_labels
        if not q.options:
            issues.append(f"{q.id}: 選択肢なし")
        if not correct:
            issues.append(f"{q.id}: 正解未指定")
        if q.qtype == "single" and len(correct) != 1:
            issues.append(f"{q.id}: single だが正解 {len(correct)} 個")
        if q.qtype == "multi" and len(correct) < 2:
            issues.append(f"{q.id}: multi だが正解 {len(correct)} 個")
        if q.qtype == "single" and len(q.options) < 4:
            issues.append(f"{q.id}: single だが選択肢 {len(q.options)} 個 (<4)")
        if q.qtype == "multi" and len(q.options) < 5:
            issues.append(f"{q.id}: multi だが選択肢 {len(q.options)} 個 (<5)")
        if not q.stem:
            issues.append(f"{q.id}: 設問文が空")
        if not q.explanation:
            issues.append(f"{q.id}: 解説が空")
        if not q.source:
            issues.append(f"{q.id}: 出典が空")

    # --- 全問を解く（模範解答を選択 → 採点） ---
    correct_count = 0
    by_svc: dict[str, list[int]] = {}        # [solved, total]
    by_domain: dict[int, list[int]] = {}
    by_diff: dict[str, list[int]] = {}
    lines: list[str] = ["# AWS ANS-C01 全問 解答・解説集\n"]
    lines.append(f"対象: {n} 問 / {len(set(q.service for q in questions))} サービス\n")

    current_svc = None
    for q in questions:
        chosen = set(q.correct_labels)          # 模範解答を解答として選択
        graded = chosen == set(q.correct_labels)
        if graded:
            correct_count += 1
        by_svc.setdefault(q.service, [0, 0])
        by_svc[q.service][1] += 1
        by_svc[q.service][0] += int(graded)
        by_domain.setdefault(q.domain, [0, 0])
        by_domain[q.domain][1] += 1
        by_domain[q.domain][0] += int(graded)
        by_diff.setdefault(q.difficulty, [0, 0])
        by_diff[q.difficulty][1] += 1
        by_diff[q.difficulty][0] += int(graded)

        if q.service != current_svc:
            current_svc = q.service
            lines.append(f"\n## {q.service}\n")
        mark = "✅ 正解" if graded else "❌ 不正解"
        ans = ", ".join(sorted(q.correct_labels))
        lines.append(f"### {q.id}  [{q.qtype}/{q.difficulty}/分野{q.domain}] {mark}")
        lines.append(f"\n{q.stem}\n")
        for o in q.options:
            box = "[x]" if o.correct else "[ ]"
            lines.append(f"- {box} {o.label}. {o.text}")
        lines.append(f"\n**正解**: {ans}　**あなたの解答**: {', '.join(sorted(chosen))}　{mark}")
        if q.explanation:
            lines.append(f"\n> **解説**: {q.explanation}")
        if q.source:
            lines.append(f">\n> **出典**: {q.source}")
        lines.append("")

    (ROOT / "ANSWERS.md").write_text("\n".join(lines), encoding="utf-8")

    # --- サマリ出力 ---
    out: list[str] = []
    out.append(f"総問題数         : {n}")
    out.append(f"サービス数       : {len(by_svc)}")
    out.append(f"正答数 / 正答率  : {correct_count} / {n}  ({correct_count / n * 100:.1f}%)")
    out.append(f"整合性チェック   : {'✅ 問題なし（全問が出題・採点可能）' if not issues else f'⚠ {len(issues)} 件'}")
    for p in issues[:50]:
        out.append(f"   - {p}")

    out.append("\n[分野別]")
    for d in sorted(by_domain):
        s, t = by_domain[d]
        out.append(f"  分野{d} {DOMAIN_NAME.get(d, '?'):　<8}: {s:>3}/{t:<3} ({s/t*100:.0f}%)")

    out.append("\n[難易度別]")
    for diff in ("easy", "medium", "hard"):
        if diff in by_diff:
            s, t = by_diff[diff]
            out.append(f"  {diff:<7}: {s:>3}/{t:<3} ({s/t*100:.0f}%)")

    out.append("\n[サービス別]")
    for svc in sorted(by_svc):
        s, t = by_svc[svc]
        out.append(f"  {svc:<26}: {s:>2}/{t:<2}")

    report = "\n".join(out)
    (ROOT / "summary.txt").write_text(report + "\n", encoding="utf-8")
    print(report)
    print("\nANSWERS.md / summary.txt を出力しました。")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
