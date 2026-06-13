---
service: aws-cli
domain_default: 2
source: README.md
source_sha256: e7c3a2a3551cc14744037cfc7adbc1fadda95daecef5c538d5324b6ed32ef614
generated: 2026-05-24
---

## aws-cli-001
- type: single
- difficulty: medium
- domain: 2
- tags: [iac]

再現性ある VPC ネットワーク基盤を反復構築・バージョン管理したい。AWS CLI と比較して最も適した手段はどれか。

- [ ] A. AWS CLI スクリプトを cron で繰り返し実行する
- [x] B. CloudFormation 等の宣言的 IaC を使う
- [ ] C. マネジメントコンソールで毎回手動構築する
- [ ] D. SDK で命令的に毎回作り直す

> **解説**: 一度きりの調査や緊急対応は命令的な CLI/SDK が向くが、再現性・バージョン管理・レビュー可能性が必要な環境構築は CloudFormation 等の宣言的 IaC が適する。CLI スクリプトは状態管理がなく冪等性を担保しにくい。
> **出典**: [aws-cli README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## aws-cli-002
- type: single
- difficulty: medium
- domain: 3
- tags: [reachability-analyzer, troubleshooting]

VPC Reachability Analyzer による到達性解析を CLI で自動化したい。使用するコマンドの組み合わせはどれか。

- [ ] A. `aws ec2 create-flow-logs` と `describe-flow-logs`
- [x] B. `aws ec2 create-network-insights-path` と `start-network-insights-analysis`
- [ ] C. `aws cloudtrail put-event-selectors` と `lookup-events`
- [ ] D. `aws directconnect describe-connections` と `describe-virtual-interfaces`

> **解説**: Reachability Analyzer の経路定義は `create-network-insights-path`、解析実行は `start-network-insights-analysis` で行う。フローログ系や CloudTrail セレクター系、Direct Connect 系は別目的のコマンド。
> **出典**: [aws-cli README #2 ネットワーク運用での使いどころ](README.md#2-ネットワーク運用での使いどころ)

## aws-cli-003
- type: single
- difficulty: medium
- domain: 4
- tags: [iam-policy, security-group]

EC2 上で動くスクリプトから CLI を実行する。認証情報の扱いとして最も適切なのはどれか。

- [ ] A. アクセスキーをスクリプトにハードコードする
- [ ] B. アクセスキーを環境変数に平文で常時設定する
- [x] C. EC2 のインスタンスプロファイル（IAM ロール）を利用する
- [ ] D. ルートユーザーのアクセスキーを使う

> **解説**: 認証情報はハードコードせず、EC2 ではインスタンスプロファイル（IAM ロール）を使うのが最小権限・安全性の観点で適切。ロールは一時認証情報を自動ローテーションする。ルートキーの利用は禁止事項。
> **出典**: [aws-cli README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## aws-cli-004
- type: single
- difficulty: hard
- domain: 3
- tags: [dns, automation, quotas]

大量のセキュリティグループから特定条件のものだけを抽出・整形して出力したい。CLI の機能はどれか。

- [ ] A. `--profile` でプロファイルを切り替える
- [x] B. `--query`（JMESPath）とページネーションで抽出・整形する
- [ ] C. `--endpoint-url` でリージョンを変更する
- [ ] D. `--dry-run` で実行をシミュレートする

> **解説**: 大量のネットワークリソースは `--query`（JMESPath）で絞り込み・整形し、ページネーションで全件を取得する。`--profile` は認証切替、`--dry-run` は権限確認用で抽出機能ではない。
> **出典**: [aws-cli README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## aws-cli-005
- type: single
- difficulty: easy
- domain: 3
- tags: [automation, troubleshooting]

SG・ルートテーブル・ENI の現状を素早く調査したい。代表的な CLI コマンド群はどれか。

- [x] A. `describe-security-groups` / `describe-route-tables` / `describe-network-interfaces`
- [ ] B. `create-security-group` / `create-route` / `create-network-interface`
- [ ] C. `delete-security-group` / `delete-route` / `delete-network-interface`
- [ ] D. `put-event-selectors` / `start-network-insights-analysis` / `create-flow-logs`

> **解説**: 調査・トラブルシュートには `describe-*` 系の読み取りコマンドを用いる。`create-*`/`delete-*` は変更操作で調査用途ではない。
> **出典**: [aws-cli README #2 ネットワーク運用での使いどころ](README.md#2-ネットワーク運用での使いどころ)

## aws-cli-006
- type: single
- difficulty: medium
- domain: 4
- tags: [cloudtrail-events]

CloudTrail のネットワークアクティビティイベントを CLI で有効化したい。使用するコマンドはどれか。

- [ ] A. `aws ec2 create-flow-logs`
- [x] B. `aws cloudtrail put-event-selectors`
- [ ] C. `aws config put-config-rule`
- [ ] D. `aws ec2 create-network-insights-path`

> **解説**: CloudTrail のネットワークアクティビティイベントを含むイベントセレクター設定は `put-event-selectors` で行う。フローログや Reachability Analyzer、Config ルールは別サービスのコマンド。
> **出典**: [aws-cli README #2 ネットワーク運用での使いどころ](README.md#2-ネットワーク運用での使いどころ)

## aws-cli-007
- type: single
- difficulty: easy
- domain: 2
- tags: [cost, api-endpoint]

AWS CLI のコストとして正しいものはどれか。

- [ ] A. コマンド実行 1 回ごとに固定の CLI 利用料が発生する
- [x] B. CLI 自体は無料で、API 呼び出しに伴う各サービス料金のみが発生する
- [ ] C. `--query` を使うと追加課金される
- [ ] D. ページネーションのページ数に応じて課金される

> **解説**: CLI 自体は無料で、課金されるのは呼び出した先の各 AWS サービスの料金のみ。ただし API スロットリングには留意する必要がある。
> **出典**: [aws-cli README #5 制約・コスト](README.md#5-制約コスト)

## aws-cli-008
- type: single
- difficulty: medium
- domain: 3
- tags: [hybrid, direct-connect, vpn]

ハイブリッド接続の状態を CLI で確認したい。Direct Connect 接続と VPN 接続を調べるコマンドの組み合わせはどれか。

- [ ] A. `aws ec2 describe-subnets` と `aws ec2 describe-route-tables`
- [x] B. `aws directconnect describe-connections` と `aws ec2 describe-vpn-connections`
- [ ] C. `aws cloudtrail lookup-events` と `aws config describe-compliance`
- [ ] D. `aws ec2 create-flow-logs` と `aws ec2 describe-flow-logs`

> **解説**: Direct Connect 接続は `directconnect describe-connections`、Site-to-Site VPN 接続は `ec2 describe-vpn-connections` で確認する。サブネットやフローログ、CloudTrail/Config は別目的。
> **出典**: [aws-cli README #2 ネットワーク運用での使いどころ](README.md#2-ネットワーク運用での使いどころ)

## aws-cli-009
- type: multi
- difficulty: medium
- domain: 2
- tags: [iac, use-case-fit]

AWS CLI（命令的）の利用が適しているシナリオを 2 つ選べ。

- [x] A. 一度きりのネットワーク到達性の調査
- [x] B. 障害発生時の緊急対応として SG ルールを即座に修正する
- [ ] C. 複数アカウントへ標準ネットワーク基盤を再現性をもって展開する
- [ ] D. ドリフト検出により手動変更を継続的に監査する
- [ ] E. 組織全体のリソース構成準拠を一元評価する

> **解説**: CLI は一度きりの調査やスクリプト的処理、緊急対応に向く。再現性ある基盤展開やドリフト検出は CloudFormation、構成準拠の継続監査は Config の領域。
> **出典**: [aws-cli README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## aws-cli-010
- type: single
- difficulty: easy
- domain: 3
- tags: [flow-logs, automation]

コンソールで設定するフローログを CLI で自動化したい。正しい認識はどれか。

- [x] A. `aws ec2 create-flow-logs` でフローログ作成を自動化できる
- [ ] B. フローログはコンソールでしか設定できず CLI では不可
- [ ] C. フローログ作成には CloudFormation が必須
- [ ] D. フローログは Config ルールでのみ有効化できる

> **解説**: フローログ・到達性解析・CloudTrail セレクター等、コンソールで設定する内容は CLI/SDK でも自動化可能で、フローログ作成は `create-flow-logs` で行える。CloudFormation や Config は必須ではない。
> **出典**: [aws-cli README #2 ネットワーク運用での使いどころ](README.md#2-ネットワーク運用での使いどころ)
