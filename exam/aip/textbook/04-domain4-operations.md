# Domain 4: Operational Efficiency and Optimization for GenAI Applications（12%）

> **配点**: 12% ／ **タスク数**: 3 ／ **スキル数**: 16
> 出典: AWS 公式 AIP-C01 試験ガイド Content Domain 4

## 1. ドメイン概要

GenAI アプリの**コスト最適化、性能最適化、可観測性**を扱う。出題比は 12% と相対的に小さいが、**Bedrock の課金モデルとパフォーマンスチューニング**は実務直結で頻出パターンが明確。

主要トピック:
- コスト最適化（Task 4.1） … トークン削減、Provisioned Throughput、IPR、キャッシング
- パフォーマンス最適化（Task 4.2） … レイテンシ、スループット、SageMaker Neo、temperature/top-k
- 監視（Task 4.3） … CloudWatch、X-Ray、Model Invocation Logs

学習優先度: **4.1 ≧ 4.2 > 4.3**。Provisioned Throughput と Intelligent Prompt Routing は確実に押さえる。

---

## 2. Task 4.1: コスト最適化・リソース効率化

### 2.1 何が問われるか

**FM のトークン課金を抑える**ための具体的手段。プロンプト圧縮、モデル選択、キャパシティ予約、キャッシング。

### 2.2 公式スキル一覧

- **Skill 4.1.1**: トークン効率（トークン推定・追跡、コンテキストウィンドウ最適化、応答サイズ制御、プロンプト圧縮、コンテキストプルーニング、応答制限）
- **Skill 4.1.2**: コスト効率モデル選定（コスト・能力トレードオフ、クエリ複雑さに応じた階層化 FM 利用、推論コストと品質のバランス、価格対性能比、効率的な推論パターン）
- **Skill 4.1.3**: 高性能 FM システム（バッチ戦略、キャパシティ計画、利用率監視、Auto Scaling、Provisioned Throughput 最適化）
- **Skill 4.1.4**: 知的キャッシング（セマンティックキャッシング、結果フィンガープリント、エッジキャッシング、決定的リクエストハッシング、プロンプトキャッシング）

### 2.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Amazon Bedrock Provisioned Throughput** | 専用キャパ予約 |
| **Bedrock Intelligent Prompt Routing** | 自動モデル振り分け |
| **Bedrock Prompt Caching** | プロンプトキャッシュ |
| **Bedrock Batch Inference** | バッチ処理割引 |
| **Amazon ElastiCache** | セマンティックキャッシュ実装 |
| **Amazon CloudFront** | エッジキャッシング |
| **AWS Cost Explorer / Anomaly Detection** | コスト分析 |
| **CloudWatch** | トークン使用量監視 |

### 2.4 Bedrock の課金モデル

| 課金 | 特徴 | 用途 |
|---|---|---|
| **オンデマンド** | 入出力トークン × 単価 | 不定期ワークロード |
| **Provisioned Throughput** | 1 分あたり最大入出力トークンで予約 | 高負荷・予測可能 |
| **Batch Inference** | オンデマンドの **50% 引き** | バッチ処理（リアルタイム不要） |

#### Provisioned Throughput の詳細
> **Amazon Bedrock のプロビジョンスループットは、特定の基盤モデル専用の推論キャパシティを確保する。1 分あたりの最高入出力トークンで定義。大量のリクエストでも安心。**

**契約単位**: モデル単位（1 ヶ月 / 6 ヶ月コミットメント）。
**選定基準**: 大量・予測可能トラフィック、低レイテンシ要件、Bedrock 標準のスロットルを超えたい場合。

> 出典: `../point/exam/tech/a.md`「プロビジョンスループットは特定基盤モデル専用の推論キャパシティを確保する。1 分あたりの最高入出力トークンで定義。大量のリクエストでも安心」

### 2.5 Intelligent Prompt Routing（IPR）

**プロンプトの複雑さを Bedrock 自身が分析し、安価な小型モデルと高性能モデルを自動振り分け** する機能。
- 単純なクエリ → Haiku 等の軽量モデル
- 複雑なクエリ → Sonnet / Opus 等の高性能モデル
- **同一プロバイダー内** での切替が基本（Anthropic family 内、Meta family 内）

#### Lambda での自前実装との比較

| 項目 | Bedrock IPR | Lambda の LLM ルータ |
|---|---|---|
| 実装工数 | マネージド（ほぼ 0） | 高い |
| レイテンシ | 低い | 追加 1 ホップ |
| ルーティングロジック | AWS 管理 | カスタム可能 |
| マルチプロバイダ対応 | 限定的 | 自由 |

**結論**: 標準的な要件は IPR、特殊要件のみ Lambda 自前。

> 出典: `../point/exam/tech/a.md`「インテリジェントプロンプトルーティング = プロンプトの複雑さを自動で分析して、使用するモデルを振り分ける。Lambda でも同様のこと（LLM ルータパターン）はできるが実装の工数が多い、レイテンシもかかる」

### 2.6 トークン削減テクニック

| 手法 | 説明 |
|---|---|
| **コンテキスト圧縮** | 過去の対話を要約して短縮 |
| **コンテキストプルーニング** | 関連の薄い文書をフィルタ |
| **応答 max_tokens 制限** | 出力の上限設定 |
| **Few-shot 例数の最適化** | 効果のない例は削除 |
| **チャンクサイズ最適化** | RAG の取得件数・サイズを調整 |
| **プロンプトキャッシング** | 共通システムプロンプトをキャッシュ化 |
| **セマンティックキャッシング** | 類似クエリへ過去応答を再利用 |

### 2.7 キャッシング戦略

| キャッシュ層 | 実装 | 効果 |
|---|---|---|
| **クライアント側** | ブラウザ／アプリ | 同一ユーザの再質問 |
| **エッジ** | CloudFront | 地理的近接 |
| **アプリ層** | ElastiCache（Redis） | サーバ側共通キャッシュ |
| **プロンプト層** | Bedrock Prompt Caching | 共通プレフィックスのトークン削減 |
| **意味層** | セマンティックキャッシュ | 類似クエリ |

### 2.8 引っかけ

- 「予測可能な高負荷をコスト効率良く」→ **Provisioned Throughput**
- 「夜間バッチで大量処理を半額で」→ **Batch Inference**
- 「単純な質問を安いモデルへ自動回す」→ **Bedrock Intelligent Prompt Routing**
- 「同じシステムプロンプトを毎回送る」→ **Prompt Caching**
- 「文言違いだけど同じ意味の質問」→ **セマンティックキャッシング**

### 2.9 Exam Tips

- **オンデマンド vs Provisioned vs Batch** の 3 課金モデルを覚える
- 「**実装工数が低く、レイテンシも低い** 自動ルーティング」→ IPR
- セマンティックキャッシングは「**意味類似度（埋め込みベクトル比較）** で再利用」と言える

### 2.10 チェックポイント
- [ ] Bedrock の 3 課金モデルを言える
- [ ] IPR と自前 Lambda ルータの比較ができる
- [ ] キャッシング 5 階層を挙げられる

---

## 3. Task 4.2: アプリケーションパフォーマンス最適化

### 3.1 何が問われるか

**レイテンシ・スループット・コストのトレードオフ**を最適点で取る技術。

### 3.2 公式スキル一覧

- **Skill 4.2.1**: 応答性の高い AI（事前計算、レイテンシ最適化 Bedrock モデル、並列リクエスト、ストリーミング応答、性能ベンチマーク）
- **Skill 4.2.2**: 検索性能（インデックス最適化、クエリ前処理、ハイブリッド検索のカスタムスコアリング）
- **Skill 4.2.3**: FM スループット最適化（トークン処理最適化、バッチ推論、並行モデル呼び出し管理）
- **Skill 4.2.4**: FM 性能改善（モデル固有パラメータ、A/B テスト、要件に応じた temperature・top-k/top-p 選定）
- **Skill 4.2.5**: FM 用リソース割当（トークン処理向けキャパ計画、利用率監視、Auto Scaling）
- **Skill 4.2.6**: FM システム性能（API 呼び出しプロファイリング、ベクトル DB クエリ最適化、LLM 推論固有のレイテンシ削減）

### 3.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Bedrock Latency-Optimized モデル** | レイテンシ重視の専用版 |
| **Bedrock Cross-Region Inference** | 地理的近接／HA |
| **Amazon SageMaker Neo** | エッジ向け軽量化 |
| **Amazon CloudFront** | レスポンス配信 |
| **AWS Auto Scaling** | エンドポイント自動拡縮 |
| **AWS X-Ray** | プロファイリング |
| **Amazon OpenSearch** | インデックス最適化 |

### 3.4 レイテンシ削減テクニック

| 手段 | 効果 |
|---|---|
| **ストリーミング応答** | TTFB（Time To First Byte）短縮 |
| **Latency-Optimized モデル** | 推論最適化版 FM |
| **並列リクエスト** | 複数ステップを並列化 |
| **事前計算** | 予測可能なクエリを先回り |
| **Cross-Region Inference** | レイテンシ最小リージョン |
| **Edge 推論（SageMaker Neo）** | エッジで完結 |

### 3.5 SageMaker Neo

> **SageMaker Neo は軽量化される。ローカル LLM みたいな使い方ができる。**

機能:
- モデルを **ターゲットハードウェア向けにコンパイル**（INT8 量子化等）
- フットプリント縮小（メモリ・サイズ）
- レイテンシ短縮
- IoT デバイスや低スペック環境での推論を可能に

**Bedrock との対比**: クラウドの大量リクエスト ≒ Bedrock、エッジ／オンデバイス ≒ SageMaker Neo。

> 出典: `../point/exam/tech/a.md`「SageMaker neo → 軽量、ローカル LLM みたいな使い方ができる。SageMaker Neo（規制、エッジ）／Amazon Bedrock（クラウド大量リクエスト）」

### 3.6 サンプリングパラメータの選定

| 要件 | Temperature | Top-k | Top-p |
|---|---|---|---|
| 決定的応答（FAQ、SQL生成） | 0 | 1 | - |
| 通常の Q&A | 0.2-0.5 | 50 | 0.9 |
| 創作・ブレスト | 0.7-1.0 | 100 | 0.95 |

### 3.7 RAG の検索性能最適化

- **インデックス最適化**: OpenSearch のシャード／レプリカ設計
- **ハイブリッド検索**: BM25 + ベクトル
- **リランカ**: 第 1 段で k=50 取得 → リランカで上位 k=5
- **クエリ前処理**: 不要トークンの除去、HyDE 等
- **メタデータフィルタ**: 候補集合を絞ってから類似度計算

### 3.8 引っかけ

- 「レイテンシを最小化したい」→ **Latency-Optimized Bedrock モデル + ストリーミング**
- 「IoT デバイスで推論」→ **SageMaker Neo**
- 「TTFB を縮める」→ **ストリーミング**
- 「決定的な応答」→ **Temperature 0**

### 3.9 Exam Tips

- **「クラウド大量 = Bedrock、エッジ軽量 = Neo」** をセットで覚える
- TTFB はストリーミングが効く。総応答時間とは別概念
- Cross-Region Inference は性能（地理的近接）と HA の両方の文脈で使われる

### 3.10 チェックポイント
- [ ] レイテンシ削減手段を 5 つ挙げられる
- [ ] Bedrock と SageMaker Neo の使い分けを言える
- [ ] Top-k と Top-p の違いを説明できる

---

## 4. Task 4.3: GenAI アプリ監視

### 4.1 何が問われるか

**FM 特有の監視メトリクス**と、**トラブルシュートに役立つ可観測性**の構築。

### 4.2 公式スキル一覧

- **Skill 4.3.1**: 包括的可観測性（運用メトリクス、性能トレース、FM 対話トレース、ビジネス影響メトリクス、カスタムダッシュボード）
- **Skill 4.3.2**: GenAI 特化監視（トークン使用量、プロンプト効果、ハルシネーション率、応答品質、トークンバースト異常検知、Bedrock Model Invocation Logs、コスト異常検知）
- **Skill 4.3.3**: 統合可観測性（運用ダッシュボード、ビジネス可視化、コンプライアンス監視、フォレンジック追跡、ユーザ行動トラッキング、モデル動作パターン）
- **Skill 4.3.4**: ツール性能（呼出パターン追跡、性能メトリクス、ツールコール可観測性、マルチエージェント協調追跡、利用ベースライン）
- **Skill 4.3.5**: ベクトルストア運用管理（ベクトル DB 性能監視、自動インデックス最適化、データ品質バリデーション）
- **Skill 4.3.6**: FM 固有トラブルシュート（ハルシネーション検出のためのゴールデンデータセット、応答一貫性のための出力差分、推論経路追跡、特化観測パイプライン）

### 4.3 中核となる AWS サービス

| サービス | 用途 |
|---|---|
| **Amazon CloudWatch** | メトリクス・アラーム・ダッシュボード |
| **Amazon CloudWatch Logs（Insights）** | ログ分析（SQL 風） |
| **Amazon Bedrock Model Invocation Logs** | プロンプト・応答全文 |
| **AWS X-Ray** | 分散トレース |
| **Amazon Managed Grafana** | ビジュアライゼーション |
| **AWS CloudTrail** | API 監査 |
| **AWS Cost Anomaly Detection** | コスト異常検知 |
| **SageMaker Model Monitor** | データ／品質ドリフト |

### 4.4 GenAI 特有のメトリクス

| メトリクス | 取得方法 |
|---|---|
| **入力／出力トークン数** | Bedrock CloudWatch メトリクス |
| **InvocationLatency** | CloudWatch |
| **InvocationThrottles / Errors** | CloudWatch |
| **ハルシネーション率** | カスタム（ゴールデンデータセットとの一致率） |
| **Guardrails ブロック率** | Guardrails メトリクス |
| **エージェントツール成功率** | アプリログ集計 |
| **コスト** | Cost Explorer + CloudWatch カスタム |

### 4.5 観測パターン

```
[アプリ] ──CloudWatch──→ [メトリクス・アラーム]
   │
   ├──CloudWatch Logs──→ [Logs Insights / Grafana]
   │
   ├──X-Ray──→ [トレース可視化]
   │
   └──Bedrock Model Invocation Logs──→ [S3 / CloudWatch]
                                              ↓
                                       [後分析・QA]
```

### 4.6 ベクトルストア監視

- **クエリレイテンシ**: OpenSearch の検索時間メトリクス
- **インデックスサイズ**: 自動最適化（force merge、segment マージ）
- **データ品質**: 取り込み失敗率、重複率
- **検索精度**: 定期的なゴールデンクエリで Recall@K を計測

### 4.7 トラブルシュート手法

| 問題 | 観測手段 |
|---|---|
| **応答品質低下** | ゴールデンデータセットとの差分計算 |
| **ハルシネーション** | Grounding Check 失敗率、citations 一致率 |
| **応答の不一致** | 同じプロンプトの複数応答を出力差分（output diff） |
| **エージェント暴走** | Bedrock Agent Tracing で各ステップ可視化 |
| **コスト急増** | Cost Anomaly Detection、トークンバースト検知 |

### 4.8 引っかけ

- 「プロンプト・応答の事後分析」→ **Bedrock Model Invocation Logs**
- 「分散トレース」→ **X-Ray**
- 「コスト急増の自動通知」→ **AWS Cost Anomaly Detection**
- 「ハルシネーション継続監視」→ **ゴールデンデータセット + CloudWatch カスタムメトリクス**

### 4.9 Exam Tips

- **CloudTrail は API 呼び出し**、**Model Invocation Logs はコンテンツ**、**X-Ray はトレース** の三役を区別
- Cost Anomaly Detection は ML ベースで自動検知。閾値設定不要
- GenAI 監視はトークン・レイテンシ・品質の 3 軸で考える

### 4.10 チェックポイント
- [ ] GenAI 特有のメトリクスを 5 つ挙げられる
- [ ] CloudTrail / Model Invocation Logs / X-Ray の役割を区別できる
- [ ] ハルシネーション監視の方法を述べられる

---

## 5. このドメインで主に出てくる AWS サービス一覧

| サービス | 主な用途 | 関連タスク |
|---|---|---|
| Amazon Bedrock Provisioned Throughput | キャパ予約 | 4.1 |
| Amazon Bedrock Intelligent Prompt Routing | 自動モデル振り分け | 4.1 |
| Amazon Bedrock Batch Inference | バッチ割引 | 4.1 |
| Amazon Bedrock Prompt Caching | プロンプトキャッシュ | 4.1 |
| Amazon Bedrock Latency-Optimized モデル | 低レイテンシ | 4.2 |
| Amazon Bedrock Cross-Region Inference | 地理的近接 | 4.2 |
| Amazon SageMaker Neo | エッジ軽量化 | 4.2 |
| Amazon CloudFront | エッジキャッシング | 4.1, 4.2 |
| Amazon ElastiCache | アプリ層キャッシュ | 4.1 |
| AWS Auto Scaling | エンドポイント拡縮 | 4.2 |
| Amazon CloudWatch | メトリクス | 4.3 |
| Amazon CloudWatch Logs Insights | ログ分析 | 4.3 |
| Amazon Bedrock Model Invocation Logs | プロンプト監査 | 4.3 |
| AWS X-Ray | 分散トレース | 4.3 |
| AWS CloudTrail | API 監査 | 4.3 |
| AWS Cost Explorer / Anomaly Detection | コスト分析 | 4.1, 4.3 |
| Amazon Managed Grafana | 可視化 | 4.3 |
| SageMaker Model Monitor | ドリフト | 4.3 |

---

## 6. ドメイン横断キーワード

- **Provisioned Throughput**: 予約型キャパ
- **Intelligent Prompt Routing（IPR）**: 自動モデル振り分け
- **Prompt Caching**: 共通プレフィックスのキャッシュ
- **Semantic Caching**: 意味類似のキャッシュ
- **Latency-Optimized モデル**: 推論最適化版
- **SageMaker Neo**: エッジ軽量化
- **TTFB**: Time To First Byte（ストリーミングで改善）
- **Top-k / Top-p / Temperature**: サンプリング 3 兄弟
- **Model Invocation Logs vs CloudTrail vs X-Ray**: コンテンツ／API／トレース

---

## 7. 参考リンク

- [Amazon Bedrock Provisioned Throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html)
- [Amazon Bedrock Intelligent Prompt Routing](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html)
- [Amazon Bedrock Batch Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html)
- [Amazon Bedrock Prompt Caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)
- [Amazon SageMaker Neo](https://docs.aws.amazon.com/sagemaker/latest/dg/neo.html)
- [AWS Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html)
- [Bedrock CloudWatch メトリクス](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-cw.html)

---

## 8. 既存メモからの取り込み出典

- `../point/exam/tech/a.md`: Provisioned Throughput（→ 2 章）、Intelligent Prompt Routing（→ 2 章）、SageMaker Neo（→ 3 章）
