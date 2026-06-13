"""questions.md をパースして Question のリストを返す。

SPEC.md「3. 問題バンク形式」に準拠。標準ライブラリのみ使用。
"""
from __future__ import annotations

import re
from pathlib import Path

from .models import Option, Question

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_OPTION_RE = re.compile(r"^- \[( |x|X)\]\s*([A-Z])\.\s*(.*)$")
_META_RE = re.compile(r"^- (\w+):\s*(.*)$")


def _parse_scalar_list(value: str) -> list[str]:
    """`[a, b, c]` または `a, b` を list[str] に。"""
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [v.strip() for v in value.split(",") if v.strip()]


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm: dict = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^(\w+):\s*(.*)$", line.strip())
        if mm:
            fm[mm.group(1)] = mm.group(2).strip()
    return fm, text[m.end():]


def parse_questions_file(path: Path) -> list[Question]:
    raw = path.read_text(encoding="utf-8")
    fm, body = _parse_frontmatter(raw)
    service = fm.get("service", path.parent.name)
    domain_default = int(fm.get("domain_default", "1") or 1)

    questions: list[Question] = []
    # "## <id>" で問題ブロックに分割
    blocks = re.split(r"^##\s+(\S+)\s*$", body, flags=re.MULTILINE)
    # blocks = [前文, id1, block1, id2, block2, ...]
    for i in range(1, len(blocks), 2):
        qid = blocks[i].strip()
        block = blocks[i + 1]
        q = _parse_block(qid, block, service, domain_default)
        if q:
            questions.append(q)
    return questions


def _parse_block(qid: str, block: str, service: str, domain_default: int) -> Question | None:
    meta: dict = {}
    options: list[Option] = []
    stem_lines: list[str] = []
    expl_lines: list[str] = []
    source = ""
    state = "meta"  # meta -> stem -> options -> notes

    for line in block.splitlines():
        stripped = line.strip()
        opt_m = _OPTION_RE.match(stripped)
        meta_m = _META_RE.match(stripped)

        if opt_m:
            state = "options"
            options.append(
                Option(
                    label=opt_m.group(2),
                    text=opt_m.group(3).strip(),
                    correct=opt_m.group(1).lower() == "x",
                )
            )
            continue

        if state == "meta" and meta_m:
            meta[meta_m.group(1)] = meta_m.group(2).strip()
            continue

        # 解説・出典（引用ブロック）
        if stripped.startswith(">"):
            content = stripped.lstrip(">").strip()
            if "**出典**" in content or "**Source**" in content:
                source = re.sub(r"\*\*(出典|Source)\*\*:?\s*", "", content).strip()
            elif "**解説**" in content or "**Explanation**" in content:
                expl_lines.append(re.sub(r"\*\*(解説|Explanation)\*\*:?\s*", "", content).strip())
            else:
                expl_lines.append(content)
            state = "notes"
            continue

        if state in ("meta", "stem") and stripped:
            state = "stem"
            stem_lines.append(stripped)

    if not options:
        return None

    tags = _parse_scalar_list(meta.get("tags", ""))
    return Question(
        id=qid,
        service=meta.get("service", service),
        qtype=meta.get("type", "single").strip(),
        difficulty=meta.get("difficulty", "medium").strip(),
        domain=int(meta.get("domain", domain_default) or domain_default),
        tags=tags,
        stem=" ".join(stem_lines).strip(),
        options=options,
        explanation=" ".join(expl_lines).strip(),
        source=source,
    )


def load_all_questions(services_root: Path) -> list[Question]:
    """services/ 配下の全 questions.md を読み込む。"""
    out: list[Question] = []
    for qf in sorted(services_root.glob("**/questions.md")):
        out.extend(parse_questions_file(qf))
    return out
