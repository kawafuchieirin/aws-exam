# AWS CloudTrail（ネットワーク監査観点）

> カテゴリ: マネジメントとガバナンス / 重要度: ○
> 最終更新: 2026-05-24

---

## 1. 概要

AWS CloudTrail は AWS アカウント内の **API コール（誰が・いつ・何を・どこから）を記録する監査ログ**サービス。ANS-C01 では「ネットワーク構成変更の追跡」「誰が SG/ルートテーブル/VPC を変更したか」「VPC エンドポイント経由のアクセス監査」が問われる。CloudWatch がメトリクス/トラフィックの監視であるのに対し、CloudTrail は**コントロールプレーンの操作監査**を担う。

### 試験での位置づけ

- ネットワーク変更（`CreateRoute`、`AuthorizeSecurityGroupIngress`、`ModifyVpcAttribute` 等）の**誰が・いつ**の特定。
- セキュリティ事故時の調査（不審な SG 開放、ルート改ざんの追跡）。
- **ネットワークアクティビティイベント**による、VPC エンドポイント経由のアクセス（特に拒否 `VpceAccessDenied`）の可視化。

---

## 2. コアコンセプト

| 要素 | 内容 | ネットワーク観点 |
|---|---|---|
| **管理イベント（Management Events）** | コントロールプレーン操作（リソースの作成/変更/削除） | `CreateSubnet`・`CreateRoute`・SG 変更など**ネットワーク構成変更**はここ。既定で記録（無料の管理イベント1コピー） |
| **データイベント（Data Events）** | データプレーン操作（S3 オブジェクト、Lambda 実行など） | 高頻度・既定オフ・追加課金。ネットワーク構成変更の追跡には基本不要 |
| **ネットワークアクティビティイベント** | **VPC エンドポイント経由**の API コールを記録 | エンドポイント所有者が、エンドポイント越しの API（特に**拒否**）を監査。既定オフ・追加課金 |
| **証跡（Trail）** | イベントを S3（任意で CloudWatch Logs）へ継続配信 | マルチリージョン証跡・組織証跡が推奨 |
| **イベント履歴（Event History）** | 直近90日の管理イベントをコンソールで閲覧 | 証跡不要で簡易調査可能 |
| **CloudTrail Lake** | イベントデータストアで SQL 分析 | 長期保持・横断分析 |

---

## 3. アーキテクチャ / 仕組み

- すべての API コールは CloudTrail が記録し、**証跡**を作成すると S3 バケットへ継続配信される。任意で **CloudWatch Logs** にも送り、メトリクスフィルター＋アラームでリアルタイム検知できる。
- **組織証跡（Organization Trail）** を AWS Organizations の管理アカウントで作成すると、全メンバーアカウントのイベントを単一バケットに集約できる（[Organizations](../organizations/README.md)）。
- **ネットワークアクティビティイベント**は、**高度なイベントセレクター**で `eventCategory = NetworkActivity` と `eventSource`（例 `ec2.amazonaws.com`、`s3.amazonaws.com`、`kms.amazonaws.com`、`secretsmanager.amazonaws.com`、`cloudtrail.amazonaws.com` ほか）を指定して有効化する。`errorCode = VpceAccessDenied` と `vpcEndpointId` で**特定エンドポイントの拒否のみ**を抽出可能。

---

## 4. 試験頻出ポイント

- **ネットワーク構成変更の追跡は「管理イベント」**。SG ルール変更（`AuthorizeSecurityGroupIngress` / `RevokeSecurityGroupIngress`）、ルート変更（`CreateRoute` / `ReplaceRoute`）、VPC/サブネット/ピアリング/TGW の作成・削除などはここに記録される。管理イベントは既定でオン。
- **イベント履歴は90日**。それ以上の保持や横断分析が必要なら**証跡（S3）または CloudTrail Lake**。
- **リアルタイム検知**: CloudTrail → CloudWatch Logs → メトリクスフィルター → アラーム → SNS で、「想定外の SG 全開放」等を即時通知。
- **VPC エンドポイント経由のアクセス監査**は、フローログ（IP メタデータ）では不可。**ネットワークアクティビティイベント**で「どの API がどのエンドポイント経由で・許可/拒否されたか」を記録する。組織外の認証情報がエンドポイントを使おうとする試みの検知に有効。
- **マルチリージョン証跡**を有効にすると、新規リージョン追加時も自動的に記録対象になる。
- CloudTrail はあくまで**コントロールプレーンの監査**。トラフィックの中身やフロー量は VPC フローログ／トラフィックミラーリングの領域。

---

## 5. 他サービスとの連携

- **CloudWatch Logs**: 証跡を連携し、メトリクスフィルター＋アラームで不正な構成変更を検知（[CloudWatch](../cloudwatch/README.md)）。
- **AWS Organizations**: 組織証跡で全アカウントの監査ログを集約（[Organizations](../organizations/README.md)）。
- **AWS Config**: 「構成の状態」を記録する Config に対し、CloudTrail は「変更を行った API コール」を記録。両者は補完関係（[Config](../config/README.md)）。
- **VPC / PrivateLink**: ネットワークアクティビティイベントの対象である VPC エンドポイントは [VPC](../../networking-content-delivery/vpc/README.md) を参照。
- **EventBridge**: CloudTrail 由来の API イベントを起点に自動修復を実行。

---

## 6. 制約・上限・コスト

| 項目 | 値 |
|---|---|
| イベント履歴の保持 | 90日（コンソール、無料） |
| 管理イベント | 1コピー目は無料。追加証跡コピーは課金 |
| データイベント / ネットワークアクティビティイベント | 既定オフ・**追加課金** |
| 証跡数 / リージョン | 5 |

- **コスト**: 管理イベントの1証跡コピーは無料。データイベント・ネットワークアクティビティイベント・CloudTrail Lake の取り込み/クエリ、S3 保管は課金。
- コスト最適化: 高頻度なデータイベントは必要なリソースに絞る。ネットワーク監査目的では管理イベント＋必要に応じネットワークアクティビティイベントで十分なことが多い。

---

## 7. 出典

- [Understanding CloudTrail events – AWS Docs](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-events.html)
- [Logging management events – AWS Docs](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html)
- [Logging network activity events – AWS Docs](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html)
- [AWS CloudTrail network activity events for VPC endpoints now GA – AWS Blog](https://aws.amazon.com/blogs/aws/aws-cloudtrail-network-activity-events-for-vpc-endpoints-now-generally-available/)
- [CloudTrail concepts – AWS Docs](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html)
