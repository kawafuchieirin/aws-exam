---
service: cost-explorer
domain_default: 3
source: README.md
source_sha256: 447cfcf7d8c58dc6eafcd249c2992a3198594dc01a3e07de5a45d5942bf79068
generated: 2026-05-24
---

## cost-explorer-001
- type: single
- difficulty: easy
- domain: 3
- tags: [cost, data-transfer]

どのネットワークコンポーネントが転送料を押し上げているか特定したい。Cost Explorer で最初に行うべきグループ化はどれか。

- [ ] A. リンクされたアカウント別にグループ化する
- [x] B. Usage Type（または Usage Type Group）でグループ化する
- [ ] C. API オペレーション別にグループ化する
- [ ] D. 請求エンティティ別にグループ化する

> **解説**: データ転送は `DataTransfer-Out-Bytes` や `NatGateway-Bytes` 等の課金細目（Usage Type）で表現される。Usage Type / Usage Type Group でグループ化することで、インターネット送出・AZ 間・リージョン間などの転送料を分離して把握できる。
> **出典**: [cost-explorer README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## cost-explorer-002
- type: single
- difficulty: medium
- domain: 3
- tags: [nat, cost]

NAT Gateway のコストを Cost Explorer で分析した結果、`NatGateway-Bytes`（データ処理料）が大半を占めていた。最も適切な最適化はどれか。

- [ ] A. NAT Gateway を NAT インスタンスに置き換える
- [x] B. S3/DynamoDB 向けトラフィックを Gateway エンドポイントに逃がす
- [ ] C. NAT Gateway の時間課金を削減するため台数を増やす
- [ ] D. Cost Explorer の API 呼び出し回数を減らす

> **解説**: `NatGateway-Bytes` はデータ処理料。S3/DynamoDB へのアクセスを無料の Gateway エンドポイント経由にすると NAT を通らなくなり、データ処理料を直接削減できる。台数を増やしてもデータ処理量は減らない。
> **出典**: [cost-explorer README #3 NAT Gateway コスト分析](README.md#3-試験頻出ポイントネットワーク観点)

## cost-explorer-003
- type: single
- difficulty: medium
- domain: 3
- tags: [nat, cost]

Cost Explorer で確認できる NAT Gateway の 2 つの課金細目の組み合わせとして正しいものはどれか。

- [ ] A. `NatGateway-Hours` と `DataTransfer-Out-Bytes`
- [x] B. `NatGateway-Hours`（時間課金）と `NatGateway-Bytes`（データ処理料）
- [ ] C. `VPC-Endpoint-Bytes` と `NatGateway-Bytes`
- [ ] D. `NatGateway-Requests` と `NatGateway-Hours`

> **解説**: NAT Gateway は「稼働時間（`NatGateway-Hours`）」と「処理データ量（`NatGateway-Bytes`）」の 2 軸で課金される。どちらが支配的かで最適化アプローチが変わる。
> **出典**: [cost-explorer README #3 NAT Gateway コスト分析](README.md#3-試験頻出ポイントネットワーク観点)

## cost-explorer-004
- type: single
- difficulty: medium
- domain: 3
- tags: [vpc-endpoint, cost]

インターフェイスエンドポイントの時間・データ処理課金が高額だと Cost Explorer で判明した。コスト削減の検討事項として最も適切なのはどれか。

- [ ] A. すべてのエンドポイントを削除する
- [x] B. 対象サービスが Gateway エンドポイントで代替可能か確認する
- [ ] C. Interface エンドポイントのサブネット数を増やす
- [ ] D. Cost Explorer の予測期間を延ばす

> **解説**: S3/DynamoDB は無料の Gateway エンドポイントで代替できる。Interface エンドポイントは時間＋データ処理課金が発生するため、Usage Type で課金を確認し Gateway で代替可能かを判断するのが定石。
> **出典**: [cost-explorer README #3 VPC エンドポイントコスト](README.md#3-試験頻出ポイントネットワーク観点)

## cost-explorer-005
- type: single
- difficulty: medium
- domain: 1
- tags: [data-transfer, cost]

同一リージョン内で AZ をまたぐ通信のコストを削減する根拠データを得たい。Cost Explorer の活用として正しいものはどれか。

- [ ] A. AZ 間転送は無料なので分析の必要はない
- [x] B. AZ 間転送も課金対象であり、同一 AZ 配置への見直し根拠として可視化する
- [ ] C. AZ 間転送は Gateway エンドポイントを使えばゼロになる
- [ ] D. AZ 間転送は Cost Explorer では一切確認できない

> **解説**: 同一リージョン内でも AZ をまたぐ通信は課金対象。Cost Explorer で可視化し、レイテンシ・コスト要件に応じて同一 AZ 配置などアーキテクチャ見直しの根拠データに使える。
> **出典**: [cost-explorer README #3 AZ 間転送](README.md#3-試験頻出ポイントネットワーク観点)

## cost-explorer-006
- type: single
- difficulty: medium
- domain: 3
- tags: [data-transfer, transit-gateway]

クロスリージョンレプリケーションや Transit Gateway のリージョン間ピアリングによる転送料を特定したい。適切な手段はどれか。

- [ ] A. サービス別グループ化のみで十分
- [x] B. リージョン別グループ化または Usage Type で特定する
- [ ] C. タグ別グループ化のみで特定できる
- [ ] D. リージョン間転送は Cost Explorer の対象外

> **解説**: リージョン間転送はリージョン別グループ化や Usage Type で切り分けられる。クロスリージョンレプリケーションや TGW のリージョン間ピアリングのコスト要因の特定に使う。
> **出典**: [cost-explorer README #3 リージョン間転送](README.md#3-試験頻出ポイントネットワーク観点)

## cost-explorer-007
- type: single
- difficulty: easy
- domain: 3
- tags: [cost, api-endpoint]

Cost Explorer の利用料金について正しいものはどれか。

- [ ] A. UI 利用・API 利用ともに無料
- [x] B. UI 利用は無料、API はリクエストごとに $0.01
- [ ] C. UI 利用は有料、API は無料
- [ ] D. 有効化した時点で月額固定料金が発生する

> **解説**: Cost Explorer の UI 利用は無料だが、API はリクエストごとに $0.01 課金される。プログラムから頻繁に呼び出す場合はコストに注意。
> **出典**: [cost-explorer README #5 制約・上限・コスト](README.md#5-制約上限コスト)

## cost-explorer-008
- type: single
- difficulty: medium
- domain: 3
- tags: [cost, use-case-fit, monitoring]

Cost Explorer のデータ反映・履歴・予測に関する説明として正しいものはどれか。

- [ ] A. データはリアルタイムに反映され、履歴は無制限
- [x] B. 当月分は約 24 時間後に反映、履歴は最大 13 か月、予測は最大 18 か月先
- [ ] C. 履歴は最大 18 か月、予測は最大 13 か月先
- [ ] D. データ反映は即時で、予測機能は提供されない

> **解説**: コストデータは当月分が約 24 時間後に反映され以降 24 時間ごとに更新。履歴は最大 13 か月、予測は最大 18 か月先まで可能。リアルタイム性が必要なアラートは Cost Anomaly Detection 等を併用する。
> **出典**: [cost-explorer README #5 制約・上限・コスト](README.md#5-制約上限コスト)

## cost-explorer-009
- type: single
- difficulty: medium
- domain: 4
- tags: [cost, landing-zone]

組織として Cost Explorer の有効化を検討している。運用上注意すべき点はどれか。

- [ ] A. 月初にしか有効化できない
- [x] B. 一度有効化すると無効化できない
- [ ] C. 有効化にはルートアカウントの MFA 解除が必須
- [ ] D. リージョンごとに個別有効化が必要

> **解説**: Cost Explorer は一度有効化すると無効化できない仕様。ガバナンス上、有効化の意思決定時に把握しておくべきポイント。
> **出典**: [cost-explorer README #5 制約・上限・コスト](README.md#5-制約上限コスト)

## cost-explorer-010
- type: multi
- difficulty: medium
- domain: 3
- tags: [cost, use-case-fit]

ネットワーク転送コストを継続的に分析・監視する構成を作りたい。適切な連携はどれか。2 つ選べ。

- [x] A. Cost & Usage Report (CUR) を S3 に出力し Athena で詳細明細を解析する
- [x] B. AWS Budgets / Cost Anomaly Detection で転送料の急増をアラートする
- [ ] C. VPC フローログを Cost Explorer に直接取り込んで課金する
- [ ] D. Cost Explorer の UI からパケットの中身を解析する
- [ ] E. CloudTrail のログを Cost Explorer に保存して転送料を算出する

> **解説**: CUR は Cost Explorer と同一データセットで、S3 出力＋Athena による詳細解析に向く。転送料の急増検知は Budgets / Cost Anomaly Detection。Cost Explorer はパケット内容やフローログそのものを扱う分析ツールではない。
> **出典**: [cost-explorer README #4 他サービスとの連携](README.md#4-他サービスとの連携)

## cost-explorer-011
- type: multi
- difficulty: hard
- domain: 3
- tags: [cost, data-transfer]

Cost Explorer の Usage Type を使ってネットワーク転送料を切り分ける際に該当する課金細目はどれか。2 つ選べ。

- [x] A. `DataTransfer-Out-Bytes`（インターネット送出）
- [x] B. `VPC-Endpoint-Bytes`（インターフェイスエンドポイントのデータ処理）
- [ ] C. `S3-Storage-GB-Month`（ストレージ容量）
- [ ] D. `EC2-Instance-Hours`（インスタンス稼働時間）
- [ ] E. `Lambda-GB-Second`（関数実行時間）

> **解説**: 転送料の Usage Type には `DataTransfer-Out-Bytes`・`NatGateway-Bytes`・`VPC-Endpoint-Bytes` などがある。ストレージ容量・インスタンス時間・Lambda 実行時間は転送料ではなくリソース利用課金。
> **出典**: [cost-explorer README #2 コアコンセプト](README.md#2-コアコンセプト)
