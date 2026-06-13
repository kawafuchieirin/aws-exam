---
service: eks
domain_default: 1
source: README.md
source_sha256: 4ac43b972f63a1e7453b545f3e8c18d7dcb01129efd1bfccb62fa0cca07fe4e7
generated: 2026-05-24
---

## eks-001
- type: single
- difficulty: medium
- domain: 1
- tags: [awsvpc, eni, transit-gateway]

Amazon EKS の VPC CNI プラグインによる Pod のネットワークモデルとして正しいものはどれか。

- [x] A. 各 Pod に VPC 内のルーティング可能な実 IP が割り当てられ、オーバーレイは使わない
- [ ] B. 各 Pod は VXLAN オーバーレイ上のプライベート IP を持つ
- [ ] C. Pod はノード IP を NAT 共有し固有 IP を持たない
- [ ] D. Pod IP はクラスタ内のみで VPC からはルーティング不可

> **解説**: VPC CNI はノードの ENI にセカンダリ IP（またはプレフィックス）を束ね、各 Pod に VPC ネイティブな実 IP を付与する。オーバーレイが無いため VPC からルーティング可能だが、Pod ごとに VPC の IP を消費する。
> **出典**: [eks README #1 概要](README.md#1-概要)

## eks-002
- type: single
- difficulty: hard
- domain: 1
- tags: [ip-exhaustion, awsvpc, enhanced-networking]

EKS クラスタで Pod 数を増やすと VPC の IPv4 が枯渇しがちである。RFC1918 空間を温存しつつノードあたりの Pod 密度を上げたい場合、最も適した手法はどれか。

- [x] A. プレフィックス委任（ENI に /28 を割り当てる）を有効化する
- [ ] B. すべてのノードを host ネットワークに切り替える
- [ ] C. NAT Gateway を AZ ごとに増設する
- [ ] D. instance ターゲットモードに変更する

> **解説**: プレフィックス委任は ENI に /28（16 アドレス）を割り当て、Pod 密度・起動速度を高め EC2 API 呼び出しを削減する。Linux のみで、既存ノードへの混在は非推奨のため新規ノードグループで移行する。
> **出典**: [eks README #4 IP 枯渇対策（最頻出）](README.md#4-ip-枯渇対策最頻出)

## eks-003
- type: single
- difficulty: hard
- domain: 1
- tags: [ip-exhaustion, cidr, awsvpc]

VPC のプライマリ CIDR（RFC1918）を使い切ったため、Pod を別の IP 空間から払い出して枯渇を回避したい。適切な組み合わせはどれか。

- [ ] A. プレフィックス委任のみ
- [x] B. セカンダリ CIDR（例 100.64.0.0/10）追加 + カスタムネットワーキング（ENIConfig）
- [ ] C. Security Groups for Pods
- [ ] D. ip ターゲットモードへの変更

> **解説**: VPC にセカンダリ CIDR（CG-NAT 帯など）を追加し、カスタムネットワーキング（ENIConfig CRD）で Pod をそのサブネットから払い出すと、プライマリ CIDR を温存できる。Pod 専用 SG も指定できる。
> **出典**: [eks README #4 IP 枯渇対策（最頻出）](README.md#4-ip-枯渇対策最頻出)

## eks-004
- type: single
- difficulty: medium
- domain: 1
- tags: [ipv6, ip-exhaustion, troubleshooting]

IPv4 アドレス枯渇を根本的に解決する AWS 推奨の方法はどれか。

- [ ] A. カスタムネットワーキング
- [ ] B. プレフィックス委任
- [x] C. IPv6 クラスタを作成する
- [ ] D. max-pods を下げる

> **解説**: IPv6 クラスタは Pod に IPv6 を割り当て IPv4 枯渇を根本解決する（AWS 推奨）。ただしクラスタ作成時に選択する必要があり、後から IPv4↔IPv6 の変更はできない。外部 IPv4 へは送信側 NAT で到達する。
> **出典**: [eks README #4 IP 枯渇対策（最頻出）](README.md#4-ip-枯渇対策最頻出)

## eks-005
- type: single
- difficulty: medium
- domain: 4
- tags: [eni]

特定の Pod から RDS へ Pod 単位の最小権限でセキュリティグループ制御したい。適切な機能はどれか。

- [x] A. Security Groups for Pods（trunk ENI + branch ENI）
- [ ] B. NACL で Pod の IP を個別に許可
- [ ] C. ノードのプライマリ ENI の SG を全 Pod 共通に設定
- [ ] D. instance ターゲットモード

> **解説**: Security Groups for Pods はノードに 1 つの trunk ENI と Pod ごとの branch ENI を使い、Pod 単位で SG を適用する。これにより Pod から RDS への最小権限アクセスが実現できる。
> **出典**: [eks README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## eks-006
- type: single
- difficulty: medium
- domain: 1
- tags: [alb, nlb, security-group]

AWS Load Balancer Controller のプロビジョニング挙動として正しいものはどれか。

- [x] A. Kubernetes Ingress は ALB、Service type=LoadBalancer は NLB を作成する
- [ ] B. Ingress は NLB、Service は ALB を作成する
- [ ] C. Ingress も Service も常に CLB を作成する
- [ ] D. Ingress は NAT Gateway を作成する

> **解説**: AWS Load Balancer Controller は Ingress に対して ALB、Service type=LoadBalancer に対して NLB をプロビジョンする。
> **出典**: [eks README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## eks-007
- type: single
- difficulty: hard
- domain: 1
- tags: [target-type, public-ip, awsvpc]

NLB/ALB が Pod の IP に直接トラフィックを転送し、ホップを削減して Fargate でも利用できるターゲットモードはどれか。

- [x] A. ip ターゲットモード
- [ ] B. instance ターゲットモード
- [ ] C. host ターゲットモード
- [ ] D. bridge ターゲットモード

> **解説**: ip ターゲットモードは LB が Pod IP へ直接転送しホップを削減する。SG は各 Pod の ENI で選択する。instance モードはノードの NodePort 経由で kube-proxy が転送する。Fargate はノードが無いため ip モード必須。
> **出典**: [eks README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## eks-008
- type: single
- difficulty: medium
- domain: 1
- tags: [awsvpc, eni, enhanced-networking]

EKS ノードあたりの Pod 数（max-pods）を決める基本要素として正しいものはどれか。

- [ ] A. クラスタの Kubernetes バージョンのみ
- [x] B. インスタンスタイプの ENI 数 × ENI あたり IP 数（から予約を引いた値）
- [ ] C. NAT Gateway の数
- [ ] D. ALB のターゲットグループ数

> **解説**: max-pods は (ENI 数 × ENI あたり IP 数) − 予約で決まりインスタンスタイプ依存。既定上限は 110/ノード（変更可）で、プレフィックス委任により大幅に増やせる。
> **出典**: [eks README #4 IP 枯渇対策（最頻出）](README.md#4-ip-枯渇対策最頻出)

## eks-009
- type: single
- difficulty: hard
- domain: 1
- tags: [eni, vpc-peering, transit-gateway, direct-connect]

VPC CNI で Pod が VPC ネイティブ IP を持つことの帰結として正しいものはどれか。

- [x] A. ピアリング/TGW/Direct Connect 越しに Pod へ直接到達できる（重複 CIDR は不可）
- [ ] B. Pod IP はオーバーレイのため外部からは到達不可
- [ ] C. Pod は常にノード IP を共有する
- [ ] D. Pod 間通信に必ず NAT が介在する

> **解説**: Pod が VPC の実 IP を持つため、ピアリング・Transit Gateway・Direct Connect 越しに Pod へ直接到達できる。ただし接続先と CIDR が重複していると到達不可になる。
> **出典**: [eks README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## eks-010
- type: multi
- difficulty: hard
- domain: 1
- tags: [ip-exhaustion, awsvpc, ipv6, cidr]

EKS の IPv4 枯渇対策に関する記述として正しいものを2つ選べ。

- [x] A. プレフィックス委任は IPv4 で /28、IPv6 で /80 を ENI に割り当てる
- [x] B. IPv6 クラスタはクラスタ作成時に選択し、後から IPv4↔IPv6 の変更はできない
- [ ] C. プレフィックス委任は Windows ノードのみサポートされる
- [ ] D. カスタムネットワーキングを使うとノードあたり Pod 数は必ず増える
- [ ] E. セカンダリ CIDR の追加には別途料金が発生する

> **解説**: プレフィックス委任は IPv4 /28・IPv6 /80 を割り当て Linux のみサポート（CNI v1.9.0 以上）。IPv6 はクラスタ作成時に選択し後から変更不可。カスタムネットワーキングはノードあたり Pod 数がやや減る場合があり、セカンダリ CIDR や IPv6 自体は無料。
> **出典**: [eks README #4 IP 枯渇対策（最頻出）](README.md#4-ip-枯渇対策最頻出)

## eks-011
- type: multi
- difficulty: medium
- domain: 4
- tags: [target-type, security-group, public-ip]

AWS Load Balancer Controller のターゲットモードとセキュリティグループの関係について正しいものを2つ選べ。

- [x] A. ip ターゲットモードでは SG を各 Pod の ENI で選択する
- [x] B. instance ターゲットモードでは SG をノードのプライマリ ENI で選択する
- [ ] C. ip ターゲットモードはノードの NodePort 経由で kube-proxy が転送する
- [ ] D. instance ターゲットモードは Fargate で必須となる
- [ ] E. どちらのモードでも SG は NACL で代替する

> **解説**: ip モードは Pod IP に直接転送し SG は Pod の ENI で選択、instance モードは NodePort 経由で kube-proxy が転送し SG はノードのプライマリ ENI で選択する。Fargate はノードが無いため ip モード必須。
> **出典**: [eks README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)
</content>
