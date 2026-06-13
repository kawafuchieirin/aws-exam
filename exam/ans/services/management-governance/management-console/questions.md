---
service: management-console
domain_default: 4
source: README.md
source_sha256: 83bda2b577eb69d14c7fe5081672ef6dd75988e6b085952fac72a1eeaa5e33a1
generated: 2026-05-24
---

## management-console-001
- type: single
- difficulty: medium
- domain: 4
- tags: [console-security, source-condition]

社内ネットワークからのみ AWS Management Console へのアクセスを許可したい。最も適切な手段はどれか。

- [ ] A. VPC のセキュリティグループで送信元 IP を制限する
- [x] B. IAM ポリシーの `aws:SourceIp` 条件で送信元 IP を制限する
- [ ] C. ルートテーブルで社内 IP のみ許可する
- [ ] D. NACL で社内 IP のみ許可する

> **解説**: コンソールへのアクセス自体を IP で制御するには、IAM の `aws:SourceIp` 条件を使う。SG/NACL/ルートテーブルは VPC 内のリソースへの通信制御であり、コンソール（AWS のグローバルエンドポイント）アクセスの制限手段ではない。
> **出典**: [Management Console README #1 概要](README.md#1-概要)

## management-console-002
- type: single
- difficulty: easy
- domain: 3
- tags: [cloudtrail-events]

コンソールで実行した操作の監査ログを確認したい。どこに記録されているか。

- [ ] A. VPC フローログ
- [x] B. CloudTrail の管理イベント
- [ ] C. CloudWatch メトリクス
- [ ] D. Config の構成履歴のみ

> **解説**: コンソール操作も裏では API コールであり、CloudTrail の管理イベントとしてすべて記録される。フローログはネットワークトラフィック、CloudWatch はメトリクスで操作監査とは別。
> **出典**: [Management Console README #1 概要](README.md#1-概要)

## management-console-003
- type: single
- difficulty: medium
- domain: 1
- tags: [iac]

ネットワーク構成の再現性を重視する場合、コンソールでの手動操作と比較してより適切な手段はどれか。

- [ ] A. コンソールの操作履歴をスクリーンショットで残す
- [x] B. CloudFormation 等の IaC でコード化する
- [ ] C. Trusted Advisor のチェックに任せる
- [ ] D. Health Dashboard で構成を管理する

> **解説**: コンソールは手動操作のため再現性が IaC に劣る。CloudFormation 等で構成をコード化すると再現性・レビュー性が高まる。コンソールは確認・トラブルシュート・可視化に有用。
> **出典**: [Management Console README #1 概要](README.md#1-概要)

## management-console-004
- type: single
- difficulty: medium
- domain: 4
- tags: [vpc-endpoint]

インターネットを経由しない管理アクセス経路を設計したい。コンソール／管理アクセスをプライベートに保つ手段として README が挙げるものはどれか。

- [ ] A. パブリックサブネットに踏み台を置く
- [x] B. コンソールへのインターフェイス VPC エンドポイント／プライベート接続を組み合わせる
- [ ] C. Internet Gateway にルートを追加する
- [ ] D. NAT Gateway を経由させる

> **解説**: README は `aws:SourceIp` 条件に加え、インターフェイス VPC エンドポイント／プライベート接続を組み合わせ、インターネットを経由しない管理アクセス経路を設計できると述べる。IGW/NAT はインターネット経由になり趣旨に反する。
> **出典**: [Management Console README #1 概要](README.md#1-概要)

## management-console-005
- type: single
- difficulty: easy
- domain: 3
- tags: [monitoring]

コンソールから対話的に扱える、ネットワークの可視化・到達性分析ツールとして README が挙げるものはどれか。

- [ ] A. Cost Explorer / Budgets
- [x] B. Reachability Analyzer / Network Access Analyzer / フローログ
- [ ] C. CodeDeploy / CodePipeline
- [ ] D. Athena / QuickSight

> **解説**: README は VPC・サブネット・SG/NACL の設定に加え、Reachability Analyzer・Network Access Analyzer・フローログといった可視化ツールをコンソールから対話的に扱えると述べる。
> **出典**: [Management Console README #1 概要](README.md#1-概要)

## management-console-006
- type: single
- difficulty: medium
- domain: 3
- tags: [console-security]

AWS Management Console がネットワーク運用で特に有用とされる用途はどれか。

- [ ] A. 大規模かつ反復的なリソースの一括デプロイ
- [x] B. 構成の確認・トラブルシュート・可視化
- [ ] C. バージョン管理されたインフラ定義の保持
- [ ] D. CI/CD パイプラインの実行

> **解説**: コンソールは再現性では IaC に劣るが、構成の確認・トラブルシュート・可視化には有用とされる。一括デプロイやバージョン管理は IaC/CI/CD の領域。
> **出典**: [Management Console README #1 概要](README.md#1-概要)

## management-console-007
- type: multi
- difficulty: hard
- domain: 4
- tags: [console-security, security-group]

AWS Management Console をネットワーク的に保護する設計として、README に沿った適切な記述を2つ選べ。

- [x] A. IAM ポリシーの `aws:SourceIp` 条件で社内 IP からのアクセスに限定する
- [ ] B. SCP でコンソールのログイン画面を VPC 内に移動させる
- [x] C. インターフェイス VPC エンドポイント／プライベート接続でインターネットを経由しない経路を設計する
- [ ] D. セキュリティグループでコンソールへの HTTPS を許可する
- [ ] E. NACL でコンソール用の戻りポートを開放する

> **解説**: コンソール保護は `aws:SourceIp` による IP 制限と、インターフェイス VPC エンドポイント／プライベート接続の組み合わせが正しい。SG/NACL は VPC リソース向けの制御で、コンソールのグローバルエンドポイント保護には使えない。
> **出典**: [Management Console README #1 概要](README.md#1-概要)

## management-console-008
- type: single
- difficulty: easy
- domain: 3
- tags: [console-security, use-case-fit]

コンソール操作とプログラム操作の関係について正しいものはどれか。

- [x] A. コンソール操作も裏では API コールであり、CloudTrail に記録される
- [ ] B. コンソール操作は API とは無関係で監査対象外である
- [ ] C. コンソール操作は CloudTrail ではなく CloudWatch に記録される
- [ ] D. コンソール操作は記録されない

> **解説**: コンソールでの操作も内部的には API コールであり、CloudTrail の管理イベントとしてすべて記録される。CLI/SDK と同様に監査可能。
> **出典**: [Management Console README #1 概要](README.md#1-概要)
