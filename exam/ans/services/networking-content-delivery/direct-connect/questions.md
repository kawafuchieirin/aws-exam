---
service: direct-connect
domain_default: 1
source: README.md
source_sha256: 6b08b118a07fa5b99b2cd2a6fa2f6fc80e0b821f3aefd12ad2705c196f8d1ac9
generated: 2026-05-24
---

## direct-connect-001
- type: single
- difficulty: medium
- domain: 1
- tags: [direct-connect]

オンプレミスから複数アカウント・複数リージョンの多数の VPC へ、Transit Gateway 経由で集約接続したい。使用すべき VIF はどれか。

- [ ] A. Private VIF
- [ ] B. Public VIF
- [x] C. Transit VIF（DXGW → TGW）
- [ ] D. Hosted VIF

> **解説**: Transit VIF は DXGW を介して TGW に接続し、多数 VPC・マルチアカウント・マルチリージョンを集約できる。Private VIF は VGW/DXGW で VPC へ、Public VIF は S3 等の AWS パブリックサービスへ接続する。
> **出典**: [direct-connect README #3 仮想インターフェイス](README.md#3-仮想インターフェイスvif三種)

## direct-connect-002
- type: single
- difficulty: medium
- domain: 1
- tags: [direct-connect, vpc-endpoint]

S3 や DynamoDB などの AWS パブリックサービスへ、全リージョン向けにプライベート経路（インターネット非経由）でアクセスしたい。使用すべき VIF はどれか。

- [ ] A. Private VIF
- [x] B. Public VIF
- [ ] C. Transit VIF
- [ ] D. VPN VIF

> **解説**: Public VIF はパブリック IP を使い、S3・DynamoDB 等の AWS パブリックサービスへ全リージョンでアクセスできる。広告経路は最大 1,000 で、全広告に NO_EXPORT が付与され推移ルーティングは不可。
> **出典**: [direct-connect README #3 仮想インターフェイス](README.md#3-仮想インターフェイスvif三種)

## direct-connect-003
- type: single
- difficulty: hard
- domain: 1
- tags: [bgp, routing-policy]

複数の Private VIF で AWS→オンプレの戻りトラフィックを Active/Active（負荷分散・ECMP）にしたい。オンプレ広告に付けるべき BGP コミュニティはどれか。

- [ ] A. 全 VIF に `7224:7300`
- [x] B. 全 VIF に同じ `7224:7200`（Medium）
- [ ] C. 一方に `7224:7300`、他方に `7224:7100`
- [ ] D. 全 VIF に `7224:9300`

> **解説**: LOCAL_PREF コミュニティが同一（例 `7224:7200` Medium）でプレフィックス長・AS_PATH・MED も等しいと ECMP で負荷分散される（ASN は一致不要）。`7224:7300`/`7224:7100` の組み合わせは Active/Passive 用。
> **出典**: [direct-connect README #4 BGP ルーティングとトラフィック制御](README.md#4-bgp-ルーティングとトラフィック制御最頻出)

## direct-connect-004
- type: single
- difficulty: hard
- domain: 1
- tags: [bgp, failover]

DX を Active/Passive（フェイルオーバ）構成にし、AWS→オンプレの戻りトラフィックをアクティブ側へ寄せたい。アクティブ側とパッシブ側に付けるべき LOCAL_PREF コミュニティの組み合わせはどれか。

- [x] A. アクティブ `7224:7300`（High） / パッシブ `7224:7100`（Low）
- [ ] B. アクティブ `7224:7100`（Low） / パッシブ `7224:7300`（High）
- [ ] C. 双方 `7224:7200`（Medium）
- [ ] D. アクティブ `7224:9100` / パッシブ `7224:9300`

> **解説**: LOCAL_PREF は高いほど優先される。アクティブに High（`7224:7300`）、パッシブに Low（`7224:7100`）を付けるとアクティブ側が選択される。`7224:92xx`/`93xx` は Public VIF のスコープコミュニティで用途が異なる。
> **出典**: [direct-connect README #4 BGP ルーティングとトラフィック制御](README.md#4-bgp-ルーティングとトラフィック制御最頻出)

## direct-connect-005
- type: multi
- difficulty: hard
- domain: 1
- tags: [bgp, security-group]

オンプレ→AWS（アウトバウンド）の経路をオンプレ側で制御し、特定回線を優先させたい。有効な手法を 2 つ選べ。

- [x] A. アクティブ側でより長い（more-specific）プレフィックスを広告する
- [x] B. 非優先側で AS_PATH プリペンド（自 ASN を複数回付加）して経路を長く見せる
- [ ] C. AWS 側で LOCAL_PREF コミュニティを設定する
- [ ] D. Public VIF のスコープコミュニティ `7224:9100` を使う
- [ ] E. BGP の hold タイマーを延ばす

> **解説**: アウトバウンドはオンプレ側で制御する。most-specific（より長いプレフィックス）広告が最優先で、AS_PATH プリペンドで非優先化する。LOCAL_PREF コミュニティ（`7224:73xx` 等）は AWS→オンプレの戻り（インバウンド）制御用。Public VIF スコープコミュニティは広告範囲制御用。
> **出典**: [direct-connect README #4 BGP ルーティングとトラフィック制御](README.md#4-bgp-ルーティングとトラフィック制御最頻出)

## direct-connect-006
- type: single
- difficulty: hard
- domain: 1
- tags: [bgp]

BGP の経路選択則において、最も先に評価される（最優先の）要素はどれか。

- [x] A. 最長プレフィックスマッチ（more specific）
- [ ] B. LOCAL_PREF
- [ ] C. AS_PATH 長
- [ ] D. MED

> **解説**: 経路選択は「最長プレフィックスマッチ → LOCAL_PREF（高いほど優先） → AS_PATH 長（短いほど優先） → MED（小さいほど優先） → ECMP」の順で評価される。プレフィックス長と LOCAL_PREF が同じときに初めて AS_PATH が効く点に注意。
> **出典**: [direct-connect README #4 BGP ルーティングとトラフィック制御](README.md#4-bgp-ルーティングとトラフィック制御最頻出)

## direct-connect-007
- type: single
- difficulty: hard
- domain: 1
- tags: [well-architected, high-availability, direct-connect]

ミッションクリティカルな本番ワークロードに SLA 99.99% の最大耐障害性を確保したい。Resiliency Toolkit のモデルとして正しい構成はどれか。

- [x] A. 2 つ以上のロケーションそれぞれに、別々のデバイスで独立した接続を配置する
- [ ] B. 単一ロケーションに 2 接続を別デバイスで配置する
- [ ] C. 単一ロケーションに 1 接続＋複数 VIF
- [ ] D. 1 DX ＋ Site-to-Site VPN バックアップ

> **解説**: 最大耐障害性（SLA 99.99%）は 2 ロケーション以上に、各ロケーションで別々のデバイスを使った独立接続を配置する。単一ロケーション 2 接続は高耐障害性（99.9%）に相当する。
> **出典**: [direct-connect README #7 冗長性設計モデル](README.md#7-冗長性設計モデルresiliency-toolkit暗記)

## direct-connect-008
- type: single
- difficulty: medium
- domain: 1
- tags: [well-architected, high-availability, direct-connect]

SLA 99.9% の高耐障害性モデルの構成として正しいものはどれか。

- [ ] A. 1 ロケーションに 1 接続
- [x] B. 2 ロケーションに、それぞれ別デバイスで 2 接続
- [ ] C. 1 ロケーションに 4 接続（2 デバイス×2）
- [ ] D. 4 ロケーションに各 1 接続

> **解説**: 高耐障害性（SLA 99.9%）は 2 ロケーションに別デバイスで 2 接続を配置する。1 ロケーション単一接続は SLA なし（開発/テスト）、2 ロケーション×別デバイスの独立接続は最大耐障害性（99.99%）。
> **出典**: [direct-connect README #7 冗長性設計モデル](README.md#7-冗長性設計モデルresiliency-toolkit暗記)

## direct-connect-009
- type: single
- difficulty: medium
- domain: 1
- tags: [direct-connect, multi-region, multi-account]

Direct Connect Gateway（DXGW）に関する説明として正しいものはどれか。

- [ ] A. リージョン固有のリソースである
- [x] B. グローバルリソースで、1 つの DX 接続から複数リージョン・複数アカウントの VPC/TGW へ到達できる
- [ ] C. DXGW 経由で関連付けた VGW 同士が相互通信できる
- [ ] D. DXGW の利用には追加課金が必要

> **解説**: DXGW はグローバルリソースで、1 つの DX 接続から複数リージョン・複数アカウントの VPC/TGW へ到達できる（中国リージョン除く）。ただし VGW 同士は DXGW 経由で相互通信できない（ハブにならない）。DXGW 自体は無料。
> **出典**: [direct-connect README #5 Direct Connect Gateway](README.md#5-direct-connect-gatewaydxgw)

## direct-connect-010
- type: single
- difficulty: medium
- domain: 4
- tags: [encryption]

「DX 接続でも回線レベルの暗号化が必須」というコンプライアンス要件に、スループット低下を最小限にして応えたい。適切な選択肢はどれか。

- [x] A. MACsec（Dedicated 10G/100G、IEEE 802.1AE による L2 暗号化）
- [ ] B. すべての接続で IPsec VPN over DX のみ
- [ ] C. Public VIF で TLS を強制する
- [ ] D. DXGW で自動暗号化する

> **解説**: MACsec は IEEE 802.1AE による L2 のニアラインレート暗号化で、Dedicated 10G/100G 接続かつ対応 PoP で使える。IPsec VPN よりスループット低下が小さく、DX 回線の暗号化要件の解。
> **出典**: [direct-connect README #6 MACsec・SiteLink](README.md#6-macsecsitelink)

## direct-connect-011
- type: single
- difficulty: medium
- domain: 1
- tags: [direct-connect, transit-gateway]

DX ロケーションに接続したオンプレ拠点間を、AWS リージョンを経由せず AWS グローバルバックボーン経由で最短に接続したい。使用する機能はどれか。

- [ ] A. Transit Gateway peering
- [ ] B. Public VIF
- [x] C. SiteLink
- [ ] D. DXGW の Allowed prefixes

> **解説**: SiteLink は DX ロケーション間（オンプレ拠点間）を AWS グローバルバックボーン経由で直接接続する機能。トラフィックは AWS リージョンを経由せず最短経路で拠点間を結び、AWS をグローバル WAN として利用できる。
> **出典**: [direct-connect README #6 MACsec・SiteLink](README.md#6-macsecsitelink)

## direct-connect-012
- type: single
- difficulty: hard
- domain: 3
- tags: [quotas, bgp]

Private/Transit VIF でオンプレから AWS へ広告できる経路数の上限を超えると、どうなるか。

- [ ] A. 超過分が自動的に集約される
- [x] B. 上限（IPv4・IPv6 各 100）を超えると BGP セッションが idle になりダウンする
- [ ] C. 何も起きず全経路が広告される
- [ ] D. Public VIF へ自動的にフェイルオーバーする

> **解説**: Private/Transit VIF のオンプレ→AWS 広告経路は IPv4・IPv6 各 100 が上限で、超過すると BGP セッションが idle ダウンする。経路集約（サマリ）で 100 以内に収める必要がある。Public VIF は最大 1,000。
> **出典**: [direct-connect README #9 制約・上限・BGP タイマー](README.md#9-制約上限bgp-タイマー暗記推奨)

## direct-connect-013
- type: single
- difficulty: medium
- domain: 3
- tags: [vpn, failover, well-architected]

DX 障害時に Site-to-Site VPN へ自動フェイルオーバさせるバックアップ構成にしたい。経路制御の考え方として正しいものはどれか。

- [x] A. TGW/VGW で DX 経路（伝播）を優先し、DX 断時に VPN 経路へ自動切替させる
- [ ] B. VPN 経路を常時優先し、DX は使わない
- [ ] C. DX と VPN を同一プレフィックス・同一優先度で常時 ECMP させる
- [ ] D. Public VIF を VPN のバックアップにする

> **解説**: VPN バックアップでは TGW/VGW で DX 経路を優先（伝播）させ、DX 断時に VPN 経路へ自動切替する。コスト重視のバックアップ構成として Resiliency Toolkit にも含まれる。
> **出典**: [direct-connect README #7 冗長性設計モデル](README.md#7-冗長性設計モデルresiliency-toolkit暗記)

## direct-connect-014
- type: single
- difficulty: medium
- domain: 1
- tags: [direct-connect]

Hosted 接続（パートナー経由）の特徴として正しいものはどれか。

- [ ] A. 1 接続あたり最大 51 の VIF を作成できる
- [x] B. 1 接続あたり VIF は 1 つで、帯域はパートナーが細かく分割提供（50 Mbps〜10 Gbps）する
- [ ] C. MACsec に標準対応する
- [ ] D. AWS が物理ポートを占有割当する

> **解説**: Hosted 接続は APN パートナーが分割提供し、1 接続あたり VIF は 1 つ、帯域は 50 Mbps〜10 Gbps と細かい。MACsec は一般に非対応。Dedicated は物理ポート占有割当で 1/10/100/400 Gbps、VIF 最大 51。
> **出典**: [direct-connect README #2 コアコンポーネント](README.md#2-コアコンポーネント)
