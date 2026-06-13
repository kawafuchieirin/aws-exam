# Amazon CloudWatch の要点

> 重要度: ○ ／ 第3分野「ネットワーク管理と運用」の中核。フローログ/各種ログの集約先、メトリクス・アラームによる異常検知、3つのネットワーク監視機能の使い分けが問われる。

## これは何
- AWS リソースとアプリの**メトリクス・ログ・イベント**を収集し、可視化・アラート・自動アクションを行う統合監視サービス。
- ネットワーク観点では、VPC フローログ等の**配信先（CloudWatch Logs）**、各サービスの**名前空間メトリクス**からの閾値アラーム、専用の能動計測機能を提供する。

## 試験頻出ポイント
- **VPC フローログの配信先**は **CloudWatch Logs / S3 / Data Firehose**。CloudWatch Logs に送れば **Logs Insights** で即時クエリ可能（REJECT 多発・特定 IP の特定など）。
- **ELB（ALB/NLB）のアクセスログの既定保存先は S3**。CloudWatch には ELB の**メトリクス**（`ActiveFlowCount`・`ProcessedBytes`・`HealthyHostCount`）が送られる。両者を混同しない。
- 各サービスは**名前空間メトリクス**を送出: `AWS/NATGateway`・`AWS/TransitGateway`・`AWS/VPN`・`AWS/NetworkELB`。閾値アラームで帯域・パケットドロップ・BGP 状態を監視。
- **アラーム**のアクション: **SNS 通知**・Auto Scaling・EC2 アクション。複合（複合アラーム）も可。
- **メトリクスフィルター**: ログ中のパターン出現回数を**メトリクス化**しアラーム化（CloudTrail 由来の不正操作検知などに活用）。
- **CloudWatch Agent**: 標準メトリクスで取れない**メモリ・ディスク使用率・プロセス・カスタムログ**を収集。**オンプレサーバーにも導入可**（ハイブリッド監視）。
- **3つのネットワーク監視機能**（最重要、下表）。
- **NHI（Network Health Indicator）**: Synthetic / Flow Monitor 共通の指標。劣化原因が **AWS ネットワーク側か否か**を確率的に示す**バイナリ指標**。
- [CloudTrail](cloudtrail.md) の監査ログを CloudWatch Logs に連携し、メトリクスフィルター＋アラームで不正操作を検知。

## 比較・選択の判断

### 3つのネットワーク監視機能
| 要件 | 解答 |
|---|---|
| オンプレ宛の能動計測（合成監視、Direct Connect/VPN の劣化切り分け） | **Network Synthetic Monitor**（マネージドプローブ、エージェント不要） |
| VPC 内ワークロードの実 TCP トラフィック（自社アプリか AWS 基盤か判別） | **Network Flow Monitor**（インスタンスに軽量エージェント、TCP RTT/再送） |
| エンドユーザーとアプリ間のインターネット経路の体感 | **Internet Monitor**（city-network 単位、ヘルスイベントは EventBridge へ） |

### その他の選択
| 要件 | 解答 |
|---|---|
| フローログを即時クエリ分析 | CloudWatch Logs + **Logs Insights** |
| 大量フローログを低コストでバッチ分析 | **S3 + Athena** |
| メモリ/ディスク/カスタムログ収集 | **CloudWatch Agent** |
| ログのパターン出現をアラーム化 | **メトリクスフィルター** |
| インターネット経路の地域/ISP 起因遅延 → CDN 切替検討 | **Internet Monitor** |

## よく問われる上限・注意点（ひっかけ）
- **ELB アクセスログの既定は S3**。CloudWatch Logs を選ぶ誤答に注意（CloudWatch に送られるのはメトリクスのみ）。
- **標準メトリクス（基本モニタリング・5分間隔）は無料**、**詳細モニタリング（1分間隔）は課金**。カスタムメトリクスも課金。
- **プローブ単位課金**は Network Synthetic Monitor のコスト構造。Internet Monitor は監視 city-network 数に依存。
- NHI は NAT Gateway 専用メトリクスでも、レイテンシ生値でもない（Synthetic/Flow 共通のバイナリ指標）。
- 標準メトリクスの保持は**最大 15 か月**（時間経過で粒度が粗くなる集約）。
- ログ保持は**既定で無期限**（1日〜10年または無期限を設定可）。
- アラーム上限はリージョン/アカウントあたり **5,000**（引き上げ可）、Logs Insights 同時クエリは **30**。
- オンプレ監視は CloudWatch Agent / Synthetic Monitor で可能。Flow Monitor は VPC 内ワークロード対象である点に注意。
