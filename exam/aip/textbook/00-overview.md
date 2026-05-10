# 00. 試験概要・学習方針

> 出典: AWS公式 AIP-C01 試験ガイド（2026年4月版）

## 1. 試験の位置づけ

AWS Certified Generative AI Developer - Professional（AIP-C01）は、**生成AIアプリケーションを本番環境で実装・運用するデベロッパー**向けの**プロフェッショナルレベル**認定。

### 1.1 期待される候補者像

- AWS 上または OSS 技術での **本番グレードアプリケーション構築 2年以上** の経験
- 一般的な AI/ML またはデータエンジニアリングの経験
- **GenAI ソリューション実装のハンズオン経験 1年以上**

### 1.2 候補者が遂行できるべきタスク（公式記載）

- ベクトルストア、RAG、Knowledge Bases、その他の GenAI アーキテクチャを使ったソリューション設計・実装
- FM をアプリケーション・業務ワークフローに統合
- プロンプトエンジニアリング・プロンプト管理
- エージェンティック AI ソリューションの実装
- コスト・パフォーマンス・ビジネス価値の観点で GenAI アプリを最適化
- セキュリティ・ガバナンス・責任ある AI 実践の実装
- GenAI アプリのトラブルシュート、監視、最適化
- FM の品質・責任性評価

### 1.3 推奨される AWS 知識

- AWS のコンピュート、ストレージ、ネットワークサービス
- AWS セキュリティベストプラクティスと ID 管理
- AWS デプロイと IaC ツール（CloudFormation, CDK）
- AWS の監視・可観測性サービス（CloudWatch, X-Ray）
- AWS コスト最適化原則

### 1.4 スコープ外（試験で問われない）

- モデル開発・トレーニング
- 高度な ML テクニック
- データエンジニアリング・特徴量エンジニアリング

→ 本試験は **「FM を使う側のデベロッパー」** が対象。モデルそのものを作る側（MLA など）とは住み分けされている。

## 2. 試験フォーマット

| 項目 | 内容 |
|---|---|
| 出題数 | 65問（採点）＋ 10問（採点外、評価のみ） |
| 試験時間 | 公式公表通り |
| 問題形式 | Multiple Choice（4択1正解） / Multiple Response（5択以上で2つ以上正解） |
| 採点方式 | スケールドスコア 100〜1000、合格 750 |
| 採点 | 補償スコアリング（各セクション合格不要、総合点のみ） |

無回答は不正解扱い。**当てずっぽうペナルティはない** ので、必ず全問解答する。

## 3. コンテンツ分野と配点

| ドメイン | タイトル | 配点 |
|---|---|---|
| Domain 1 | Foundation Model Integration, Data Management, and Compliance | **31%** |
| Domain 2 | Implementation and Integration | 26% |
| Domain 3 | AI Safety, Security, and Governance | 20% |
| Domain 4 | Operational Efficiency and Optimization for GenAI Applications | 12% |
| Domain 5 | Testing, Validation, and Troubleshooting | 11% |

**Domain 1+2 で 57%** を占める → ここを落とすと合格は厳しい。最優先で固める。

## 4. 推奨学習ステップ

### Step 1: 全体像把握（半日）
- 本ファイル + [README.md](./README.md) を通読
- [appendix-glossary.md](./appendix-glossary.md) で用語の地ならし
- [appendix-services.md](./appendix-services.md) で対象サービスの全体マップを確認

### Step 2: 配点順に深掘り（数日〜1週間）
1. [Domain 1（31%）](./01-domain1-foundation-models.md) ← FM・RAG・プロンプト
2. [Domain 2（26%）](./02-domain2-implementation.md) ← Agents・API・統合
3. [Domain 3（20%）](./03-domain3-safety-security.md) ← Guardrails・PII・ガバナンス
4. [Domain 4（12%）](./04-domain4-operations.md) ← コスト・性能・監視
5. [Domain 5（11%）](./05-domain5-testing.md) ← 評価・トラブルシュート

### Step 3: 横断復習（試験直前）
- 各ドメインの「試験頻出ポイント」セクションをざっと再読
- 用語集を音読して反射的に思い出せるか確認
- 旧メモ（[../point/](../point/)）の弱点問題を解き直す

## 5. 学習リソース（公式・準公式）

### 公式
- [AIP-C01 試験ガイド（HTML）](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01.html)
- [AIP-C01 試験ガイド（PDF）](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/certification/approved/pdfs/docs-aip/AWS-Certified-Generative-AI-Developer-Pro_Exam-Guide.pdf)
- [AWS Skill Builder: AIP-C01 学習パス](https://skillbuilder.aws/category/exam-prep/generative-ai-developer-professional-aip-c01)
- [AWS Well-Architected Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/)

### 公式ドキュメント（必読）
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/)
- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Amazon SageMaker AI Developer Guide](https://docs.aws.amazon.com/sagemaker/latest/dg/)

### 準公式・コミュニティ
- [Tutorials Dojo AIP-C01 Study Path](https://tutorialsdojo.com/aws-certified-generative-ai-developer-professional-study-path-aip-c01-exam-guide/)
- [Classmethod ブログ（生成AI / Bedrock 系）](https://dev.classmethod.jp/)

## 6. AIF-C01（AI Practitioner）との違い

| 観点 | AIF-C01（AI Practitioner） | **AIP-C01（GenAI Developer Pro）** |
|---|---|---|
| レベル | Foundational | **Professional** |
| 想定対象 | AI/ML を業務で使うすべての人 | **GenAI 実装デベロッパー** |
| 出題範囲 | AI/ML 全般、生成AI入門 | **生成AI 実装・運用に特化** |
| 求められる経験 | 半年〜1年程度 | **3年以上（AWS 2年＋GenAI 1年）** |
| Bedrock の問われ方 | 概要レベル | **API、Agents、Guardrails、Knowledge Bases などの深い実装知識** |

AIF-C01 合格者でも、本試験は別物として腰を据えて学習が必要。

## 7. 学習時の注意

- **Bedrock 系機能は更新が早い**ため、各章末の `Last verified` 日付を意識し、本番試験直前には最新ドキュメントで再確認する
- **多肢選択（複数正解）の問題が多い** ので、「最も適切な1つ」と「許容できるすべて」を見分ける訓練が必要
- **コスト・運用・セキュリティの最適解** を選ばせる問題が多く、技術的に動くだけの選択肢は不正解になりやすい
