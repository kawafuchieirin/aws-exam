"""全 questions.md の tags を canonical へ正規化する。

- TAGS.md = 統制語彙の単一情報源。tag_map.TAG_MAP で synonym -> canonical を適用。
- 安全策: (1) 実バンクの全タグが TAG_MAP に存在するか、(2) 全 canonical が CANONICAL 内か
  を先に検証し、欠けがあれば中断（rewrite しない）。
- `--apply` 無しは dry-run（差分件数とサンプルのみ表示）。
実行: python3 tools/apply_tag_map.py [--apply]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tag_map import CANONICAL, TAG_MAP  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT.parent / "services"
TAGS_LINE = re.compile(r"^(\s*-\s*tags:\s*)\[(.*)\]\s*$")


def canonical_from_tagsmd() -> set[str]:
    """TAGS.md のバッククォート語を抽出して統制語彙を取り出す。"""
    text = (ROOT / "TAGS.md").read_text(encoding="utf-8")
    body = text.split("## 語彙")[1] if "## 語彙" in text else text
    return set(re.findall(r"`([a-z0-9-]+)`", body))


def main() -> int:
    apply = "--apply" in sys.argv

    # --- 検証1: CANONICAL と TAGS.md の一致 ---
    vocab = canonical_from_tagsmd()
    if vocab != CANONICAL:
        print("⚠ CANONICAL と TAGS.md が不一致:")
        print("  TAGS.mdのみ:", sorted(vocab - CANONICAL))
        print("  mapのみ    :", sorted(CANONICAL - vocab))
        return 1
    print(f"✅ 統制語彙 {len(CANONICAL)} 語が TAGS.md と一致")

    # --- 検証2: 値が全て canonical か ---
    bad = {v for v in TAG_MAP.values() if v not in CANONICAL}
    if bad:
        print("⚠ canonical 外の値:", sorted(bad))
        return 1

    files = sorted(SERVICES.glob("**/questions.md"))
    used: set[str] = set()
    for f in files:
        for line in f.read_text(encoding="utf-8").splitlines():
            m = TAGS_LINE.match(line)
            if m:
                used |= {t.strip() for t in m.group(2).split(",") if t.strip()}

    # --- 検証3: 実バンクの全タグがマップ済みか ---
    missing = sorted(used - set(TAG_MAP))
    if missing:
        print(f"⚠ 未マップのタグ {len(missing)} 件 → 中断:", missing)
        return 1
    print(f"✅ 実バンクの全 {len(used)} タグがマップ済み")

    # --- 置換 ---
    changed_files = 0
    changed_lines = 0
    samples: list[str] = []
    for f in files:
        lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
        out = []
        fchanged = False
        for line in lines:
            m = TAGS_LINE.match(line.rstrip("\n"))
            if not m:
                out.append(line)
                continue
            orig = [t.strip() for t in m.group(2).split(",") if t.strip()]
            # canonical 化 + 重複排除（順序維持）
            seen: list[str] = []
            for t in orig:
                c = TAG_MAP[t]
                if c not in seen:
                    seen.append(c)
            new_line = f"{m.group(1)}[{', '.join(seen)}]\n"
            if new_line != line:
                fchanged = True
                changed_lines += 1
                if len(samples) < 12:
                    samples.append(f"  [{f.parent.name}] {orig} -> {seen}")
            out.append(new_line)
        if fchanged:
            changed_files += 1
            if apply:
                f.write_text("".join(out), encoding="utf-8")

    mode = "適用" if apply else "DRY-RUN"
    print(f"\n[{mode}] 変更ファイル {changed_files} / 変更行 {changed_lines}")
    print("サンプル:")
    print("\n".join(samples))
    if not apply:
        print("\n→ 実際に書き込むには: python3 tools/apply_tag_map.py --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
