---
service: cloudwatch
domain_default: 3
source: README.md
source_sha256: bfb331c2569d51db80a542b6fb7c114021f4d507b0211740fe63cbb66b5f4e55
generated: 2026-05-24
---

## cloudwatch-001
- type: single
- difficulty: medium
- domain: 3
- tags: [flow-logs, monitoring]

VPC フローログを CloudWatch Logs と S3 のどちらに送るか検討している。即時にクエリ分析したい場合の選択として正しいものはどれか。

- [ ] A. S3 に送り Logs Insights で分析する
- [x] B. CloudWatch Logs に送り Logs Insights で即時クエリする
- [ ] C. S3 に送り CloudWatch メトリクスで分析する
- [ ] D. Data Firehose に送りアラームで分析する

> **解説**: フローログを CloudWatch Logs に送ると Logs Insights で即時クエリ可能。大規模・低コストのバッチ分析は S3 + Athena が向く。Logs Insights は CloudWatch Logs に対するクエリ機能。
> **出典**: [cloudwatch README #4-1 フローログ／ELB ログの集約](README.md#4-1-フローログelb-ログの集約)

## cloudwatch-002
- type: single
- difficulty: medium
- domain: 3
- tags: [alb, network-firewall]

ALB のアクセスログの既定の保存先はどこか。

- [ ] A. CloudWatch Logs
- [x] B. S3
- [ ] C. CloudTrail
- [ ] D. CloudWatch メトリクス

> **解説**: ELB（ALB/NLB）のアクセスログの既定保存先は S3。CloudWatch には ELB のメトリクス（`ActiveFlowCount`、`ProcessedBytes`、`HealthyHostCount` 等）が送られる。両者を混同しないこと。
> **出典**: [cloudwatch README #4-1 フローログ／ELB ログの集約](README.md#4-1-フローログelb-ログの集約)

## cloudwatch-003
- type: single
- difficulty: hard
- domain: 3
- tags: [monitoring, hybrid]

Direct Connect 経由のオンプレ接続でパケットロスやレイテンシ劣化が疑われる。エージェント不要で数分で切り分けたい。最適な機能はどれか。

- [x] A. Network Synthetic Monitor
- [ ] B. Network Flow Monitor
- [ ] C. Internet Monitor
- [ ] D. Logs Insights

> **解説**: Network Synthetic Monitor は AWS マネージドのプローブ（エージェント不要、サブネットと宛先 IP を指定）で AWS↔オンプレ間のハイブリッド接続のパケットロス/レイテンシを能動計測する。オンプレ宛の合成監視に最適。
> **出典**: [cloudwatch README #4-2 3つのネットワーク監視機能の使い分け](README.md#4-2-3つのネットワーク監視機能の使い分け最重要)

## cloudwatch-004
- type: single
- difficulty: hard
- domain: 3
- tags: [monitoring, awsvpc]

VPC 内の実トラフィックの遅延/パケットロスが「自社アプリ」起因か「AWS 基盤」起因かを判別したい。最適な機能はどれか。

- [ ] A. Network Synthetic Monitor
- [x] B. Network Flow Monitor
- [ ] C. Internet Monitor
- [ ] D. メトリクスフィルター

> **解説**: Network Flow Monitor はインスタンスに軽量エージェントを導入し、VPC 内の実ワークロードの TCP RTT・再送・再送タイムアウト等を計測。NHI と合わせ、劣化の原因が自社か AWS 基盤かを判別できる。
> **出典**: [cloudwatch README #4-2 3つのネットワーク監視機能の使い分け](README.md#4-2-3つのネットワーク監視機能の使い分け最重要)

## cloudwatch-005
- type: single
- difficulty: hard
- domain: 3
- tags: [monitoring, use-case-fit]

エンドユーザーとアプリ間のインターネット経路で、特定の ISP/地域起因の遅延を検知し CloudFront 等への切替えを検討したい。最適な機能はどれか。

- [ ] A. Network Synthetic Monitor
- [ ] B. Network Flow Monitor
- [x] C. Internet Monitor
- [ ] D. CloudWatch Agent

> **解説**: Internet Monitor は AWS のグローバル計測データと city-network（クライアント所在地×ASN）単位の計測で、エンドユーザー体感（可用性・パフォーマンス・TTFB）を把握する。ヘルスイベントは EventBridge に送られ、ISP/地域起因の遅延検知に向く。
> **出典**: [cloudwatch README #4-2 3つのネットワーク監視機能の使い分け](README.md#4-2-3つのネットワーク監視機能の使い分け最重要)

## cloudwatch-006
- type: single
- difficulty: medium
- domain: 3
- tags: [eni, monitoring]

Network Health Indicator (NHI) について正しいものはどれか。

- [ ] A. NAT Gateway 専用のメトリクスである
- [x] B. 劣化の原因が AWS ネットワーク側か否かを確率的に示すバイナリ指標
- [ ] C. Internet Monitor のみで使えるレイテンシ生値
- [ ] D. アラームの評価期間を表す設定値

> **解説**: NHI は Network Synthetic Monitor / Flow Monitor 共通の指標で、劣化原因が AWS ネットワーク側か否かを確率的に示すバイナリ指標。切り分けの初動判断に使える。
> **出典**: [cloudwatch README #4-2 3つのネットワーク監視機能の使い分け](README.md#4-2-3つのネットワーク監視機能の使い分け最重要)

## cloudwatch-007
- type: single
- difficulty: medium
- domain: 3
- tags: [monitoring]

EC2 のメモリ使用率やオンプレサーバーのカスタムログを CloudWatch で監視したい。必要なものはどれか。

- [ ] A. 標準メトリクスのみで取得できる
- [x] B. CloudWatch Agent を導入する
- [ ] C. VPC フローログを有効化する
- [ ] D. Internet Monitor を関連付ける

> **解説**: メモリ・ディスク使用率・プロセスやアプリのカスタムログは標準メトリクスでは取れず、CloudWatch Agent を導入して収集する。Agent は EC2 だけでなくオンプレサーバーにも導入でき、ログは Logs、メトリクスはメトリクスへ送る。
> **出典**: [cloudwatch README #4-3 CloudWatch Agent](README.md#4-3-cloudwatch-agent)

## cloudwatch-008
- type: single
- difficulty: medium
- domain: 3
- tags: [monitoring, service-discovery]

NAT Gateway や Transit Gateway の帯域・パケットドロップを監視したい。CloudWatch で参照する対象はどれか。

- [ ] A. CloudTrail の管理イベント
- [x] B. `AWS/NATGateway`・`AWS/TransitGateway` 等の名前空間メトリクス
- [ ] C. Config の構成項目
- [ ] D. ELB のアクセスログ

> **解説**: NAT Gateway・Transit Gateway・VPN・Direct Connect 等はそれぞれ名前空間メトリクス（`AWS/NATGateway` 等）を CloudWatch に送出し、閾値アラームを作って運用を自動化する。CloudTrail/Config は監査用途。
> **出典**: [cloudwatch README #2 コアコンセプト](README.md#2-コアコンセプト)

## cloudwatch-009
- type: single
- difficulty: easy
- domain: 3
- tags: [monitoring]

CloudWatch Logs に集約したログ中の特定パターンの出現回数をメトリクス化してアラームを作りたい。使う機能はどれか。

- [ ] A. ダッシュボード
- [x] B. メトリクスフィルター
- [ ] C. Internet Monitor
- [ ] D. アグリゲーター

> **解説**: メトリクスフィルターはログ中のパターン出現回数をメトリクスに変換し、それを基にアラーム化できる。CloudTrail 由来の不正操作検知などに活用される。ダッシュボードは可視化機能。
> **出典**: [cloudwatch README #2 コアコンセプト](README.md#2-コアコンセプト)

## cloudwatch-010
- type: multi
- difficulty: hard
- domain: 3
- tags: [monitoring, use-case-fit]

CloudWatch の 3 つのネットワーク監視機能の使い分けとして正しいものを 2 つ選べ。

- [x] A. オンプレ宛の能動計測（合成監視）には Network Synthetic Monitor
- [x] B. VPC 内ワークロードの実トラフィック計測には Network Flow Monitor
- [ ] C. インターネット越しのエンドユーザー体感には Network Synthetic Monitor
- [ ] D. オンプレ宛の合成監視には Internet Monitor
- [ ] E. VPC 内の実トラフィック計測には Internet Monitor

> **解説**: オンプレ宛の能動計測は Synthetic Monitor、VPC 内の実トラフィックは Flow Monitor、インターネット越しのエンドユーザー体感は Internet Monitor。計測対象と仕組み（プローブ/エージェント/グローバル計測）の組み合わせを押さえる。
> **出典**: [cloudwatch README #4-2 3つのネットワーク監視機能の使い分け](README.md#4-2-3つのネットワーク監視機能の使い分け最重要)

## cloudwatch-011
- type: single
- difficulty: medium
- domain: 3
- tags: [cost, flow-logs]

大量のフローログを低コストでバッチ分析したい。最も適した構成はどれか。

- [ ] A. CloudWatch Logs + Logs Insights
- [x] B. S3 + Athena
- [ ] C. Network Flow Monitor のエージェント
- [ ] D. ダッシュボードのみ

> **解説**: フローログを大量にバッチ分析するなら S3 + Athena が低コストで向く。リアルタイム性が要る場合は CloudWatch Logs + Logs Insights を使い分けるのがコスト最適化の定石。
> **出典**: [cloudwatch README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## cloudwatch-012
- type: single
- difficulty: easy
- domain: 3
- tags: [monitoring, cost]

CloudWatch の標準メトリクスと詳細モニタリングの料金について正しいものはどれか。

- [ ] A. 標準も詳細も無料である
- [x] B. 標準メトリクス（5 分間隔）は無料、詳細モニタリング（1 分間隔）は課金
- [ ] C. 標準メトリクスは課金、詳細モニタリングは無料
- [ ] D. いずれもプローブ単位で課金される

> **解説**: 標準メトリクス（基本モニタリング、5 分間隔）は無料、詳細モニタリング（1 分間隔）は課金。プローブ単位課金は Network Synthetic Monitor のコスト構造。
> **出典**: [cloudwatch README #6 制約・上限・コスト](README.md#6-制約上限コスト)
