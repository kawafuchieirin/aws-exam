# Amazon SQS（Simple Queue Service）

> カテゴリ: アプリケーション統合 / 重要度: △（周辺）
> 最終更新: 2026-05-24 ／ 出典は本ドキュメント末尾

---

## 1. 概要

Amazon SQS はフルマネージドの**メッセージキュー**サービス。送信側と受信側を疎結合にし、メッセージをバッファリングして耐障害性とスケーラビリティを高める。ANS-C01 では「VPC エンドポイント経由のプライベートなキューアクセス」という観点で周辺的に問われる。

### 試験での位置づけ

- ネットワーク構成サービスではないが、**プライベートサブネットからインターネットを経由せずに AWS API を呼ぶ典型例**として VPC エンドポイントの理解確認に使われる。
- 自動化の信頼性確保（リトライ・DLQ・バッファ）の文脈で EventBridge/SNS と組で登場。

---

## 2. コアコンセプト

| 要素 | 役割 | ネットワーク観点の要点 |
|---|---|---|
| **キュー** | メッセージの保管（Standard / FIFO） | 高スループット or 厳密順序 |
| **プロデューサ / コンシューマ** | 送信・受信側 | VPC エンドポイント経由でプライベートアクセス可 |
| **可視性タイムアウト / DLQ** | 重複防止・失敗隔離 | 自動化の信頼性確保 |
| **エンドポイントポリシー** | 経由アクセス制御 | 特定ユーザ/アクション/キューに限定 |

---

## 3. 試験頻出ポイント（ネットワーク観点）

- **VPC エンドポイント経由のプライベートアクセス**: SQS への接続は**インターフェイス VPC エンドポイント（PrivateLink）**で行う（サービス名 `com.amazonaws.<region>.sqs`、FIPS は `...sqs-fips`）。プライベートサブネットの EC2/Lambda が IGW・NAT・VPN なしでキューに送受信できる。
- **必須設定**: VPC で**プライベート DNS を有効化**し、標準の `sqs.<region>.amazonaws.com` 形式のエンドポイントを使う。**HTTPS のみ**サポート。レガシーエンドポイント（`queue.amazonaws.com` 等）はプライベート DNS 非対応。
- **エンドポイントポリシー** で「`sqs:SendMessage` を特定キューにのみ許可」のように経路単位で最小権限を実現。
- **VPC 限定アクセス**: キューのアクセスポリシーで `aws:sourceVpce` を条件に「このエンドポイント経由でなければ拒否」を設定できる（データ漏洩経路の遮断）。

---

## 4. 他サービスとの連携

- [SNS](../sns/README.md): SNS→SQS ファンアウトの受け先。
- [EventBridge](../eventbridge/README.md): イベント配信のバッファ／DLQ。
- [VPC](../../networking-content-delivery/vpc/README.md): インターフェイスエンドポイントでプライベートアクセス。

---

## 5. 制約・上限・コスト

- **転送中暗号化**: HTTPS 必須。保存時は SSE-SQS / SSE-KMS。
- インターフェイスエンドポイントは時間課金＋データ処理課金。ただし NAT GW を経由しないためトラフィックがインターネットに出ない設計に寄与。
- メッセージ操作は従量課金（リクエスト数ベース）。

---

## 6. 出典

- [Internetwork traffic privacy in Amazon SQS – AWS Docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-internetwork-traffic-privacy.html)
- [AWS services that integrate with AWS PrivateLink – AWS Docs](https://docs.aws.amazon.com/vpc/latest/privatelink/aws-services-privatelink-support.html)
