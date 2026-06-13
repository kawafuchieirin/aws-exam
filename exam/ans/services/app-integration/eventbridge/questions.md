---
service: eventbridge
domain_default: 3
source: README.md
source_sha256: c58740d4359a8b6a3a7dcfcc2d071f56e3711233107beeda0e87a50829ca9a24
generated: 2026-05-24
---

## eventbridge-001
- type: single
- difficulty: easy
- domain: 3
- tags: [event-routing, automation, use-case-fit]

EventBridge におけるルール（Rule）の役割として最も適切なものはどれか。

- [ ] A. イベントの内容を JSON で生成して発行する
- [x] B. イベントパターンまたはスケジュールでイベントをマッチさせ、ターゲットへ振り分ける
- [ ] C. マッチしたイベントを実際に修復・処理する
- [ ] D. AWS サービスからのイベントを保存する耐久ストレージ

> **解説**: ルールはイベントパターンまたはスケジュールでイベントをマッチさせ、ターゲットへ配信する役割を持つ。イベント生成はソース側、実際の処理は Lambda などのターゲット、受け口はイベントバスであり、それぞれ役割が異なる。
> **出典**: [eventbridge README #2 コアコンセプト](README.md#2-コアコンセプト)

## eventbridge-002
- type: single
- difficulty: easy
- domain: 3
- tags: [event-routing, cloudtrail-events]

AWS サービスが発するイベント（EC2 状態変化、Direct Connect 状態など）は、既定でどこに届くか。

- [ ] A. カスタムイベントバス
- [ ] B. パートナーイベントバス
- [x] C. デフォルトイベントバス
- [ ] D. SQS キュー

> **解説**: AWS サービスのイベントはアカウント既定の「デフォルトイベントバス」に届く。カスタムバスは自前アプリ用、パートナーバスは SaaS 連携用であり、AWS サービスイベントの既定の受け口ではない。
> **出典**: [eventbridge README #2 コアコンセプト](README.md#2-コアコンセプト)

## eventbridge-003
- type: single
- difficulty: medium
- domain: 4
- tags: [security-group, automation, cloudtrail-events]

セキュリティグループに 0.0.0.0/0 を許可する意図しない変更が行われた瞬間を検知し、自動で取り消したい。最も適切な構成はどれか。

- [ ] A. CloudWatch アラームから直接セキュリティグループを修正する
- [x] B. CloudTrail / Config のイベントを EventBridge ルールで捕捉し、Lambda / SSM Automation で修復する
- [ ] C. SNS トピックにポリシーを設定して変更をブロックする
- [ ] D. VPC フローログを有効化して変更を防止する

> **解説**: `AuthorizeSecurityGroupIngress` のような API コールは CloudTrail/Config のイベントとして EventBridge ルールで捕捉でき、Lambda や SSM Automation を起動して自動修復する。EventBridge はルーターであり修復自体は行わない。フローログは通信記録であり変更防止はできない。
> **出典**: [eventbridge README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## eventbridge-004
- type: single
- difficulty: medium
- domain: 3
- tags: [route-table, eni, automation, iam-policy]

イベント駆動の自動修復フローにおける EventBridge の役割の説明として正しいものはどれか。

- [ ] A. 修復スクリプトを実行する
- [ ] B. 運用者へメール通知を送る
- [x] C. イベントを適切なターゲットへルーティングする
- [ ] D. 失敗したイベントを永続的にバッファリングする

> **解説**: EventBridge はあくまで「イベントのルーター」。実際の修復は Lambda / SSM Automation、通知は SNS、バッファリングは SQS が担う。それぞれの責務を取り違えないことが頻出ポイント。
> **出典**: [eventbridge README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## eventbridge-005
- type: single
- difficulty: medium
- domain: 2
- tags: [privatelink, vpc-endpoint, event-routing]

プライベートサブネットの Lambda から NAT/IGW を経由せずに EventBridge へ `PutEvents` したい。必要な構成はどれか。

- [ ] A. NAT ゲートウェイを追加する
- [ ] B. ゲートウェイ型 VPC エンドポイント（`com.amazonaws.<region>.events`）
- [x] C. インターフェイス型 VPC エンドポイント（`com.amazonaws.<region>.events`）
- [ ] D. パブリックサブネットへ Lambda を移設する

> **解説**: EventBridge は PrivateLink（インターフェイス VPC エンドポイント）に対応し、サービス名は `com.amazonaws.<region>.events`。これによりプライベートサブネットから NAT/IGW なしで `PutEvents` できる。EventBridge にゲートウェイ型エンドポイントは提供されていない。
> **出典**: [eventbridge README #5 制約・上限・コスト](README.md#5-制約上限コスト)

## eventbridge-006
- type: single
- difficulty: hard
- domain: 3
- tags: [pub-sub, message-queue]

重要なネットワーク自動化において、配信失敗時もイベントを取りこぼさずバッファリング・リトライしたい。EventBridge のターゲットとして最も適切なものはどれか。

- [ ] A. Email サブスクリプション
- [ ] B. CloudWatch ダッシュボード
- [x] C. SQS キュー
- [ ] D. AWS Config ルール

> **解説**: AWS サービスイベントには durable / best-effort の区別があり、重要な自動化では SQS をターゲットにしてバッファリングとリトライ、DLQ を確保する。Email や CloudWatch ダッシュボードは耐久バッファにならない。
> **出典**: [eventbridge README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## eventbridge-007
- type: single
- difficulty: easy
- domain: 3
- tags: [event-routing, automation]

定期的なヘルスチェックを一定間隔で実行したい。EventBridge で利用する仕組みはどれか。

- [ ] A. EventBridge Pipes
- [x] B. EventBridge Scheduler（スケジュールルール）
- [ ] C. カスタムイベントバス
- [ ] D. トピックポリシー

> **解説**: 定期実行は EventBridge Scheduler（またはスケジュール式のルール）で行う。Pipes はソース→ターゲットを直結する単純連携用であり、定期実行の主目的の機能ではない。
> **出典**: [eventbridge README #2 コアコンセプト](README.md#2-コアコンセプト)

## eventbridge-008
- type: multi
- difficulty: medium
- domain: 3
- tags: [cloudtrail-events, monitoring]

EventBridge ルールで捕捉できる「ネットワーク関連のイベント源」として適切なものを2つ選べ。

- [ ] A. ルートテーブルのパケット転送ログ
- [x] B. EC2 インスタンスの状態変化イベント
- [ ] C. CloudFront のキャッシュヒット率
- [x] D. Direct Connect の接続状態変化
- [ ] E. ALB のレスポンスタイム秒数

> **解説**: EventBridge のネットワーク関連イベント源には、EC2 インスタンス状態変化、Direct Connect 接続状態、AWS Health、VPC/TGW の API 操作（CloudTrail 経由）などがある。キャッシュヒット率やレスポンスタイムはメトリクスであり、イベントとしてルールに直接届くものではない。
> **出典**: [eventbridge README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## eventbridge-009
- type: multi
- difficulty: hard
- domain: 3
- tags: [target-type, automation, pub-sub]

ネットワーク構成変更を検知して「自動修復」と「運用者への通知」を同時に行う。EventBridge のターゲットとして適切な組み合わせを2つ選べ。

- [x] A. 修復用の Lambda 関数 / SSM Automation
- [ ] B. VPC フローログ
- [x] C. 通知ファンアウト用の SNS トピック
- [ ] D. ルートテーブル
- [ ] E. セキュリティグループ

> **解説**: 修復は Lambda / SSM Automation、通知は SNS がターゲットとなる。フローログ・ルートテーブル・セキュリティグループは EventBridge のターゲットではなく、修復「対象」や監視「対象」のリソースである。
> **出典**: [eventbridge README #4 他サービスとの連携](README.md#4-他サービスとの連携)

## eventbridge-010
- type: single
- difficulty: medium
- domain: 3
- tags: [cost, event-routing]

EventBridge のコストに関する記述として正しいものはどれか。

- [ ] A. AWS サービスが発するイベントの取り込みは従量課金される
- [x] B. カスタムイベントの `PutEvents` は従量課金、AWS サービスイベントの取り込みは無料
- [ ] C. すべてのイベント取り込みが無料である
- [ ] D. ルール作成ごとに月額固定料金がかかる

> **解説**: カスタムイベントの `PutEvents` は従量課金だが、AWS サービスが発するイベントの取り込みは無料。ルール数やターゲット数にはクォータがあるが、ネットワーク設計上の制約ではなく暗記は不要。
> **出典**: [eventbridge README #5 制約・上限・コスト](README.md#5-制約上限コスト)
