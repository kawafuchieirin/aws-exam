---
service: routing-bgp
domain_default: 0
source: README.md
source_sha256: 0658c21a2f3c6cf8bf945e29a164c46b373b854d3ce6d74a83dc87923ede58dc
generated: 2026-05-24
---

## routing-bgp-001
- type: single
- difficulty: easy
- domain: 0
- tags: [longest-prefix, route-table]

ルートテーブルに `10.0.0.0/16 → TGW`、`10.0.1.0/24 → VPC ピアリング`、`0.0.0.0/0 → IGW` がある。宛先 `10.0.1.50` 宛てのトラフィックはどこへ転送されるか（計算ドリル）。

- [ ] A. TGW
- [x] B. VPC ピアリング
- [ ] C. IGW
- [ ] D. ローカル

> **解説**: 最長プレフィックス一致により、最も具体的な /24（10.0.1.0/24 → VPC ピアリング）が選ばれる。/16 や /0 はより一般的なので負ける。
> **出典**: [routing-bgp README #2.1 ロンゲストプレフィックスマッチ](README.md#21-ロンゲストプレフィックスマッチ最長一致)

## routing-bgp-002
- type: single
- difficulty: easy
- domain: 0
- tags: [bgp]

BGP の LOCAL_PREF 属性について正しいものはどれか。

- [x] A. 値が大きいほど優先され、AS からの出口（アウトバウンド）制御に使う
- [ ] B. 値が小さいほど優先され、インバウンド制御に使う
- [ ] C. 経由する AS の数を表す
- [ ] D. 隣接 AS への入口のヒントを与える

> **解説**: LOCAL_PREF は AS 内で共有され、大きいほど優先される。自 AS からどの経路で外へ出るか（アウトバウンド）を制御する。小さいほど優先で入口ヒントなのは MED。
> **出典**: [routing-bgp README #2.4 BGP の主要属性と経路選択順序](README.md#24-bgp-の主要属性と経路選択順序頻出)

## routing-bgp-003
- type: single
- difficulty: medium
- domain: 0
- tags: [bgp, longest-prefix]

次の 4 経路が宛先 `192.168.10.5` に存在する。BGP の選択ロジックで最終的に選ばれる経路はどれか（計算ドリル）。経路1: 192.168.0.0/16, LOCAL_PREF 200, AS_PATH [65001] ／ 経路2: 192.168.10.0/24, LOCAL_PREF 100, AS_PATH [65001 65002] ／ 経路3: 192.168.10.0/24, LOCAL_PREF 200, AS_PATH [65003 65004 65005] ／ 経路4: 192.168.10.0/24, LOCAL_PREF 200, AS_PATH [65006]

- [ ] A. 経路1
- [ ] B. 経路2
- [ ] C. 経路3
- [x] D. 経路4

> **解説**: まず最長一致で /24 が /16 に勝ち経路1脱落。次に LOCAL_PREF（大きいほど優先）で 100 の経路2脱落。残る経路3・4 は AS_PATH の短さ（3 対 1）で経路4が選ばれる。
> **出典**: [routing-bgp README #3 例題 A](README.md#例題-a-最長一致--local_pref--as_path-の順で選ぶ)

## routing-bgp-004
- type: single
- difficulty: medium
- domain: 0
- tags: [bgp, direct-connect]

オンプレが同じ `10.0.0.0/16` を Direct Connect と Site-to-Site VPN の両方から AWS へ広報している。平常時に AWS から見て優先される経路はどれか（計算ドリル）。

- [x] A. Direct Connect
- [ ] B. Site-to-Site VPN
- [ ] C. ランダムにロードバランスされる
- [ ] D. プレフィックス長で決まるため判定不能

> **解説**: プレフィックス長が同じなので最長一致では決まらず、AWS の伝播経路優先順位で Direct Connect が VPN に優先される。VPN は DX 障害時のバックアップになる。
> **出典**: [routing-bgp README #3 例題 B](README.md#例題-b-direct-connect-と-vpn-の優先同一プレフィックス)

## routing-bgp-005
- type: single
- difficulty: medium
- domain: 0
- tags: [bgp, direct-connect]

2 本の Direct Connect 回線のうち、回線 B をバックアップにしてインバウンド方向（AWS からオンプレへ）を回線 A に寄せたい。定石となる手法はどれか。

- [ ] A. 回線 A の広報に AS_PATH プリペンドを付ける
- [x] B. 回線 B の広報に AS_PATH プリペンドを付けて非優先にする
- [ ] C. 回線 A の LOCAL_PREF を下げる
- [ ] D. 回線 B の MED を下げる

> **解説**: AS_PATH プリペンドは AS_PATH を長くして経路を非優先にする。バックアップにしたい回線 B にプリペンドする。優先したい A にプリペンドするのは逆効果。インバウンド制御は AS_PATH プリペンドが定石。
> **出典**: [routing-bgp README #3 例題 C](README.md#例題-c-as_path-プリペンドでインバウンドを誘導)

## routing-bgp-006
- type: single
- difficulty: easy
- domain: 0
- tags: [route-propagation, route-table]

VGW や TGW が BGP で学習した経路をルートテーブルへ自動で書き込む機能の名称はどれか。

- [ ] A. ロンゲストマッチ
- [x] B. ルート伝播（route propagation）
- [ ] C. ブラックホール
- [ ] D. ECMP

> **解説**: ルート伝播を有効化すると、オンプレから広報されたプレフィックスが手動入力なしでルートテーブルに現れる。
> **出典**: [routing-bgp README #2.6 経路伝播](README.md#26-経路伝播route-propagation)

## routing-bgp-007
- type: single
- difficulty: medium
- domain: 0
- tags: [ecmp, transit-gateway]

複数の Site-to-Site VPN トンネルを束ねて 1.25 Gbps を超える帯域を得たい。正しい構成はどれか。

- [x] A. ECMP を有効にした Transit Gateway に複数トンネルをアタッチする
- [ ] B. VGW で VPN の ECMP を有効にする
- [ ] C. 1 本の VPN トンネルの帯域上限を引き上げる
- [ ] D. VPC ピアリングでトンネルを束ねる

> **解説**: VPN 1 接続は最大 1.25 Gbps。VGW は VPN ECMP 非対応のため、ECMP を有効にした TGW に複数トンネルを束ねて帯域を集約する。
> **出典**: [routing-bgp README #2.7 ECMP](README.md#27-ecmp等コストマルチパス)

## routing-bgp-008
- type: single
- difficulty: medium
- domain: 0
- tags: [blackhole, transit-gateway]

特定の CIDR 宛てトラフィックを意図的に破棄したい。TGW ルートテーブルで使う仕組みはどれか。

- [ ] A. ルート伝播を無効化する
- [x] B. ブラックホールルートを設定する
- [ ] C. LOCAL_PREF を 0 にする
- [ ] D. MED を最大にする

> **解説**: ブラックホールルートは宛先を破棄するルート。TGW ルートテーブルで明示的に設定して特定 CIDR を遮断できる。アタッチメント削除で経路が自動的に blackhole 状態になることもある。
> **出典**: [routing-bgp README #2.8 ブラックホールルート](README.md#28-ブラックホールルート)

## routing-bgp-009
- type: multi
- difficulty: medium
- domain: 0
- tags: [bgp, longest-prefix]

BGP の経路選択について正しい記述を 2 つ選べ。

- [x] A. 最長プレフィックス一致は BGP 属性の比較よりも先に適用される
- [ ] B. LOCAL_PREF は値が小さいほど優先される
- [x] C. MED は値が小さいほど優先され、同一隣接 AS への入口ヒントに使う
- [ ] D. AS_PATH は長いほど優先される
- [ ] E. iBGP で学習した経路は eBGP より優先される

> **解説**: A と C が正しい。LOCAL_PREF は大きいほど優先（B 誤り）、AS_PATH は短いほど優先（D 誤り）、eBGP が iBGP より優先（E 誤り）。最長一致は属性比較の前段に位置する。
> **出典**: [routing-bgp README #2.4 BGP の主要属性と経路選択順序](README.md#24-bgp-の主要属性と経路選択順序頻出)

## routing-bgp-010
- type: multi
- difficulty: hard
- domain: 0
- tags: [route-table, longest-prefix, route-propagation]

AWS のルートテーブルにおける経路の優先順位について正しいものを 2 つ選べ。

- [x] A. まず最長プレフィックス一致が適用され、その後に優先順位が比較される
- [ ] B. 伝播（BGP）経路は同一プレフィックス長の静的ルートより優先される
- [x] C. 同一プレフィックス長では静的（手動）ルートが伝播ルートより優先される
- [ ] D. ローカルルートはより具体的な静的ルートがあれば上書きできる
- [ ] E. VGW は VPN の ECMP に対応している

> **解説**: A と C が正しい。AWS では同一プレフィックス長で ローカル > 静的 > 伝播 の順（B は逆で誤り）。ローカルルートは最優先で削除・上書き不可（D 誤り）。VGW は VPN ECMP 非対応（E 誤り）。
> **出典**: [routing-bgp README #2.2 ルートテーブル](README.md#22-ルートテーブルaws)
