---
service: organizations
domain_default: 4
source: README.md
source_sha256: a8d7f1102d7c29941f27916f1987cc80463d813122e6eb98e2058598606219ab
generated: 2026-05-24
---

## organizations-001
- type: single
- difficulty: medium
- domain: 4
- tags: [scp, iam-policy]

SCP（サービスコントロールポリシー）の性質について正しいものはどれか。

- [ ] A. SCP はアカウントに権限を「付与」する
- [x] B. SCP は許可の「上限（ガードレール）」であり、実効権限は SCP ∩ IAM ポリシーで決まる
- [ ] C. SCP は IAM ポリシーを上書きして強制的に許可する
- [ ] D. SCP は管理アカウントを含む全アカウントに必ず適用される

> **解説**: SCP は許可を付与せず上限を定めるガードレール。実効権限は SCP（上限）と IAM ポリシー（付与）の AND（積集合）。管理アカウント自身には効かない点も重要。
> **出典**: [Organizations README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## organizations-002
- type: single
- difficulty: medium
- domain: 4
- tags: [scp, security-group, public-ip]

組織配下の全アカウントで Internet Gateway の作成を一律禁止したい。最も適切な手段はどれか。

- [ ] A. 各アカウントの IAM ロールから `ec2:CreateInternetGateway` を外す
- [x] B. `ec2:CreateInternetGateway` を Deny する SCP を組織/OU に適用する
- [ ] C. NACL で IGW へのトラフィックを拒否する
- [ ] D. Firewall Manager で IGW を削除する

> **解説**: SCP で `ec2:CreateInternetGateway` を Deny すれば、配下全アカウントの IGW 作成を一律禁止できる。IAM ロールの個別変更は抜け漏れが生じ、組織全体のガードレールにならない。
> **出典**: [Organizations README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## organizations-003
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-sharing, ip-exhaustion]

ワークロードアカウントが自前の VPC/TGW を作らず、ネットワークアカウントの集約された基盤を利用してIPアドレス空間を効率化したい。前提となる仕組みはどれか。

- [ ] A. VPC ピアリングを全アカウント間にフルメッシュで張る
- [x] B. RAM（Resource Access Manager）でサブネット/TGW を共有する
- [ ] C. 各アカウントで NAT Gateway を個別に作る
- [ ] D. SCP で VPC 作成を禁止する

> **解説**: RAM でサブネットや TGW を共有すると、各ワークロードアカウントが自前の基盤を作らず集約された基盤を利用でき、IP 効率化と管理集中を実現する。組織と統合すると招待不要で共有可能。
> **出典**: [Organizations README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## organizations-004
- type: single
- difficulty: medium
- domain: 4
- tags: [firewall-manager, use-case-fit, multi-account]

AWS Firewall Manager で全アカウントへセキュリティポリシーを展開するための前提条件として正しい組み合わせはどれか。

- [ ] A. Control Tower のランディングゾーンのみ
- [x] B. Organizations の有効化、委任管理者の指定、AWS Config の有効化
- [ ] C. Direct Connect と Transit Gateway
- [ ] D. Business サポートプランのみ

> **解説**: Firewall Manager の前提は Organizations であり、委任管理者の指定と AWS Config の有効化が必要。新規アカウント追加時も自動でポリシーが適用され、ガバナンスの抜け漏れを防ぐ。
> **出典**: [Organizations README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## organizations-005
- type: single
- difficulty: hard
- domain: 4
- tags: [scp, multi-account, use-case-fit]

SCP の適用範囲に関する重要な注意点はどれか。

- [ ] A. SCP は OU 階層を継承せず、適用した階層だけに効く
- [x] B. SCP は管理アカウント自身には効かないため、日常運用は別アカウントへ分離すべき
- [ ] C. SCP は管理アカウントにのみ効き、メンバーアカウントには効かない
- [ ] D. SCP はリージョン単位でしか適用できない

> **解説**: SCP は管理アカウント自身には適用されない。ガードレールをすり抜けないよう、運用は委任管理者など別アカウントに分離するのが推奨。SCP は OU 階層に沿って上位のものも継承される。
> **出典**: [Organizations README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## organizations-006
- type: single
- difficulty: easy
- domain: 4
- tags: [multi-account, use-case-fit]

管理アカウントの権限を集中させず、ネットワーク/セキュリティ運用を専用アカウントで行いたい。Organizations の機能はどれか。

- [ ] A. クロスアカウントロールの手動作成のみ
- [x] B. 委任管理者（delegated administrator）の指定
- [ ] C. SCP による全権限の委譲
- [ ] D. RAM の招待

> **解説**: 委任管理者を指定すると、Firewall Manager・RAM・IPAM 等を管理アカウント以外の専用アカウントで運用でき、権限と運用を分離できる。
> **出典**: [Organizations README #2 コアコンセプト](README.md#2-コアコンセプト)

## organizations-007
- type: single
- difficulty: medium
- domain: 3
- tags: [cloudtrail-events, config-rules, multi-account]

組織全体の監査・監視を集約する仕組みの組み合わせとして適切なものはどれか。

- [ ] A. 各アカウントで個別に CloudTrail を有効化し手動集約する
- [x] B. 組織証跡（CloudTrail）とクロスアカウント CloudWatch オブザーバビリティ、Config 組織アグリゲーター
- [ ] C. VPC フローログをすべて1つの S3 に手動コピーする
- [ ] D. Trusted Advisor のレポートを定期エクスポートする

> **解説**: 組織証跡で全アカウントの監査ログを集約し、クロスアカウント CloudWatch オブザーバビリティで監視、Config 組織アグリゲーターで構成準拠を集約する。これがガバナンスの標準パターン。
> **出典**: [Organizations README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## organizations-008
- type: single
- difficulty: easy
- domain: 1
- tags: [cost, vpc-sharing, transit-gateway]

VPC 共有・TGW 共有によるコスト面のメリットとして正しいものはどれか。

- [ ] A. SCP の適用数を削減できる
- [x] B. アカウントごとに重複していた NAT Gateway やエンドポイントを削減できる
- [ ] C. Organizations の月額料金が割引される
- [ ] D. Direct Connect の回線数を増やせる

> **解説**: VPC 共有・TGW 共有により、各アカウントが個別に持っていた NAT Gateway やエンドポイント等の重複ネットワークを削減でき、コスト最適化につながる。Organizations 自体は無料。
> **出典**: [Organizations README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## organizations-009
- type: multi
- difficulty: hard
- domain: 4
- tags: [scp, security-group, use-case-fit]

ネットワーク統制でよく使われる SCP の典型例として、正しいものを2つ選べ。

- [x] A. 承認外リージョンの利用を禁止する
- [x] B. VPC ピアリング/IGW/VPN の作成を禁止する
- [ ] C. 特定の IP からのコンソールアクセスを許可する
- [ ] D. NAT Gateway のデータ処理料を割り引く
- [ ] E. ワークロードアカウントに管理者権限を付与する

> **解説**: ネットワーク向け SCP の典型は、承認外リージョン禁止、VPC ピアリング/IGW/VPN 作成禁止、特定 SG ルール変更禁止、デフォルト VPC 削除保護など。SCP は許可を付与しないため C/E は誤り、D はコストで無関係。
> **出典**: [Organizations README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## organizations-010
- type: multi
- difficulty: medium
- domain: 1
- tags: [vpc-sharing]

RAM を通じて組織内で共有できるネットワーク関連リソースとして、正しいものを2つ選べ。

- [x] A. Transit Gateway
- [x] B. VPC サブネット
- [ ] C. IAM ロール
- [ ] D. EC2 インスタンス
- [ ] E. CloudTrail 証跡

> **解説**: RAM は TGW・サブネット・Route 53 解決ルール・Prefix List 等のネットワーク基盤を共有できる。IAM ロールや EC2 インスタンス、CloudTrail 証跡は RAM の共有対象ではない。
> **出典**: [Organizations README #5 他サービスとの連携](README.md#5-他サービスとの連携)

## organizations-011
- type: single
- difficulty: medium
- domain: 4
- tags: [vpc-sharing, multi-account]

RAM を Organizations と統合した場合の挙動として正しいものはどれか。

- [ ] A. 共有のたびに各アカウントの承諾（招待の受諾）が必要になる
- [x] B. 組織内共有を有効にすると、共有招待の承諾なしにサブネット/TGW を共有できる
- [ ] C. 管理アカウントでしかリソースを受け取れない
- [ ] D. SCP がないと RAM 共有はできない

> **解説**: 組織内共有を有効にすると、共有招待の承諾なしに組織内アカウントへサブネット/TGW を共有できる。これによりネットワーク基盤の集約が容易になる。
> **出典**: [Organizations README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)
