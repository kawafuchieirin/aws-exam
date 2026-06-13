---
service: vpc
domain_default: 1
source: README.md
source_sha256: 8c20e732796a93b1386f24bcffbac8559ae0207927aba41e947bd8b829d832cb
generated: 2026-05-24
---

## vpc-001
- type: single
- difficulty: easy
- domain: 4
- tags: [stateful-stateless]

特定の送信元 IP アドレスからの通信をサブネット単位で「拒否」したい。最も適切な手段はどれか。

- [ ] A. セキュリティグループに拒否ルールを追加する
- [x] B. ネットワーク ACL に Deny ルールを追加する
- [ ] C. ルートテーブルにブラックホールルートを追加する
- [ ] D. IAM ポリシーで送信元 IP を制限する

> **解説**: セキュリティグループは「許可」ルールしか持てず Deny できない。ネットワーク ACL はステートレスで Deny ルールを持てるため、特定 IP の遮断は NACL で行う。
> **出典**: [VPC README #3 SG vs NACL](README.md#3-セキュリティ制御-sg-vs-nacl最頻出)

## vpc-002
- type: single
- difficulty: medium
- domain: 4
- tags: [stateful-stateless]

ネットワーク ACL を使う際、戻りトラフィックについて正しいものはどれか。

- [ ] A. ステートフルなので戻りは自動的に許可される
- [x] B. ステートレスなのでエフェメラルポートの戻りを明示的に許可する必要がある
- [ ] C. 戻りトラフィックは常にすべて許可される
- [ ] D. 戻りトラフィックはセキュリティグループが処理するため NACL では不要

> **解説**: NACL はステートレスのため、インバウンドを許可しても戻り（アウトバウンド）を自動許可しない。エフェメラルポート 1024–65535 のアウトバウンド許可を忘れると通信が成立しない。
> **出典**: [VPC README #3](README.md#3-セキュリティ制御-sg-vs-nacl最頻出)

## vpc-003
- type: single
- difficulty: medium
- domain: 1
- tags: [nat, high-availability]

複数 AZ にまたがるプライベートサブネットのインターネットアウトバウンドを、AZ 障害に強い構成で実現したい。推奨はどれか。

- [ ] A. 1 つの NAT Gateway を全 AZ で共有する
- [x] B. AZ ごとに NAT Gateway を作り、各 AZ のルートを自 AZ の NAT に向ける
- [ ] C. NAT インスタンスを単一 AZ に冗長構成で配置する
- [ ] D. Internet Gateway を AZ ごとに作成する

> **解説**: NAT Gateway は単一 AZ 内で冗長化されるが AZ をまたがない。共有すると NAT の AZ 障害で他 AZ がインターネット断になる。AZ ごとに配置するのがベストプラクティス。
> **出典**: [VPC README #5 NAT Gateway](README.md#5-nat-gateway-詳細頻出)

## vpc-004
- type: single
- difficulty: hard
- domain: 1
- tags: [nat, route-table, transit-gateway]

オンプレミスから Site-to-Site VPN 経由で AWS 側の NAT Gateway を使ってインターネットへ抜けたい。正しいものはどれか。

- [ ] A. Virtual Private Gateway (VGW) 経由で NAT Gateway にルーティングできる
- [x] B. VGW 経由では不可。Transit Gateway を使えばルーティングできる
- [ ] C. VPC ピアリング経由で NAT Gateway にインバウンドできる
- [ ] D. NAT Gateway はオンプレからのトラフィックを一切扱えない

> **解説**: VGW 経由の VPN/Direct Connect から NAT Gateway へはルーティングできないが、Transit Gateway を使えば可能。また VPC ピアリング越しに NAT へインバウンドすることはできない。
> **出典**: [VPC README #5 経路制約](README.md#5-nat-gateway-詳細頻出)

## vpc-005
- type: single
- difficulty: medium
- domain: 3
- tags: [flow-logs, monitoring]

VPC フローログについて正しいものはどれか。

- [ ] A. パケットのペイロード（中身）まで記録できる
- [x] B. IP トラフィックのメタデータを記録し、ACCEPT/REJECT を判別できる
- [ ] C. CloudWatch Logs にしか出力できない
- [ ] D. リアルタイムにパケットを書き換えできる

> **解説**: フローログはメタデータ（送信元/宛先 IP・ポート・プロトコル・バイト数・ACCEPT/REJECT 等）を記録する。中身の解析にはトラフィックミラーリングが必要。出力先は CloudWatch Logs / S3 / Data Firehose。
> **出典**: [VPC README #7 監視](README.md#7-監視トラブルシュート第3分野で頻出)

## vpc-006
- type: single
- difficulty: hard
- domain: 3
- tags: [flow-logs, nat]

NAT やセカンダリ IP の背後で、フローログから「本来の宛先 IP」を知りたい。使うべきフィールドはどれか。

- [ ] A. dstaddr
- [x] B. pkt-dstaddr
- [ ] C. srcaddr
- [ ] D. interface-id

> **解説**: `dstaddr` は ENI のプライマリ IP を表すことがあるため、NAT 前/セカンダリ IP 等の実際の宛先は拡張フィールド `pkt-dstaddr` で取得する。
> **出典**: [VPC README #7 フローログの要点](README.md#7-監視トラブルシュート第3分野で頻出)

## vpc-007
- type: multi
- difficulty: medium
- domain: 3
- tags: [monitoring, reachability-analyzer, traffic-mirroring]

「2 点間の到達可否を静的に解析する」用途と「パケットの中身を解析する」用途に対し、適切なツールの組み合わせはどれか。2 つ選べ。

- [x] A. 到達性検証には Reachability Analyzer を使う
- [x] B. パケット内容の解析には VPC トラフィックミラーリングを使う
- [ ] C. 到達性検証には VPC フローログを使う
- [ ] D. パケット内容の解析には Reachability Analyzer を使う
- [ ] E. 到達性検証にはトラフィックミラーリングを使う

> **解説**: Reachability Analyzer は実トラフィック不要で経路の到達可否を静的解析する。パケットのペイロード解析（IDS/IPS 等）にはトラフィックミラーリングを使う。
> **出典**: [VPC README #7](README.md#7-監視トラブルシュート第3分野で頻出)

## vpc-008
- type: single
- difficulty: hard
- domain: 1
- tags: [cidr, ip-exhaustion, privatelink]

2 つの組織の VPC が同一 CIDR で重複している。重複したまま、片方の単一サービスへ接続させたい。最適なのはどれか。

- [ ] A. VPC ピアリング
- [ ] B. Transit Gateway アタッチメント
- [x] C. AWS PrivateLink（インターフェイスエンドポイント）
- [ ] D. VPC 間で同一ルートテーブルを共有

> **解説**: ピアリング/TGW は CIDR 重複を許容しない。PrivateLink は一方向で重複 CIDR でも接続でき、単一サービスへの最小権限アクセスに適する。
> **出典**: [VPC README #6 CIDR 重複対策](README.md#6-ip-アドレッシングと-cidr-設計)

## vpc-009
- type: single
- difficulty: easy
- domain: 1
- tags: [vpc-endpoint, cost]

S3 へのアクセスで NAT Gateway のデータ処理料を回避しつつコストを抑えたい。適切なのはどれか。

- [x] A. S3 用の Gateway エンドポイント（無料）を使う
- [ ] B. S3 用の Interface エンドポイントを使う
- [ ] C. NAT Gateway を増設する
- [ ] D. Internet Gateway を直接ルーティングする

> **解説**: S3/DynamoDB は Gateway エンドポイント（ルートテーブル方式・無料）でアクセスでき、NAT を経由しないためデータ処理料を削減できる。
> **出典**: [VPC README #8 VPCエンドポイント](README.md#8-vpc-エンドポイント)

## vpc-010
- type: single
- difficulty: medium
- domain: 1
- tags: [eni, enhanced-networking]

密結合な HPC / 分散機械学習で、OS バイパスによる超低レイテンシ通信が必要。適切なネットワークインターフェイスはどれか。

- [ ] A. ENI
- [ ] B. ENA
- [x] C. EFA
- [ ] D. NAT Gateway

> **解説**: EFA（Elastic Fabric Adapter）は OS バイパスで超低レイテンシを実現し、MPI/NCCL 等の集団通信に最適。高スループットの一般用途は ENA、通常は ENI。
> **出典**: [VPC README #4 ネットワークインターフェイス](README.md#4-ネットワークインターフェイスの種類)

## vpc-011
- type: single
- difficulty: hard
- domain: 3
- tags: [mtu]

ジャンボフレーム設定後、一部の通信が無応答になった。経路に MTU 1500 区間があると疑われる。確認すべきことはどれか。

- [x] A. PMTUD のための ICMP（Type3 Code4 "Fragmentation Needed"）が遮断されていないか
- [ ] B. セキュリティグループの Deny ルール
- [ ] C. NAT Gateway の同時接続数上限
- [ ] D. Route 53 のヘルスチェック設定

> **解説**: 経路上の最小 MTU に PMTUD で調整されるが、ICMP の "Fragmentation Needed" を遮断するとパスがブラックホール化して無応答になる。ICMP を通す必要がある。
> **出典**: [VPC README #9 MTU/ジャンボフレーム](README.md#9-mtu--ジャンボフレーム)

## vpc-012
- type: multi
- difficulty: medium
- domain: 1
- tags: [cidr, ip-exhaustion, vpc-sharing]

VPC の IP 枯渇およびマルチアカウントの IP 効率化への対策として適切なものはどれか。2 つ選べ。

- [x] A. セカンダリ CIDR を追加してアドレス空間を拡張する
- [x] B. RAM による VPC 共有でサブネットを他アカウントに共有し、1 VPC に集約する
- [ ] C. プライマリ CIDR を後から拡大変更する
- [ ] D. サブネットの予約アドレス 5 個を再利用する
- [ ] E. VPC ピアリングで他 VPC の空き CIDR を自 VPC のアドレスとして流用する

> **解説**: プライマリ CIDR は変更不可。対策はセカンダリ CIDR の追加や、RAM による VPC 共有でのアドレス集約。予約 5 アドレスは利用不可で、ピアリングは別 VPC のアドレス空間を自 VPC に流用する仕組みではない。
> **出典**: [VPC README #6 CIDR 設計](README.md#6-ip-アドレッシングと-cidr-設計)
