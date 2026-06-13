---
service: firewall-manager
domain_default: 4
source: README.md
source_sha256: 894c72ab1d792d9f81d0d9b8ebc2b22d50c7dd7120ca082bc1d7871834e6f6bc
generated: 2026-05-24
---

## firewall-manager-001
- type: single
- difficulty: medium
- domain: 4
- tags: [firewall-manager, multi-account, iac]

ある企業は AWS Organizations で多数のアカウントを運用しており、すべての ALB に共通の WAF Web ACL を強制し、さらに将来新規に作成されるアカウントやリソースにも自動的に同じ保護を適用したい。最も適切なサービスはどれか。

- [ ] A. 各アカウントで AWS WAF を個別に設定するランブックを配布する
- [x] B. AWS Firewall Manager で WAF ポリシーを定義しスコープを組織全体にする
- [ ] C. SCP で WAF の使用を必須化する
- [ ] D. AWS Config ルールで Web ACL の有無のみを評価する

> **解説**: Firewall Manager はポリシーを一度定義すれば組織横断で適用し、新規アカウント・新規リソースにも自動展開できる唯一の選択肢。各アカウント個別設定は運用負荷が高く自動適用されない。SCP は許可の上限を定めるだけで Web ACL を配布しない。Config は評価のみで強制適用しない。
> **出典**: [firewall-manager README #1 概要](README.md#1-概要)

## firewall-manager-002
- type: multi
- difficulty: medium
- domain: 4
- tags: [firewall-manager, use-case-fit]

AWS Firewall Manager を利用開始するために満たすべき前提条件はどれか。3つ選べ。

- [x] A. AWS Organizations を全機能（all features）で有効化する
- [x] B. FMS 管理者アカウントを指定する
- [x] C. 各アカウント/リージョンで AWS Config を有効化する
- [ ] D. すべてのアカウントで GuardDuty を有効化する
- [ ] E. すべての VPC で VPC フローログを有効化する

> **解説**: FMS の前提は Organizations の全機能有効化、FMS 管理者アカウントの指定、そして準拠評価基盤としての AWS Config 有効化の3点。GuardDuty や VPC フローログは FMS の動作要件ではない。
> **出典**: [firewall-manager README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## firewall-manager-003
- type: single
- difficulty: easy
- domain: 4
- tags: [firewall-manager, multi-account]

FMS 管理者アカウントについて正しい説明はどれか。

- [ ] A. メンバーアカウントであれば任意に指定できる
- [x] B. Organizations 管理アカウント（または委任管理者）が指定される
- [ ] C. 各 OU に1つずつ必須となる
- [ ] D. 管理者アカウントの指定は不要で自動選定される

> **解説**: FMS 管理者は Organizations の管理アカウントが指定し、委任管理者を指名することもできる。OU ごとではなく組織で運用する。
> **出典**: [firewall-manager README #2 コアコンセプト](README.md#2-コアコンセプト)

## firewall-manager-004
- type: multi
- difficulty: medium
- domain: 4
- tags: [firewall-manager]

AWS Firewall Manager が管理できるポリシータイプはどれか。3つ選べ。

- [x] A. AWS WAF の Web ACL
- [x] B. VPC セキュリティグループ
- [x] C. AWS Network Firewall
- [ ] D. IAM ロールの権限境界
- [ ] E. Amazon EBS の暗号化

> **解説**: FMS は WAF、Shield Advanced、VPC セキュリティグループ/NACL、Network Firewall、Route 53 Resolver DNS Firewall、サードパーティファイアウォールを管理できる。IAM 権限境界や EBS 暗号化は FMS ポリシーの対象外。
> **出典**: [firewall-manager README #2 管理できるポリシータイプ](README.md#管理できるポリシータイプ)

## firewall-manager-005
- type: single
- difficulty: medium
- domain: 4
- tags: [firewall-manager, security-group]

組織内で「未使用・冗長なセキュリティグループ」を検出したい。FMS の SG ポリシーのうちどれを使うか。

- [ ] A. 共通セキュリティグループポリシー
- [ ] B. コンテンツ監査セキュリティグループポリシー
- [x] C. 使用状況監査セキュリティグループポリシー
- [ ] D. NACL ポリシー

> **解説**: SG ポリシーには共通（共通 SG 配布）、コンテンツ監査（許可/拒否ルールの監査）、使用状況監査（未使用・冗長 SG の検出）の3種があり、未使用/冗長の検出は使用状況監査ポリシー。
> **出典**: [firewall-manager README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## firewall-manager-006
- type: single
- difficulty: medium
- domain: 4
- tags: [firewall-manager, shield]

組織内の全メンバーアカウントを Shield Advanced に一括サブスクライブし、新規アカウントも自動加入させたい。どうするか。

- [ ] A. 各アカウントで個別に Shield Advanced を購入する
- [x] B. FMS の Shield Advanced ポリシーを作成しスコープを組織全体にする
- [ ] C. SCP で Shield Standard を有効化する
- [ ] D. WAF ポリシーで Shield を有効化する

> **解説**: FMS の Shield Advanced ポリシーは組織全アカウントを一括サブスク・保護有効化し、新規アカウントも自動加入させられる。Standard は無料で自動付帯なので SCP 不要。
> **出典**: [firewall-manager README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## firewall-manager-007
- type: single
- difficulty: hard
- domain: 4
- tags: [firewall-manager, multi-region, route-table]

リージョナルな保護（例: Regional スコープの WAF や Network Firewall）を複数リージョンに適用する場合、FMS ポリシーについて正しいのはどれか。

- [ ] A. 1つのポリシーで全リージョンに自動適用される
- [x] B. リージョナルポリシーはリージョンごとに作成する必要がある
- [ ] C. リージョナルポリシーは us-east-1 でのみ作成できる
- [ ] D. FMS はリージョン非依存でポリシーを管理する

> **解説**: FMS のリージョナルポリシーはリージョンごとに作成が必要。CloudFront など一部のグローバルリソースはグローバル扱い。
> **出典**: [firewall-manager README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## firewall-manager-008
- type: single
- difficulty: medium
- domain: 4
- tags: [firewall-manager, automation]

FMS の自動修復（remediation）の役割として正しいものはどれか。

- [ ] A. 非準拠リソースを自動的に削除する
- [x] B. スコープ内の非準拠リソース・新規リソースへポリシーを自動適用する
- [ ] C. 攻撃トラフィックを自動でブロックする
- [ ] D. IAM 権限を自動で付与する

> **解説**: 自動修復は非準拠リソースや新規リソースにポリシーを自動適用しドリフトを修復する仕組み。リソース削除や攻撃ブロックそのものではない。
> **出典**: [firewall-manager README #2 コアコンセプト](README.md#2-コアコンセプト)

## firewall-manager-009
- type: single
- difficulty: easy
- domain: 4
- tags: [firewall-manager, cost]

FMS の課金について正しいものはどれか。

- [ ] A. FMS は完全に無料で背後サービスも無料
- [x] B. アクティブなポリシーあたりの月額＋背後サービス（WAF/Shield/Config 等）の通常料金がかかる
- [ ] C. 共有アカウント数に応じた課金のみ
- [ ] D. 検査したデータ量にのみ課金

> **解説**: FMS の課金はアクティブポリシー単位。実コストの大半は WAF/Shield Advanced/Config など下層サービスの通常料金。
> **出典**: [firewall-manager README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## firewall-manager-010
- type: single
- difficulty: medium
- domain: 4
- tags: [firewall-manager, config-rules]

FMS が準拠状態を評価するために前提として依存するサービスはどれか。

- [ ] A. AWS CloudTrail
- [x] B. AWS Config
- [ ] C. Amazon Inspector
- [ ] D. AWS Trusted Advisor

> **解説**: FMS は AWS Config を準拠状態の評価基盤として必須とする。CloudTrail は API 監査、Inspector は脆弱性評価で役割が異なる。
> **出典**: [firewall-manager README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)
