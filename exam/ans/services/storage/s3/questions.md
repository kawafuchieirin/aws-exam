---
service: s3
domain_default: 4
source: README.md
source_sha256: 24b03a54ba7d9dd5b557688e2d5167b21997c754183cf945371f32acbadbb829
generated: 2026-05-24
---

## s3-001
- type: single
- difficulty: easy
- domain: 1
- tags: [vpc-endpoint, cost]

VPC 内の EC2 から、インターネットも NAT も経由せず無料で S3 へプライベートアクセスしたい。適切なのはどれか。

- [x] A. S3 用の Gateway エンドポイントを使い、ルートテーブルに S3 プレフィックスリスト宛ルートを追加する
- [ ] B. S3 用の Interface エンドポイントを使う
- [ ] C. NAT Gateway 経由でインターネットから S3 にアクセスする
- [ ] D. Internet Gateway を直接ルーティングする

> **解説**: Gateway エンドポイントは無料で、ルートテーブルに S3 プレフィックスリスト宛のルートを追加するだけで VPC 内からプライベートにアクセスできる。Interface は課金があり、NAT/IGW 経由はインターネット転送料が発生する。
> **出典**: [s3 README #3 VPC エンドポイントによるプライベートアクセス](README.md#3-vpc-エンドポイントによるプライベートアクセス最重要)

## s3-002
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-endpoint, hybrid]

オンプレミスから Direct Connect 経由で、S3 へプライベートにアクセスしたい。適切なエンドポイントはどれか。

- [ ] A. Gateway エンドポイント
- [x] B. Interface エンドポイント（PrivateLink）
- [ ] C. NAT Gateway
- [ ] D. Egress-Only Internet Gateway

> **解説**: Gateway エンドポイントの接続は VPC 外へ拡張できず、VPN/ピアリング/TGW/Direct Connect の先からは到達不可。オンプレからのプライベートアクセスには ENI を持つ Interface エンドポイント（PrivateLink）が必須。
> **出典**: [s3 README #3 使い分け / 経路制約](README.md#3-vpc-エンドポイントによるプライベートアクセス最重要)

## s3-003
- type: single
- difficulty: hard
- domain: 1
- tags: [vpc-endpoint, route-table, transit-gateway]

Gateway エンドポイント経由の S3 アクセスについて、経路制約として正しいものはどれか。

- [ ] A. Transit Gateway 越しの他 VPC からも Gateway エンドポイントで S3 に到達できる
- [x] B. VPN/ピアリング/TGW/Direct Connect の先のリソースは Gateway エンドポイントを使えない
- [ ] C. Gateway エンドポイントはオンプレからのアクセスを ENI 経由で受ける
- [ ] D. Gateway エンドポイントは複数リージョンの S3 にまたがって使える

> **解説**: Gateway エンドポイントの接続は VPC の外へ拡張できない。TGW/VPN/ピアリング/DX の先のリソースからは到達できず、その場合は Interface エンドポイントを使う必要がある。リージョン内のみ有効。
> **出典**: [s3 README #3 重要な経路制約](README.md#3-vpc-エンドポイントによるプライベートアクセス最重要)

## s3-004
- type: single
- difficulty: medium
- domain: 4
- tags: [iam-policy, source-condition]

特定の VPC エンドポイント経由のアクセスのみを許可し、それ以外を拒否するバケットポリシーの条件キーはどれか。

- [ ] A. `aws:SourceIp`
- [x] B. `aws:SourceVpce`
- [ ] C. `aws:PrincipalOrgID`
- [ ] D. `aws:SecureTransport`

> **解説**: `aws:SourceVpce` は指定 VPC エンドポイント経由「以外」を拒否でき、特定経路のみ許可する制御に使う。`aws:SourceIp` は VPC エンドポイント経由のリクエストには使えない点が引っかけ。
> **出典**: [s3 README #4 バケットポリシーによる経路制限](README.md#4-バケットポリシーによる経路制限)

## s3-005
- type: single
- difficulty: hard
- domain: 4
- tags: [iam-policy, source-condition, vpc-endpoint, use-case-fit]

VPC エンドポイント経由のリクエストに対して送信元 IP で制限したい。バケットポリシーで使う条件キーとして正しいものはどれか。

- [ ] A. `aws:SourceIp` をそのまま使う
- [x] B. `aws:VpcSourceIp` を使う
- [ ] C. `aws:SourceVpc` を IP レンジで指定する
- [ ] D. `aws:SourceVpce` に IP を記述する

> **解説**: `aws:SourceIp` は VPC エンドポイント経由のリクエストでは機能しない。エンドポイント経由のプライベート送信元 IP で制限するには `aws:VpcSourceIp` を使う。よくある引っかけポイント。
> **出典**: [s3 README #4 バケットポリシーによる経路制限](README.md#4-バケットポリシーによる経路制限)

## s3-006
- type: single
- difficulty: medium
- domain: 4
- tags: [iam-policy, source-condition]

同一 VPC 内に複数の S3 エンドポイントがあり、どのエンドポイント経由でも「その VPC からのアクセス」だけを許可したい。最も便利な条件キーはどれか。

- [ ] A. `aws:SourceVpce`
- [x] B. `aws:SourceVpc`
- [ ] C. `aws:SourceIp`
- [ ] D. `aws:SecureTransport`

> **解説**: `aws:SourceVpc` は指定 VPC からのリクエスト「以外」を拒否する。エンドポイント単位ではなく VPC 単位で制限できるため、同一 VPC に複数エンドポイントがある場合に便利。
> **出典**: [s3 README #4 バケットポリシーによる経路制限](README.md#4-バケットポリシーによる経路制限)

## s3-007
- type: single
- difficulty: medium
- domain: 4
- tags: [encryption, tls]

S3 への通信で TLS（HTTPS）を強制したい。バケットポリシーの定石はどれか。

- [ ] A. `aws:SecureTransport == true` を Deny する
- [x] B. `aws:SecureTransport == false` を Deny する
- [ ] C. `aws:SourceVpce` を Allow する
- [ ] D. SSE-KMS を有効化する

> **解説**: `aws:SecureTransport` が `false`（= 非 TLS）のリクエストを Deny することで TLS を強制できる。SSE-KMS は保存時暗号化であり、転送中暗号化の強制とは別物。
> **出典**: [s3 README #5 転送中暗号化](README.md#5-ネットワークログの保存先--転送中暗号化)

## s3-008
- type: single
- difficulty: medium
- domain: 4
- tags: [security-group, nacl, route-table]

Gateway エンドポイント経由の S3 アクセスを許可するセキュリティグループ／NACL の設定として正しいものはどれか。

- [ ] A. SG・NACL ともに S3 マネージドプレフィックスリストを参照できる
- [x] B. SG は S3 マネージドプレフィックスリストを参照、NACL はプレフィックスリスト不可なので IP レンジを記述する
- [ ] C. SG・NACL ともに IP レンジ直書きのみ可能
- [ ] D. SG は不要で NACL だけ設定すればよい

> **解説**: セキュリティグループはアウトバウンドで S3 マネージドプレフィックスリストを参照して許可できる。NACL はプレフィックスリストを参照できないため IP レンジを記述する必要がある。
> **出典**: [s3 README #3 SG/NACL](README.md#3-vpc-エンドポイントによるプライベートアクセス最重要)

## s3-009
- type: single
- difficulty: easy
- domain: 3
- tags: [monitoring, flow-logs]

S3 が保存先となるネットワーク監視データとして適切でないものはどれか。

- [ ] A. VPC フローログ
- [ ] B. ELB（ALB/NLB）アクセスログ
- [x] C. リアルタイムにパケットのペイロードを書き換えたデータ
- [ ] D. AWS CloudTrail / Network Firewall ログ

> **解説**: S3 はフローログ・ELB/CloudFront アクセスログ・CloudTrail・Network Firewall ログ・Resolver クエリログなどの保存先になる。パケットペイロードのリアルタイム書き換えはトラフィックミラーリング等の領域で S3 の役割ではない。
> **出典**: [s3 README #5 ネットワークログの保存先](README.md#5-ネットワークログの保存先--転送中暗号化)

## s3-010
- type: single
- difficulty: medium
- domain: 1
- tags: [cost, vpc-endpoint, nat]

VPC 内アプリの S3 アクセスでコストを最小化する最頻出の最適化パターンはどれか。

- [ ] A. Interface エンドポイントを使ってデータ処理料を払う
- [x] B. Gateway エンドポイントを使い NAT Gateway のデータ処理料を回避する
- [ ] C. NAT Gateway を増設してスループットを上げる
- [ ] D. S3 を別リージョンに移してリージョン間転送する

> **解説**: VPC 内からの S3 アクセスを無料の Gateway エンドポイントにすると NAT を経由しないため、NAT Gateway のデータ処理料を回避できる。これが ANS 試験の最頻出コスト最適化パターン。
> **出典**: [s3 README #7 制約・上限・コスト](README.md#7-制約上限コスト)

## s3-011
- type: multi
- difficulty: medium
- domain: 1
- tags: [vpc-endpoint, hybrid]

VPC 内からは無料で、オンプレからもプライベートに S3 へアクセスしたいハイブリッド構成で適切な設計はどれか。2 つ選べ。

- [x] A. VPC 内アクセス用に Gateway エンドポイントを使う
- [x] B. オンプレ/TGW 越しのアクセス用に Interface エンドポイントを使う
- [ ] C. すべてのアクセスを単一の Gateway エンドポイントに集約する
- [ ] D. オンプレからは Gateway エンドポイントに VPN でルーティングする
- [ ] E. VPC 内アクセスにも Interface エンドポイントを使いデータ処理料を払う

> **解説**: Gateway は VPC 外へ拡張できないためオンプレには使えない。VPC 内は無料の Gateway、オンプレ/TGW 越しは Interface と振り分けることでデータ処理料を最小化できる。プライベート DNS の扱いを工夫すると VPC 内アクセスを Gateway に寄せられる。
> **出典**: [s3 README #3 使い分け / コスト最適化](README.md#3-vpc-エンドポイントによるプライベートアクセス最重要)

## s3-012
- type: multi
- difficulty: hard
- domain: 4
- tags: [iam-policy, source-condition, use-case-fit]

VPC エンドポイント経由のアクセス制御に関する記述のうち正しいものはどれか。2 つ選べ。

- [x] A. `aws:SourceVpce` で指定エンドポイント経由以外を拒否できる
- [x] B. エンドポイント経由のリクエストを送信元 IP で制限するには `aws:VpcSourceIp` を使う
- [ ] C. `aws:SourceIp` は VPC エンドポイント経由のリクエストにも有効である
- [ ] D. `aws:SourceVpc` はエンドポイント単位での制限に使う
- [ ] E. これらの Deny ポリシーはマネジメントコンソール経由のアクセスはブロックしない

> **解説**: `aws:SourceVpce` は経路を限定、`aws:VpcSourceIp` はエンドポイント経由の送信元 IP 制限に使う。`aws:SourceIp` はエンドポイント経由では機能せず、`aws:SourceVpc` は VPC 単位の制限。これらの Deny はコンソール経由のアクセスもブロックする点に注意。
> **出典**: [s3 README #4 バケットポリシーによる経路制限](README.md#4-バケットポリシーによる経路制限)
