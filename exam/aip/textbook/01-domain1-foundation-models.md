# Domain 1: Foundation Model Integration, Data Management, and Compliance（31%）

> **配点**: 31%（最大）／ **タスク数**: 6 ／ **スキル数**: 28
> 出典: AWS 公式 AIP-C01 試験ガイド Content Domain 1

## 1. ドメイン概要

本ドメインは試験の中核であり、**FM をどう選び、どうデータを供給し、どう RAG / プロンプトを構築するか** を一貫して問う。

「**生成 AI アプリのデータ側のすべて**」と理解するとよい:
- どの FM を選ぶか（1.2）
- どんなデータを通すか（1.3）
- どう蓄えるか（1.4 ベクトルストア）
- どう取り出すか（1.5 Retrieval / RAG）
- どう指示するか（1.6 プロンプト）
- そもそもどう設計するか（1.1）

Bedrock 系の機能、特に **Knowledge Bases / Prompt Management / Prompt Flows / Cross-Region Inference** が頻出する。SageMaker AI は FM ホスティングと FT 周りで登場。

学習優先度は **1.5 ≧ 1.4 > 1.6 > 1.2 > 1.3 > 1.1** が目安（試験頻出順）。

---

## 2. Task 1.1: 要件分析と GenAI ソリューション設計

### 2.1 何が問われるか

ビジネス要件・技術制約から **どのような構成で GenAI を実装するか** を判断する力。AWS Well-Architected Framework と Generative AI Lens を踏まえ、PoC → 本番の流れを設計できることが期待される。

### 2.2 公式スキル一覧

- **Skill 1.1.1**: ビジネスニーズ・技術制約に整合した包括的アーキテクチャ設計（適切な FM、統合パターン、デプロイ戦略）
- **Skill 1.1.2**: 実現可能性・性能・ビジネス価値を検証する技術 PoC を Amazon Bedrock 等で構築
- **Skill 1.1.3**: AWS Well-Architected Framework / WA Tool Generative AI Lens を用いて標準化された技術コンポーネントを作成

### 2.3 中核となる AWS サービス

- **Amazon Bedrock**: PoC・本番ともに第一選択
- **AWS Well-Architected Tool（Generative AI Lens）**: 設計レビューの公式ツール
- **AWS CDK / CloudFormation**: 標準化テンプレート提供
- **AWS Service Catalog**: 標準化されたコンポーネントの組織内配布

### 2.4 設計パターン・ベストプラクティス

| 場面 | 推奨パターン |
|---|---|
| 短期 PoC | Bedrock + Lambda + API Gateway の最小構成 |
| 本番化 | 上記 + VPC Endpoint + Guardrails + CloudTrail + KMS |
| 大規模／複数チーム | Service Catalog で「承認済 GenAI スタック」を配布 |
| 多モデル比較 | Prompt Flows or Lambda で A/B 切替 |

### 2.5 引っかけ

- 「最も早く PoC を作る」→ **Bedrock**（SageMaker でモデルをホスティングして、は冗長）
- 「Well-Architected レビューを行う」→ **WA Tool + Generative AI Lens**（AWS Trusted Advisor は別物）

### 2.6 Exam Tips

- 「組織標準化されたテンプレート配布」→ **Service Catalog**
- 「PoC を素早く」→ **Bedrock + Lambda**
- 「設計品質を体系的に確認」→ **Well-Architected Tool（Generative AI Lens）**

### 2.7 チェックポイント
- [ ] Generative AI Lens の柱を 3 つ以上挙げられる
- [ ] PoC と本番でアーキテクチャがどう差分化するか説明できる

---

## 3. Task 1.2: FM の選定と構成

### 3.1 何が問われるか

ユースケースに対する **FM の選び方、切り替え可能性、可用性、ライフサイクル管理**。

### 3.2 公式スキル一覧

- **Skill 1.2.1**: 性能ベンチマーク・能力分析・制約評価で FM を選定
- **Skill 1.2.2**: コード変更なしで動的にモデル／プロバイダを切替できる柔軟なアーキテクチャ（Lambda / API GW / AppConfig）
- **Skill 1.2.3**: サービス停止時にも継続稼働するレジリエント AI（Step Functions のサーキットブレーカ、Bedrock Cross-Region Inference、クロスリージョンモデルデプロイ、優雅な機能低下）
- **Skill 1.2.4**: SageMaker AI による FM カスタマイズ（LoRA・アダプタ等の PEFT、SageMaker Model Registry、自動デプロイ／ロールバック、ライフサイクル管理）

### 3.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Amazon Bedrock** | 標準的な FM 利用 |
| **Amazon Bedrock Cross-Region Inference** | リージョン制限を超えるアクセス、HA |
| **Amazon SageMaker AI** | 独自カスタム FM のホスティング |
| **SageMaker JumpStart** | OSS FM の取得 |
| **SageMaker Model Registry** | バージョン・承認管理 |
| **AWS AppConfig** | モデル ID 等のフィーチャーフラグ／動的構成 |
| **AWS Step Functions** | サーキットブレーカ、フォールバック |

### 3.4 FM 選定の評価軸

- **能力**: マルチモーダル対応、コンテキスト長、ツール使用、JSON モード
- **性能**: TPS、レイテンシ
- **コスト**: 入出力トークン単価
- **可用性**: リージョン、Provisioned Throughput 対応
- **コンプライアンス**: PII 取扱、データ保持
- **言語対応**: 日本語精度

### 3.5 設計パターン

- **モデル切替の抽象化**: API GW + Lambda の前段で AppConfig からモデル ID を読む → デプロイなしでモデル変更可能
- **Cross-Region Inference**: us-west-2 で Anthropic Claude が混雑時、ap-northeast-1 経由でフォールバック
- **PEFT デプロイ**: LoRA アダプタを SageMaker Model Registry で管理し、メインモデル＋アダプタで提供

### 3.6 引っかけ

- 「コード変更せずモデル切替」→ **AppConfig**（環境変数での切替は再デプロイが必要）
- 「FT より計算コストを抑えたい」→ **LoRA / PEFT**（フル FT は高コスト）
- 「特定リージョン専用 FM の冗長化」→ **Cross-Region Inference**

### 3.7 Exam Tips

- **PEFT = LoRA**、フル FT より圧倒的に安い・速い・忘却が少ない
- **SageMaker Model Registry** は承認ワークフローと CI/CD の起点
- ロールバック戦略の言及があれば **Model Registry の前バージョン参照**

### 3.8 チェックポイント
- [ ] LoRA とフル FT の差分（コスト・データ量・適用場面）を説明できる
- [ ] AppConfig を使ったモデル切替の流れが描ける
- [ ] Cross-Region Inference の用途を即答できる

---

## 4. Task 1.3: FM 用データ検証・処理パイプライン

### 4.1 何が問われるか

FM に投入するデータが**品質を満たし、適切な形式に整形されている**ことを保証する仕組み。

### 4.2 公式スキル一覧

- **Skill 1.3.1**: データ品質ワークフロー（AWS Glue Data Quality、SageMaker Data Wrangler、Lambda、CloudWatch メトリクス）
- **Skill 1.3.2**: テキスト・画像・音声・表形式の混在データ処理（Bedrock マルチモーダル、SageMaker Processing、AWS Transcribe、高度なマルチモーダルパイプライン）
- **Skill 1.3.3**: モデル固有要件に応じた入力フォーマット整形（Bedrock API JSON、SageMaker AI エンドポイント、対話形式整形）
- **Skill 1.3.4**: 入力データ品質の向上（Bedrock による再フォーマット、Comprehend のエンティティ抽出、Lambda の正規化）

### 4.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **AWS Glue / Glue Data Quality** | パイプライン＋品質ルール |
| **SageMaker Data Wrangler** | GUI 中心の前処理 |
| **AWS Lambda** | カスタム前処理 |
| **Amazon Comprehend** | エンティティ抽出、PII 検出、感情分析 |
| **Amazon Transcribe** | 音声 → テキスト |
| **Amazon Textract** | PDF / 画像 → 構造化テキスト |
| **Amazon Bedrock マルチモーダルモデル** | 画像入力対応 |
| **CloudWatch** | 品質メトリクス監視 |

### 4.4 入力フォーマットの実例

Bedrock Converse API:
```json
{
  "modelId": "anthropic.claude-3-7-sonnet-20250219-v1:0",
  "messages": [
    {"role": "user", "content": [{"text": "..."}]}
  ],
  "system": [{"text": "You are a helpful assistant."}]
}
```

→ 共通形式なので**モデル切替に強い**（InvokeModel API はモデルごとに JSON 構造が違う）。

### 4.5 引っかけ

- 「PDF 文書から構造化したい」→ **Textract**（OCR は Rekognition ではない）
- 「PII を含むかチェック」→ **Comprehend PII** または **Macie**（Macie は S3 上限定）
- 「対話履歴を整形」→ **DynamoDB に保存＋ Lambda で整形**

### 4.6 Exam Tips

- データソースが S3 → **Glue Data Quality** が第一候補
- データ品質ルールを宣言的に書きたい → **Glue Data Quality（DQDL）**
- リアルタイム入力検証 → **Lambda + CloudWatch メトリクス**

### 4.7 チェックポイント
- [ ] Comprehend と Macie の使い分け（リアルタイム/データセット監査）を説明できる
- [ ] Bedrock Converse API と InvokeModel API の利点差分を述べられる

---

## 5. Task 1.4: ベクトルストアの設計・実装

### 5.1 何が問われるか

RAG の心臓部である **ベクトルストアの選定・設計・運用** 全般。

### 5.2 公式スキル一覧

- **Skill 1.4.1**: FM 拡張用の高度なベクトル DB アーキテクチャ（Bedrock Knowledge Bases、OpenSearch + Neural plugin、RDS + S3、DynamoDB + ベクトル DB）
- **Skill 1.4.2**: 検索精度向上のためのメタデータフレームワーク（S3 オブジェクトメタデータ、カスタム属性、タグ）
- **Skill 1.4.3**: 大規模高性能ベクトル DB（OpenSearch シャーディング、マルチインデックス、階層インデックス）
- **Skill 1.4.4**: 文書管理・社内 wiki 等との統合
- **Skill 1.4.5**: ベクトルストアの鮮度維持（差分更新、リアルタイム変更検知、自動同期、定期リフレッシュ）

### 5.3 中核となる AWS サービス

| サービス | 用途 | 特徴 |
|---|---|---|
| **Bedrock Knowledge Bases** | フルマネージド RAG | 取り込み→ベクトル化→検索を一括 |
| **OpenSearch Service（k-NN / Neural）** | 自前ベクトル検索 | スケーラブル、ハイブリッド検索可 |
| **OpenSearch Serverless** | サーバレス | KB のデフォルトバックエンド |
| **Aurora PostgreSQL（pgvector）** | RDB＋ベクトル検索 | トランザクションと統合可能 |
| **Amazon Neptune Analytics** | グラフ＋ベクトル | 関係性も活かす RAG |
| **DynamoDB + 別ベクトル DB** | メタデータ＋ベクトル分離 | スケール特性が異なる場合 |

### 5.4 選定マトリクス

| 要件 | 推奨 |
|---|---|
| とにかく早く RAG を作りたい | **Bedrock Knowledge Bases** |
| 既存 OpenSearch を活用したい | **OpenSearch + Neural plugin** |
| RDB データと一緒に扱いたい | **Aurora pgvector** |
| 文書間の関係性も活かす | **Neptune Analytics** |
| 厳密なメタデータフィルタが必要 | OpenSearch（柔軟なクエリ） |

### 5.5 メタデータ設計

メタデータは検索精度に直結する。設計観点:
- **時刻**: `created_at`, `expired_at`（古い情報の除外）
- **権限**: `tenant_id`, `acl_groups`（マルチテナント分離）
- **分類**: `category`, `tags`
- **出典**: `source_url`, `document_id`（帰属表示用）

### 5.6 鮮度維持パターン

| 方式 | 特徴 |
|---|---|
| **イベント駆動更新** | S3 → EventBridge → Bedrock KB Sync API |
| **定期リフレッシュ** | EventBridge Scheduler で定時 ingest |
| **差分検知** | S3 ETag、ファイル更新日時で再 ingest |
| **リアルタイム** | DynamoDB Streams → Lambda → ベクトル更新 |

### 5.7 引っかけ

- 「マネージド RAG」→ **Bedrock Knowledge Bases**（自前 OpenSearch を選ぶのは構成過剰）
- 「リレーショナルデータと統合」→ **Aurora pgvector**
- 「既存全文検索を残しつつベクトルも」→ **OpenSearch ハイブリッド検索**

### 5.8 Exam Tips

- KB のデフォルトバックエンドは **OpenSearch Serverless**
- 「ドキュメント間の関係性」が出たら **Neptune Analytics** の可能性大
- 「マルチテナントで権限分離」→ メタデータに `tenant_id` を付けて検索フィルタで絞る

### 5.9 チェックポイント
- [ ] KB と素の OpenSearch を選ぶ判断軸を 3 つ説明できる
- [ ] 鮮度維持の 4 パターンを名前と用途で挙げられる

---

## 6. Task 1.5: 検索メカニズム（RAG）の設計

### 6.1 何が問われるか

**RAG の検索品質を最大化する技術**。チャンキング、埋め込み選定、検索アルゴリズム、リランキング、クエリ変換、API 統合まで。

### 6.2 公式スキル一覧

- **Skill 1.5.1**: 文書セグメント化（Bedrock チャンキング、Lambda の固定サイズ、階層チャンキング）
- **Skill 1.5.2**: 埋め込みモデルの選択・構成（Titan Embeddings、Bedrock embedding モデルの性能評価、Lambda でのバッチ生成）
- **Skill 1.5.3**: ベクトル検索の構築（OpenSearch、Aurora pgvector、Bedrock KB マネージド）
- **Skill 1.5.4**: 高度な検索アーキテクチャ（OpenSearch のセマンティック検索、ハイブリッド検索、Bedrock リランカ）
- **Skill 1.5.5**: 高度なクエリ処理（Bedrock でクエリ拡張、Lambda でクエリ分解、Step Functions でクエリ変換）
- **Skill 1.5.6**: FM とのシームレスな統合（function calling、MCP クライアント、標準 API パターン）

### 6.3 RAG の処理フロー

```
[クエリ] → [前処理] → [埋め込み生成] → [ベクトル検索] → [リランク] → [プロンプト構築] → [FM] → [応答（引用付き）]
                                                                                                     ↑
                                                                                                  帰属機能
```

各ステップでの選択肢を理解しておく。

### 6.4 チャンキング戦略

| 戦略 | 用途 |
|---|---|
| **固定サイズ（Fixed-size）** | 単純、汎用 |
| **階層（Hierarchical）** | 文書構造を尊重（章 → 節 → 段落） |
| **セマンティック** | 意味の切れ目で分割 |
| **No Chunking** | 短い文書、各文書 1 ベクトル |

Bedrock Knowledge Bases では、これらのチャンキング戦略を選択可能（カスタムも Lambda で実装可）。

### 6.5 埋め込みモデルの選定

| モデル | 次元 | 特徴 |
|---|---|---|
| **Amazon Titan Embeddings G1** | 1536 | バランス型 |
| **Amazon Titan Text Embeddings V2** | 256/512/1024 可変 | コスト効率重視 |
| **Cohere Embed multilingual** | 1024 | 多言語強い |

選定軸: 次元（メモリ／精度）、対応言語、コスト、最大入力長。

### 6.6 ハイブリッド検索

意味類似（ベクトル）と語彙一致（BM25）を組み合わせる:
- 略語、製品名、ID など**語彙一致が大事な場面**ではベクトル単独より精度↑
- OpenSearch / Bedrock KB でサポート

### 6.7 リランキング

第一段階で広く取り（k=50 等）、第二段階で**より高精度なリランカモデル**で再評価して上位に絞る:
- Bedrock の Rerank モデル（Cohere Rerank 等）
- 計算コストは増えるが精度は明確に向上

### 6.8 高度なクエリ処理

| 手法 | 説明 |
|---|---|
| **クエリ拡張** | LLM で類義語・関連語を追加生成 |
| **クエリ分解** | 複合質問を複数の小クエリに分割（Step Functions） |
| **HyDE** | LLM に仮想的な回答を作らせ、その埋め込みで検索 |
| **会話履歴を含めた再構成** | 「それ」「その後」等を解決 |

### 6.9 統合方式

- **RetrieveAndGenerate API**（Bedrock KB）: 検索＋生成を 1 API、citations（**帰属**）を返す
- **Retrieve API**（KB）: 検索のみ、生成は Bedrock 別呼び出し
- **Function Calling**: Agents が必要時のみ KB を検索ツールとして呼ぶ
- **MCP クライアント**: 標準化されたツール接続

### 6.10 引っかけ

- 「引用付きで応答」→ **RetrieveAndGenerate**（**帰属機能**）
- 「略語のヒット率を上げたい」→ **ハイブリッド検索**
- 「曖昧クエリの精度向上」→ **クエリ拡張 + リランカ**

### 6.11 Exam Tips

- 帰属機能 = **citations / source attribution**。RAG の信頼性の核
- リランカは **二段階検索の上位精度向上** に効く
- MCP は新しい標準。MCP クライアント／サーバの両方が出題候補

### 6.12 チェックポイント
- [ ] チャンキング戦略を 3 つ以上挙げ、用途を説明できる
- [ ] ハイブリッド検索の利点を述べられる
- [ ] RetrieveAndGenerate と Retrieve の違いを言える

---

## 7. Task 1.6: プロンプトエンジニアリングとガバナンス

### 7.1 何が問われるか

**プロンプトの作り方** だけでなく、**組織として一貫したプロンプト運用** ができるかも問われる。Prompt Management、Prompt Flows、Guardrails、テンプレート、品質保証が中心。

### 7.2 公式スキル一覧

- **Skill 1.6.1**: モデル指示フレームワーク（Bedrock Prompt Management でロール定義、Bedrock Guardrails で責任ある AI、テンプレート構成で出力フォーマット）
- **Skill 1.6.2**: 文脈維持・対話改善（Step Functions の明確化ワークフロー、Comprehend で意図認識、DynamoDB で会話履歴）
- **Skill 1.6.3**: プロンプト管理・ガバナンス（Bedrock Prompt Management でパラメータ化テンプレート＋承認、S3 でテンプレートリポジトリ、CloudTrail で利用追跡、CloudWatch Logs でアクセスログ）
- **Skill 1.6.4**: 品質保証（Lambda で期待出力検証、Step Functions でエッジケーステスト、CloudWatch でリグレッション）
- **Skill 1.6.5**: 反復的プロンプト改善（構造化入力、出力フォーマット指定、CoT、フィードバックループ）
- **Skill 1.6.6**: 複雑プロンプトシステム（Bedrock Prompt Flows で逐次チェイン、条件分岐、再利用部品、前処理／後処理の統合）

### 7.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Bedrock Prompt Management** | テンプレート版管理＋承認 |
| **Bedrock Prompt Flows** | チェイン構築（ローコード） |
| **Bedrock Guardrails** | 安全制御（出力検閲、PII フィルタ） |
| **DynamoDB** | 会話履歴／コンテキスト保持 |
| **Step Functions** | 明確化ループ、HITL |
| **Amazon Comprehend** | 意図検出 |
| **CloudTrail / CloudWatch Logs** | 監査 |

### 7.4 主要プロンプト技法

| 技法 | 用途 |
|---|---|
| **Zero-shot** | シンプルな指示のみ |
| **Few-shot** | 例を 2〜10 個示す |
| **Chain-of-Thought (CoT)** | 中間推論を出させる |
| **Self-consistency** | 複数推論パスから多数決 |
| **ReAct** | 推論＋行動の交互（エージェント） |
| **Output schema指定** | JSON Schema で出力強制 |

### 7.5 サンプリングパラメータ

- **Temperature**: 0 ≒ 決定的、1+ ≒ 創造的。推論／要約は 0 寄り、創作は 0.7-1.0
- **Top-k**: 上位 k 候補から選択。**top-k=50** が一般的。`top-k=1` は決定的に最尤を選ぶ
- **Top-p**（Nucleus）: 累積確率 p までの候補から選択
- **Max tokens**: 出力上限。コスト制御の基本

### 7.6 ガバナンス・運用観点

- **テンプレート版管理**: Prompt Management で `production` / `staging` / `experimental` のステージ分け
- **承認ワークフロー**: Prompt Management の承認 + CodePipeline で本番適用
- **A/B テスト**: Prompt Flows or Lambda + フィーチャーフラグで実験
- **回帰テスト**: 期待入出力ペアを Step Functions で定期実行
- **監査**: CloudTrail で「誰がどのテンプレートを呼んだか」を記録

### 7.7 引っかけ

- 「プロンプトの版管理」→ **Bedrock Prompt Management**（S3 だけは要件不足）
- 「複数プロンプトの分岐統合」→ **Bedrock Prompt Flows**（Step Functions より GenAI 用途で第一候補）
- 「決定的な出力にしたい」→ **Temperature 0、top-k=1（または greedy decoding）**

### 7.8 Exam Tips

- **Prompt Management = 版管理／承認**、**Prompt Flows = チェイン構築** で混同しない
- 安全制御の話で Prompt 系が出たら **Guardrails** を選ぶ（Prompt Management だけでは検閲できない）
- top-k は「上位 k 個から選ぶ」基本概念。検索／推薦／生成の全文脈で同じ意味

### 7.9 チェックポイント
- [ ] Temperature と top-k の差を 1 行で説明できる
- [ ] Prompt Management と Prompt Flows の役割分担を言える
- [ ] CoT・Few-shot・ReAct の使い分けが描ける

> 出典: `../point/a.md` の「top-k」（候補から上位 k を選ぶ。top-1 = 最尤、top-5 accuracy など多用途）

---

## 8. このドメインで主に出てくる AWS サービス一覧

| サービス | 主な用途 | 関連タスク |
|---|---|---|
| Amazon Bedrock | FM 利用全般 | 1.1, 1.2, 1.3, 1.5, 1.6 |
| Amazon Bedrock Knowledge Bases | マネージド RAG | 1.4, 1.5 |
| Amazon Bedrock Prompt Management | プロンプト版管理 | 1.6 |
| Amazon Bedrock Prompt Flows | プロンプトチェイン | 1.6 |
| Amazon Bedrock Cross-Region Inference | 高可用 FM 推論 | 1.2 |
| Amazon SageMaker AI | カスタム FM ホスト | 1.2 |
| SageMaker JumpStart | OSS FM 取得 | 1.2 |
| SageMaker Model Registry | モデル版管理 | 1.2 |
| SageMaker Data Wrangler | データ前処理 | 1.3 |
| Amazon OpenSearch Service | ベクトル／ハイブリッド検索 | 1.4, 1.5 |
| Amazon Aurora（pgvector） | RDB＋ベクトル | 1.4 |
| AWS Glue / Data Quality | データパイプライン／品質 | 1.3 |
| AWS Lambda | 汎用前処理／統合 | 1.3, 1.5, 1.6 |
| AWS Step Functions | ワークフロー／HITL | 1.5, 1.6 |
| Amazon DynamoDB | 会話履歴 | 1.6 |
| Amazon Comprehend | NLP 前処理／意図検出 | 1.3, 1.6 |
| Amazon Textract / Transcribe | マルチモーダル前処理 | 1.3 |
| Amazon Titan | 埋め込み・生成 | 1.5 |
| AWS AppConfig | モデル動的構成 | 1.2 |
| AWS Well-Architected Tool | 設計レビュー | 1.1 |
| AWS Service Catalog | 標準コンポーネント配布 | 1.1 |
| Amazon S3 | データソース／テンプレート | 全タスク |
| AWS CloudTrail | 監査 | 1.6 |
| Amazon CloudWatch | メトリクス監視 | 1.3, 1.6 |

---

## 9. ドメイン横断キーワード

- **FM 選定軸**: 能力 / 性能 / コスト / 可用性 / コンプライアンス / 言語
- **PEFT / LoRA**: 軽量 FT
- **Cross-Region Inference**: HA／スループット
- **Knowledge Bases**: マネージド RAG
- **Hybrid Search**: ベクトル + BM25
- **Reranker**: 二段階検索
- **帰属機能（citations）**: 出典付き応答
- **Prompt Management vs Prompt Flows**: 版管理 vs チェイン
- **Top-k / Top-p / Temperature**: サンプリング 3 兄弟

---

## 10. 参考リンク

- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/)
- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Bedrock RetrieveAndGenerate API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html)
- [Bedrock Cross-Region Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
- [Bedrock Prompt Management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html)
- [Bedrock Prompt Flows](https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html)
- [SageMaker JumpStart](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html)
- [Well-Architected Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/)
- [Classmethod: Amazon Bedrock Converse API](https://dev.classmethod.jp/articles/amazon-bedrock-converse-api/)

---

## 11. 既存メモからの取り込み出典

- `../point/a.md`: top-k（→ 7.5 / 用語集に統合）、帰属機能（→ 6.9 / 用語集）
- `../point/exam/tech/a.md`: 一部の質問解釈は他ドメインに分散
