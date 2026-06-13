# AWS Firewall Manager の要点

> 重要度: ○ ／ Organizations 横断でファイアウォール/保護を一元管理する定番サービス。「複数アカウントに同一保護を強制し新規にも自動適用」が即答パターン。

## これは何
- AWS Organizations 全体で各種保護を一元的に設定・維持するサービス（FMS）。
- ポリシーを一度定義すれば、スコープ内の既存リソースに加え新規アカウント・新規リソースにも自動適用される。
- 管理対象は WAF / Shield Advanced / VPC SG・NACL / Network Firewall / Route 53 Resolver DNS Firewall など。

## 試験頻出ポイント
- **複数アカウント横断**で同一の WAF/SG/Network Firewall を強制し、**新規アカウント・新規リソースへ自動適用**したい → FMS が定番解。
- **前提条件3点**: ①**Organizations を全機能(all features)で有効化**、②**FMS 管理者アカウントを指定**、③**各アカウント/リージョンで AWS Config を有効化**。
- **FMS 管理者**は Organizations 管理アカウントが指定（**委任管理者**も可）。OU ごとではなく組織単位で運用。
- 管理できるポリシータイプ（暗記）: **WAF Web ACL** / **Shield Advanced** / **VPC SG** / **VPC NACL** / **Network Firewall** / **Route 53 DNS Firewall** / サードパーティ(Palo Alto 等)。
- **SG ポリシー3種**: **共通**(共通 SG を配布) / **コンテンツ監査**(許可・拒否ルールを監査) / **使用状況監査**(**未使用・冗長 SG を検出**)。
- **Shield Advanced ポリシー**で組織全アカウントを一括サブスク、新規アカウントも自動加入。
- **自動修復(remediation)**: 非準拠リソース・新規リソースへポリシーを自動適用しドリフトを修復（リソース削除や攻撃ブロックそのものではない）。

## 比較・選択の判断
| 要件 | 解答 |
|---|---|
| 組織横断で WAF/SG/Network Firewall を強制、新規にも自動適用 | **Firewall Manager** |
| 全アカウントを Shield Advanced に一括加入 | **FMS の Shield Advanced ポリシー** |
| 未使用・冗長な SG を検出 | **SG 使用状況監査ポリシー** |
| 許可/拒否される SG ルールを監査 | **SG コンテンツ監査ポリシー** |
| 準拠状態の評価基盤 | **AWS Config**（前提） |
| 許可の上限を定めるだけ（配布・強制適用はしない） | SCP（FMS の代替にならない） |

## よく問われる上限・注意点（ひっかけ）
- **前提に Organizations(all features) + FMS 管理者指定 + AWS Config が必須**。GuardDuty や VPC フローログは要件ではない。
- 準拠評価の依存先は **AWS Config**（CloudTrail/Inspector/Trusted Advisor ではない）。
- **リージョナルポリシーはリージョンごとに作成**が必要。1ポリシーで全リージョン自動適用はされない（CloudFront 等のグローバルリソースのみグローバル扱い）。
- **SCP は許可の上限を定めるだけ**で Web ACL や SG を配布・強制適用しない。**Config ルールは評価のみ**で強制適用しない。
- 課金は**アクティブなポリシー単位の月額 ＋ 背後サービス（WAF/Shield/Config 等）の通常料金**。FMS が完全無料ではない。
- IAM 権限境界・EBS 暗号化などは **FMS ポリシーの対象外**。

関連: [Organizations](organizations.md) / [WAF](waf.md) / [Shield](shield.md) / [Network Firewall](network-firewall.md) / [Config](config.md)
