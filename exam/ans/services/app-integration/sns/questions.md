---
service: sns
domain_default: 3
source: README.md
source_sha256: f732998ccc26b0bcc8e3b4a6c8fab207b5d1a7cb4af6a6fd0055004f43ccb832
generated: 2026-05-24
---

## sns-001
- type: single
- difficulty: easy
- domain: 3
- tags: [pub-sub, use-case-fit]

SNS の基本的な動作モデルとして正しいものはどれか。

- [ ] A. キューに保存したメッセージを 1 つのコンシューマがポーリングして取得する
- [x] B. トピックに発行したメッセージを複数のサブスクライバへファンアウトする
- [ ] C. イベントパターンでマッチしたイベントをターゲットへルーティングする
- [ ] D. メッセージを順序保証付きで 1 対 1 配信する

> **解説**: SNS は publish/subscribe 型で、トピックへ発行したメッセージを Lambda・SQS・HTTP/S・Email・SMS など複数のサブスクライバへファンアウトする。ポーリング取得は SQS、イベントルーティングは EventBridge の特性。
> **出典**: [sns README #1 概要](README.md#1-概要)

## sns-002
- type: single
- difficulty: easy
- domain: 3
- tags: [monitoring, pub-sub]

NAT ゲートウェイのバイト数や VPN トンネル状態の CloudWatch アラームを運用者へ届けたい。標準的な通知パターンはどれか。

- [x] A. CloudWatch アラーム → SNS トピック → メール/Slack/PagerDuty へファンアウト
- [ ] B. CloudWatch アラーム → SQS → Lambda でメール送信
- [ ] C. CloudWatch アラーム → EventBridge Scheduler で定期通知
- [ ] D. CloudWatch アラーム → VPC フローログへ記録

> **解説**: ネットワーク監視の標準通知パターンは、CloudWatch アラームのアクションとして SNS トピックに通知し、メール/Slack/PagerDuty などへファンアウトする構成。SNS が「監視・検知の結果を人やシステムへ届ける終端」となる。
> **出典**: [sns README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sns-003
- type: single
- difficulty: medium
- domain: 2
- tags: [privatelink, vpc-endpoint]

プライベートサブネットのアプリがインターネットを経由せず SNS トピックへ発行したい。必要な構成はどれか。

- [ ] A. NAT ゲートウェイ経由で発行する
- [ ] B. ゲートウェイ型 VPC エンドポイント（`com.amazonaws.<region>.sns`）
- [x] C. インターフェイス型 VPC エンドポイント（`com.amazonaws.<region>.sns`）
- [ ] D. パブリック IP を割り当てた EC2 から発行する

> **解説**: SNS は PrivateLink（インターフェイス VPC エンドポイント）に対応し、サービス名は `com.amazonaws.<region>.sns`。これによりインターネットを経由せずプライベート発行できる。SNS にゲートウェイ型エンドポイントは提供されていない。
> **出典**: [sns README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sns-004
- type: single
- difficulty: medium
- domain: 2
- tags: [vpc-endpoint, automation, use-case-fit]

SNS のインターフェイス VPC エンドポイントを使う際、既存 SDK のエンドポイント URL を変更せず透過的に利用するために有効化すべき設定はどれか。

- [ ] A. パブリック DNS の無効化
- [x] B. プライベート DNS の有効化
- [ ] C. FIFO トピックの利用
- [ ] D. SSE-KMS の有効化

> **解説**: プライベート DNS を有効化すると、標準のエンドポイント URL がエンドポイントのプライベート IP に解決されるため、既存 SDK のコードを変更せず透過的に利用できる。FIFO や暗号化は DNS 解決とは無関係。
> **出典**: [sns README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sns-005
- type: single
- difficulty: hard
- domain: 4
- tags: [iam-policy, source-condition]

「特定の VPC エンドポイント経由の発行のみを許可」して漏洩経路を絞りたい。トピックポリシーで使う条件キーはどれか。

- [ ] A. `aws:SourceIp`
- [x] B. `aws:SourceVpce`
- [ ] C. `aws:PrincipalOrgID`
- [ ] D. `aws:SecureTransport`

> **解説**: トピックポリシーの `aws:SourceVpc` / `aws:SourceVpce` 条件で、特定 VPC やエンドポイント経由の発行のみを許可でき、漏洩経路を絞れる。`aws:SecureTransport` は HTTPS 強制用、`SourceIp` は IP 制限であり、エンドポイント単位の制御には使えない。
> **出典**: [sns README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sns-006
- type: single
- difficulty: medium
- domain: 4
- tags: [monitoring, event-routing]

GuardDuty・Security Hub・Config の検知結果を運用チームへ即時通知したい。一般的な経路はどれか。

- [ ] A. 検知結果を直接 SNS API でポーリングする
- [x] B. 検知結果を EventBridge 経由で SNS に流し、サブスクライバへファンアウトする
- [ ] C. 検知結果を SQS に保存し、運用者が定期確認する
- [ ] D. 検知結果を VPC フローログへ転送する

> **解説**: セキュリティ検知結果は EventBridge 経由で SNS に流し、メールや Slack などへファンアウトして即時通知するのが定石。SNS は検知結果を能動的にポーリングするサービスではない。
> **出典**: [sns README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sns-007
- type: single
- difficulty: easy
- domain: 4
- tags: [encryption, tls]

SNS の暗号化に関する記述として正しいものはどれか。

- [ ] A. SNS API は HTTP も HTTPS も選択できる
- [x] B. SNS API は HTTPS のみ、保存時暗号化は SSE（KMS）に対応
- [ ] C. 転送中も保存時も暗号化はサポートされない
- [ ] D. 保存時暗号化は SSE-SNS のみで KMS は使えない

> **解説**: SNS API は HTTPS のみで転送中暗号化が保証され、保存時は SSE（KMS）に対応する。HTTP は使えず、KMS による暗号化も利用可能。
> **出典**: [sns README #5 制約・上限・コスト](README.md#5-制約上限コスト)

## sns-008
- type: single
- difficulty: hard
- domain: 3
- tags: [cost, vpc-endpoint]

SNS をインターフェイス VPC エンドポイント経由で発行する場合のコストに関する記述として正しいものはどれか。

- [ ] A. NAT データ処理料もエンドポイント料金も完全に無料になる
- [x] B. NAT データ処理料は回避できるが、エンドポイント自体に時間課金＋データ処理課金が発生する
- [ ] C. エンドポイントは無料だが NAT データ処理料が二重にかかる
- [ ] D. メッセージ発行は無料、エンドポイントのみ従量課金

> **解説**: VPC エンドポイント経由の発行は NAT データ処理料を回避できるが、インターフェイスエンドポイント自体に時間課金＋データ処理課金が発生する。メッセージ発行も従量課金（SMS は別料金）であり、無料ではない。
> **出典**: [sns README #5 制約・上限・コスト](README.md#5-制約上限コスト)

## sns-009
- type: multi
- difficulty: medium
- domain: 3
- tags: [pub-sub, use-case-fit]

SNS トピックのサブスクライバ（配信先）として有効なものを2つ選べ。

- [x] A. SQS キュー
- [ ] B. ルートテーブル
- [x] C. Lambda 関数
- [ ] D. セキュリティグループ
- [ ] E. VPC エンドポイント

> **解説**: SNS のサブスクリプション先は Lambda・SQS・HTTP/S・Email・SMS。SNS→SQS のファンアウトは耐久バッファとして頻出。ルートテーブル・セキュリティグループ・VPC エンドポイントは通知の配信先にはならない。
> **出典**: [sns README #2 コアコンセプト](README.md#2-コアコンセプト)

## sns-010
- type: multi
- difficulty: hard
- domain: 4
- tags: [iam-policy, source-condition]

トピックポリシーで「特定 VPC/エンドポイント経由の発行のみ許可」する設定に使える条件キーを2つ選べ。

- [x] A. `aws:SourceVpc`
- [ ] B. `aws:UserAgent`
- [x] C. `aws:SourceVpce`
- [ ] D. `aws:RequestedRegion`
- [ ] E. `aws:CalledVia`

> **解説**: `aws:SourceVpc` は特定 VPC からのアクセスを、`aws:SourceVpce` は特定エンドポイント経由のアクセスを制限する条件キー。両者を使うことで漏洩経路を VPC/エンドポイント単位で絞れる。他のキーは経由元 VPC/エンドポイントの制限には使えない。
> **出典**: [sns README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)
