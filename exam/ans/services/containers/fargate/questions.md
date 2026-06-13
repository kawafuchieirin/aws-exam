---
service: fargate
domain_default: 1
source: README.md
source_sha256: ada0be8ecbd199448f456b5f7c4bb931dfd1cb9318071ad89305ff20e5944a46
generated: 2026-05-24
---

## fargate-001
- type: single
- difficulty: easy
- domain: 1
- tags: [awsvpc]

AWS Fargate で利用できるネットワークモードはどれか。

- [x] A. awsvpc（固定）
- [ ] B. bridge
- [ ] C. host
- [ ] D. none

> **解説**: Fargate はホストを管理しないため awsvpc モード固定。各タスク/Pod が専用 ENI と VPC の IP、専用 SG を持つ。bridge/host は選べない。
> **出典**: [fargate README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## fargate-002
- type: single
- difficulty: medium
- domain: 1
- tags: [security-group, subnetting, awsvpc]

パブリックサブネットの Fargate タスクにパブリック IP を直接付与してインターネットへ出したい。必要な設定はどれか。

- [x] A. assignPublicIp=ENABLED（パブリックサブネット + IGW 経路が前提）
- [ ] B. プライベートサブネットで assignPublicIp=ENABLED
- [ ] C. NAT Gateway をパブリックサブネットに配置
- [ ] D. host モードでホスト IP を共有

> **解説**: assignPublicIp=ENABLED はパブリックサブネット + IGW 経路が前提でタスクに直接パブリック IP を付与する。プライベートサブネットでは付与できない。
> **出典**: [fargate README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## fargate-003
- type: single
- difficulty: medium
- domain: 1
- tags: [security-group, subnetting, nat]

プライベートサブネットの Fargate タスクをインターネットへアウトバウンド接続させる推奨構成はどれか。

- [ ] A. assignPublicIp=ENABLED を有効化する
- [x] B. NAT Gateway 経由で IGW へ出す
- [ ] C. プライベートサブネットに IGW を直接アタッチ
- [ ] D. bridge モードでホスト経由にする

> **解説**: プライベートサブネットではパブリック IP を付与できないため、アウトバウンドは NAT Gateway 経由が推奨。AWS サービスへは VPC エンドポイントを使う。
> **出典**: [fargate README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## fargate-004
- type: single
- difficulty: medium
- domain: 3
- tags: [vpc-endpoint, troubleshooting]

プライベートサブネットの Fargate タスクが起動時にイメージ pull で失敗する。NAT が無い前提で原因として最も妥当なものはどれか。

- [x] A. ecr.api / ecr.dkr の Interface と S3 Gateway エンドポイントが揃っていない
- [ ] B. assignPublicIp が DISABLED になっている
- [ ] C. ネットワークモードが awsvpc になっていない
- [ ] D. host モードのポートが競合している

> **解説**: プライベートサブネットの Fargate は ECR の ecr.api/ecr.dkr + S3 エンドポイント、または NAT が無いと pull に失敗する。CloudWatch Logs 送信にもエンドポイント/NAT が必要。
> **出典**: [fargate README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## fargate-005
- type: single
- difficulty: medium
- domain: 1
- tags: [awsvpc, alb, target-type]

EKS on Fargate で AWS Load Balancer Controller を使う際のターゲットモードはどれか。

- [x] A. ip ターゲットモード（必須）
- [ ] B. instance ターゲットモード（必須）
- [ ] C. host ターゲットモード
- [ ] D. bridge ターゲットモード

> **解説**: EKS on Fargate にはワーカーノードが無いため instance ターゲットモードは使えず、ip ターゲットモードが必須。各 Pod が専用 ENI を持ち Security Groups for Pods もサポートされる。
> **出典**: [fargate README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## fargate-006
- type: single
- difficulty: easy
- domain: 4
- tags: [eni, security-group]

Fargate のセキュリティグループ適用について正しいものはどれか。

- [x] A. 各タスクが専用 ENI を持ちタスク単位で SG を適用できる
- [ ] B. ホストの ENI を共有するため SG はホスト共通
- [ ] C. SG は付与できず NACL のみで制御する
- [ ] D. タスク単位の SG 適用には bridge モードが必要

> **解説**: Fargate はホストを共有せず各タスクが独立した ENI を持つため、SG をタスク単位で適用できる。これは awsvpc 固定であることの帰結。
> **出典**: [fargate README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## fargate-007
- type: single
- difficulty: medium
- domain: 3
- tags: [awsvpc, eni]

プラットフォームバージョン 1.4.0 以降の Fargate タスクのネットワークについて正しいものはどれか。

- [x] A. 全トラフィックが単一のタスク ENI を経由する
- [ ] B. タスクごとに複数の ENI が必須になる
- [ ] C. host モードが追加でサポートされる
- [ ] D. タスク ENI が廃止されホスト ENI を使う

> **解説**: PV 1.4.0 以降は全トラフィックが単一タスク ENI に集約され、エフェメラルストレージ等も整理されている。
> **出典**: [fargate README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## fargate-008
- type: multi
- difficulty: medium
- domain: 1
- tags: [security-group, public-ip, nat, vpc-endpoint]

Fargate タスクのアウトバウンド経路設計について正しいものを2つ選べ。

- [x] A. パブリックサブネット + assignPublicIp=ENABLED でタスクに直接パブリック IP を付与できる
- [x] B. プライベートサブネット + NAT Gateway が推奨で、AWS サービスへは VPC エンドポイントを使う
- [ ] C. プライベートサブネットでも assignPublicIp=ENABLED でパブリック IP を付与できる
- [ ] D. host モードに切り替えればアウトバウンド経路は不要
- [ ] E. アウトバウンドには必ず IGW をタスクに直接アタッチする

> **解説**: アウトバウンドの2択は (A) パブリックサブネット + assignPublicIp=ENABLED、(B) プライベートサブネット + NAT Gateway（推奨、AWS サービスは VPC エンドポイント）。プライベートサブネットではパブリック IP を付与できない。
> **出典**: [fargate README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## fargate-009
- type: multi
- difficulty: hard
- domain: 1
- tags: [awsvpc, eni]

Fargate のネットワーク特性として正しいものを2つ選べ。

- [x] A. host や bridge は使えず awsvpc 固定である
- [x] B. EKS on Fargate でも各 Pod が専用 ENI を持ち Security Groups for Pods がサポートされる
- [ ] C. タスク単位で SG を分離することはできない
- [ ] D. ホストを共有するためポート競合が発生する
- [ ] E. プライベートサブネットでもタスクにパブリック IP を付与できる

> **解説**: Fargate はホストを管理しないため awsvpc 固定でタスク単位の SG 分離が可能。EKS on Fargate では各 Pod が専用 ENI を持ち Security Groups for Pods もサポートされる。プライベートサブネットでパブリック IP は付与不可。
> **出典**: [fargate README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)
</content>
