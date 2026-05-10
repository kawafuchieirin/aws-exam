# AWS Certified Generative AI Developer - Professional (AIP-C01) 参考書

AWS公式試験ガイド（AIP-C01）に基づき、コンテンツ分野別にまとめた参考書です。

## 試験基本情報

| 項目 | 内容 |
|---|---|
| 認定名 | AWS Certified Generative AI Developer - Professional |
| 試験コード | AIP-C01 |
| 対象者 | 2年以上のAWS本番運用経験＋1年以上のGenAI実装経験を持つGenAIデベロッパー |
| 出題数 | 65問（採点対象）＋ 10問（採点対象外） |
| 合格スコア | 750 / 1000 |
| 問題形式 | 単一選択（4択）／複数選択（5択以上） |

## 学習の進め方

1. **[00-overview.md](./00-overview.md)** で試験全体像と学習方針を把握
2. **配点が高いドメインから順に学習**（Domain 1 → 2 → 3 → 4 → 5）
3. 各ドメインのチェックポイントで理解度を確認
4. 仕上げに **[appendix-glossary.md](./appendix-glossary.md)** と **[appendix-services.md](./appendix-services.md)** で用語・サービスを横断整理

## コンテンツ分野（5ドメイン）

| # | ドメイン | 配点 | ファイル | 進捗 |
|---|---|---|---|---|
| 1 | Foundation Model Integration, Data Management, and Compliance | **31%** | [01-domain1-foundation-models.md](./01-domain1-foundation-models.md) | ☐ |
| 2 | Implementation and Integration | 26% | [02-domain2-implementation.md](./02-domain2-implementation.md) | ☐ |
| 3 | AI Safety, Security, and Governance | 20% | [03-domain3-safety-security.md](./03-domain3-safety-security.md) | ☐ |
| 4 | Operational Efficiency and Optimization for GenAI Applications | 12% | [04-domain4-operations.md](./04-domain4-operations.md) | ☐ |
| 5 | Testing, Validation, and Troubleshooting | 11% | [05-domain5-testing.md](./05-domain5-testing.md) | ☐ |

## 付録（Appendix）

| ファイル | 内容 |
|---|---|
| [appendix-glossary.md](./appendix-glossary.md) | 用語集（top-k / 帰属機能 / グラウンディング / RAG / LoRA など） |
| [appendix-services.md](./appendix-services.md) | In-Scope AWSサービス早見表（カテゴリ別） |

## ドメイン別 学習チェックリスト

### Domain 1: Foundation Model Integration（31%）
- [ ] Task 1.1: 要件分析と GenAI ソリューション設計
- [ ] Task 1.2: FM の選定と構成
- [ ] Task 1.3: FM 用データ検証・処理パイプライン
- [ ] Task 1.4: ベクトルストア設計・実装
- [ ] Task 1.5: FM 拡張のための検索メカニズム（RAG）
- [ ] Task 1.6: プロンプトエンジニアリング戦略・ガバナンス

### Domain 2: Implementation and Integration（26%）
- [ ] Task 2.1: エージェンティック AI とツール統合
- [ ] Task 2.2: モデルデプロイ戦略
- [ ] Task 2.3: エンタープライズ統合アーキテクチャ
- [ ] Task 2.4: FM API 統合
- [ ] Task 2.5: アプリケーション統合パターン・開発ツール

### Domain 3: AI Safety, Security, and Governance（20%）
- [ ] Task 3.1: 入出力安全制御
- [ ] Task 3.2: データセキュリティ・プライバシー制御
- [ ] Task 3.3: AI ガバナンス・コンプライアンス機構
- [ ] Task 3.4: 責任ある AI 原則の実装

### Domain 4: Operational Efficiency and Optimization（12%）
- [ ] Task 4.1: コスト最適化・リソース効率化
- [ ] Task 4.2: アプリケーションパフォーマンス最適化
- [ ] Task 4.3: GenAI 監視システム

### Domain 5: Testing, Validation, and Troubleshooting（11%）
- [ ] Task 5.1: GenAI 評価システム
- [ ] Task 5.2: GenAI アプリケーションのトラブルシュート

## 公式ソース

- [AWS Certified Generative AI Developer - Professional 認定情報](https://aws.amazon.com/certification/certified-generative-ai-developer-professional/)
- [AIP-C01 試験ガイド（HTML版）](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01.html)
- [AIP-C01 試験ガイド（PDF版）](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/certification/approved/pdfs/docs-aip/AWS-Certified-Generative-AI-Developer-Pro_Exam-Guide.pdf)

## 関連ファイル

- [../point/a.md](../point/a.md): 学習過程の旧メモ（参考書側に統合済み、出典として保持）
- [../point/exam/tech/a.md](../point/exam/tech/a.md): 過去問演習メモ
- [../point/exam/tech/正答.md](../point/exam/tech/正答.md): 弱点問題番号リスト
