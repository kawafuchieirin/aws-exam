# Amazon EventBridge

> カテゴリ: アプリケーション統合 / 重要度: △（周辺）
> 最終更新: 2026-05-24 ／ 出典は本ドキュメント末尾

---

## 1. 概要

Amazon EventBridge は AWS サービス・SaaS・自前アプリが発するイベントを受け取り、**ルール**でフィルタリングして**ターゲット**へ配信するサーバーレスのイベントバス。ANS-C01 では「ネットワーク構成変更を検知して自動修復・通知するイベント駆動オートメーション」の文脈で周辺的に問われる。

### 試験での位置づけ

- 第3分野（運用・最適化）の**自動化**で登場。構成変更の検知 → Lambda/SSM Automation での自動修復、SNS での通知という連鎖の起点。
- ネットワーク自体を構成するサービスではないため深掘りは不要。**「変化に反応する仕組み」の起点**として押さえれば十分。

---

## 2. コアコンセプト

| 要素 | 役割 | ネットワーク観点の要点 |
|---|---|---|
| **イベントバス** | イベントの受け口（デフォルト/カスタム/パートナー） | AWS サービスのイベントは**デフォルトバス**に届く |
| **イベント** | 環境変化を表す JSON | EC2 状態変化、Direct Connect 状態、Health イベント等 |
| **ルール** | イベントパターンまたはスケジュールでマッチ | パターンで「VPC/DX/Config の変更」だけを抽出 |
| **ターゲット** | マッチ時の配信先 | Lambda・SNS・SQS・Step Functions・SSM Automation 等 |
| **EventBridge Scheduler / Pipes** | 定期実行 / ソース→ターゲット直結 | 定期ヘルスチェックや単純連携に利用 |

---

## 3. 試験頻出ポイント（ネットワーク観点）

- **構成変更トリガ**: `AWS Config` のルール非準拠イベント、`CloudTrail` API コール（例: `AuthorizeSecurityGroupIngress` で 0.0.0.0/0 を許可した瞬間）を EventBridge ルールで捕捉し、自動修復関数を起動する。
- **ネットワーク自動化の役割**: EventBridge はあくまで**イベントのルーター**。実際の修復は Lambda / SSM Automation、通知は SNS が担う。試験では「SG の意図しない変更を検知して自動で取り消すには？」→ Config/CloudTrail イベント + EventBridge + 修復アクションの組み合わせ。
- **ネットワーク関連イベント源**: EC2 インスタンス状態変化、Direct Connect の接続状態、AWS Health（メンテナンス/障害）、VPC・TGW 等の API 操作（CloudTrail 経由）。
- **配信信頼性**: AWS サービスイベントは durable / best-effort の区別あり。重要な自動化では SQS をターゲットにしてバッファリング・リトライを確保。

---

## 4. 他サービスとの連携

- [SNS](../sns/README.md): セキュリティアラートの通知ファンアウト先。
- [SQS](../sqs/README.md): 失敗時のバッファ・デッドレターキュー。
- [VPC](../../networking-content-delivery/vpc/README.md): 構成変更（フローログ・SG・ルートテーブル）の監視対象。
- CloudWatch / AWS Config / CloudTrail: イベントソース。

---

## 5. 制約・上限・コスト

- **VPC からのプライベートアクセス**: インターフェイス VPC エンドポイント（PrivateLink）に対応。サービス名は `com.amazonaws.<region>.events`。プライベートサブネットの Lambda 等から NAT/IGW を経由せず `PutEvents` 可能。
- カスタムイベントの **`PutEvents` は従量課金**。AWS サービスが発するイベントの取り込みは無料。
- ルールあたりのターゲット数など各種クォータあり（引き上げ可）。ネットワーク設計上の制約ではないため暗記不要。

---

## 6. 出典

- [Events in Amazon EventBridge – AWS Docs](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events.html)
- [Using Amazon EventBridge with interface VPC endpoints – AWS Docs](https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-interface-VPC.html)
- [AWS services that integrate with AWS PrivateLink – AWS Docs](https://docs.aws.amazon.com/vpc/latest/privatelink/aws-services-privatelink-support.html)
