---
service: privatelink
domain_default: 1
source: README.md
source_sha256: 9c53cd0b9a9d41baa8da0e044c362b997749c0ea0be5637dd4a52ed320e2d660
generated: 2026-05-24
---

## privatelink-001
- type: single
- difficulty: hard
- domain: 1
- tags: [ip-exhaustion, nat, vpc-peering]

CIDR が完全に重複している 2 つの組織の VPC を、双方向ではなく一方向（消費側→提供側）で特定サービスのみ接続したい。最適な方式はどれか。

- [x] A. AWS PrivateLink（Interface エンドポイント + エンドポイントサービス）
- [ ] B. VPC ピアリング
- [ ] C. Transit Gateway
- [ ] D. VPN 接続

> **解説**: PrivateLink は提供側 NLB が IP NAT を行うため、CIDR が完全に重複していても接続できる。接続は本質的に一方向（消費→提供）で、特定サービス 1 つだけを最小露出で公開できる。ピアリング/TGW は重複 CIDR を許容せず、IP レベルで双方向に広く接続する。
> **出典**: [privatelink README #3 アーキテクチャ](README.md#3-アーキテクチャinterface-エンドポイント--エンドポイントサービス)

## privatelink-002
- type: single
- difficulty: medium
- domain: 1
- tags: [privatelink, use-case-fit]

エンドポイントサービス（提供側）のフロントに必須なロードバランサはどれか。

- [ ] A. ALB（直接指定）
- [x] B. NLB または GWLB
- [ ] C. CLB
- [ ] D. いずれも不要

> **解説**: エンドポイントサービスは NLB または GWLB が必須。ALB は直接指定できないが、NLB のターゲットに ALB を置く構成は可能。NLB はサービス公開、GWLB は仮想アプライアンス（FW/IDS）連携に使う。
> **出典**: [privatelink README #3 アーキテクチャ](README.md#3-アーキテクチャinterface-エンドポイント--エンドポイントサービス)

## privatelink-003
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-endpoint, cost]

VPC 内から S3 へプライベートにアクセスし、コストを最小化したい（オンプレからの利用は要件にない）。最適なエンドポイントはどれか。

- [x] A. Gateway エンドポイント
- [ ] B. Interface エンドポイント（PrivateLink）
- [ ] C. NAT Gateway 経由
- [ ] D. VPC ピアリング

> **解説**: S3/DynamoDB は Gateway エンドポイントが対応し、ルートテーブルにマネージドプレフィックスリスト経由のルートを追加するだけで無料。Interface エンドポイントは時間課金＋データ処理課金が発生する。コスト最小なら Gateway。
> **出典**: [privatelink README #5 Gateway エンドポイント vs Interface エンドポイント](README.md#5-gateway-エンドポイント-vs-interface-エンドポイント最頻出)

## privatelink-004
- type: single
- difficulty: hard
- domain: 1
- tags: [vpc-endpoint, hybrid]

オンプレミスから Direct Connect/VPN 経由で S3 にプライベートアクセスしたい。適切なエンドポイントはどれか。

- [ ] A. Gateway エンドポイント
- [x] B. Interface エンドポイント
- [ ] C. NAT Gateway
- [ ] D. Internet Gateway

> **解説**: Gateway エンドポイントはルート起点が VPC 内に必要なため、オンプレからは利用できない。オンプレ（DX/VPN）から S3 へプライベートアクセスするには Interface エンドポイントを使い、ENI のプライベート IP へ到達させる。
> **出典**: [privatelink README #5 Gateway エンドポイント vs Interface エンドポイント](README.md#5-gateway-エンドポイント-vs-interface-エンドポイント最頻出)

## privatelink-005
- type: single
- difficulty: hard
- domain: 4
- tags: [proxy-protocol]

PrivateLink 経由で接続したとき、提供側のアプリが見る送信元 IP は何か。実 IP を取得するにはどうするか。

- [ ] A. 消費側の実 IP がそのまま見える
- [x] B. NLB ノードのプライベート IP が見える。実 IP/エンドポイント ID が必要なら Proxy Protocol v2 を有効化する
- [ ] C. 提供側の IGW の IP が見える
- [ ] D. 常に 0.0.0.0 になる

> **解説**: NLB が NAT を行うため、提供側アプリが見る送信元 IP は NLB ノードのプライベート IP（消費側の実 IP ではない）。実 IP やエンドポイント ID が必要なら NLB で Proxy Protocol v2 を有効化する。
> **出典**: [privatelink README #3 アーキテクチャ](README.md#3-アーキテクチャinterface-エンドポイント--エンドポイントサービス)

## privatelink-006
- type: single
- difficulty: medium
- domain: 4
- tags: [vpc-endpoint, least-privilege]

S3 Gateway エンドポイント経由のアクセスを特定バケットの読み取りのみに絞り、データ流出経路を限定したい。利用する仕組みはどれか。

- [x] A. エンドポイントポリシー
- [ ] B. セキュリティグループの Deny ルール
- [ ] C. ネットワーク ACL
- [ ] D. ルートテーブルのブラックホール

> **解説**: エンドポイントポリシーは Interface/Gateway エンドポイントに付与する IAM リソースポリシーで、どのプリンシパルがどのリソースに何をできるかを制限する。例えば特定バケットへの s3:GetObject のみ許可し、データ流出経路を絞れる。
> **出典**: [privatelink README #4 エンドポイントポリシーとアクセス制御](README.md#4-エンドポイントポリシーとアクセス制御)

## privatelink-007
- type: single
- difficulty: medium
- domain: 4
- tags: [multi-account, iam-policy]

エンドポイントサービスの提供側が、消費側からの接続を手動で承認できるようにするには何を有効化するか。

- [ ] A. プライベート DNS
- [x] B. 接続承認（Acceptance required）
- [ ] C. クロスゾーン負荷分散
- [ ] D. エンドポイントポリシー

> **解説**: 提供側は接続承認（Acceptance required）を有効化すると、消費側からの接続リクエストを手動承認できる。許可プリンシパル（アカウント/IAM ロール/ARN）も明示的に登録する。
> **出典**: [privatelink README #4 エンドポイントポリシーとアクセス制御](README.md#4-エンドポイントポリシーとアクセス制御)

## privatelink-008
- type: single
- difficulty: medium
- domain: 2
- tags: [vpc-endpoint, dns]

Interface エンドポイントのプライベート DNS を利用してサービス正規名でアクセスするための VPC 設定の前提はどれか。

- [ ] A. VPC でフロー ログを有効化していること
- [x] B. VPC で enableDnsSupport と enableDnsHostnames を有効化していること
- [ ] C. パブリックサブネットにエンドポイントを置くこと
- [ ] D. NAT Gateway があること

> **解説**: プライベート DNS は消費側 VPC の Route 53 Resolver にサービス正規名をエンドポイント ENI の IP へ解決させる仕組み。前提として VPC で enableDnsSupport と enableDnsHostnames を有効化している必要がある。
> **出典**: [privatelink README #7 プライベート DNS](README.md#7-プライベート-dns)

## privatelink-009
- type: single
- difficulty: hard
- domain: 1
- tags: [transit-gateway, use-case-fit]

多数の顧客 VPC（一部は CIDR 重複）に対し、自社の 1 つのサービスだけをプライベート公開し、VPC が増えてもルート管理を増やしたくない。最適な方式はどれか。

- [x] A. PrivateLink（1 つのエンドポイントサービスで公開）
- [ ] B. 各顧客と VPC ピアリングを張る
- [ ] C. Transit Gateway で全顧客 VPC を集約
- [ ] D. 顧客ごとに VPN を張る

> **解説**: PrivateLink なら提供側は 1 つのエンドポイントサービスで公開し、各顧客は自 VPC に Interface エンドポイントを作るだけ。CIDR 重複を気にせず、ルート管理不要でスケールする。ピアリング/TGW は重複 CIDR を許容せずルート管理も増える。
> **出典**: [privatelink README #6 ピアリング / TGW との使い分け](README.md#6-ピアリング--tgw-との使い分け頻出)

## privatelink-010
- type: single
- difficulty: medium
- domain: 1
- tags: [gwlb, network-firewall]

各 VPC のトラフィックを集中型のファイアウォール/IDS アプライアンス層へ透過的に転送したい。PrivateLink を用いた構成として正しいものはどれか。

- [ ] A. 各 VPC に Interface エンドポイント（NLB ベース）を配置
- [x] B. GWLB をエンドポイントサービスとして公開し、各 VPC に GWLB エンドポイント（GWLBe）を配置
- [ ] C. 各 VPC に Gateway エンドポイントを配置
- [ ] D. ALB をエンドポイントサービスとして公開

> **解説**: 集中型インスペクションでは Security VPC の GWLB をエンドポイントサービスとして公開し、各 Spoke VPC に GWLB エンドポイント（GWLBe）を配置して GENEVE で検査層へ透過転送する。GWLBe は AZ・サービスあたり 1 つ。
> **出典**: [privatelink README #10 よくある設計パターン](README.md#10-よくある設計パターン)

## privatelink-011
- type: multi
- difficulty: hard
- domain: 1
- tags: [vpc-endpoint, use-case-fit]

Interface エンドポイント（PrivateLink）が Gateway エンドポイントと異なる点として正しいものを 2 つ選べ。

- [x] A. ENI とプライベート IP を VPC 内に作成する
- [ ] B. S3 / DynamoDB のみを対象とする
- [x] C. オンプレ（DX/VPN）から到達できる
- [ ] D. 無料でデータ転送料も発生しない
- [ ] E. ルートテーブルにプレフィックスリスト経由のルートを追加して使う

> **解説**: Interface エンドポイントは ENI＋プライベート IP を作り、オンプレから到達でき、時間課金＋データ処理課金が発生する。S3/DynamoDB のみ対象・無料・ルートテーブル方式・オンプレ不可は Gateway エンドポイントの特徴。
> **出典**: [privatelink README #5 Gateway エンドポイント vs Interface エンドポイント](README.md#5-gateway-エンドポイント-vs-interface-エンドポイント最頻出)

## privatelink-012
- type: multi
- difficulty: medium
- domain: 1
- tags: [use-case-fit, quotas]

PrivateLink に関して正しいものを 2 つ選べ。

- [x] A. 1 つの NLB は 1 つのエンドポイントサービスにのみ紐付けられる
- [ ] B. 1 つのエンドポイントサービスには NLB を 1 つしか紐付けられない
- [x] C. Interface エンドポイントはクロスリージョン接続が可能（NLB ベースのサービスのみ）
- [ ] D. 接続は提供側から消費側へ開始できる
- [ ] E. ALB を直接エンドポイントサービスに指定できる

> **解説**: 1 NLB が紐付けられるエンドポイントサービスは 1 つ（逆に 1 サービスは複数 NLB 可）。Interface エンドポイントは NLB ベースのサービスに限りクロスリージョン接続が可能。接続は消費側→提供側の一方向で、提供側からは開始できない。ALB は直接指定不可。
> **出典**: [privatelink README #9 制約・上限・コスト](README.md#9-制約上限コスト)
