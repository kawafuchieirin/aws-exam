# Domain 2: Implementation and Integration（26%）

> **配点**: 26% ／ **タスク数**: 5 ／ **スキル数**: 24
> 出典: AWS 公式 AIP-C01 試験ガイド Content Domain 2

## 1. ドメイン概要

Domain 1 が「**データと FM の選び方**」だったのに対し、本ドメインは「**FM をどう動くアプリケーションに組み込むか**」が中心。

具体的には:
- エージェント実装（Task 2.1）
- モデルデプロイ（Task 2.2）
- エンタープライズ統合（Task 2.3）
- FM API 統合（Task 2.4）
- アプリ統合パターン・開発ツール（Task 2.5）

学習優先度は **2.1 ≧ 2.4 > 2.5 > 2.2 > 2.3** が目安。Bedrock Agents、Converse API、Strands Agents、AWS Agent Squad、MCP、Q Developer が頻出。

---

## 2. Task 2.1: エージェンティック AI とツール統合

### 2.1 何が問われるか

**自律的に複数ステップを推論・実行する AI エージェント** の設計と実装。記憶・状態管理、ReAct、ガードレール付きワークフロー、ツール統合まで。

### 2.2 公式スキル一覧

- **Skill 2.1.1**: メモリ・状態管理を持つ自律システム（Strands Agents、AWS Agent Squad、MCP）
- **Skill 2.1.2**: 高度な問題解決（Step Functions で ReAct パターン、CoT 推論）
- **Skill 2.1.3**: 安全な AI ワークフロー（Step Functions の停止条件、Lambda タイムアウト、IAM の境界、サーキットブレーカ）
- **Skill 2.1.4**: モデル協調（特化 FM、独自集約ロジック、モデル選定フレームワーク）
- **Skill 2.1.5**: 人間と協調する AI（Step Functions のレビュー／承認、API GW のフィードバック収集）
- **Skill 2.1.6**: 信頼性のあるツール統合（Strands API、標準関数定義、Lambda のエラーハンドリング）
- **Skill 2.1.7**: モデル拡張フレームワーク（Lambda の軽量 MCP サーバ、ECS の本格 MCP サーバ、MCP クライアントライブラリ）

### 2.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Amazon Bedrock Agents** | マネージドエージェント |
| **Amazon Bedrock AgentCore** | エージェント観測・運用基盤 |
| **Strands Agents** | AWS 製コードファーストエージェントフレームワーク |
| **AWS Agent Squad** | マルチエージェント連携 |
| **AWS Step Functions** | ReAct ループ／HITL |
| **AWS Lambda / Amazon ECS** | MCP サーバ |
| **Amazon API Gateway** | フィードバック収集 |
| **Amazon DynamoDB** | エージェントメモリ・状態 |

### 2.4 エージェント設計パターン

| パターン | 説明 |
|---|---|
| **ReAct（Reason + Act）** | 推論 → ツール呼び出し → 観察 → 再推論 |
| **CoT（Chain-of-Thought）** | 多段推論を出力させてから最終回答 |
| **Plan-and-Execute** | 全体計画を最初に立て、各ステップを実行 |
| **Multi-Agent** | 役割分担した複数エージェントを協調（Agent Squad） |
| **Reflection** | 自己評価して再生成 |

### 2.5 ツール統合（Tool Use / Function Calling）

エージェントが外部 API や DB を呼ぶ仕組み。実装の選択肢:
- **Bedrock Agents Action Groups**: マネージド方式。OpenAPI スキーマでツール定義
- **Converse API のツール使用**: Bedrock 直接、Lambda などにルーティング
- **MCP**: 標準プロトコルで複数 LLM・ツール基盤を疎結合化

### 2.6 安全性ガードレール

エージェントは**自律的に動く分、暴走リスクが高い**。試験で問われる安全策:
- **停止条件**: 最大ステップ数、タイムアウト
- **IAM 境界**: ツールが触れる範囲を Action Group / Lambda 実行ロールで制限
- **サーキットブレーカ**: ツール失敗が連続したら全体停止
- **HITL**: 高リスク操作（送金、メール送信）は人間承認

### 2.7 引っかけ

- 「コードファーストでエージェント作成」→ **Strands Agents**（Bedrock Agents は宣言型寄り）
- 「複数エージェントの協調」→ **AWS Agent Squad**
- 「ツールへの軽量接続」→ **Lambda での MCP サーバ**
- 「複雑ツール、ステートフル」→ **ECS での MCP サーバ**

### 2.8 Exam Tips

- **Bedrock Agents** は OpenAPI スキーマでツール定義 + KB 連携が標準
- **MCP** は新興だが本試験では重要トピック。Lambda（軽量）/ ECS（重量）の選定が頻出
- 「自律的に何ステップも回す → **Step Functions or エージェント**」

> 出典: `../point/a.md`「Bedrock agent」（マネージドエージェント。タスク分解、API 呼び出し、KB 参照を自律実行）

### 2.9 チェックポイント
- [ ] ReAct と CoT の違いを言える
- [ ] Bedrock Agents / Strands Agents / Agent Squad の使い分けを説明できる
- [ ] Lambda MCP と ECS MCP の選定基準を述べられる

---

## 3. Task 2.2: モデルデプロイ戦略

### 3.1 何が問われるか

FM の**デプロイ方式の選定**と、LLM 特有のデプロイ課題（メモリ、GPU、トークン処理）への対応。

### 3.2 公式スキル一覧

- **Skill 2.2.1**: アプリ要件に応じた FM デプロイ（Lambda のオンデマンド、Bedrock Provisioned Throughput、SageMaker AI のハイブリッド）
- **Skill 2.2.2**: LLM 固有の課題に対応した FM デプロイ（メモリ最適コンテナ、GPU 利用、トークン処理容量、専用モデルローディング）
- **Skill 2.2.3**: 性能とリソース要件をバランスする FM デプロイ（適切なモデル選定、特定タスクには小型事前学習モデル、API ベースモデルカスケード）

### 3.3 デプロイ選択肢

| 方式 | 特徴 | 用途 |
|---|---|---|
| **Bedrock オンデマンド** | サーバレス、トークン課金 | 不定期・小規模 |
| **Bedrock Provisioned Throughput** | 専用キャパ予約、TPM ベース課金 | 高負荷・予測可能 |
| **SageMaker AI Endpoint（リアルタイム）** | カスタム FM、独自実装 | 自社 FT モデル |
| **SageMaker Asynchronous** | 大入力／長時間推論 | 文書要約、長動画 |
| **SageMaker Serverless Inference** | 軽量 ML | コールドスタート許容 |
| **SageMaker Batch Transform** | バッチ推論 | 夜間大量処理 |
| **AWS Lambda** | API 統合層 | 軽量モデル、ラッパ |

### 3.4 LLM 固有の考慮事項

- **GPU 必須**: 大規模 FM は GPU インスタンス（`ml.g5`, `ml.p4d` 等）
- **メモリ最適コンテナ**: モデルウェイトを共有・遅延ロード
- **トークン処理容量**: 同時並列性の設計（バッチング、KV キャッシュ）
- **モデルカスケード**: 軽量モデルで前段判定、本命 FM は必要時のみ

### 3.5 引っかけ

- 「予測可能な高負荷」→ **Provisioned Throughput**
- 「長時間推論（10 分超）」→ **SageMaker Asynchronous**
- 「夜間バッチで大量処理」→ **Batch Transform**
- 「コスト最小、軽量タスクが大半」→ **モデルカスケード（小型モデル先行）**

### 3.6 Exam Tips

- **Provisioned Throughput** は 1 分あたりの最大入出力トークンで定義。突発スパイクに強い
- **SageMaker Neo** はエッジ／IoT 向け軽量化（Domain 4 で詳述）
- 「Bedrock vs SageMaker」: 標準 FM = Bedrock、独自カスタム = SageMaker

> 出典: `../point/exam/tech/a.md`「Bedrock のプロビジョンスループット = 特定基盤モデル専用の推論キャパシティ、1 分あたり最大入出力トークンで定義、大量リクエストでも安心」

### 3.7 チェックポイント
- [ ] Bedrock の 2 種類の課金（オンデマンド / Provisioned Throughput）の使い分けを説明できる
- [ ] SageMaker の 4 種類のエンドポイント（Real-time / Async / Serverless / Batch）の用途を述べられる

---

## 4. Task 2.3: エンタープライズ統合アーキテクチャ

### 4.1 何が問われるか

**既存エンタープライズシステム（CRM、ERP、レガシー）に GenAI をどう組み込むか**。セキュリティ境界、CI/CD、ハイブリッドクラウドまで。

### 4.2 公式スキル一覧

- **Skill 2.3.1**: 既存環境への接続（API ベース統合、イベント駆動アーキ、データ同期）
- **Skill 2.3.2**: AI 機能の組込（API GW のマイクロサービス統合、Lambda の Webhook、EventBridge のイベント駆動）
- **Skill 2.3.3**: セキュアアクセス（FM サービスとエンタープライズ ID フェデレーション、RBAC、最小権限 API）
- **Skill 2.3.4**: データレジデンシー対応（Outposts でオンプレ統合、Wavelength でエッジ、安全ルーティング）
- **Skill 2.3.5**: GenAI ゲートウェイと CI/CD（CodePipeline、CodeBuild、自動テスト、セキュリティスキャン、ロールバック、中央化抽象化レイヤ、可観測性）

### 4.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Amazon API Gateway** | 外部公開／統合 API |
| **AWS Lambda** | Webhook、変換層 |
| **Amazon EventBridge** | イベント駆動疎結合 |
| **AWS PrivateLink + VPC Endpoint** | 閉域 Bedrock |
| **AWS Outposts / Wavelength** | データレジデンシー／低遅延 |
| **AWS CodePipeline / CodeBuild / CodeDeploy** | CI/CD |
| **IAM Identity Center** | SSO・フェデレーション |

### 4.4 GenAI Gateway パターン

エンタープライズで頻出: **アプリと FM の間に共通ゲートウェイ層を置く**。
- 認証認可の中央化
- レート制限／クォータ
- 監査ログの集中
- モデル切替の透過化
- コスト追跡

実装: API Gateway + Lambda + DynamoDB（ポリシー・ログ）

### 4.5 ハイブリッドクラウド

- **Outposts**: オンプレに AWS サービスを延伸。データ主権要件を満たしつつ Bedrock 等を利用
- **Wavelength**: 5G エッジ。低遅延が必須のリアルタイム生成

### 4.6 引っかけ

- 「既存基幹システムに非侵襲で GenAI を足す」→ **EventBridge / API GW + Lambda**
- 「データはオンプレを離れさせられない」→ **Outposts**
- 「中央化された GenAI 利用ポリシー」→ **GenAI Gateway（API GW + Lambda）**

### 4.7 Exam Tips

- VPC + PrivateLink で Bedrock 閉域接続は鉄板パターン
- CI/CD は **CodePipeline + CodeBuild + 自動テスト** の流れ

### 4.8 チェックポイント
- [ ] GenAI Gateway の 3 つの責務を挙げられる
- [ ] PrivateLink を使う典型シナリオを説明できる

---

## 5. Task 2.4: FM API 統合

### 5.1 何が問われるか

**FM を呼び出す API の設計と実装**: 同期／非同期、ストリーミング、レジリエンス、ルーティング。

### 5.2 公式スキル一覧

- **Skill 2.4.1**: 柔軟なモデル対話（Bedrock API による同期、SDK + SQS による非同期、API GW + 検証）
- **Skill 2.4.2**: リアルタイム AI（Bedrock ストリーミング API、WebSocket / SSE、API GW のチャンク転送）
- **Skill 2.4.3**: レジリエント FM（SDK の指数バックオフ、API GW のレート制限、フォールバック、X-Ray の可観測性）
- **Skill 2.4.4**: 知的モデルルーティング（静的、Step Functions の動的コンテンツベース、メトリクスベース、API GW の変換）

### 5.3 Bedrock API の主要メソッド

| API | 用途 | 特徴 |
|---|---|---|
| **Converse** | 同期生成（推奨） | モデル横断統一形式、ツール使用対応 |
| **ConverseStream** | ストリーミング生成 | 同上＋逐次返却 |
| **InvokeModel** | レガシー同期 | モデル固有 JSON |
| **InvokeModelWithResponseStream** | レガシーストリーム | 同上 |
| **Retrieve** | KB 検索のみ | 自前で生成 |
| **RetrieveAndGenerate** | KB 検索＋生成 | citations 付き |

#### Converse API の特徴
- **モデル間差異を吸収** → モデル切替が容易
- ストリーミングも対応
- ツール使用（Function Calling）対応
- 必要 IAM: `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`
- 一部モデルはまだ非対応（最新ドキュメント要確認）

> 出典: `../point/a.md`「Converse API では Bedrock の基盤モデルに対して共通したアクセスができる。InvokeModel API のようにモデルごとの差異を意識せず、モデル切替が容易」

### 5.4 ストリーミング実装

クライアントへの逐次返却:
- **API Gateway WebSocket**: 双方向、長時間接続
- **Server-Sent Events（SSE）**: 一方向（サーバ→クライアント）、HTTP 互換
- **API Gateway Chunked Transfer**: HTTP 1.1 chunked

Bedrock の `ConverseStream` を Lambda で受け、SSE で転送するパターンが頻出。

### 5.5 レジリエンスパターン

| 課題 | 対策 |
|---|---|
| 一時的な ThrottlingException | **指数バックオフリトライ（SDK デフォルト）** |
| 特定リージョンの可用性低下 | **Cross-Region Inference / 複数リージョン** |
| モデル選定の柔軟性 | **API GW + Lambda で抽象化** |
| トレーシング | **AWS X-Ray** |
| クライアント急増 | **API GW のレート制限・使用量プラン** |

### 5.6 モデルルーティング

| 方式 | 説明 |
|---|---|
| **静的** | 環境変数／設定でモデル ID 固定 |
| **コンテンツベース** | 入力長・トピックで振り分け |
| **メトリクスベース** | レイテンシ・エラー率で動的 |
| **Bedrock Intelligent Prompt Routing** | マネージドな自動ルーティング（→Domain 4 で詳述） |

### 5.7 引っかけ

- 「モデル切替を将来も容易に」→ **Converse API**
- 「リアルタイム逐次表示」→ **ConverseStream + WebSocket / SSE**
- 「スロットルへの対処」→ **指数バックオフ + リトライ**
- 「複数モデルへの動的ルーティング（自前）」→ **Step Functions or Lambda**
- 「マネージドな動的ルーティング」→ **Bedrock Intelligent Prompt Routing**

### 5.8 Exam Tips

- 新規実装は **Converse API** 推奨。InvokeModel はレガシー扱い
- ストリーミングが要件なら **API GW WebSocket / SSE** のどちらかを選ぶ
- 「観測性」「分散トレース」キーワードに対しては **X-Ray**

### 5.9 チェックポイント
- [ ] Converse / ConverseStream / Retrieve / RetrieveAndGenerate の使い分けを説明できる
- [ ] WebSocket と SSE の違いを言える
- [ ] Bedrock のスロットルにどう対処するか述べられる

---

## 6. Task 2.5: アプリ統合パターン・開発ツール

### 6.1 何が問われるか

**FM をユーザ／開発者から見えるアプリへ落とし込む技術**、および**開発生産性を上げるツール**。

### 6.2 公式スキル一覧

- **Skill 2.5.1**: GenAI 用 API（API GW でストリーミング応答、トークン制限管理、リトライ）
- **Skill 2.5.2**: アクセシブルな AI インターフェース（AWS Amplify の宣言型 UI、OpenAPI 仕様、Bedrock Prompt Flows のノーコード）
- **Skill 2.5.3**: ビジネスシステム強化（Lambda の CRM 強化、Step Functions の文書処理、Amazon Q Business データソース、Bedrock Data Automation）
- **Skill 2.5.4**: 開発者生産性（Amazon Q Developer によるコード生成・リファクタ、API 補完、AI コンポーネントテスト、性能最適化）
- **Skill 2.5.5**: 高度な GenAI アプリ（Strands Agents・AWS Agent Squad の AWS ネイティブ協調、Step Functions のエージェントパターン、Bedrock のプロンプトチェイン）
- **Skill 2.5.6**: トラブルシュート効率化（CloudWatch Logs Insights、X-Ray、Q Developer の GenAI 固有エラーパターン認識）

### 6.3 Amazon Q シリーズ

| サービス | 対象 | 用途 |
|---|---|---|
| **Amazon Q Developer** | 開発者 | コード生成、補完、リファクタ、IaC |
| **Amazon Q Business** | 業務ユーザ | 社内文書／業務システムへの問合せ |
| **Amazon Q Business Apps** | 業務ユーザ | Q Business 上のカスタムアプリ |

#### Q Developer のキーポイント

- **`.amazonq` ディレクトリ**: コンテキストファイルを置く場所（プロジェクト用ではなく、Q Developer がコンテキストとして読む設定ファイルの置き場）
- **`@workspace` 参照**: 現在のワークスペース全体を Q に参照させる
- **カスタム機能**: Pro 以上のプランで利用可能な機能（自動適用される）
- **コード補完／リファクタ／生成／テスト** を統合して提供

> 出典: `../point/exam/tech/a.md`「カスタム機能は pro 以上、`.amazonq` はコンテキストファイル置き場（プロジェクト用ではない）、`@workspace` で参照させる」

### 6.4 ビジネスシステム強化のパターン

- **CRM 統合**: Lambda が CRM API を呼び出し、Bedrock で要約・回答ドラフト
- **文書処理**: Step Functions + Textract + Bedrock で OCR → 要約 → 構造化
- **Bedrock Data Automation**: 文書／音声／画像から構造化データを抽出するマネージドパイプライン

### 6.5 開発者向けツール

- **AWS Amplify**: フロントエンドを宣言型に。AI コンポーネントの統合に強い
- **OpenAPI 仕様**: 「API ファースト」で先にスキーマ定義 → SDK 自動生成
- **Bedrock Prompt Flows**: ノーコードでプロンプトチェイン構築

### 6.6 トラブルシュート

- **CloudWatch Logs Insights**: ログを SQL 風に検索。プロンプト・応答の分析
- **X-Ray**: 分散トレース。Bedrock 呼び出しの追跡
- **Q Developer**: GenAI 固有エラー（プロンプト設計問題、トークン超過等）の認識を支援

### 6.7 引っかけ

- 「開発者の生産性」→ **Amazon Q Developer**
- 「業務ユーザ向け社内チャット」→ **Amazon Q Business**
- 「ノーコードでプロンプトチェイン」→ **Bedrock Prompt Flows**
- 「文書 → 構造化を一括」→ **Bedrock Data Automation**
- 「`.amazonq` の役割」→ **Q Developer のコンテキストファイル置き場**

### 6.8 Exam Tips

- Q Developer を使うシナリオは「**開発者がコード書きを早めたい**」場面
- Q Business は「**業務ユーザが既存社内データに問い合わせたい**」場面
- 両者を混同しない

### 6.9 チェックポイント
- [ ] Q Developer / Q Business / Q Business Apps の使い分けを言える
- [ ] `.amazonq` の役割を説明できる
- [ ] Bedrock Data Automation の用途を述べられる

---

## 7. このドメインで主に出てくる AWS サービス一覧

| サービス | 主な用途 | 関連タスク |
|---|---|---|
| Amazon Bedrock Agents | マネージドエージェント | 2.1 |
| Amazon Bedrock AgentCore | エージェント運用基盤 | 2.1 |
| Strands Agents | コードファーストエージェント | 2.1, 2.5 |
| AWS Agent Squad | マルチエージェント協調 | 2.1, 2.5 |
| Amazon Bedrock Data Automation | 自動データ処理 | 2.5 |
| Amazon Bedrock Prompt Flows | プロンプトチェイン構築 | 2.5 |
| Amazon Q Developer | コード生成支援 | 2.5 |
| Amazon Q Business / Apps | 業務アシスタント | 2.5 |
| AWS Lambda | API・ツール統合層 | 2.1, 2.3, 2.4, 2.5 |
| AWS Step Functions | ReAct、ワークフロー | 2.1, 2.5 |
| Amazon API Gateway | 外部公開 API | 2.3, 2.4, 2.5 |
| AWS PrivateLink / VPC Endpoint | 閉域 Bedrock | 2.3 |
| Amazon EventBridge | イベント駆動統合 | 2.3 |
| AWS Outposts / Wavelength | ハイブリッド／エッジ | 2.3 |
| AWS Code* シリーズ | CI/CD | 2.3 |
| Amazon SageMaker AI | 独自 FM ホスト | 2.2 |
| Amazon SageMaker（Real-time / Async / Batch） | 各種推論方式 | 2.2 |
| Amazon ECS / EKS / Fargate | コンテナ MCP サーバ | 2.1 |
| AWS X-Ray | 分散トレース | 2.4, 2.5 |
| Amazon CloudWatch Logs Insights | ログ分析 | 2.5 |
| AWS Amplify | フロントエンド | 2.5 |
| Amazon DynamoDB | エージェント状態 | 2.1 |
| AWS SQS | 非同期処理 | 2.4 |

---

## 8. ドメイン横断キーワード

- **Converse API**: モデル横断統一インターフェース、新規実装の第一選択
- **Bedrock Agents / Strands Agents / AWS Agent Squad**: エージェント実装の 3 選択肢
- **MCP（Model Context Protocol）**: 標準化ツール接続
- **GenAI Gateway**: エンタープライズの抽象化レイヤ
- **Provisioned Throughput**: 専用キャパ予約
- **Q Developer / Q Business**: 開発者向け／業務向け
- **`.amazonq`**: Q Developer のコンテキストディレクトリ

---

## 9. 参考リンク

- [Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
- [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Strands Agents](https://strandsagents.com/)
- [AWS Agent Squad](https://github.com/awslabs/multi-agent-orchestrator)
- [Amazon Q Developer User Guide](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/)
- [Amazon Q Business User Guide](https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/)
- [Bedrock Data Automation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html)
- [Classmethod: Amazon Bedrock Converse API](https://dev.classmethod.jp/articles/amazon-bedrock-converse-api/)

---

## 10. 既存メモからの取り込み出典

- `../point/a.md`: Bedrock agent（→ 2 章）、Converse API（→ 5 章）
- `../point/exam/tech/a.md`: Q Developer / `.amazonq` / `@workspace` / カスタム機能（→ 6 章）
