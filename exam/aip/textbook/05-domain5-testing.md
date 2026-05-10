# Domain 5: Testing, Validation, and Troubleshooting（11%）

> **配点**: 11% ／ **タスク数**: 2 ／ **スキル数**: 14
> 出典: AWS 公式 AIP-C01 試験ガイド Content Domain 5

## 1. ドメイン概要

GenAI アプリの**評価（Evaluation）**と**トラブルシュート（Troubleshooting）**を扱う最終ドメイン。

主要トピック:
- 評価システム（Task 5.1） … Bedrock Model Evaluation、A/B テスト、LLM-as-a-Judge、RAG 評価
- トラブルシュート（Task 5.2） … コンテキスト超過、API 統合、プロンプト改善、検索系問題

学習優先度: **5.1 ≧ 5.2**。Bedrock Model Evaluation と RAG 評価指標が頻出。

---

## 2. Task 5.1: GenAI 評価システム

### 2.1 何が問われるか

**FM 出力の品質を、従来の ML を超えた多面的指標で評価する仕組み**。自動評価、人手評価、A/B テスト、LLM-as-a-Judge、RAG 専用評価。

### 2.2 公式スキル一覧

- **Skill 5.1.1**: 包括評価フレームワーク（関連性、事実正確性、一貫性、流暢性のメトリクス）
- **Skill 5.1.2**: 系統的モデル評価（Bedrock Model Evaluations、A/B テスト、カナリアテスト、マルチモデル評価、コスト性能分析、トークン効率、品質と遅延の比、ビジネス成果）
- **Skill 5.1.3**: ユーザー中心評価（フィードバック UI、評価システム、アノテーションワークフロー）
- **Skill 5.1.4**: 系統的品質保証（継続評価、回帰テスト、自動品質ゲート）
- **Skill 5.1.5**: 多面的評価（RAG 評価、LLM-as-a-Judge、人間フィードバック収集）
- **Skill 5.1.6**: 検索品質テスト（関連性スコア、コンテキスト整合性、検索遅延）
- **Skill 5.1.7**: エージェント性能（タスク完了率、ツール使用効果、Bedrock Agent 評価、推論品質）
- **Skill 5.1.8**: レポーティング（可視化、自動レポート、モデル比較可視化）
- **Skill 5.1.9**: デプロイ検証（合成ユーザワークフロー、AI 固有出力検証、ハルシネーション率、意味ドリフト、自動品質チェック）

### 2.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Amazon Bedrock Model Evaluation** | 自動／人手評価のマネージドサービス |
| **Amazon Bedrock Agent Evaluation** | エージェント特化評価 |
| **SageMaker Clarify** | バイアス・公平性 |
| **Amazon A2I** | 人間レビュー |
| **AWS Step Functions** | 評価ワークフロー |
| **CloudWatch Synthetics** | 合成ユーザワークフロー |
| **Amazon QuickSight / Managed Grafana** | 可視化 |

### 2.4 Bedrock Model Evaluation

評価ジョブの 2 種類:
| 種類 | 説明 |
|---|---|
| **Automatic** | 組込メトリクスで自動評価 |
| **Human（Bring-your-own / Managed）** | 人手評価 |

組込タスクと推奨メトリクス:
| タスク | 自動メトリクス |
|---|---|
| **General Text Generation** | Robustness, Toxicity, Accuracy |
| **Summarization** | ROUGE, BERTScore, BLEU |
| **Question Answering** | F1, Accuracy, BERTScore |
| **Text Classification** | Accuracy, Precision/Recall, F1 |
| **Custom** | LLM-as-a-Judge も選択可 |

### 2.5 LLM-as-a-Judge

別の LLM に出力を採点させる手法。
- **メリット**: 大量評価が低コスト、24/7 稼働
- **デメリット**: 採点 LLM 自体のバイアス、長文評価の限界
- **Bedrock Model Evaluation で標準サポート**

評価軸の例: 関連性 / 正確性 / 一貫性 / 流暢性 / 安全性 / 文脈整合性

### 2.6 RAG 評価

RAG は「検索」と「生成」の 2 段構造のため**両方を別々に評価**する必要がある。

#### 検索（Retrieval）評価
| メトリクス | 説明 |
|---|---|
| **Recall@K** | 関連文書のうち上位 K に含まれた割合 |
| **Precision@K** | 上位 K のうち関連文書の割合 |
| **Mean Reciprocal Rank（MRR）** | 関連文書が出る順位の逆数の平均 |
| **NDCG** | ランキング品質（順序を考慮） |
| **Context Relevance** | 取得チャンクの質問関連度（LLM 採点） |

#### 生成（Generation）評価
| メトリクス | 説明 |
|---|---|
| **Faithfulness** | 応答が取得文脈に忠実か（ハルシネーション低減指標） |
| **Answer Relevance** | 応答が質問に答えているか |
| **Context Precision** | 取得文脈の必要部分の割合 |

これらは Bedrock Model Evaluation の RAG 評価モードで自動計算可能。

### 2.7 エージェント評価

| メトリクス | 説明 |
|---|---|
| **Task Completion Rate** | タスクを最後まで完了した率 |
| **Tool Selection Accuracy** | 適切なツールを選んだ率 |
| **Tool Call Success Rate** | ツール呼び出しが正常終了した率 |
| **Steps to Completion** | 完了までのステップ数（少ないほど良い） |
| **Reasoning Quality** | CoT の論理性 |

Bedrock Agent Evaluation でこれらを自動計測できる。

### 2.8 デプロイ検証

新モデル／プロンプト適用時のリスク検出:
- **シャドーテスト**: 旧モデルに本番トラフィック、新モデルにも並列で送って比較
- **カナリアデプロイ**: 一部トラフィックのみ新モデルへ
- **A/B テスト**: 利用者を 2 群に分け、KPI で比較
- **回帰テスト**: ゴールデンデータセットでの自動チェック
- **意味ドリフト検知**: 過去応答と新応答の埋め込み距離を継続計測

### 2.9 引っかけ

- 「LLM 出力を別 LLM で採点」→ **LLM-as-a-Judge**
- 「RAG の検索精度」→ **Recall@K / Precision@K / MRR**
- 「RAG の応答忠実性」→ **Faithfulness**
- 「エージェントの完了率」→ **Bedrock Agent Evaluation の Task Completion Rate**
- 「定期的な品質劣化検知」→ **CloudWatch Synthetics + ゴールデンデータセット**

### 2.10 Exam Tips

- **RAG 評価は 2 軸（検索／生成）** で考える
- ROUGE / BLEU は **要約 / 翻訳** で従来から使われる。FM でも残っている
- **Faithfulness ≒ ハルシネーション抑制指標** と覚える

### 2.11 チェックポイント
- [ ] Bedrock Model Evaluation の 2 種類（Automatic / Human）を区別できる
- [ ] RAG の検索評価指標を 3 つ挙げられる
- [ ] エージェント評価メトリクスを 3 つ挙げられる
- [ ] LLM-as-a-Judge のメリット・デメリットを言える

---

## 3. Task 5.2: GenAI アプリのトラブルシュート

### 3.1 何が問われるか

**実運用で発生する問題の切り分けと修正**。コンテキスト超過、API 統合、プロンプト不調、検索系問題、プロンプトメンテナンス。

### 3.2 公式スキル一覧

- **Skill 5.2.1**: コンテンツ処理問題（コンテキストウィンドウ超過診断、動的チャンキング、プロンプト設計最適化、トランケーションエラー分析）
- **Skill 5.2.2**: FM 統合問題（エラーログ、リクエスト検証、応答分析）
- **Skill 5.2.3**: プロンプトエンジニアリング問題（プロンプトテストフレームワーク、版比較、系統的改善）
- **Skill 5.2.4**: 検索系問題（応答関連性分析、埋め込み品質診断、ドリフト監視、ベクトル化問題、チャンキング・前処理修正、ベクトル検索性能最適化）
- **Skill 5.2.5**: プロンプトメンテナンス（テンプレートテスト・CloudWatch Logs でのプロンプト混乱診断、X-Ray でプロンプト可観測性、スキーマ検証、系統的プロンプト精緻化）

### 3.3 トラブルパターン別 切り分け

#### 3.3.1 コンテキストウィンドウ超過

**症状**: `ValidationException: input length exceeds context window` 等。
**対処**:
- プロンプト圧縮（要約・関連部分のみ）
- 動的チャンキング（入力に応じて分割サイズ変更）
- より大きなコンテキスト長のモデルへ切替
- Prompt Caching で固定部分のトークン削減
- 出力 max_tokens の調整

#### 3.3.2 ハルシネーション

**症状**: 事実と異なる応答。
**対処**:
- RAG（Knowledge Bases）でグラウンディング
- Grounding Check で事後検証
- citations を出力に含めて利用者に検証可能化
- Temperature を下げる
- システムプロンプトで「知らない時は知らないと答えよ」を明示

#### 3.3.3 応答品質の劣化（ドリフト）

**症状**: 数週間後に同じ入力で異なる／劣化した応答。
**対処**:
- ゴールデンデータセットで継続評価
- モデルバージョンの確認（プロバイダ側で更新があった可能性）
- 埋め込みモデルの変更があれば再ベクトル化
- プロンプトテンプレート版管理（Prompt Management）

#### 3.3.4 検索の関連性低下

**症状**: RAG で関連薄い文書が上位。
**対処**:
- チャンクサイズ／オーバーラップ見直し
- 埋め込みモデル変更（Titan v1 → v2 等）
- ハイブリッド検索（BM25＋ベクトル）の導入
- リランカ追加
- メタデータフィルタの見直し

#### 3.3.5 API スロットル

**症状**: `ThrottlingException`。
**対処**:
- 指数バックオフリトライ（SDK デフォルト）
- Provisioned Throughput への移行
- Cross-Region Inference でリージョン分散
- リクエストのバッチ化

#### 3.3.6 エージェントの暴走

**症状**: ループ、無関係なツール呼び出し。
**対処**:
- Bedrock Agent Tracing で各ステップ確認
- 最大ステップ数制限
- ツール定義（OpenAPI スキーマ）の明確化
- ガードレール強化

### 3.4 観測ツールの選び方

| 状況 | ツール |
|---|---|
| **API 呼出元の追跡** | CloudTrail |
| **アプリログ詳細分析** | CloudWatch Logs Insights |
| **プロンプト・応答の事後監査** | Bedrock Model Invocation Logs |
| **複数サービスにまたがる遅延** | AWS X-Ray |
| **エージェントの推論経路** | Bedrock Agent Tracing |
| **GenAI 固有のエラーパターン** | Q Developer の支援 |

### 3.5 プロンプト改善の系統的アプローチ

1. **失敗事例を収集**: ユーザーフィードバック / Logs Insights から
2. **テストケース化**: ゴールデンデータセットへ追加
3. **テンプレート版を作成**: Prompt Management で `experimental` バージョン
4. **A/B 比較**: 旧版 vs 新版で評価メトリクス比較
5. **昇格**: `staging` → `production`（承認ワークフロー）
6. **回帰防止**: 全バージョンで定期テスト実行

### 3.6 引っかけ

- 「コンテキスト超過」→ **プロンプト圧縮 / 動的チャンキング / 大コンテキストモデル**
- 「事実誤りが頻発」→ **RAG + Grounding Check**
- 「埋め込みモデルを変えたら検索精度が変わった」→ **再ベクトル化が必要**
- 「ThrottlingException」→ **指数バックオフ / Provisioned Throughput**
- 「プロンプトの改善履歴を残す」→ **Prompt Management の版管理**

### 3.7 Exam Tips

- 「**症状 → 根本原因 → 対処サービス**」の三段論法で問われる
- ハルシネーション対策は **RAG + Grounding Check + 出典 + 低 Temperature** の組合せ
- プロンプト改善は属人化させず、**Prompt Management で版管理**

### 3.8 チェックポイント
- [ ] コンテキスト超過の対処を 3 つ挙げられる
- [ ] ハルシネーション対策を 4 つ挙げられる
- [ ] 観測ツールの使い分け（CloudTrail / Model Invocation Logs / X-Ray）を即答できる

---

## 4. このドメインで主に出てくる AWS サービス一覧

| サービス | 主な用途 | 関連タスク |
|---|---|---|
| Amazon Bedrock Model Evaluation | FM 評価 | 5.1 |
| Amazon Bedrock Agent Evaluation | エージェント評価 | 5.1 |
| Amazon Bedrock Knowledge Bases | RAG（評価対象） | 5.1, 5.2 |
| Amazon Bedrock Prompt Management | プロンプト版管理・改善 | 5.2 |
| Amazon Bedrock Guardrails | Grounding Check | 5.2 |
| SageMaker Clarify | バイアス検出 | 5.1 |
| Amazon A2I | 人間レビュー | 5.1 |
| AWS Step Functions | 評価ワークフロー | 5.1 |
| AWS CloudWatch Synthetics | 合成ユーザテスト | 5.1 |
| Amazon QuickSight / Managed Grafana | 可視化 | 5.1 |
| Amazon CloudWatch Logs Insights | ログ分析 | 5.2 |
| AWS X-Ray | 分散トレース | 5.2 |
| Bedrock Model Invocation Logs | プロンプト監査 | 5.2 |
| Amazon Q Developer | エラーパターン認識支援 | 5.2 |

---

## 5. ドメイン横断キーワード

- **LLM-as-a-Judge**: LLM が LLM を採点
- **Recall@K / Precision@K / MRR / NDCG**: 検索評価指標
- **Faithfulness / Answer Relevance / Context Precision**: 生成評価指標
- **ROUGE / BERTScore / BLEU**: 要約・翻訳の自動指標
- **Task Completion Rate / Tool Selection Accuracy**: エージェント指標
- **シャドー / カナリア / A/B**: デプロイ検証パターン
- **ゴールデンデータセット**: 回帰テストの基盤
- **意味ドリフト**: 応答の埋め込み距離変化

---

## 6. 参考リンク

- [Amazon Bedrock Model Evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html)
- [Bedrock RAG Evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/rag-evaluation.html)
- [Bedrock Agent Evaluation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-evaluation.html)
- [SageMaker Clarify for FM](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-foundation-model-evaluate.html)
- [CloudWatch Synthetics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html)
- [Amazon Augmented AI（A2I）](https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html)

---

## 7. 既存メモからの取り込み出典

- `../point/exam/tech/正答.md`: 弱点問題番号（21,22,23,26,27,31,34,36,39,40,41,50）→ 演習側の進捗管理ファイルとして保持
- このドメインの「症状 → 対処」表は実機問題演習の補助として活用可能
