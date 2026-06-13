---
service: site-to-site-vpn
domain_default: 1
source: README.md
source_sha256: 6971b00a6ac15712c33801d31a3a855beb6a2e01a6fb3917a8598cd12ea28c31
generated: 2026-05-24
---

## site-to-site-vpn-001
- type: single
- difficulty: easy
- domain: 1
- tags: [vpn, high-availability]

1 つの Site-to-Site VPN 接続に含まれるトンネル数として正しいものはどれか。

- [ ] A. 1 本
- [x] B. 2 本（冗長のため、別々の AWS 側エンドポイントに終端）
- [ ] C. 4 本
- [ ] D. CGW の数だけ

> **解説**: 1 つの VPN 接続には冗長のため自動的に 2 本のトンネルが含まれ、別々の AWS 側エンドポイントに終端する。高可用の前提として CGW 側で両トンネルを設定する必要がある。
> **出典**: [site-to-site-vpn README #3 アーキテクチャ](README.md#3-アーキテクチャ2トンネル冗長)

## site-to-site-vpn-002
- type: single
- difficulty: hard
- domain: 1
- tags: [ecmp, enhanced-networking, transit-gateway]

標準トンネルの帯域上限（約 1.25 Gbps）を超える帯域を VPN で実現したい。正しい方法はどれか。

- [ ] A. 1 つの VPN 接続のトンネルを 4 本に増やす
- [x] B. 複数の VPN 接続を TGW 終端で ECMP 束ね（動的ルーティング）し帯域を集約する
- [ ] C. VGW 終端で静的ルーティングを使う
- [ ] D. MTU を 9001 に上げる

> **解説**: 標準トンネルは最大 1.25 Gbps/140,000 pps。これを超えるには複数 VPN 接続を ECMP で束ねる。要件は TGW で「VPN ECMP support」を有効化＋動的ルーティング（BGP）。静的や VGW では不可。N 接続で約 1.25 Gbps × N。
> **出典**: [site-to-site-vpn README #4 VGW 終端 vs TGW 終端](README.md#4-vgw-終端-vs-tgw-終端最頻出)

## site-to-site-vpn-003
- type: single
- difficulty: medium
- domain: 1
- tags: [transit-gateway, vpn]

Accelerated Site-to-Site VPN や Private IP VPN over DX を利用するために必要な終端はどれか。

- [ ] A. VGW 終端
- [x] B. TGW 終端
- [ ] C. Client VPN
- [ ] D. Internet Gateway

> **解説**: Accelerated VPN、Private IP VPN over DX、ECMP 帯域集約はいずれも TGW 終端でのみ可能。VGW 終端は単一 VPC への手軽な接続向けで、これらの機能は使えない。
> **出典**: [site-to-site-vpn README #4 VGW 終端 vs TGW 終端](README.md#4-vgw-終端-vs-tgw-終端最頻出)

## site-to-site-vpn-004
- type: single
- difficulty: medium
- domain: 1
- tags: [route-table, bgp, ecmp]

ECMP による帯域集約に必須のルーティング方式はどれか。

- [ ] A. 静的ルーティング
- [x] B. 動的ルーティング（BGP）
- [ ] C. ポリシーベースルーティング
- [ ] D. デフォルトルートのみ

> **解説**: ECMP は動的ルーティング（BGP）かつ TGW 終端時のみ可能。静的ルーティングでは ECMP はできない。CGW デバイスが BGP に対応していることも前提となる。
> **出典**: [site-to-site-vpn README #3 アーキテクチャ](README.md#3-アーキテクチャ2トンネル冗長)

## site-to-site-vpn-005
- type: single
- difficulty: hard
- domain: 1
- tags: [vpn]

Accelerated Site-to-Site VPN の説明として正しいものはどれか。

- [ ] A. インターネット経由のままトンネル数を倍増させる
- [x] B. AWS グローバルネットワーク（Global Accelerator 基盤）経由でインターネット混雑を回避し、TGW 終端のみで有効化できる
- [ ] C. VGW 終端で有効化する
- [ ] D. データ転送が無料になる

> **解説**: Accelerated VPN は VPN トラフィックを最寄りエッジから AWS グローバルバックボーンへ載せ、インターネット混雑を回避してレイテンシ/ジッターを改善する。TGW 終端のみで有効化でき、アクセラレータ 2 基を自動管理（追加課金）。
> **出典**: [site-to-site-vpn README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## site-to-site-vpn-006
- type: single
- difficulty: hard
- domain: 1
- tags: [vpn, hybrid]

複数の拠点（CGW）を単一 VGW に BGP 接続し、拠点同士を AWS 経由でハブ＆スポーク接続したい。利用する構成はどれか。

- [x] A. VPN CloudHub
- [ ] B. TGW Peering
- [ ] C. Private IP VPN over DX
- [ ] D. ECMP

> **解説**: VPN CloudHub は単一 VGW に複数 CGW（拠点）を BGP 接続し、各拠点のプレフィックスを他拠点へ再広告することで拠点間メッシュを AWS 上で実現する。各拠点は異なる ASN を使う必要がある。
> **出典**: [site-to-site-vpn README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## site-to-site-vpn-007
- type: single
- difficulty: hard
- domain: 4
- tags: [vpn, direct-connect]

Direct Connect 上を、インターネットを経由せずプライベート IP で暗号化接続したい。利用する構成はどれか。

- [ ] A. パブリック VIF 上の標準 VPN
- [x] B. Private IP VPN over DX（Transit VIF 上にプライベート IP で IPsec、TGW 終端）
- [ ] C. VPN CloudHub
- [ ] D. Accelerated VPN

> **解説**: Private IP VPN over DX は DX の Transit VIF 上にプライベート IP で IPsec を張り、インターネット非経由で暗号化＋プライベートを両立する。TGW 終端が前提。
> **出典**: [site-to-site-vpn README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## site-to-site-vpn-008
- type: single
- difficulty: medium
- domain: 3
- tags: [mtu]

Site-to-Site VPN の MTU に関して正しいものはどれか。

- [ ] A. ジャンボフレーム（9001）に対応している
- [x] B. MTU は 1446 バイト（MSS 1406）でジャンボフレーム非対応、PMTUD 非対応のため MSS クランプが必要
- [ ] C. MTU は 8500 バイト
- [ ] D. PMTUD により自動調整される

> **解説**: VPN の MTU は 1446 バイト（MSS 1406）。ジャンボフレーム非対応かつ PMTUD 非対応のため、フラグメント由来の通信不良を避けるには MSS クランプが必須。
> **出典**: [site-to-site-vpn README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## site-to-site-vpn-009
- type: single
- difficulty: medium
- domain: 1
- tags: [ipv6, transit-gateway]

Site-to-Site VPN で IPv6（インナー/アウター）を利用できる条件として正しいものはどれか。

- [ ] A. VGW 終端で利用できる
- [x] B. TGW / Cloud WAN 終端でのみ利用でき、1 接続で IPv4 と IPv6 を同時に使うことはできない
- [ ] C. すべての終端で IPv4 と IPv6 を同時に使える
- [ ] D. CGW の ASN を 4-byte にすれば使える

> **解説**: インナー/アウター IPv6 は TGW / Cloud WAN 終端のみで、VGW は IPv6 非対応。1 接続で IPv4 と IPv6 を同時には使えない。
> **出典**: [site-to-site-vpn README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## site-to-site-vpn-010
- type: single
- difficulty: hard
- domain: 3
- tags: [direct-connect, longest-prefix]

Direct Connect をプライマリ、Site-to-Site VPN をバックアップにする構成で、同一プレフィックスを両方で広告した場合の挙動として正しいものはどれか。

- [ ] A. VPN が常に優先される
- [x] B. TGW のルート評価で DX 伝播が VPN 伝播より優先され、DX 断時に VPN 経路へ自動切替される
- [ ] C. 両経路が常に ECMP で同時利用される
- [ ] D. 手動切替が必要

> **解説**: TGW のルート評価では DX 伝播 > VPN 伝播。DX 正常時は DX のみ採用（プライマリ経路のみ表示）され、DX 断時に VPN 経路がバックアップとして現れて自動切替される。
> **出典**: [site-to-site-vpn README #8 よくある設計パターン](README.md#8-よくある設計パターン)

## site-to-site-vpn-011
- type: multi
- difficulty: hard
- domain: 1
- tags: [transit-gateway, use-case-fit]

TGW 終端の VPN が VGW 終端より優れる点として正しいものを 2 つ選べ。

- [x] A. ECMP による帯域集約ができる
- [ ] B. 単一 VPC への接続がより簡単になる
- [x] C. Accelerated VPN / Private IP VPN over DX が利用できる
- [ ] D. CGW デバイスに BGP が不要になる
- [ ] E. トンネル数が 4 本になる

> **解説**: TGW 終端は ECMP 帯域集約、Accelerated VPN、Private IP VPN over DX、多数 VPC 集約に対応する。VGW 終端は単一 VPC への手軽な接続向け。トンネル数は終端に関係なく 2 本、ECMP には BGP が必要。
> **出典**: [site-to-site-vpn README #4 VGW 終端 vs TGW 終端](README.md#4-vgw-終端-vs-tgw-終端最頻出)

## site-to-site-vpn-012
- type: multi
- difficulty: medium
- domain: 1
- tags: [bgp, route-table, use-case-fit]

Site-to-Site VPN の設計に関して正しいものを 2 つ選べ。

- [x] A. CGW の ASN は 2-byte（1〜65535）で設定する
- [ ] B. 静的ルーティングでも ECMP が利用できる
- [x] C. VPN CloudHub では各拠点が異なる ASN を使用する
- [ ] D. 高可用には片方のトンネルだけ設定すればよい
- [ ] E. VGW の ASN は 2-byte に限定される

> **解説**: CGW の ASN は 2-byte（1〜65535）、VGW は 4-byte（1〜2147483647）設定可。CloudHub では各拠点が異なる ASN を使う。ECMP は動的ルーティングが必須で静的では不可。高可用には CGW 側で両トンネルを設定する必要がある。
> **出典**: [site-to-site-vpn README #2 コアコンセプト](README.md#2-コアコンセプト)
