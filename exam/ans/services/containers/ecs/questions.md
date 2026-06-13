---
service: ecs
domain_default: 1
source: README.md
source_sha256: 4b9f40347cb8b1738423ed74d4bb905b34d9c42655ed49cb77758cd5ae4e2f84
generated: 2026-05-24
---

## ecs-001
- type: single
- difficulty: medium
- domain: 1
- tags: [awsvpc, eni, security-group]

各 ECS タスクに VPC ネイティブな IP を持たせ、タスク単位でセキュリティグループを適用したい。選ぶべきネットワークモードはどれか。

- [x] A. awsvpc モード
- [ ] B. bridge モード
- [ ] C. host モード
- [ ] D. none モード

> **解説**: awsvpc モードは各タスクに専用 ENI と VPC の IP を割り当て、タスク単位の SG 適用を可能にする。bridge/host はホストの ENI を共有するためタスク単位の SG 分離ができない。
> **出典**: [ecs README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecs-002
- type: single
- difficulty: easy
- domain: 1
- tags: [awsvpc]

Fargate 起動タイプで利用できる ECS のネットワークモードはどれか。

- [ ] A. bridge
- [ ] B. host
- [x] C. awsvpc（固定）
- [ ] D. none

> **解説**: Fargate はホストを管理しないため awsvpc モードが固定（必須）。bridge/host/none は EC2 起動タイプでのみ利用できる。
> **出典**: [ecs README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## ecs-003
- type: single
- difficulty: medium
- domain: 1
- tags: [awsvpc, tcp-udp, alb]

EC2 起動タイプで、1 つのコンテナインスタンスに同一コンテナを複数配置しつつ ALB で負荷分散したい。適切な構成はどれか。

- [x] A. bridge モードの動的ポートマッピング + ALB ターゲットグループ
- [ ] B. host モードで同一ポートに複数タスクを配置
- [ ] C. awsvpc で 1 インスタンス 1 タスクに固定
- [ ] D. none モードで内部通信のみ

> **解説**: bridge モードの動的ポートマッピングを使うと 1 ホストに同一コンテナを複数置け、ALB のターゲットグループが動的ポートを解決して負荷分散できる。host は同一ポート競合で複数置けない。
> **出典**: [ecs README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecs-004
- type: single
- difficulty: medium
- domain: 1
- tags: [awsvpc, enhanced-networking, troubleshooting]

host ネットワークモードの特徴として正しいものはどれか。

- [ ] A. タスクごとに専用 ENI が割り当てられる
- [x] B. ホスト NIC を直接使い最高スループットだが同一ポートのタスクを複数置けない
- [ ] C. Fargate で利用できる
- [ ] D. 動的ポートマッピングが自動で行われる

> **解説**: host モードはホストの ENI を直接利用し NAT を介さず最高スループットを得られるが、ポート競合のため同一ポートのタスクを複数配置できない。EC2 のみで Fargate では使えない。
> **出典**: [ecs README #2 コアコンセプト](README.md#2-コアコンセプト)

## ecs-005
- type: single
- difficulty: hard
- domain: 1
- tags: [awsvpc, eni, enhanced-networking]

EC2 起動タイプで awsvpc タスクを多数稼働させたいが、インスタンスタイプの ENI 上限がタスク数を律速している。1 インスタンスあたりの awsvpc タスク数を増やす手段はどれか。

- [ ] A. bridge モードに切り替える
- [x] B. ENI トランキングを有効化する
- [ ] C. NAT Gateway を追加する
- [ ] D. Cloud Map の名前空間を増やす

> **解説**: awsvpc モードはタスクごとに ENI を消費し、EC2 のインスタンスタイプの ENI 上限がタスク密度を律速する。ENI トランキングで 1 インスタンスあたりの awsvpc タスク数を増やせる。
> **出典**: [ecs README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecs-006
- type: single
- difficulty: medium
- domain: 3
- tags: [service-discovery, dns]

awsvpc モードの ECS サービスで、各タスクの IP を DNS で名前解決できるようにしたい。適切な仕組みはどれか。

- [x] A. AWS Cloud Map によるサービスディスカバリで各タスク IP を DNS 登録する
- [ ] B. ALB のターゲットグループに静的 IP を登録する
- [ ] C. NACL で IP を固定する
- [ ] D. host モードでホスト名を登録する

> **解説**: ECS は Cloud Map に名前空間を作成しタスク IP を登録する。awsvpc では各タスクが固有 IP を持つため、それを直接 DNS 解決できる。
> **出典**: [ecs README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecs-007
- type: single
- difficulty: medium
- domain: 1
- tags: [service-discovery, service-mesh]

ECS のサービス間通信をサービス名で行い、メッシュ的な接続を実現する機能はどれか。

- [ ] A. bridge モードの動的ポートマッピング
- [x] B. Service Connect（Cloud Map + Envoy）
- [ ] C. host モードのホスト名解決
- [ ] D. NACL ベースのルーティング

> **解説**: Service Connect は Cloud Map と Envoy を組み合わせ、サービス名でのサービス間通信（メッシュ的）を提供する。
> **出典**: [ecs README #2 コアコンセプト](README.md#2-コアコンセプト)

## ecs-008
- type: single
- difficulty: medium
- domain: 2
- tags: [subnetting, nat, vpc-endpoint]

プライベートサブネットの ECS タスクが、外部インターネットと AWS サービス（ECR からの pull）の両方へ到達する必要がある。正しい構成はどれか。

- [ ] A. インターネットへも AWS サービスへも NAT Gateway のみで対応
- [x] B. 外部は NAT Gateway、ECR は ecr.api/ecr.dkr + S3 の VPC エンドポイント
- [ ] C. IGW をプライベートサブネットに直接アタッチ
- [ ] D. host モードに切り替えれば経路は不要

> **解説**: プライベートサブネットのタスクが外部へ出るには NAT Gateway、AWS サービス（ECR）へは VPC エンドポイント（api/dkr + S3）が必要。VPC エンドポイント化は NAT データ処理料の削減にもなる。
> **出典**: [ecs README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecs-009
- type: multi
- difficulty: hard
- domain: 1
- tags: [target-type, alb, nlb, awsvpc]

ECS タスクを ELB のターゲットに登録する際のターゲットタイプについて正しいものを2つ選べ。

- [x] A. awsvpc モードのタスクは ip ターゲットとして登録する
- [x] B. bridge モードの動的ポートのタスクは instance ターゲットとして登録する
- [ ] C. awsvpc モードのタスクは常に instance ターゲットになる
- [ ] D. host モードでは ELB 登録ができない
- [ ] E. Fargate タスクは instance ターゲットで登録する

> **解説**: awsvpc はタスク固有 IP を持つため ip ターゲット、bridge の動的ポートはノード経由のため instance ターゲットで登録する。Fargate は awsvpc 固定なので ip ターゲットになる。
> **出典**: [ecs README #5 他サービスとの連携](README.md#5-他サービスとの連携)

## ecs-010
- type: multi
- difficulty: medium
- domain: 4
- tags: [awsvpc, security-group, flow-logs, privatelink]

awsvpc モードを選ぶ理由として正しいものを2つ選べ。

- [x] A. タスク単位でセキュリティグループを分離できる
- [x] B. VPC フローログでタスクの IP 単位の通信を追跡できる
- [ ] C. ホストの ENI を共有してポートを節約できる
- [ ] D. 1 つのポートに複数タスクを同居できる
- [ ] E. ENI を一切消費しないため大量タスクに最適

> **解説**: awsvpc はタスクごとに ENI と VPC IP を持つため、タスク単位の SG 分離、フローログでの IP 追跡、PrivateLink/ピアリング越しの直接到達が可能。一方で ENI を消費するため密度には注意が必要。
> **出典**: [ecs README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)
</content>
