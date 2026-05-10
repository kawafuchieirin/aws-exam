# Domain 3: AI Safety, Security, and Governance（20%）

> **配点**: 20% ／ **タスク数**: 4 ／ **スキル数**: 15
> 出典: AWS 公式 AIP-C01 試験ガイド Content Domain 3

## 1. ドメイン概要

GenAI アプリの**安全性（Safety）／セキュリティ（Security）／ガバナンス（Governance）／責任ある AI（Responsible AI）**を一手に扱う。

主要トピック:
- 入出力安全制御（Task 3.1） … Bedrock Guardrails、プロンプトインジェクション対策
- データセキュリティ・プライバシー（Task 3.2） … VPC、IAM、Macie、PII 検出
- ガバナンス・コンプライアンス（Task 3.3） … モデルカード、データリネージ、CloudTrail
- 責任ある AI（Task 3.4） … 透明性、公平性、バイアス検査

学習優先度: **3.1 ≧ 3.2 > 3.4 > 3.3**。Guardrails と Comprehend / Macie が頻出。

---

## 2. Task 3.1: 入出力安全制御

### 2.1 何が問われるか

ユーザーの**有害入力**から FM を守り、FM の**有害出力**からユーザーを守る、双方向の安全制御。

### 2.2 公式スキル一覧

- **Skill 3.1.1**: 包括的なコンテンツ安全性（Bedrock Guardrails、Step Functions / Lambda のカスタムモデレーション、リアルタイムバリデーション）
- **Skill 3.1.2**: 有害出力の防止（Bedrock Guardrails、コンテンツモデレーション／毒性検出用 FM 評価、決定的結果のための text-to-SQL）
- **Skill 3.1.3**: ハルシネーション低減（Bedrock Knowledge Base のグラウンディング、信頼度スコア・意味類似度、JSON Schema 強制）
- **Skill 3.1.4**: 多層防御（Comprehend の前処理フィルタ、Bedrock のモデルベースガードレール、Lambda の後処理、API GW の応答フィルタ）
- **Skill 3.1.5**: 高度な脅威検知（プロンプトインジェクション・脱獄検知、入力サニタイズ、安全分類器、自動敵対テスト）

### 2.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Amazon Bedrock Guardrails** | 入出力フィルタの中心 |
| **Amazon Comprehend** | 前処理での PII / 毒性検出 |
| **AWS Lambda** | 後処理／カスタムロジック |
| **AWS Step Functions** | 多層モデレーションワークフロー |
| **Amazon API Gateway** | 応答フィルタ／レート制限 |
| **AWS WAF** | API 前段の入力フィルタ |
| **Amazon Bedrock Knowledge Bases** | グラウンディング |

### 2.4 Bedrock Guardrails の機能

| 機能 | 内容 |
|---|---|
| **Content Filters** | 性的、暴力、誹謗、不適切助言、悪用、誤情報の 6 カテゴリでブロック |
| **Topic Denial** | 自然言語でトピックを禁止指定 |
| **Word Filters** | 製品固有の禁止語 |
| **Sensitive Information Filter** | PII（28 種以上）と正規表現での検出・マスク |
| **Contextual Grounding Check** | 応答が提示ソースに基づくか／クエリに関連するかの自動検証 |

### 2.5 グラウンディングチェックの詳細

> **定義**: モデルレスポンスがソースに基づいて事実上正確であり、ソースに基づいているかどうかが確認される。レスポンスに追加された新しい情報は、根拠がないと見なされる。

「AI の回答が事実に基づいているかを保証するためのもの」と理解する。Knowledge Base の citations と組み合わせると強力。

> 出典: `../point/a.md`「グラウンディングチェック」（[公式ドキュメント](https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/guardrails-contextual-grounding-check.html)）

### 2.6 多層防御パターン

```
[ユーザー入力]
    ↓
[1. WAF / API GW でレート制限・サイズ制限]
    ↓
[2. Comprehend で前処理（PII 検出、感情）]
    ↓
[3. Bedrock Guardrails 入力フィルタ]
    ↓
[FM（Bedrock）]
    ↓
[4. Bedrock Guardrails 出力フィルタ＋ Grounding Check]
    ↓
[5. Lambda で後処理（JSON Schema 検証等）]
    ↓
[ユーザーへ応答]
```

各層で**異なる種類**の脅威を防ぐのがポイント。

### 2.7 ハルシネーション対策

| 手段 | 説明 |
|---|---|
| **RAG（Knowledge Bases）** | ソースに基づく回答 |
| **Grounding Check** | ソースとの整合性検証 |
| **Citations** | 出典明示で利用者が検証可能 |
| **JSON Schema 強制** | 構造化出力で逸脱を検出 |
| **温度を低く** | ランダム性を抑える |
| **Self-Consistency** | 複数生成で多数決 |

### 2.8 引っかけ

- 「PII を含む応答を避けたい」→ **Bedrock Guardrails の Sensitive Information Filter**
- 「事実と違う応答を抑止」→ **Knowledge Bases + Grounding Check**
- 「特定トピックに触れさせない」→ **Guardrails の Topic Denial**
- 「プロンプトインジェクション対策」→ **Guardrails + 入力サニタイズ + 監査**

### 2.9 Exam Tips

- **Guardrails は入力／出力の両方** に適用できる
- Grounding Check は Guardrails の機能の一つ。**KB と組合せで効果最大**
- 「決定的な結果」が要件なら **text-to-SQL** や JSON Schema 制約

### 2.10 チェックポイント
- [ ] Guardrails の 5 つの機能を挙げられる
- [ ] グラウンディングチェックが何を検証するか説明できる
- [ ] ハルシネーション対策を 4 つ以上挙げられる

---

## 3. Task 3.2: データセキュリティとプライバシー

### 3.1 何が問われるか

**機密データを FM 関連処理から守る**仕組み。VPC 隔離、IAM、PII 検出・マスク、データ保持ポリシー。

### 3.2 公式スキル一覧

- **Skill 3.2.1**: 保護された AI 環境（VPC エンドポイントでネットワーク隔離、IAM、AWS Lake Formation の細粒度アクセス、CloudWatch でアクセス監視）
- **Skill 3.2.2**: プライバシー保護（Comprehend と Macie で PII 検出、Bedrock のデータプライバシー機能、Bedrock Guardrails で出力フィルタ、S3 ライフサイクルでデータ保持）
- **Skill 3.2.3**: プライバシー重視 AI（データマスキング、Comprehend PII、匿名化、Bedrock Guardrails）

### 3.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **VPC Endpoint + AWS PrivateLink** | Bedrock を閉域接続 |
| **IAM / IAM Identity Center** | きめ細かい権限 |
| **AWS KMS** | 保存／転送暗号化 |
| **AWS Lake Formation** | データレイク権限管理 |
| **Amazon Macie** | S3 内 PII の検出 |
| **Amazon Comprehend（PII 検出）** | リアルタイム PII 検出 |
| **Amazon Bedrock Guardrails** | 応答内 PII マスク |
| **Amazon S3 Lifecycle** | データ保持ポリシー |
| **CloudWatch / CloudTrail** | アクセス監視・監査 |

### 3.4 PII 検出・マスクの選択肢

| サービス | 適用範囲 | 特徴 |
|---|---|---|
| **Amazon Comprehend** | リアルタイムテキスト | API でテキストごとに検出。日本語対応 |
| **Amazon Macie** | S3 オブジェクト | ML ベースで定期スキャン、可視化 |
| **Bedrock Guardrails Sensitive Info Filter** | プロンプト／応答 | FM 入出力で自動マスク |

### 3.5 ネットワーク隔離パターン

```
[VPC内 Lambda] → [VPC Endpoint (PrivateLink)] → [Bedrock]
                                                  ↑
                                          インターネットを通らない
```

`bedrock-runtime`, `bedrock-agent-runtime` などの VPC エンドポイントが提供されている。

### 3.6 Bedrock のデータ取扱

- **モデル学習に使用されない**: Bedrock 経由のプロンプト／応答は AWS のモデル改善に使われない
- **顧客 KMS 鍵**: カスタムモデル（FT 後）は CMK で暗号化可能
- **ログ取得**: Model Invocation Logs を S3 / CloudWatch に保存（オプション）

### 3.7 引っかけ

- 「S3 内の PII を継続監視」→ **Macie**
- 「リアルタイムテキストでの PII 検出」→ **Comprehend**
- 「FM の応答から PII を消す」→ **Bedrock Guardrails Sensitive Info Filter**
- 「Bedrock を閉域で使う」→ **VPC Endpoint + PrivateLink**
- 「データレイクで列単位の権限制御」→ **Lake Formation**

### 3.8 Comprehend の特徴

> **Amazon Comprehend** は AWS が提供する自然言語処理 (NLP) サービスで、機械学習を活用してテキストからインサイトを抽出。キーフレーズ抽出、感情分析、エンティティ抽出、PII 検出、トピックモデリング、言語識別。日本語対応。拡張サービス **Amazon Comprehend Medical** は医療文書解析に特化。

> 出典: `../point/a.md`「Amazon Comprehend」

### 3.9 Exam Tips

- **Macie と Comprehend の使い分け**: Macie は S3 の保管データ、Comprehend はリアルタイム
- VPC Endpoint は Bedrock の閉域必須要件で頻出
- KMS の `aws:KMS` 条件キーで「特定鍵で暗号化されたデータのみ Bedrock で使える」制御も可

### 3.10 チェックポイント
- [ ] Macie と Comprehend の使い分けを説明できる
- [ ] Bedrock を VPC 閉域で使う構成を描ける
- [ ] Bedrock のプロンプトデータが学習に使われないことを言える

---

## 4. Task 3.3: AI ガバナンス・コンプライアンス

### 4.1 何が問われるか

**規制対応・組織ポリシー遵守の仕組み**。モデルカード、データリネージ、監査ログ、ドリフト監視。

### 4.2 公式スキル一覧

- **Skill 3.3.1**: コンプライアンスフレームワーク（SageMaker のプログラマティックモデルカード、Glue のデータリネージ自動追跡、メタデータタグ、CloudWatch Logs の決定ログ）
- **Skill 3.3.2**: データソース追跡（Glue Data Catalog でのデータソース登録、メタデータタグでの出典帰属、CloudTrail の監査）
- **Skill 3.3.3**: 組織ガバナンス（組織ポリシー・規制要件・責任ある AI 原則と整合する包括フレームワーク）
- **Skill 3.3.4**: 継続監視と高度ガバナンス（誤用・ドリフト・ポリシー違反の自動検知、バイアスドリフト監視、自動アラート、トークン単位リダクション、応答ログ、AI 出力ポリシーフィルタ）

### 4.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **SageMaker AI（Model Cards）** | モデル文書化 |
| **AWS Glue Data Catalog** | データリネージ・カタログ |
| **AWS CloudTrail** | API 監査ログ |
| **Amazon CloudWatch Logs** | アプリログ |
| **Amazon Bedrock Model Invocation Logs** | プロンプト・応答ログ |
| **SageMaker Model Monitor** | ドリフト監視 |
| **SageMaker Clarify** | バイアス・公平性 |
| **Amazon Macie** | データ分類監査 |

### 4.4 モデルカード（Model Card）

モデルの**目的、性能、制約、想定用途、トレーニングデータ、バイアス**を文書化したカード。SageMaker AI で **programmatic に作成・更新可能**。

含めるべき項目:
- モデルの目的と想定ユースケース
- 想定外の用途（Out of scope）
- 訓練データの出所と前処理
- 評価メトリクスとデータセット
- 既知のバイアスと制約
- 倫理的考慮

### 4.5 データリネージ

データの**出所と変換履歴**を追跡。RAG では「**この応答はどの文書から派生したか**」を示せることが重要。
- **Glue Data Catalog**: データソース・スキーマ・タグの中央管理
- **Glue Data Lineage**: 自動的なリネージグラフ生成
- **メタデータタグ**: ベクトル DB に source_uri / created_at / author 等を持たせる

### 4.6 監査ログ

| ログ | 取得先 | 用途 |
|---|---|---|
| **CloudTrail** | AWS API 呼び出し | 「誰が」Bedrock を呼んだか |
| **Bedrock Model Invocation Logs** | プロンプト・応答全文 | 内容の事後監査 |
| **CloudWatch Logs** | アプリログ | アプリ層の動作 |

Model Invocation Logs は明示的に有効化が必要（S3 / CloudWatch に出力）。

### 4.7 継続監視

- **バイアスドリフト**: SageMaker Clarify + Model Monitor
- **品質ドリフト**: Model Monitor のデータ品質／モデル品質メトリクス
- **誤用検知**: 異常なトークン使用パターン → CloudWatch Anomaly Detection
- **ポリシー違反**: Guardrails のブロック率を CloudWatch メトリクス化

### 4.8 引っかけ

- 「モデルの責任性を文書化」→ **SageMaker Model Cards**
- 「誰がいつ Bedrock を呼んだか」→ **CloudTrail**
- 「プロンプト内容の監査」→ **Bedrock Model Invocation Logs**
- 「データソースの自動カタログ化」→ **Glue Data Catalog**
- 「バイアスの継続監視」→ **SageMaker Clarify + Model Monitor**

### 4.9 Exam Tips

- 「**API レベルの監査 = CloudTrail**」「**コンテンツレベルの監査 = Model Invocation Logs**」と覚える
- Model Card は **programmatic API** で更新可能（CI/CD 統合可）
- データリネージは Glue Data Catalog が中心

### 4.10 チェックポイント
- [ ] CloudTrail と Bedrock Model Invocation Logs の役割の違いを言える
- [ ] Model Card に含める項目を 4 つ以上挙げられる
- [ ] バイアスドリフト検知のサービス組み合わせを述べられる

---

## 5. Task 3.4: 責任ある AI 原則の実装

### 5.1 何が問われるか

**AWS の Responsible AI（責任ある AI）原則**: 透明性、公平性、安全性、プライバシー、説明責任の実装。

### 5.2 公式スキル一覧

- **Skill 3.4.1**: 透明な AI（推論ディスプレイ、CloudWatch の信頼度メトリクス、出典提示、Bedrock エージェントトレース）
- **Skill 3.4.2**: 公平性評価（CloudWatch の公平性メトリクス、Bedrock Prompt Management / Prompt Flows での A/B テスト、Bedrock LLM-as-a-Judge による自動評価）
- **Skill 3.4.3**: ポリシー準拠 AI（Bedrock Guardrails の組織ポリシー化、モデルカードでの制約文書化、Lambda の自動コンプライアンスチェック）

### 5.3 AWS Responsible AI の柱

AWS が公表している責任ある AI の柱:
1. **Fairness（公平性）**
2. **Explainability（説明可能性）**
3. **Privacy & Security**
4. **Robustness（堅牢性）**
5. **Governance（ガバナンス）**
6. **Transparency（透明性）**
7. **Veracity & Robustness（真実性）**
8. **Controllability（制御可能性）**

### 5.4 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Amazon Bedrock Guardrails** | ポリシー強制 |
| **Bedrock Model Evaluation** | 自動・人手評価 |
| **SageMaker Clarify** | バイアス検出・説明可能性（SHAP） |
| **Amazon A2I** | 人間レビュー |
| **Bedrock Agent Tracing** | 推論経路の透明化 |
| **CloudWatch** | 公平性・信頼度メトリクス |

### 5.5 透明性の実装パターン

| 機能 | 実装 |
|---|---|
| **理由の表示** | CoT で中間推論を出させて表示 |
| **出典の表示** | Knowledge Base の citations（**帰属機能**） |
| **信頼度** | 出力に確率／スコアを付与、CloudWatch で可視化 |
| **エージェントの行動履歴** | Bedrock Agent Tracing で各ステップを可視化 |

### 5.6 公平性評価

- **A/B テスト**: 同じプロンプトで異なるモデル／プロンプトを比較
- **LLM-as-a-Judge**: 別 LLM に採点させる（Bedrock Model Evaluation でサポート）
- **属性別パフォーマンス**: 性別・年齢・人種など保護属性ごとに精度・偽陽性率を比較

### 5.7 引っかけ

- 「エージェントの推論をデバッグ」→ **Bedrock Agent Tracing**
- 「出典付きで応答」→ **Knowledge Bases citations（帰属機能）**
- 「LLM 出力を別 LLM で採点」→ **LLM-as-a-Judge / Bedrock Model Evaluation**
- 「保護属性のバイアス検出」→ **SageMaker Clarify**

### 5.8 Exam Tips

- 「**透明性 = citations + tracing**」と覚える
- LLM-as-a-Judge は新しめだが頻出。**Bedrock Model Evaluation** で扱える
- Clarify は ML 全般向けだが、**FM のバイアス検査でも使える**

### 5.9 チェックポイント
- [ ] AWS Responsible AI の柱を 5 つ以上挙げられる
- [ ] 透明性を実現する 4 つの実装手段を言える
- [ ] LLM-as-a-Judge がどんなシナリオで有効か述べられる

---

## 6. このドメインで主に出てくる AWS サービス一覧

| サービス | 主な用途 | 関連タスク |
|---|---|---|
| Amazon Bedrock Guardrails | 入出力フィルタ | 3.1, 3.2, 3.4 |
| Amazon Bedrock Knowledge Bases | グラウンディング | 3.1 |
| Amazon Bedrock Model Evaluation | 公平性評価 | 3.4 |
| Amazon Bedrock Agent Tracing | 推論経路可視化 | 3.4 |
| Amazon Bedrock Model Invocation Logs | プロンプト監査 | 3.3 |
| Amazon Comprehend | リアルタイム PII | 3.1, 3.2 |
| Amazon Macie | S3 PII 監査 | 3.2 |
| AWS WAF | API 入力フィルタ | 3.1 |
| AWS PrivateLink / VPC Endpoint | 閉域接続 | 3.2 |
| AWS KMS | 暗号化 | 3.2 |
| AWS Lake Formation | データレイク権限 | 3.2 |
| IAM / Identity Center | きめ細かい権限 | 3.2 |
| Amazon S3 Lifecycle | データ保持 | 3.2 |
| AWS CloudTrail | API 監査 | 3.3 |
| Amazon CloudWatch Logs | 決定ログ | 3.3 |
| AWS Glue Data Catalog | データリネージ | 3.3 |
| SageMaker Model Cards | モデル文書化 | 3.3 |
| SageMaker Model Monitor | ドリフト監視 | 3.3 |
| SageMaker Clarify | バイアス・SHAP | 3.4 |
| Amazon Augmented AI | HITL | 3.4 |

---

## 7. ドメイン横断キーワード

- **Guardrails**: 6 種コンテンツフィルタ、PII フィルタ、トピック禁止、グラウンディングチェック
- **Grounding Check**: ソースへの整合性検証
- **帰属機能（citations）**: 出典付き応答
- **PII 検出**: Comprehend（リアルタイム）／Macie（S3）／Guardrails（FM 入出力）
- **VPC Endpoint + PrivateLink**: 閉域 Bedrock
- **Model Card**: モデル責任性ドキュメント
- **CloudTrail vs Model Invocation Logs**: API 監査 vs コンテンツ監査
- **LLM-as-a-Judge**: LLM による LLM 評価
- **Responsible AI 8 柱**: Fairness / Explainability / Privacy / Robustness / Governance / Transparency / Veracity / Controllability

---

## 8. 参考リンク

- [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Bedrock Contextual Grounding Check](https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/guardrails-contextual-grounding-check.html)
- [Bedrock Model Invocation Logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)
- [SageMaker Model Cards](https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html)
- [SageMaker Clarify for FM Evaluation](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-foundation-model-evaluate.html)
- [AWS Responsible AI](https://aws.amazon.com/jp/machine-learning/responsible-ai/)
- [東海ソフト: Comprehend 概要](https://www.cloudsolution.tokai-com.co.jp/white-paper/2024/1213-532.html)

---

## 9. 既存メモからの取り込み出典

- `../point/a.md`: Amazon Comprehend（→ 3 章）、グラウンディングチェック（→ 2 章）、帰属機能（→ 5 章）
