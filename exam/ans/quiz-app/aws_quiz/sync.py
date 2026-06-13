"""README 変更検知（陳腐化フラグ）。

各 questions.md の frontmatter にある source_sha256 と、
同ディレクトリの参照 README の実ハッシュを比較する。
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _frontmatter(path: Path) -> dict:
    m = _FM_RE.match(path.read_text(encoding="utf-8"))
    fm: dict = {}
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"^(\w+):\s*(.*)$", line.strip())
            if mm:
                fm[mm.group(1)] = mm.group(2).strip()
    return fm


@dataclass
class SyncStatus:
    service: str
    questions_file: Path
    source_file: Path
    recorded_sha: str
    actual_sha: str

    @property
    def stale(self) -> bool:
        return self.recorded_sha != self.actual_sha


def check_sync(services_root: Path) -> list[SyncStatus]:
    out: list[SyncStatus] = []
    for qf in sorted(services_root.glob("**/questions.md")):
        fm = _frontmatter(qf)
        source_name = fm.get("source", "README.md")
        source = qf.parent / source_name
        if not source.exists():
            continue
        out.append(
            SyncStatus(
                service=fm.get("service", qf.parent.name),
                questions_file=qf,
                source_file=source,
                recorded_sha=fm.get("source_sha256", ""),
                actual_sha=sha256_of(source),
            )
        )
    return out


def stale_services(services_root: Path) -> set[str]:
    return {s.service for s in check_sync(services_root) if s.stale}
