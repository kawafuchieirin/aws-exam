# AWS Cost Explorer

> カテゴリ: コスト管理 / 重要度: △（周辺）
> 最終更新: 2026-05-24 ／ 出典は本ドキュメント末尾

---

## 1. 概要

AWS Cost Explorer は過去最大 13 か月のコスト・使用量を可視化し、最大 18 か月先を予測できる分析ツール。ANS-C01 では「**データ転送コストの可視化と最適化**」、すなわち NAT Gateway・VPC エンドポイント・リージョン間転送などのネットワークコストを特定する観点で周辺的に問われる。

### 試験での位置づけ

- 第3分野（運用・最適化）の**コスト最適化**で登場。「どのネットワークコンポーネントが費用を押し上げているか特定するには？」→ Cost Explorer で使用タイプ別に分析、が定番の答え。
- ネットワーク設計そのものではなく、**最適化判断の根拠データを得る手段**として押さえる。

---

## 2. コアコンセプト

| 要素 | 役割 | ネットワーク観点の要点 |
|---|---|---|
| **フィルタ / グループ化** | サービス・使用タイプ・リージョン・タグ別に分解 | **Usage Type** でデータ転送を切り分ける |
| **Usage Type** | 課金単位の細目 | `DataTransfer-Out-Bytes`、`NatGateway-Bytes`、`VPC-Endpoint-Bytes` 等 |
| **Cost & Usage Report (CUR)** | 詳細な明細データ | Cost Explorer と同一データセット |
| **予測 / コスト比較** | 将来予測・期間比較 | 転送料の増加トレンド検知 |

---

## 3. 試験頻出ポイント（ネットワーク観点）

- **データ転送コストの可視化**: グループ化を **Usage Type** または **Usage Type Group**（例: "EC2: Data Transfer - Internet (Out)"）にすると、インターネット送出・リージョン間・AZ 間の転送料を分離して把握できる。
- **NAT Gateway コスト分析**: `NatGateway-Hours`（時間課金）と `NatGateway-Bytes`（データ処理料）を確認。データ処理料が高い場合は **S3/DynamoDB を Gateway エンドポイントに逃がす**等の最適化につながる。
- **VPC エンドポイントコスト**: インターフェイスエンドポイントの時間・データ処理課金を Usage Type で確認し、Gateway で代替可能かを判断。
- **リージョン間転送**: クロスリージョンレプリケーションや TGW のリージョン間ピアリング転送料を、リージョン別グループ化や Usage Type で特定。
- **AZ 間転送**: 同一リージョン内 AZ をまたぐ通信も課金対象。アーキテクチャ見直し（同一 AZ 配置）の根拠データに使う。

---

## 4. 他サービスとの連携

- [VPC](../../networking-content-delivery/vpc/README.md): NAT GW・エンドポイントのコスト要因の発生元。
- AWS Budgets / Cost Anomaly Detection: 転送料の急増アラート。
- Cost & Usage Report (CUR): 詳細明細を S3 へ出力して Athena 解析。

---

## 5. 制約・上限・コスト

- **UI での利用は無料**。Cost Explorer **API はリクエストごとに $0.01**。
- データ反映は当月分が約 24 時間後、以降 24 時間ごとに更新。履歴は最大 13 か月、予測は最大 18 か月。
- 一度有効化すると無効化できない。

---

## 6. 出典

- [Analyzing your costs and usage with AWS Cost Explorer – AWS Docs](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html)
- [Understanding your AWS data transfer charges – AWS Docs](https://docs.aws.amazon.com/cost-management/latest/userguide/cur-data-transfers-charges.html)
