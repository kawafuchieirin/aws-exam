---
service: trusted-advisor
domain_default: 3
source: README.md
source_sha256: 2dc0b3e7cd8e0167ec6c8076e3f467369304d4e61ecb171edef85d25ac5439c7
generated: 2026-05-24
---

## trusted-advisor-001
- type: single
- difficulty: medium
- domain: 3
- tags: [quotas]

EIP・VPC・Internet Gateway・VPN 接続数などのサービス上限への接近を事前に検知したい。最も適切な手段はどれか。

- [ ] A. VPC フローログを分析する
- [x] B. Trusted Advisor のサービス上限（クォータ）チェックを利用する
- [ ] C. Config ルールで上限を評価する
- [ ] D. CloudTrail で API コール数を集計する

> **解説**: Trusted Advisor のサービス上限チェックは、EIP・VPC・IGW・VPN 接続などのクォータ逼迫を事前検知し、上限引き上げ申請の判断材料になる。
> **出典**: [Trusted Advisor README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## trusted-advisor-002
- type: single
- difficulty: medium
- domain: 4
- tags: [security-group]

Trusted Advisor のセキュリティチェックが検出するネットワーク関連の代表例はどれか。

- [ ] A. IAM ユーザーの MFA 未設定のみ
- [x] B. セキュリティグループの過度に許可的なルール（22/3389 等の全開放）
- [ ] C. VPC の CIDR 重複
- [ ] D. Route 53 のドメイン期限切れ

> **解説**: セキュリティカテゴリは SG の無制限アクセス（22/3389 等の全開放）を検出する。ただし継続的な詳細監査は Config や Firewall Manager の領域。
> **出典**: [Trusted Advisor README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## trusted-advisor-003
- type: single
- difficulty: easy
- domain: 4
- tags: [cost, public-ip]

未関連付けの Elastic IP がコスト最適化チェックで検出される理由はどれか。

- [ ] A. EIP は無料だが数が多いと上限に達するため
- [x] B. 未関連付けの EIP は課金対象であり、無駄なコストになるため
- [ ] C. EIP はセキュリティリスクになるため
- [ ] D. EIP は耐障害性に影響するため

> **解説**: 未関連付け（アイドル）の EIP は課金されるため、コスト最適化チェックで検出される。アイドルなロードバランサーも同様にコスト観点で検出される。
> **出典**: [Trusted Advisor README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## trusted-advisor-004
- type: single
- difficulty: medium
- domain: 4
- tags: [cost, network-firewall]

Trusted Advisor の全カテゴリのフルチェックを利用するための前提条件はどれか。

- [ ] A. Basic サポートで利用可能
- [x] B. Business または Enterprise サポートプランが必要
- [ ] C. Organizations の管理アカウントである必要がある
- [ ] D. Config の有効化が必要

> **解説**: Basic/Developer は一部チェックのみ。全カテゴリのフルチェックは Business / Enterprise サポートプランが必要。Trusted Advisor 自体に追加料金はなくサポートプランに含まれる。
> **出典**: [Trusted Advisor README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## trusted-advisor-005
- type: single
- difficulty: medium
- domain: 4
- tags: [route-table, config-rules, firewall-manager]

SG の準拠状態を「継続的に」監査したい。Trusted Advisor より適した手段はどれか。

- [ ] A. Trusted Advisor のセキュリティチェックを毎時実行する
- [x] B. Config ルールや Firewall Manager で継続的に評価・是正する
- [ ] C. Health Dashboard で監視する
- [ ] D. Well-Architected Tool でレビューする

> **解説**: Trusted Advisor は推奨事項を提示するが、SG の継続的な準拠監査は Config や Firewall Manager の領域。試験では責務の境界が問われる。
> **出典**: [Trusted Advisor README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## trusted-advisor-006
- type: single
- difficulty: easy
- domain: 1
- tags: [high-availability, multi-az]

Trusted Advisor の耐障害性カテゴリが推奨するネットワーク関連の例はどれか。

- [ ] A. EIP の削減
- [x] B. 単一 AZ 構成の検出とマルチ AZ 化の推奨
- [ ] C. SG の全開放の検出
- [ ] D. サービス上限の引き上げ申請

> **解説**: 耐障害性カテゴリは単一 AZ 構成や ELB の最適化を検出し、マルチ AZ 化を推奨する。EIP 削減はコスト、SG 全開放はセキュリティ、上限は別カテゴリ。
> **出典**: [Trusted Advisor README #2 コアコンセプト（チェックカテゴリ）](README.md#2-コアコンセプトチェックカテゴリ)

## trusted-advisor-007
- type: single
- difficulty: easy
- domain: 4
- tags: [cost]

Trusted Advisor の料金について正しいものはどれか。

- [x] A. Trusted Advisor 自体に追加料金はなく、サポートプランに含まれる
- [ ] B. チェック1件あたり従量課金される
- [ ] C. すべてのチェックが無料で利用できる
- [ ] D. Enterprise サポートでのみ有料になる

> **解説**: Trusted Advisor 自体に追加料金はなくサポートプランに含まれる。Basic/Developer は一部チェックのみ、全チェックは Business 以上。
> **出典**: [Trusted Advisor README #5 制約・コスト](README.md#5-制約コスト)

## trusted-advisor-008
- type: multi
- difficulty: hard
- domain: 3
- tags: [quotas]

Trusted Advisor のサービス上限チェックで逼迫を監視できるネットワーク関連のクォータとして、正しいものを2つ選べ。

- [x] A. VPC 数
- [x] B. VPN 接続数
- [ ] C. IAM ユーザー数
- [ ] D. S3 バケットのオブジェクト数
- [ ] E. Lambda の同時実行数

> **解説**: ネットワーク関連のサービス上限チェックは VPC 数・EIP 数・Internet Gateway 数・VPN 接続数などを対象とする。IAM ユーザー数や S3 オブジェクト数、Lambda 同時実行はネットワークの上限チェックではない。
> **出典**: [Trusted Advisor README #2 コアコンセプト（チェックカテゴリ）](README.md#2-コアコンセプトチェックカテゴリ)

## trusted-advisor-009
- type: multi
- difficulty: medium
- domain: 4
- tags: [cost]

Trusted Advisor のコスト最適化チェックで検出されるネットワーク関連リソースとして、正しいものを2つ選べ。

- [x] A. アイドルなロードバランサー
- [x] B. 未関連付けの Elastic IP
- [ ] C. 過度に許可的なセキュリティグループ
- [ ] D. 単一 AZ の NAT Gateway
- [ ] E. サービス上限に接近した VPC 数

> **解説**: コスト最適化はアイドルなロードバランサーや未関連付け EIP（課金対象）を検出する。SG の過度な許可はセキュリティ、単一 AZ は耐障害性、上限接近はサービス上限カテゴリ。
> **出典**: [Trusted Advisor README #2 コアコンセプト（チェックカテゴリ）](README.md#2-コアコンセプトチェックカテゴリ)
