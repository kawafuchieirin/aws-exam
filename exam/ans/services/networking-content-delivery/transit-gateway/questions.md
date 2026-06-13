---
service: transit-gateway
domain_default: 1
source: README.md
source_sha256: c3f72665752cc863a968e12aba347d6de8918b91a75e9754ed1a2952297df7de
generated: 2026-05-24
---

## transit-gateway-001
- type: single
- difficulty: hard
- domain: 1
- tags: [route-propagation]

TGW の Association と Propagation の違いとして正しいものはどれか。

- [x] A. Association はアタッチメントが参照するルートテーブル（入口）、Propagation は経路を注入する先（出口）
- [ ] B. Association は経路を注入する先、Propagation は参照するルートテーブル
- [ ] C. どちらもアタッチメントごとに複数のルートテーブルに設定できる
- [ ] D. どちらも 1 アタッチメント＝1 ルートテーブルに限定される

> **解説**: Association は「このアタッチメントから出たパケットをどのルートテーブルで引くか」（1 アタッチメント＝1 ルートテーブルのみ）。Propagation は「このアタッチメントの経路をどのルートテーブルに自動登録するか」（複数可）。両者を分離してセグメンテーションを実現する。
> **出典**: [transit-gateway README #2 コアコンセプト](README.md#2-コアコンセプト)

## transit-gateway-002
- type: single
- difficulty: hard
- domain: 1
- tags: [security-group, route-table]

本番系（Prod）と開発系（Dev）の VPC 群を相互不達にしつつ、共有サービス VPC へは双方向到達させたい。TGW での実現方法はどれか。

- [ ] A. 全 VPC を単一ルートテーブルに association する
- [x] B. Prod/Dev を別ルートテーブルに association し、共有サービス VPC だけを両 RT に propagation する
- [ ] C. VPC ピアリングをフルメッシュで張る
- [ ] D. ブラックホールルートを全アタッチメントに設定する

> **解説**: 各環境を別の TGW ルートテーブルに association し、共有サービス VPC のみ両 RT へ propagation することで、Prod/Dev 間は経路なし（相互不達）にしつつ共有サービスへは双方向到達できる。
> **出典**: [transit-gateway README #8 よくある設計パターン](README.md#8-よくある設計パターン)

## transit-gateway-003
- type: single
- difficulty: hard
- domain: 1
- tags: [transit-gateway, gwlb]

複数 AZ にまたがるステートフルな検査アプライアンス（FW/IDS）で、戻りトラフィックが別 AZ のアプライアンスに着いて破棄される。解決策はどれか。

- [ ] A. クロスゾーン負荷分散を ON にする
- [x] B. Inspection VPC のアタッチメントでアプライアンスモードを有効化する
- [ ] C. ブラックホールルートを追加する
- [ ] D. TGW Peering を使う

> **解説**: 通常モードでは TGW は発信元 AZ を維持しようとし、複数 AZ にまたがると戻りが別 AZ のアプライアンスへ着き破棄される。アプライアンスモードを有効化するとフローハッシュで同一 ENI を選び対称ルーティングを保証する。Inspection VPC には TGW を 1 つだけ接続する。
> **出典**: [transit-gateway README #4 アプライアンスモード](README.md#4-アプライアンスモード対称フロー保証)

## transit-gateway-004
- type: single
- difficulty: hard
- domain: 1
- tags: [longest-prefix, hybrid]

TGW のルート評価で、同一宛先 CIDR に対し DX 伝播と S2S VPN 伝播がある場合の優先順位として正しいものはどれか。

- [ ] A. S2S VPN 伝播が優先される
- [x] B. DX Gateway 伝播が S2S VPN 伝播より優先される
- [ ] C. 常に ECMP で両方使われる
- [ ] D. AS_PATH の長い方が優先される

> **解説**: 最長プレフィックスマッチが最優先。同一 CIDR・異種別では 静的 > プレフィックスリスト > VPC 伝播 > DX Gateway 伝播 > Connect 伝播 > … > S2S VPN 伝播 の順。よって DX 伝播が VPN 伝播より優先され、DX をプライマリにできる。
> **出典**: [transit-gateway README #3 アーキテクチャ](README.md#3-アーキテクチャハブスポーク)

## transit-gateway-005
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-peering, route-table]

TGW Peering（リージョン間/アカウント間）の特徴として正しいものはどれか。

- [ ] A. 動的ルーティングと ECMP に対応
- [x] B. 静的ルートのみ対応（動的ルーティング・ECMP 非対応）で、AES-256 による二重暗号化が行われる
- [ ] C. 重複 CIDR を許容する
- [ ] D. GRE トンネルで接続する

> **解説**: TGW Peering は静的ルートのみで動的ルーティング・ECMP 非対応。リージョン間 Peering は仮想ネットワーク層と物理リンクの双方で AES-256 が掛かり二重暗号化となる。GRE＋BGP は TGW Connect の仕組み。
> **出典**: [transit-gateway README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## transit-gateway-006
- type: single
- difficulty: hard
- domain: 1
- tags: [transit-gateway, vpn, bgp]

SD-WAN 仮想アプライアンスを TGW に統合し、GRE＋BGP で接続したい。利用するアタッチメント種別はどれか。

- [ ] A. VPC アタッチメント
- [x] B. TGW Connect アタッチメント
- [ ] C. Peering アタッチメント
- [ ] D. VPN アタッチメント

> **解説**: TGW Connect は既存の VPC または DX アタッチメントをトランスポートとし、その上に GRE トンネル（Connect peer）を張り BGP で経路交換する。SD-WAN 統合の標準。静的ルート非対応・伝播のみで、Connect peer ごとに BGP セッションを 2 本確立する。
> **出典**: [transit-gateway README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## transit-gateway-007
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-peering, transit-gateway]

VPC ピアリングではなく TGW を選ぶ理由として最も適切なものはどれか。

- [ ] A. ピアリングは重複 CIDR を許容するが TGW は許容しないため
- [x] B. ピアリングは非推移的（A-B, B-C があっても A-C 不可）だが TGW は推移的でハブ集約できるため
- [ ] C. ピアリングはハイブリッド接続を集約できるが TGW はできないため
- [ ] D. ピアリングの方が大規模に向くため

> **解説**: VPC ピアリングは非推移的でフルメッシュが必要、TGW は推移的でハブ＆スポーク集約ができ大規模に向く。重複 CIDR はどちらも不可。少数 VPC・最低レイテンシ・低コストならピアリング、多数 VPC・推移接続・ハイブリッド集約なら TGW。
> **出典**: [transit-gateway README #9 VPC ピアリング / VGW との使い分け](README.md#9-vpc-ピアリング--vgw-との使い分け)

## transit-gateway-008
- type: single
- difficulty: medium
- domain: 3
- tags: [blackhole, troubleshooting]

特定の CIDR 宛トラフィックを TGW でドロップしたい（例: VPC 間通信を遮断しつつインターネット出口は共有）。利用する機能はどれか。

- [ ] A. アプライアンスモード
- [x] B. ブラックホールルート
- [ ] C. プレフィックスリスト
- [ ] D. TGW Peering

> **解説**: ブラックホールルートは特定 CIDR をドロップする。VPC 間通信を遮断しつつ共有のインターネット出口は維持する、といった用途に使う。
> **出典**: [transit-gateway README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## transit-gateway-009
- type: single
- difficulty: hard
- domain: 3
- tags: [mtu]

TGW の MTU に関して正しいものはどれか。

- [ ] A. 全アタッチメントで 1500 バイト
- [x] B. VPC/DX/Connect/Peering 間は 8500 バイト、VPN は 1500 バイト
- [ ] C. 全アタッチメントで 9001 バイト
- [ ] D. VPN は 8500 バイト

> **解説**: TGW の MTU は VPC/DX/Connect/Peering 間が 8500、VPN が 1500。全パケットで MSS クランプが行われ、PMTUD は VPC/Connect 受信のみ対応（VPN/DX/Peering は非対応）。
> **出典**: [transit-gateway README #7 制約・上限・コスト](README.md#7-制約上限コスト暗記推奨)

## transit-gateway-010
- type: single
- difficulty: medium
- domain: 3
- tags: [monitoring, reachability-analyzer]

TGW で構成したグローバルネットワークを可視化し、2 点間の経路解析・到達性検証を行いたい。利用する機能はどれか。

- [ ] A. VPC Reachability Analyzer のみ
- [x] B. Network Manager / Route Analyzer
- [ ] C. CloudWatch Logs Insights
- [ ] D. DNS Firewall

> **解説**: Network Manager はグローバルネットワークを可視化し、Route Analyzer で 2 点間の経路解析・到達性検証ができる。TGW を中心としたハイブリッド/マルチ VPC ネットワークの設計・トラブルシュートに使う。
> **出典**: [transit-gateway README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## transit-gateway-011
- type: multi
- difficulty: hard
- domain: 1
- tags: [ecmp, transit-gateway]

TGW で ECMP に対応するアタッチメント/条件として正しいものを 2 つ選べ。

- [x] A. VPN（動的ルーティングのみ）
- [x] B. TGW Connect
- [ ] C. VPC アタッチメント
- [ ] D. TGW Peering
- [ ] E. VPN Concentrator

> **解説**: ECMP に対応するのは VPN（動的のみ）と Connect。VPC・Peering・VPN Concentrator は非対応。異種アタッチメント間や異 ASN 間（AS-Path Relax 非対応）でも ECMP はできない。
> **出典**: [transit-gateway README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## transit-gateway-012
- type: multi
- difficulty: hard
- domain: 1
- tags: [network-firewall, use-case-fit]

集中検査（Inspection VPC ＋アプライアンスモード）の設計に関して正しいものを 2 つ選べ。

- [x] A. Spoke RT の 0.0.0.0/0 を Inspection VPC へ向け、検査後に TGW へ戻して宛先へ転送する
- [x] B. ステートフル検査のためアプライアンスモードを Inspection VPC のアタッチメントで有効化する
- [ ] C. Inspection VPC には複数 TGW を接続してフロー状態を共有させる
- [ ] D. East-West は検査できず North-South のみ検査できる
- [ ] E. アプライアンスモードは VPN アタッチメントで有効化する

> **解説**: Spoke RT のデフォルトルートを Inspection VPC へ向け、検査後 TGW 経由で宛先へ転送する。ステートフル検査の対称フロー保証にはアプライアンスモードを Inspection VPC のアタッチメントで有効化する。複数 TGW はフロー状態を共有しないため Inspection VPC には TGW を 1 つだけ接続する。East-West/North-South の双方を一元検査できる。
> **出典**: [transit-gateway README #8 よくある設計パターン](README.md#8-よくある設計パターン)
