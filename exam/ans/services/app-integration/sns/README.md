# Amazon SNS（Simple Notification Service）

> カテゴリ: アプリケーション統合 / 重要度: △（周辺）
> 最終更新: 2026-05-24 ／ 出典は本ドキュメント末尾

---

## 1. 概要

Amazon SNS は publish/subscribe 型のフルマネージド**通知サービス**。トピックに発行したメッセージを複数のサブスクライバ（Lambda・SQS・HTTP/S・Email・SMS）へファンアウトする。ANS-C01 では「セキュリティアラートや CloudWatch アラームの通知経路」として周辺的に登場する。

### 試験での位置づけ

- 第3分野（運用）と第4分野（セキュリティ）で、**監視・検知の結果を人やシステムへ届ける終端**として問われる。
- ネットワークそのものを構成しないが、**CloudWatch アラーム → SNS → 運用者通知**の経路と、**VPC からのプライベート発行**を押さえる。

---

## 2. コアコンセプト

| 要素 | 役割 | ネットワーク観点の要点 |
|---|---|---|
| **トピック** | メッセージの発行先（Standard / FIFO） | アラーム・イベントの集約点 |
| **サブスクリプション** | 配信先の登録 | Lambda/SQS/HTTP(S)/Email/SMS |
| **発行（Publish）** | メッセージ送信 | VPC エンドポイント経由でプライベート発行可 |
| **トピックポリシー** | アクセス制御 | `aws:SourceVpce` 条件で経由元エンドポイントを制限 |

---

## 3. 試験頻出ポイント（ネットワーク観点）

- **CloudWatch アラーム連携**: NAT GW のバイト数、フローログ由来メトリクス、VPN トンネル状態などのアラームを SNS トピックに通知 → メール/Slack/PagerDuty へファンアウト。これがネットワーク監視の標準通知パターン。
- **セキュリティアラート**: GuardDuty・Security Hub・Config の検知結果を EventBridge 経由で SNS に流し、運用チームへ即時通知。
- **VPC からのプライベート発行**: インターフェイス VPC エンドポイント（PrivateLink）に対応（サービス名 `com.amazonaws.<region>.sns`）。プライベートサブネットのアプリが**インターネットを経由せず**トピックへ発行できる。プライベート DNS を有効化すれば既存 SDK のエンドポイント URL のままで透過的に利用可能。
- **トピックポリシー** の `aws:SourceVpc` / `aws:SourceVpce` 条件で「特定 VPC/エンドポイント経由の発行のみ許可」とでき、漏洩経路を絞れる。

---

## 4. 他サービスとの連携

- [EventBridge](../eventbridge/README.md): イベントを SNS にファンアウト。
- [SQS](../sqs/README.md): SNS→SQS のファンアウト（耐久バッファ）。
- [VPC](../../networking-content-delivery/vpc/README.md): インターフェイスエンドポイントでプライベート発行。
- CloudWatch: アラームアクションの通知先。

---

## 5. 制約・上限・コスト

- **転送中暗号化**: SNS API は HTTPS のみ。保存時暗号化は SSE（KMS）対応。
- VPC エンドポイント経由の発行は NAT データ処理料を回避できるが、**インターフェイスエンドポイント自体は時間課金＋データ処理課金**が発生する点に注意。
- メッセージ発行は従量課金。SMS は別料金体系。

---

## 6. 出典

- [Amazon SNS and interface VPC endpoints (AWS PrivateLink) – AWS Docs](https://docs.aws.amazon.com/sns/latest/dg/sns-vpc-endpoint.html)
- [AWS services that integrate with AWS PrivateLink – AWS Docs](https://docs.aws.amazon.com/vpc/latest/privatelink/aws-services-privatelink-support.html)
- [Amazon SNS access control with VPC endpoint policies – AWS Docs](https://docs.aws.amazon.com/sns/latest/dg/sns-create-vpc-endpoint-policy.html)
