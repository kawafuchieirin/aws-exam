# Appendix: 用語集（Glossary）

> AIP-C01 で頻出する用語を50音／アルファベット順で整理。各用語に「**関連**」として参照ドメインを示す。
> 既存メモ（`../point/a.md`, `../point/exam/tech/a.md`）から取り込んだ項目には出典を明示。

## A

### Agentic AI（エージェンティック AI）
LLM が「ツール」を呼び出しながら自律的に複数ステップを推論・実行するアーキテクチャ。Amazon Bedrock Agents が代表的。
**関連**: Domain 2 (Task 2.1)

### Amazon Augmented AI（Amazon A2I）
人間によるレビュー（Human-in-the-Loop）を ML 推論に組み込むサービス。低信頼度結果のレビュー・サンプリング監査に使う。
**関連**: Domain 3 (Task 3.4), Domain 5

### Amazon Bedrock
基盤モデル（FM）への単一 API アクセスを提供するマネージドサービス。
**関連**: 全ドメイン

### Amazon Bedrock Agents
タスク分解、API 呼び出し、知識ベース参照を自律実行するエージェント機能。Strands Agents / AWS Agent Squad と並ぶ選択肢。
**関連**: Domain 2 (Task 2.1)
> 出典: `../point/a.md` の「Bedrock agent」

### Amazon Bedrock AgentCore
エージェントのランタイム・観測・ガバナンスを統合管理する基盤レイヤ。
**関連**: Domain 2, Domain 4

### Amazon Bedrock Guardrails
プロンプト／応答に対するコンテンツフィルタ、PII フィルタ、トピック禁止、グラウンディングチェック等を一元提供。
**関連**: Domain 3 (Task 3.1, 3.4)

### Amazon Bedrock Knowledge Bases
ベクトルストア＋取り込みパイプライン＋ RAG 検索 API（Retrieve / RetrieveAndGenerate）を提供するマネージド RAG。
**関連**: Domain 1 (Task 1.4, 1.5)

### Amazon Bedrock Model Evaluation
自動評価（ROUGE/BERTScore など）と人手評価の両方をサポートする FM 評価機能。
**関連**: Domain 5 (Task 5.1)

### Amazon Bedrock Prompt Flows
ノーコード／ローコードで複数プロンプト・条件分岐・関数呼び出しをチェイン化するワークフロービルダー。
**関連**: Domain 1 (Task 1.6), Domain 2 (Task 2.5)

### Amazon Bedrock Prompt Management
プロンプトテンプレートのバージョン管理・承認ワークフロー・パラメータ化をマネージドで提供。
**関連**: Domain 1 (Task 1.6), Domain 3 (Task 3.3)

### Amazon Comprehend
NLP マネージドサービス。エンティティ抽出、感情分析、PII 検出、トピックモデリング、言語識別、キーフレーズ抽出。
**関連**: Domain 1 (Task 1.3), Domain 3 (Task 3.2)
> 出典: `../point/a.md` の「Amazon Comprehend」

### Amazon Macie
S3 上の機密データ（PII等）を ML で検出する監視サービス。データ漏洩リスクの可視化。
**関連**: Domain 3 (Task 3.2)

### Amazon Q Business
社内データ・業務システムに接続できるエンタープライズ生成 AI アシスタント。
**関連**: Domain 2 (Task 2.5)

### Amazon Q Developer
コード生成・補完・リファクタ支援用の AI アシスタント。`.amazonq` ディレクトリにコンテキストを置いて参照させる。
**関連**: Domain 2 (Task 2.5), Domain 4 (Task 4.3)
> 出典: `../point/exam/tech/a.md`「カスタム機能 / `.amazonq` / @workspace」

### Amazon Titan
AWS が提供する自社製 FM ファミリー（Text、Embeddings、Image など）。
**関連**: Domain 1 (Task 1.5)

## B

### Batch Inference（バッチ推論）
複数リクエストを一括処理するモード。リアルタイム不要なケースでコストを抑える。Bedrock の Batch Inference 機能あり。
**関連**: Domain 4 (Task 4.1, 4.2)

## C

### Chain-of-Thought（思考連鎖、CoT）
LLM に中間推論ステップを段階的に出力させてから最終解答を出させるプロンプト技法。
**関連**: Domain 1 (Task 1.6), Domain 2 (Task 2.1)

### Circuit Breaker（サーキットブレーカ）
依存サービスの障害時に呼び出しを遮断し、システム全体の連鎖障害を防ぐパターン。Step Functions / 自前実装で実現。
**関連**: Domain 1 (Task 1.2), Domain 2 (Task 2.4)

### Converse API
Amazon Bedrock のモデル横断統一インターフェース。InvokeModel と異なりモデル間差異を吸収し、ストリーミング・ツール使用にも対応。
**必要 IAM 権限**: `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`
**関連**: Domain 2 (Task 2.4)
> 出典: `../point/a.md` の「Converse API」

### Cross-Region Inference（クロスリージョン推論）
特定リージョンに限定された FM へのリクエストを他リージョン経由で実行することで、可用性とスループットを上げる仕組み。
**関連**: Domain 1 (Task 1.2)

## D

### Distillation（蒸留）
大きな教師モデルの出力を使って小さな生徒モデルを学習させ、精度を保ちながら小型化する手法。
**関連**: Domain 1 (Task 1.2)

### Drift（モデルドリフト）
入力分布や出力品質が時間経過とともに想定からずれていく現象。SageMaker Model Monitor / Bias Drift で検知。
**関連**: Domain 3 (Task 3.3), Domain 5 (Task 5.2)

## E

### Embedding（埋め込み）
テキスト・画像などを意味を保持する数値ベクトルに変換した表現。Titan Embeddings、Cohere Embed などが代表。
**関連**: Domain 1 (Task 1.4, 1.5)

## F

### Foundation Model（FM、基盤モデル）
大規模・汎用に事前学習されたモデル。LLM はその一種。Bedrock 上では Anthropic / Meta / Cohere / Amazon Titan / Mistral 等が選択可能。
**関連**: 全ドメイン

### Fine-tuning（ファインチューニング）
事前学習済み FM をタスク・ドメイン固有データで追加学習する手法。フル FT、LoRA、PEFT 等の選択肢がある。
**関連**: Domain 1 (Task 1.2)

## G

### Grounding（グラウンディング、接地）
LLM の応答を信頼できる参照ソース（ナレッジベース等）に紐づけることで、事実性・出典性を確保する考え方。
**関連**: Domain 3 (Task 3.4)

### Grounding Check（グラウンディングチェック）
Bedrock Guardrails の機能の一つ。応答が提示されたソースに基づいているかを検証し、根拠のない情報を「ungrounded」と判定する。
**関連**: Domain 3 (Task 3.1, 3.4)
> 出典: `../point/a.md` の「グラウンディングチェック」

## H

### Hallucination（ハルシネーション、幻覚）
LLM が事実無根の情報を自信を持って出力する現象。RAG とグラウンディングチェックで低減する。
**関連**: Domain 3 (Task 3.1), Domain 5 (Task 5.2)

### Human-in-the-Loop（HITL）
ML 推論やエージェント動作の途中で人間のレビュー・承認を挟むパターン。Amazon A2I、Step Functions の人間タスク等で実装。
**関連**: Domain 2 (Task 2.1), Domain 3 (Task 3.4)

## I

### InvokeModel API
Bedrock の従来型モデル呼び出し API。モデルごとにリクエスト/レスポンス形式が異なる。新規実装は Converse API 推奨。
**関連**: Domain 2 (Task 2.4)

### Intelligent Prompt Routing（インテリジェントプロンプトルーティング）
プロンプトの複雑さを自動分析し、安価な小型モデルと高性能モデルを動的に振り分ける Bedrock の機能。Lambda の LLM ルータパターンより低レイテンシ・低工数。
**関連**: Domain 4 (Task 4.1)
> 出典: `../point/exam/tech/a.md`「インテリジェントプロンプトルーティング」

## J

### Jailbreak（脱獄）
ガードレールやセーフティ指示を回避して禁止された出力を引き出す攻撃。プロンプトインジェクションの一形態。
**関連**: Domain 3 (Task 3.1)

## K

### Knowledge Base（ナレッジベース）
RAG で参照する文書集合。Bedrock Knowledge Bases では S3 から取り込み、ベクトル化、検索 API 提供までを一括管理。
**関連**: Domain 1 (Task 1.4, 1.5)

## L

### LLM-as-a-Judge
LLM 自身に他 LLM の出力を採点させる評価手法。コストを抑えつつ大量評価が可能。Bedrock Model Evaluation の選択肢の一つ。
**関連**: Domain 3 (Task 3.4), Domain 5 (Task 5.1)

### LoRA（Low-Rank Adaptation）
パラメータ効率的ファインチューニング（PEFT）手法の一種。フル FT より大幅に少ない計算コストで適応可能。
**関連**: Domain 1 (Task 1.2)

## M

### MCP（Model Context Protocol）
LLM とツール／データソースを標準化された方法で接続するプロトコル。MCP サーバ／クライアントで実装する。
**関連**: Domain 1 (Task 1.5), Domain 2 (Task 2.1)

### Model Card
モデルの目的、性能、制約、バイアス等を文書化したカード。SageMaker AI で programmatic に作成可能。
**関連**: Domain 3 (Task 3.3)

### Multimodal（マルチモーダル）
テキスト・画像・音声・動画など複数モダリティを扱う FM。Bedrock の Anthropic Claude や Amazon Nova が対応。
**関連**: Domain 1 (Task 1.3)

## P

### PEFT（Parameter-Efficient Fine-Tuning）
LoRA、Adapter、Prefix Tuning など、限定パラメータのみ学習することで効率化した FT 手法群。
**関連**: Domain 1 (Task 1.2)

### PII（Personally Identifiable Information）
個人を特定できる情報。氏名、メール、SSN 等。Comprehend PII / Macie / Bedrock Guardrails で検出・マスクする。
**関連**: Domain 3 (Task 3.2)

### Prompt Caching（プロンプトキャッシング）
共通のシステムプロンプトや長い文脈を再利用可能な形でキャッシュし、トークン課金とレイテンシを削減する仕組み。
**関連**: Domain 4 (Task 4.1)

### Prompt Engineering（プロンプトエンジニアリング）
LLM から望む出力を引き出すためのプロンプト設計。Few-shot、CoT、ロール指示、構造化出力指定など。
**関連**: Domain 1 (Task 1.6)

### Prompt Injection（プロンプトインジェクション）
ユーザー入力に悪意のある指示を埋め込んで LLM の挙動を奪う攻撃。Bedrock Guardrails や入力サニタイズで対策。
**関連**: Domain 3 (Task 3.1)

### Provisioned Throughput（プロビジョンドスループット）
Bedrock で特定 FM 専用の推論キャパシティを 1 分あたりの最大入出力トークンで予約する課金モデル。大量・高負荷向け。
**関連**: Domain 4 (Task 4.1, 4.2)
> 出典: `../point/exam/tech/a.md`「プロビジョンスループット」

## Q

### Quantization（量子化）
モデルの重みを低精度（INT8等）に変換し、推論速度・メモリ効率を改善する手法。エッジ推論で重要。
**関連**: Domain 4 (Task 4.2)

## R

### RAG（Retrieval-Augmented Generation、検索拡張生成）
外部知識ストアから関連文書を取得して LLM のプロンプトに付与し、最新情報や独自情報に基づいて生成させる手法。
**関連**: Domain 1 (Task 1.4, 1.5)

### ReAct パターン
Reasoning + Acting。LLM が「思考 → 行動（ツール呼び出し） → 観察 → 再思考」のループを回す手法。エージェントの基本形。
**関連**: Domain 2 (Task 2.1)

### Reranker
RAG の検索結果を再ランキングして関連度を高める仕組み。Bedrock のリランカモデルや Cohere Rerank が代表。
**関連**: Domain 1 (Task 1.5)

## S

### SageMaker AI
ML モデルの学習・デプロイ・管理基盤。FM ホスティング、JumpStart によるモデル取得、Model Registry によるバージョン管理に使う。
**関連**: Domain 1 (Task 1.2), Domain 2 (Task 2.2)

### SageMaker Clarify
モデルバイアス検出、特徴量寄与（SHAP）、ドリフト監視を提供。FM 評価の責任ある AI 観点で使う。
**関連**: Domain 3 (Task 3.4), Domain 5 (Task 5.1)

### SageMaker JumpStart
事前学習済み FM とソリューションテンプレートを 1-click で取得・デプロイできるカタログ機能。
**関連**: Domain 1 (Task 1.2)

### SageMaker Model Monitor
本番モデルの入力データ品質、モデル品質、バイアスドリフト、特徴量寄与ドリフトを継続監視。
**関連**: Domain 4 (Task 4.3), Domain 5 (Task 5.2)

### SageMaker Model Registry
モデルのバージョン管理、承認状態、リネージ、デプロイ承認ワークフローを管理。
**関連**: Domain 1 (Task 1.2), Domain 3 (Task 3.3)

### SageMaker Neo
モデルをハードウェア最適化された形式にコンパイルし、エッジデバイス（IoT）や軽量推論向けに変換するサービス。
**関連**: Domain 4 (Task 4.2)
> 出典: `../point/exam/tech/a.md`「SageMaker neo→軽量、ローカル LLM みたいな使い方」

### Semantic Caching（セマンティックキャッシング）
意味的に類似したプロンプトに対して過去の応答を再利用するキャッシング。完全一致でなく埋め込みベクトル類似度で判定。
**関連**: Domain 4 (Task 4.1)

### Streaming（ストリーミング）
モデル出力をトークン単位で逐次返却する方式。WebSocket/SSE と組み合わせてリアルタイム UX を実現。
**関連**: Domain 2 (Task 2.4)

### Strands Agents
AWS のエージェント構築フレームワーク。Bedrock Agents と並ぶ選択肢で、コードファーストでカスタム挙動を作れる。
**関連**: Domain 2 (Task 2.1)

## T

### Temperature（温度）
LLM のサンプリングランダム性を制御するパラメータ（0〜1+）。低いほど決定的、高いほど創造的。
**関連**: Domain 1 (Task 1.6), Domain 4 (Task 4.2)

### Token（トークン）
LLM が処理する基本単位。入力トークン数と出力トークン数で課金されるモデルが多い。
**関連**: Domain 4 (Task 4.1)

### Top-k サンプリング
生成時、確率上位 k 個の候補トークンに絞ってサンプリングする方式。`top-k=50` などと指定。
**関連**: Domain 1 (Task 1.6), Domain 4 (Task 4.2)
> 出典: `../point/a.md` の「top-k」（検索・分類・生成すべての文脈で使う上位k選択）

### Top-p（Nucleus）サンプリング
累積確率が p に達するまでの上位候補に絞ってサンプリング。Top-k より動的に候補数を変える。
**関連**: Domain 1 (Task 1.6)

## V

### Vector Database / Vector Store
埋め込みベクトルを格納し、類似度検索（kNN/ANN）を提供する DB。OpenSearch（k-NN）, Aurora pgvector, Bedrock Knowledge Bases。
**関連**: Domain 1 (Task 1.4)

## W

### Well-Architected Generative AI Lens
AWS Well-Architected Framework の生成 AI 向けレンズ。設計指針を 6 つの柱で提供。
**関連**: Domain 1 (Task 1.1)

## 帰属機能（き属、Attribution）
RAG の応答に「この情報はどのソースから来たか」を引用付きで示す機能。Knowledge Bases の RetrieveAndGenerate API は citations を返す。
**関連**: Domain 1 (Task 1.5), Domain 3 (Task 3.4)
> 出典: `../point/a.md` の「帰属機能」（メモは未記入だが文脈から RAG 引用機能を指す）

---

> **更新日**: 2026-05 / 公式ドキュメント・公式試験ガイドに基づく
