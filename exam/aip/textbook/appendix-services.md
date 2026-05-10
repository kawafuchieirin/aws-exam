# Appendix: In-Scope AWS サービス早見表

> AIP-C01 試験で出題対象となる AWS サービスのカテゴリ別一覧。
> 出典: AWS 公式試験ガイド「In-Scope AWS Services」セクション

## 試験対策での使い方

- **頻出度**: ★★★（必修） / ★★（重要） / ★（補助的）
- 各サービス行の「主用途（試験文脈）」が試験で問われる典型パターン
- ★★★のサービスは必ずユースケースと制約を言えるようにする

---

## Machine Learning（最重要 ★★★ ゾーン）

| サービス | 頻出度 | 主用途（試験文脈） |
|---|---|---|
| **Amazon Bedrock** | ★★★ | FM への単一 API アクセス、本試験の主役 |
| **Amazon Bedrock AgentCore** | ★★ | Bedrock Agents の運用基盤・観測性 |
| **Amazon Bedrock Knowledge Bases** | ★★★ | マネージド RAG（取り込み→ベクトル化→検索） |
| **Amazon Bedrock Prompt Management** | ★★ | プロンプトのバージョン管理・承認ワークフロー |
| **Amazon Bedrock Prompt Flows** | ★★ | プロンプトチェーン・条件分岐のローコード構築 |
| **Amazon Comprehend** | ★★ | NLP（感情・エンティティ・PII 検出） |
| **Amazon Kendra** | ★★ | エンタープライズ検索。RAG の検索源にも |
| **Amazon Lex** | ★ | チャットボット／音声ボット構築 |
| **Amazon Q Business** | ★★ | 業務向け生成 AI アシスタント |
| **Amazon Q Business Apps** | ★ | Q Business 上のカスタムアプリ |
| **Amazon Q Developer** | ★★ | コード生成・補完支援 |
| **Amazon Rekognition** | ★ | 画像／動画分析 |
| **Amazon SageMaker AI** | ★★★ | FM ホスティング・カスタムモデル提供 |
| **Amazon SageMaker Clarify** | ★★ | バイアス検出・説明可能性 |
| **Amazon SageMaker Data Wrangler** | ★ | データ前処理・特徴量エンジニアリング |
| **Amazon SageMaker Ground Truth** | ★ | データラベリング |
| **Amazon SageMaker JumpStart** | ★★ | 事前学習済 FM カタログ |
| **Amazon SageMaker Model Monitor** | ★★ | 本番モデル監視・ドリフト検知 |
| **Amazon SageMaker Model Registry** | ★★ | モデル版管理・承認フロー |
| **Amazon SageMaker Neo** | ★★ | エッジ向けモデル軽量化／コンパイル |
| **Amazon SageMaker Processing** | ★ | 前処理ジョブ実行基盤 |
| **Amazon SageMaker Unified Studio** | ★ | ML ワークベンチ |
| **Amazon Textract** | ★ | ドキュメントから OCR・構造抽出 |
| **Amazon Titan** | ★★ | AWS 自社製 FM（Text/Embed/Image） |
| **Amazon Transcribe** | ★ | 音声→テキスト変換 |
| **Amazon Augmented AI（A2I）** | ★ | Human-in-the-Loop レビュー基盤 |

## Compute

| サービス | 頻出度 | 主用途（試験文脈） |
|---|---|---|
| **AWS Lambda** | ★★★ | API 統合層、エージェントツール実装、後処理 |
| AWS Lambda@Edge | ★ | エッジでの軽量推論／前処理 |
| Amazon EC2 | ★ | 自前モデルホスティング（GPU インスタンス） |
| AWS App Runner | ★ | コンテナ化 GenAI アプリの簡易デプロイ |
| AWS Outposts | ★ | データレジデンシー要件のオンプレ統合 |
| AWS Wavelength | ★ | 5G エッジ低レイテンシ推論 |

## Containers

| サービス | 頻出度 | 主用途 |
|---|---|---|
| **Amazon ECS / Fargate** | ★★ | コンテナ化エージェント／MCP サーバ |
| Amazon EKS | ★★ | Kubernetes 上の GenAI ワークロード |
| Amazon ECR | ★ | コンテナイメージレジストリ |

## Application Integration

| サービス | 頻出度 | 主用途 |
|---|---|---|
| **AWS Step Functions** | ★★★ | 複雑ワークフロー、ReAct 実装、Agentic Orchestration |
| **Amazon EventBridge** | ★★ | イベント駆動統合 |
| Amazon SNS / SQS | ★★ | 非同期処理／キューイング（バッチ推論） |
| AWS AppConfig | ★ | モデル切替の動的構成 |
| Amazon AppFlow | ★ | SaaS 連携 |

## Networking and Content Delivery

| サービス | 頻出度 | 主用途 |
|---|---|---|
| **Amazon API Gateway** | ★★★ | FM への外部公開 API、ストリーミング、レート制限 |
| **Amazon VPC** | ★★ | プライベート FM アクセス |
| **AWS PrivateLink** | ★★ | Bedrock への閉域アクセス |
| AWS AppSync | ★ | GraphQL ベースの API |
| Amazon CloudFront | ★ | レスポンスキャッシュ／配信 |
| ELB / Global Accelerator / Route 53 | ★ | 一般的な可用性確保 |

## Database / Storage

| サービス | 頻出度 | 主用途 |
|---|---|---|
| **Amazon S3** | ★★★ | RAG ソースリポジトリ、モデルアーティファクト |
| **Amazon OpenSearch Service** | ★★★ | ベクトル検索（k-NN, Neural plugin） |
| **Amazon Aurora（pgvector）** | ★★ | リレーショナル＋ベクトル検索 |
| **Amazon DynamoDB / Streams** | ★★ | 会話履歴、メタデータ、ストリーミング処理 |
| Amazon RDS | ★ | 構造化データ統合 |
| Amazon ElastiCache | ★ | プロンプトキャッシュ |
| Amazon Neptune | ★ | グラフ検索（高度 RAG パターン） |
| Amazon DocumentDB | ★ | JSON ドキュメント保存 |
| Amazon S3 Intelligent-Tiering / Lifecycle / Cross-Region Replication | ★★ | データ保持・コスト最適化 |
| Amazon EBS / EFS | ★ | コンピュート向けボリューム |

## Security, Identity, and Compliance

| サービス | 頻出度 | 主用途 |
|---|---|---|
| **IAM** | ★★★ | Bedrock API 権限境界（`bedrock:InvokeModel` 等） |
| **AWS KMS** | ★★ | 保存暗号化、Bedrock のカスタマー鍵 |
| **Amazon Macie** | ★★ | S3 内 PII 検出 |
| **AWS Secrets Manager** | ★★ | API キー・モデル認証情報管理 |
| **AWS WAF** | ★★ | API Gateway 保護、プロンプトインジェクション緩和 |
| Amazon Cognito | ★ | エンドユーザー認証 |
| AWS Encryption SDK | ★ | クライアントサイド暗号化 |
| IAM Access Analyzer / Identity Center | ★ | アクセスガバナンス |

## Management and Governance

| サービス | 頻出度 | 主用途 |
|---|---|---|
| **Amazon CloudWatch / Logs** | ★★★ | トークン使用、レイテンシ、品質指標 |
| **AWS CloudTrail** | ★★★ | 監査ログ（誰がどの FM を呼んだか） |
| **AWS X-Ray** | ★★ | エージェント・ツール呼び出しトレース |
| AWS Auto Scaling | ★★ | 推論エンドポイント自動スケール |
| AWS Cost Anomaly Detection / Cost Explorer | ★★ | トークン課金監視 |
| AWS Well-Architected Tool | ★★ | Generative AI Lens によるレビュー |
| Amazon Managed Grafana | ★ | 観測性ダッシュボード |
| AWS Systems Manager / Service Catalog | ★ | 運用管理 |
| AWS Chatbot | ★ | Slack 等への運用通知 |
| Amazon CloudWatch Synthetics | ★ | 合成監視 |

## Developer Tools / DevOps

| サービス | 頻出度 | 主用途 |
|---|---|---|
| **AWS CodePipeline / CodeBuild / CodeDeploy** | ★★ | GenAI モデルの CI/CD |
| **AWS CloudFormation / CDK** | ★★ | IaC によるエージェント・KB の宣言的管理 |
| **AWS CLI / SDK** | ★★ | 自動化／Bedrock API 呼び出し |
| AWS Amplify | ★ | フロントエンドの素早い構築 |
| AWS X-Ray | ★★ | 分散トレース（Networking 欄と重複再掲） |
| AWS CodeArtifact | ★ | パッケージ管理 |

## Analytics

| サービス | 頻出度 | 主用途 |
|---|---|---|
| **AWS Glue** | ★★ | データ取り込み、データカタログ、リネージ追跡 |
| AWS Glue Data Quality | ★★ | RAG 用データ品質バリデーション |
| Amazon OpenSearch Service | ★★★ | （ML 欄と重複再掲）ベクトル検索の主役 |
| Amazon Athena | ★ | ログ分析 |
| Amazon Kinesis | ★ | リアルタイム取り込み |
| Amazon QuickSight | ★ | 可視化 |
| Amazon EMR | ★ | 大規模バッチ処理 |
| Amazon MSK | ★ | Kafka イベントストリーミング |

## Customer Engagement / Migration

| サービス | 頻出度 | 主用途 |
|---|---|---|
| Amazon Connect | ★ | コンタクトセンタへの GenAI 組込 |
| AWS DataSync / Transfer Family | ★ | オンプレ→クラウド データ転送 |

---

## 試験 Tips: サービス選定の基本パターン

| ニーズ | 第一候補（試験で正解になりやすい） |
|---|---|
| マネージド RAG | **Amazon Bedrock Knowledge Bases** |
| ベクトル検索（自前） | **Amazon OpenSearch Service** または Aurora pgvector |
| FM への閉域アクセス | **VPC Endpoint + AWS PrivateLink** |
| プロンプトのバージョン管理＋承認 | **Bedrock Prompt Management** |
| 入出力のセーフティ制御 | **Bedrock Guardrails** |
| 監査ログ（誰が何の FM を呼んだか） | **AWS CloudTrail** |
| トークン使用量／レイテンシ可視化 | **CloudWatch + Bedrock Model Invocation Logs** |
| エッジ／IoT 向けモデル軽量化 | **SageMaker Neo** |
| 高負荷／予測可能ワークロード | **Bedrock Provisioned Throughput** |
| 安価モデル⇔高性能モデルの自動切替 | **Bedrock Intelligent Prompt Routing** |
| 人間レビュー組込 | **Amazon A2I + Step Functions** |
| PII 検出 | **Amazon Comprehend / Macie / Bedrock Guardrails** |
| 複雑ワークフロー（ReAct, HITL） | **AWS Step Functions** |
| エージェントの複数モデル協調 | **Bedrock Agents / Strands Agents / AWS Agent Squad** |
| コードアシスタンス | **Amazon Q Developer** |
| 業務アシスタント | **Amazon Q Business** |

## Out-of-Scope（試験対象外、参考）

公式が「Out-of-Scope」と明記しているのは主に以下の領域:
- カスタム ML モデルのフル学習・特徴量エンジニアリング系（深い深層学習トレーニング）
- 高度な MLOps の独自基盤構築

→ 「モデルを作る側」のサービスや手法は AIP-C01 では深く問われない。問われるのは「FM を**使う**ためのサービス」である点を意識する。
