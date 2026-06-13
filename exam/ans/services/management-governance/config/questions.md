---
service: config
domain_default: 4
source: README.md
source_sha256: 2b2412ace27ee042b3498058b61ea17802d22227fafd9f21c94042a5824758fa
generated: 2026-05-24
---

## config-001
- type: single
- difficulty: easy
- domain: 4
- tags: [cloudtrail-events, route-table]

AWS Config が記録・評価する対象として最も正確なのはどれか。

- [ ] A. 変更を行った API コール（誰が・いつ）
- [x] B. リソースの構成（設定状態）と過去の変化
- [ ] C. パケットのトラフィック流量
- [ ] D. エンドユーザーのインターネット体感

> **解説**: Config はリソースが今どういう設定か・過去どう変化したかを継続的に記録・評価する。API コールの実行者は CloudTrail、トラフィック流量はフローログ、エンドユーザー体感は Internet Monitor の領域。
> **出典**: [config README #1 概要](README.md#1-概要)

## config-002
- type: single
- difficulty: medium
- domain: 4
- tags: [waf, console-security]

SG が SSH(22) を `0.0.0.0/0` に開放していないかを継続的に評価したい。利用するマネージドルールはどれか。

- [x] A. `restricted-ssh`
- [ ] B. `vpc-flow-logs-enabled`
- [ ] C. `eip-attached`
- [ ] D. `vpc-network-acl-unused-check`

> **解説**: `restricted-ssh` は SG が SSH(22) を `0.0.0.0/0`・`::/0` に開放していないかを検査する。`vpc-flow-logs-enabled` はフローログ有効性、`eip-attached` は未使用 EIP、`vpc-network-acl-unused-check` は未使用 NACL の検出。
> **出典**: [config README #3 仕組みとネットワーク準拠ルール](README.md#3-仕組みとネットワーク準拠ルール)

## config-003
- type: single
- difficulty: medium
- domain: 4
- tags: [automation]

Config が SG の 3389 全開放を非準拠と判定した。自動でポートを閉塞する仕組みはどれか。

- [ ] A. CloudFormation のドリフト検出
- [x] B. SSM Automation による修復（Remediation）
- [ ] C. CloudTrail のイベント履歴
- [ ] D. CloudWatch のメトリクスフィルター

> **解説**: Config の修復（Remediation）は SSM Automation を用いて非準拠リソースを自動是正する。SG の制限ポート全開放を検出したら、修復アクションでポートを閉塞できる。ドリフト検出や CloudTrail は是正機能ではない。
> **出典**: [config README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## config-004
- type: single
- difficulty: medium
- domain: 4
- tags: [firewall-manager, use-case-fit]

AWS Firewall Manager を利用するための前提として必要なものはどれか。

- [ ] A. CloudTrail の組織証跡
- [x] B. AWS Config の有効化
- [ ] C. CloudFormation スタックセット
- [ ] D. Internet Monitor の関連付け

> **解説**: AWS Firewall Manager は AWS Config の有効化を前提とする。Config による構成情報を基にポリシーの準拠状況を評価するため。組織証跡やスタックセットは前提ではない。
> **出典**: [config README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## config-005
- type: single
- difficulty: medium
- domain: 4
- tags: [config-rules, multi-account]

組織内の全アカウント・全リージョンのネットワーク準拠状況を一元的に把握したい。利用する機能はどれか。

- [ ] A. コンフォーマンスパック
- [x] B. アグリゲーター
- [ ] C. 構成項目（Configuration Item）
- [ ] D. 修復（Remediation）

> **解説**: アグリゲーターは複数アカウント/リージョンの評価結果を集約し、組織横断で準拠状況を一元把握できる。コンフォーマンスパックはルール群のデプロイ、構成項目は単一リソースのスナップショット。
> **出典**: [config README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## config-006
- type: single
- difficulty: easy
- domain: 4
- tags: [cloudtrail-events, use-case-fit]

「SG の設定が望ましい状態か」を継続監査する役割と、「誰が変更したか」を記録する役割の正しい組み合わせはどれか。

- [ ] A. 継続監査=CloudTrail、実行者記録=Config
- [x] B. 継続監査=Config、実行者記録=CloudTrail
- [ ] C. 継続監査=CloudWatch、実行者記録=Config
- [ ] D. 両方とも CloudTrail

> **解説**: 設定が望ましい状態かの継続監査は Config、変更を行った実行者の記録は CloudTrail。両者は補完関係にあり、準拠判定と原因追跡を組み合わせる。
> **出典**: [config README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## config-007
- type: single
- difficulty: medium
- domain: 4
- tags: [waf, flow-logs]

VPC でフローログが有効になっているかを継続的に評価したい。利用するマネージドルールはどれか。

- [ ] A. `restricted-ssh`
- [x] B. `vpc-flow-logs-enabled`
- [ ] C. `vpc-default-security-group-closed`
- [ ] D. `vpc-sg-port-restriction-check`

> **解説**: `vpc-flow-logs-enabled` は VPC でフローログが有効かを検査する。`restricted-ssh` は SSH 開放、`vpc-default-security-group-closed` はデフォルト SG の閉塞、`vpc-sg-port-restriction-check` は制限ポートの全開放を見る。
> **出典**: [config README #3 仕組みとネットワーク準拠ルール](README.md#3-仕組みとネットワーク準拠ルール)

## config-008
- type: single
- difficulty: easy
- domain: 4
- tags: [config-rules, use-case-fit]

リソースのある時点ごとの設定スナップショットを表す Config の用語はどれか。

- [x] A. 構成項目（Configuration Item）
- [ ] B. コンフォーマンスパック
- [ ] C. アグリゲーター
- [ ] D. Config ルール

> **解説**: 構成項目はあるリソースの時点ごとの設定スナップショットで、これらが構成履歴/タイムラインとして時系列に蓄積される。コンフォーマンスパックはルール群、アグリゲーターは集約、Config ルールは評価ロジック。
> **出典**: [config README #2 コアコンセプト](README.md#2-コアコンセプト)

## config-009
- type: multi
- difficulty: hard
- domain: 4
- tags: [waf, security-group]

SG の不適切な全開放を検出するネットワーク関連の Config マネージドルールを 2 つ選べ。

- [x] A. `vpc-sg-open-only-to-authorized-ports`
- [x] B. `vpc-sg-port-restriction-check`
- [ ] C. `vpc-flow-logs-enabled`
- [ ] D. `eip-attached`
- [ ] E. `vpc-network-acl-unused-check`

> **解説**: `vpc-sg-open-only-to-authorized-ports` は `0.0.0.0/0` 開放の SG が許可ポートのみかを、`vpc-sg-port-restriction-check` は 22/3389 等の制限ポートを全開放していないかを検査する。残りはフローログ有効性や未使用リソース検出で SG 全開放の検出が目的ではない。
> **出典**: [config README #3 仕組みとネットワーク準拠ルール](README.md#3-仕組みとネットワーク準拠ルール)

## config-010
- type: single
- difficulty: medium
- domain: 4
- tags: [cost, config-rules]

AWS Config のコストを最適化したい。正しい考え方はどれか。

- [ ] A. 必ず全リソースタイプを記録対象にする
- [x] B. 記録対象リソースタイプを選択し、不要な全記録を避ける
- [ ] C. ルール評価回数は課金に影響しない
- [ ] D. コンフォーマンスパックは無料なので無制限に使う

> **解説**: 課金は記録された構成項目数＋ルール評価回数＋コンフォーマンスパック評価に基づく。記録対象リソースタイプを選択し全記録（コスト増）を避けるのが最適化の基本。ルール評価回数も課金要素。
> **出典**: [config README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## config-011
- type: single
- difficulty: medium
- domain: 4
- tags: [config-rules]

関連する複数の Config ルールと是正アクションをまとめて一括デプロイしたい。利用する機能はどれか。

- [ ] A. アグリゲーター
- [x] B. コンフォーマンスパック
- [ ] C. 構成タイムライン
- [ ] D. 修復（Remediation）単体

> **解説**: コンフォーマンスパックは関連ルールと是正をまとめてデプロイする機能で、標準的な準拠セットを一括適用できる。アグリゲーターは結果集約、修復単体は個別ルールの是正処理。
> **出典**: [config README #2 コアコンセプト](README.md#2-コアコンセプト)
