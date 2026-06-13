---
service: ip-addressing-subnetting
domain_default: 0
source: README.md
source_sha256: 97b855196c9bb061993c8d8a710829a73a6df44f9f33083c8e8ea095919b3e3a
generated: 2026-05-24
---

## ip-addressing-subnetting-001
- type: single
- difficulty: easy
- domain: 0
- tags: [cidr, subnetting]

`10.0.0.0/24` の AWS サブネットで、EC2 などに割り当て可能な利用可能ホスト数はいくつか。

- [ ] A. 256
- [ ] B. 254
- [x] C. 251
- [ ] D. 250

> **解説**: /24 の総アドレス数は 256。AWS は各サブネットで先頭 4 + 末尾 1 の計 5 アドレスを予約するため、256 − 5 = 251 が利用可能。254（−2）は一般ネットワークの数え方で AWS では誤り。
> **出典**: [ip-addressing-subnetting README #2.3 予約 5 アドレス](README.md#23-aws-が予約する-5-アドレス最重要ひっかけ頻出)

## ip-addressing-subnetting-002
- type: single
- difficulty: easy
- domain: 0
- tags: [cidr]

`/26` のサブネットマスクを正しく表しているものはどれか。

- [ ] A. 255.255.255.0
- [ ] B. 255.255.255.224
- [x] C. 255.255.255.192
- [ ] D. 255.255.255.240

> **解説**: /26 のホスト部は 6 ビットでブロックサイズは 64。第4オクテットのマスク値は 256 − 64 = 192。224 は /27、240 は /28、0 は /24。
> **出典**: [ip-addressing-subnetting README #2.1 CIDR 表記とサブネットマスク](README.md#21-cidr-表記とサブネットマスク)

## ip-addressing-subnetting-003
- type: single
- difficulty: medium
- domain: 0
- tags: [cidr, subnetting]

`10.0.0.0/22` の AWS サブネットで利用可能なホスト数はいくつか（計算ドリル）。

- [ ] A. 1,024
- [ ] B. 1,022
- [x] C. 1,019
- [ ] D. 1,021

> **解説**: ホスト部は 32 − 22 = 10 ビット、総アドレス数 = 2^10 = 1,024。AWS 予約 5 を引いて 1,024 − 5 = 1,019。1,022 は −2 の一般ネットワーク値、1,024 は予約を引き忘れた値。
> **出典**: [ip-addressing-subnetting README #3 例題 A](README.md#例題-a-10000022-のホスト数)

## ip-addressing-subnetting-004
- type: single
- difficulty: medium
- domain: 0
- tags: [subnetting]

`10.0.0.0/24` を `/26` に分割すると、いくつのサブネットができるか（計算ドリル）。

- [ ] A. 2
- [x] B. 4
- [ ] C. 8
- [ ] D. 16

> **解説**: /24 の総アドレス 256 を /26 の総アドレス 64 で割ると 256 ÷ 64 = 4 個。プレフィックスが 2 ビット伸びる（2^2 = 4）と考えてもよい。
> **出典**: [ip-addressing-subnetting README #3 例題 B](README.md#例題-b-1000024-を-2626-に分割する)

## ip-addressing-subnetting-005
- type: single
- difficulty: medium
- domain: 0
- tags: [subnetting]

`10.0.0.0/24` を `/26` で 4 分割したとき、IP アドレス `10.0.0.200` が属するサブネットはどれか（計算ドリル）。

- [ ] A. 10.0.0.0/26
- [ ] B. 10.0.0.64/26
- [ ] C. 10.0.0.128/26
- [x] D. 10.0.0.192/26

> **解説**: ブロックサイズは 64。境界は 0, 64, 128, 192。200 は 192 以上 256 未満なので 10.0.0.192/26（範囲 .192–.255）に属する。
> **出典**: [ip-addressing-subnetting README #3 例題 C](README.md#例題-c-あるip-1000200-はどの-2626-サブネットに属するか)

## ip-addressing-subnetting-006
- type: single
- difficulty: medium
- domain: 0
- tags: [subnetting, cidr]

要件として 100 台のホストを収容する AWS サブネットを 1 つ作りたい。予約 5 アドレスを考慮した上で、過不足の少ない最小プレフィックスはどれか（計算ドリル）。

- [ ] A. /26
- [x] B. /25
- [ ] C. /24
- [ ] D. /27

> **解説**: 100 台 + 予約 5 = 最低 105 アドレス必要。/26 は 64（不足）、/25 は 128（128 − 5 = 123 で十分かつ最小）、/24 は 256 で過剰。よって /25。
> **出典**: [ip-addressing-subnetting README #3 例題 D](README.md#例題-d-vlsm-で-1000024-を要件に合わせて分割)

## ip-addressing-subnetting-007
- type: single
- difficulty: easy
- domain: 0
- tags: [cidr, ip-exhaustion]

VPC のプライマリ CIDR が IP 枯渇しつつある。アドレス空間を拡張する正しい方法はどれか。

- [ ] A. プライマリ CIDR を /16 から /15 へ広げる
- [x] B. セカンダリ CIDR ブロックを追加する
- [ ] C. VPC を作り直して大きい CIDR を割り当てる
- [ ] D. サブネットのプレフィックスを縮めて広げる

> **解説**: プライマリ CIDR は変更不可。拡張はセカンダリ CIDR の追加で行う。100.64.0.0/10 などを足して枯渇を回避する手法もある。
> **出典**: [ip-addressing-subnetting README #5 よくある誤解](README.md#5-よくある誤解ひっかけ)

## ip-addressing-subnetting-008
- type: single
- difficulty: medium
- domain: 0
- tags: [ipv6, nat]

VPC で IPv6 のプライベートサブネットからインターネットへのアウトバウンド通信のみを許可したい。正しい構成はどれか。

- [ ] A. NAT Gateway を IPv6 で構成する
- [x] B. Egress-Only Internet Gateway を使う
- [ ] C. Internet Gateway を双方向で使う
- [ ] D. NAT インスタンスを IPv6 対応で配置する

> **解説**: IPv6 には NAT の概念が無いため NAT Gateway/インスタンスは IPv6 アウトバウンドに使えない。アウトバウンド専用には Egress-Only IGW を使い、外部からの接続開始を防ぐ。
> **出典**: [ip-addressing-subnetting README #2.6 IPv6 基礎](README.md#26-ipv6-基礎)

## ip-addressing-subnetting-009
- type: multi
- difficulty: medium
- domain: 0
- tags: [cidr, subnetting, public-ip]

AWS の IP アドレッシングについて正しい記述を 2 つ選べ。

- [x] A. VPC の CIDR は /16 から /28 の範囲で指定できる
- [ ] B. /28 の AWS サブネットの利用可能ホストは 14 である
- [x] C. 各 AWS サブネットでは先頭 4 と末尾 1 の計 5 アドレスが予約される
- [ ] D. IPv6 アドレスにはプライベートとパブリックの区別があり NAT が必要
- [ ] E. 172.16.0.0/12 のプライベート範囲は 172.32.x.x まで含む

> **解説**: A と C が正しい。B は 16 − 5 = 11 が正解（−2 で 14 は誤り）。D は IPv6 に NAT は無い。E は 172.16〜172.31 まで（172.32 は範囲外）。
> **出典**: [ip-addressing-subnetting README #2.3 予約 5 アドレス](README.md#23-aws-が予約する-5-アドレス最重要ひっかけ頻出)

## ip-addressing-subnetting-010
- type: multi
- difficulty: hard
- domain: 0
- tags: [cidr, ip-exhaustion, route-table]

複数の VPC を VPC ピアリングや Transit Gateway で相互接続する設計上の制約として正しいものを 2 つ選べ。

- [x] A. 接続する VPC 間で CIDR が重複してはならない
- [ ] B. CIDR が重複していてもロンゲストマッチで自動的に解決される
- [x] C. 組織全体のアドレス計画で重複を避けるのが TGW 集約の前提になる
- [ ] D. ピアリングでは重複 CIDR でも NAT で必ず回避できる
- [ ] E. 重複していても両 VPC のルートテーブルを手動編集すれば常に通信できる

> **解説**: A と C が正しい。CIDR が重複するとピアリング/TGW で宛先経路が一意に決まらず通信が成立しない。重複は事前のアドレス計画で避ける必要があり、ロンゲストマッチや手動編集で常に救えるわけではない。
> **出典**: [ip-addressing-subnetting README #4 AWSサービスとの接続](README.md#4-aws-サービスとの接続)
