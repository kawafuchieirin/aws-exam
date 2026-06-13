"""問題バンクのデータモデル。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Option:
    label: str          # "A", "B", ...
    text: str
    correct: bool


@dataclass
class Question:
    id: str
    service: str            # 例: "vpc"
    qtype: str              # "single" | "multi"
    difficulty: str         # "easy" | "medium" | "hard"
    domain: int             # 試験分野 1-4
    tags: list[str]
    stem: str               # 設問文
    options: list[Option]
    explanation: str = ""
    source: str = ""        # 出典（Markdown リンクや見出し）
    stale: bool = False     # README 変更により要見直し

    @property
    def correct_labels(self) -> set[str]:
        return {o.label for o in self.options if o.correct}

    def is_correct(self, chosen: set[str]) -> bool:
        return chosen == self.correct_labels

    # 習熟度更新に使う scope の一覧（サービス＋各タグ）
    def scopes(self) -> list[str]:
        return [f"service:{self.service}"] + [f"tag:{t}" for t in self.tags]


# 試験分野の定義と本番配点（模擬試験の配分に使用）
# 分野 0 は「ネットワーク基礎」（services/fundamentals/）。配点 0 のため
# build_mock_exam の配分ループでは 0 問となり、本番模試からは自動的に除外される。
# 一方 select_adaptive / select_weak / select_by_filter（学習モード）には含まれる。
DOMAINS = {
    0: ("ネットワーク基礎", 0),
    1: ("ネットワーク設計", 30),
    2: ("ネットワーク実装", 26),
    3: ("ネットワークの管理と運用", 20),
    4: ("セキュリティ・コンプライアンス・ガバナンス", 24),
}


def domain_label(d: int) -> str:
    """画面表示用の分野ラベル。分野 0 は「基礎」と表示する。"""
    if d == 0:
        return "基礎"
    return f"第{d}分野"

DIFFICULTY_WEIGHT = {"easy": 0.6, "medium": 1.0, "hard": 1.4}

# 誤答の自己申告原因（メタ認知）。キーは DB 保存値、値は表示ラベル。
MISTAKE_CAUSES = {
    "knowledge": "知識不足（そもそも知らなかった）",
    "confusion": "勘違い・混同（似た概念と取り違えた）",
    "careless": "ケアレスミス（設問の読み違い・選択ミス）",
    "narrowed": "二択で外した（最後の2択で迷って外した）",
    "unlearned": "未学習（手付かずの領域だった）",
}

# canonical タグ → 復習すべき基礎トピック（services/fundamentals/<topic>）。
# 「サービスで間違えた概念」を「基礎」へ降ろして復習導線にするための対応表。
TAG_TO_FUNDAMENTAL = {
    "cidr": "ip-addressing-subnetting",
    "subnetting": "ip-addressing-subnetting",
    "ipv6": "ip-addressing-subnetting",
    "ip-exhaustion": "ip-addressing-subnetting",
    "public-ip": "ip-addressing-subnetting",
    "bgp": "routing-bgp",
    "longest-prefix": "routing-bgp",
    "route-table": "routing-bgp",
    "route-propagation": "routing-bgp",
    "ecmp": "routing-bgp",
    "blackhole": "routing-bgp",
    "dns": "dns",
    "routing-policy": "dns",
    "failover": "dns",
    "tcp-udp": "transport-tcp-udp",
    "mtu": "transport-tcp-udp",
    "icmp": "transport-tcp-udp",
    "tls": "tls-and-vpn-crypto",
    "ipsec": "tls-and-vpn-crypto",
    "encryption": "tls-and-vpn-crypto",
    "vpn": "tls-and-vpn-crypto",
    "client-vpn": "tls-and-vpn-crypto",
    "nat": "nat-and-load-balancing-concepts",
    "alb": "nat-and-load-balancing-concepts",
    "nlb": "nat-and-load-balancing-concepts",
    "gwlb": "nat-and-load-balancing-concepts",
    "cross-zone": "nat-and-load-balancing-concepts",
    "proxy-protocol": "nat-and-load-balancing-concepts",
    "target-type": "nat-and-load-balancing-concepts",
    "stateful-stateless": "nat-and-load-balancing-concepts",
    "http": "osi-and-encapsulation",
}
