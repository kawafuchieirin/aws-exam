---
service: control-tower
domain_default: 4
source: README.md
source_sha256: 0dfb9ccca124507041c22e0752e6f0b5133a01202a83edfe39e0078809276116
generated: 2026-05-24
---

## control-tower-001
- type: single
- difficulty: easy
- domain: 4
- tags: [landing-zone, event-routing]

AWS Control Tower がランディングゾーン構築のために内部で組み合わせて利用するサービスの組み合わせとして、最も適切なものはどれか。

- [ ] A. EC2・S3・Lambda
- [x] B. Organizations・SCP・Config・CloudTrail
- [ ] C. Transit Gateway・Direct Connect・VPN
- [ ] D. GuardDuty・Inspector・Macie

> **解説**: Control Tower は Organizations・SCP・Config・CloudTrail をオーケストレーションし、標準化されたマルチアカウントのガバナンスを提供する。ネットワークやセキュリティ脅威検出系サービスは構成要素ではない。
> **出典**: [Control Tower README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## control-tower-002
- type: single
- difficulty: medium
- domain: 4
- tags: [scp]

Control Tower における「予防的ガードレール（preventive control）」は、内部的にどの仕組みで強制されるか。

- [ ] A. AWS Config ルール
- [x] B. SCP（サービスコントロールポリシー）
- [ ] C. CloudFormation Hooks
- [ ] D. IAM ロール

> **解説**: 予防的ガードレールは SCP で実装され、対象操作そのものを禁止する。発見的（detective）は Config ルール、プロアクティブは CloudFormation Hooks に対応する。
> **出典**: [Control Tower README #2 コアコンセプト](README.md#2-コアコンセプト)

## control-tower-003
- type: single
- difficulty: medium
- domain: 3
- tags: [scp, monitoring, config-rules]

「VPC フローログが有効になっているか」を継続的に評価するネットワークガードレールは、どの種類のコントロールに分類されるか。

- [ ] A. 予防的ガードレール
- [x] B. 発見的ガードレール
- [ ] C. プロアクティブガードレール
- [ ] D. 課金ガードレール

> **解説**: 「有効かを検出する」評価系のガードレールは発見的（detective）であり、Config ルールで実装される。予防的は操作の禁止、プロアクティブはプロビジョニング前の検査。
> **出典**: [Control Tower README #3 仕組みとネットワークガードレール](README.md#3-仕組みとネットワークガードレール)

## control-tower-004
- type: single
- difficulty: medium
- domain: 1
- tags: [landing-zone, vpc-sharing]

Account Factory を使って新規アカウントを払い出す際に、ネットワークの観点で標準化・制御できるものはどれか。

- [ ] A. オンプレミスルーターの BGP 設定
- [x] B. VPC の CIDR・サブネット・リージョン（不要なデフォルト VPC の削除を含む）
- [ ] C. Direct Connect の専用線契約
- [ ] D. Route 53 のドメイン登録

> **解説**: Account Factory は標準化されたアカウント払い出しを行い、VPC の CIDR・サブネット・リージョンを指定でき、デフォルト VPC の削除も可能。これにより CIDR 重複や野良 VPC を防ぐ。
> **出典**: [Control Tower README #3 仕組みとネットワークガードレール](README.md#3-仕組みとネットワークガードレール)

## control-tower-005
- type: single
- difficulty: easy
- domain: 3
- tags: [landing-zone, multi-account]

ランディングゾーンを敷設すると自動的に作成され、組織証跡や Config が構成されるアカウントの組み合わせはどれか。

- [ ] A. 開発アカウントと本番アカウント
- [x] B. ログアーカイブアカウントと監査アカウント
- [ ] C. ネットワークアカウントとセキュリティアカウントのみ
- [ ] D. 課金アカウントとサポートアカウント

> **解説**: ランディングゾーン構築時にログアーカイブアカウントと監査アカウントが作られ、組織証跡（CloudTrail）と Config が自動構成される。
> **出典**: [Control Tower README #3 仕組みとネットワークガードレール](README.md#3-仕組みとネットワークガードレール)

## control-tower-006
- type: single
- difficulty: medium
- domain: 4
- tags: [scp, public-ip, security-group]

組織配下の全アカウントで「インターネットゲートウェイの VPC へのアタッチを禁止」するネットワークガードレールは、どのタイプか。

- [x] A. 予防的ガードレール（SCP）
- [ ] B. 発見的ガードレール（Config）
- [ ] C. プロアクティブガードレール（Hooks）
- [ ] D. 通知ガードレール（EventBridge）

> **解説**: 「禁止」する操作の制限は予防的ガードレールで、SCP により実装される。フローログの有効性検出のような評価は発見的。
> **出典**: [Control Tower README #3 仕組みとネットワークガードレール](README.md#3-仕組みとネットワークガードレール)

## control-tower-007
- type: single
- difficulty: easy
- domain: 4
- tags: [cost]

Control Tower の料金について正しいものはどれか。

- [x] A. Control Tower 自体は無料で、配下の Config・CloudTrail・S3 等の利用料が発生する
- [ ] B. アカウント数に応じた月額固定料金がかかる
- [ ] C. ガードレール1つあたり従量課金される
- [ ] D. ランディングゾーン構築時に一括の構築費用がかかる

> **解説**: Control Tower 自体は無料。実際のコストは内部で利用する Config・CloudTrail・S3 等のサービス利用料に依存する。
> **出典**: [Control Tower README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## control-tower-008
- type: multi
- difficulty: hard
- domain: 4
- tags: [scp, config-rules, use-case-fit]

Control Tower のガードレール（コントロール）の実装方式に関する記述のうち、正しいものを2つ選べ。

- [x] A. 予防的コントロールは SCP で実装され、禁止された操作を未然に防ぐ
- [ ] B. 発見的コントロールは SCP で実装され、操作を即座にブロックする
- [x] C. 発見的コントロールは Config ルールで実装され、非準拠リソースを検出する
- [ ] D. プロアクティブコントロールは IAM ポリシーで実装される
- [ ] E. すべてのコントロールは CloudTrail のみで実装される

> **解説**: 予防的＝SCP（操作の禁止）、発見的＝Config ルール（非準拠の検出）、プロアクティブ＝CloudFormation Hooks（プロビジョニング前検査）。B は発見的を SCP とする点、D は IAM とする点が誤り。
> **出典**: [Control Tower README #2 コアコンセプト](README.md#2-コアコンセプト)

## control-tower-009
- type: single
- difficulty: medium
- domain: 1
- tags: [subnetting, cidr, landing-zone]

複数チームにアカウントを払い出す際、CIDR の重複や不要なデフォルト VPC を防ぎたい。Control Tower で最も適切なアプローチはどれか。

- [ ] A. 各チームに手動で VPC を作らせ、後から Config で監査する
- [x] B. Account Factory で VPC の CIDR・サブネット・リージョンを標準化して払い出す
- [ ] C. SCP で VPC 作成自体をすべて禁止する
- [ ] D. Trusted Advisor の上限チェックに任せる

> **解説**: Account Factory による VPC 標準化が、CIDR 重複や野良 VPC を未然に防ぐ最も適切な手段。VPC 作成を全面禁止するとワークロードが動かなくなり過剰。
> **出典**: [Control Tower README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## control-tower-010
- type: single
- difficulty: easy
- domain: 4
- tags: [source-condition, scp]

「承認外リージョンの利用を禁止」したい。Control Tower のガードレールで実現する場合の分類として正しいものはどれか。

- [x] A. 予防的ガードレール（SCP による Deny）
- [ ] B. 発見的ガードレール（Config による検出のみ）
- [ ] C. プロアクティブガードレール（Hooks）
- [ ] D. 課金ガードレールで利用額を制限

> **解説**: 承認外リージョンでの操作を未然に禁止するのは予防的ガードレールで、SCP のリージョン制限により実装される。
> **出典**: [Control Tower README #3 仕組みとネットワークガードレール](README.md#3-仕組みとネットワークガードレール)
