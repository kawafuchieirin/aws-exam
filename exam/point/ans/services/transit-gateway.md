# AWS Transit Gateway の要点

> 重要度: ◎ ／ 大規模マルチVPC・ハイブリッド接続の標準解。ANS-C01 第1分野の中核で「ピアリングか TGW か」選択問題が頻出。

## これは何
- 複数 VPC・オンプレ（VPN/DX）を**1つのリージョナル仮想ルータ**にハブ＆スポーク集約する L3 サービス。
- 宛先 IP で次ホップのアタッチメントへ転送し、トラフィック量に応じて**自動スケール**する。
- VPC ピアリングのフルメッシュが破綻する規模での「正解」。

## 試験頻出ポイント
- **Association**＝アタッチメントが参照するルートテーブル（入口、**1アタッチメント=1RTのみ**）。**Propagation**＝経路を注入する先（出口、**複数RT可・フィルタ不可**）。この分離でセグメンテーションを実現（最頻出）。
- **推移ルーティング可**（A経由でB↔C到達）。VPC ピアリングは**非推移**。
- **TGW ルートテーブル**はデフォルト1個、最大20個。association/propagation の組合せで分離・共有サービス・集中検査を構成。
- **ブラックホールルート**で特定 CIDR をドロップ（VPC 間遮断＋共有出口）。
- **アプライアンスモード**: ステートフル検査で往復を同一 ENI/AZ に固定し**対称フロー保証**。Inspection VPC のアタッチメントで有効化。
- **TGW Peering**: **静的ルートのみ**（動的・ECMP 非対応）。リージョン間は **AES-256 の二重暗号化**。同/別アカウント・リージョン可。
- **TGW Connect**: **GRE＋BGP** で SD-WAN 統合。既存 VPC/DX アタッチメントをトランスポートに使用。**伝播のみ（静的非対応）**、Connect peer ごと BGP 2 本。
- **ECMP 対応**: **VPN（動的のみ）と Connect** のみ。VPC・Peering・VPN Concentrator は非対応。異種・異 ASN 間も不可。
- **Network Manager / Route Analyzer**: グローバルネットワーク可視化と 2 点間の経路解析・到達性検証。
- **ルート評価順**: ①最長プレフィックスマッチ ②静的 > プレフィックスリスト > VPC伝播 > **DXGW伝播 > Connect伝播 > VPN伝播** ③BGP は AS_PATH短→MED低→eBGP優先。静的は同一宛先の伝播より優先。
- **RAM** で TGW を他アカウント/OU に共有しマルチアカウント単一 TGW を実現。

## 比較・選択の判断
| 要件 | 解答 |
|---|---|
| 少数 VPC・最低レイテンシ・低コスト・重複なし | VPC ピアリング |
| 多数 VPC・推移接続・ハイブリッド集約 | **Transit Gateway** |
| ECMP で VPN 帯域集約・Accelerated/Private IP VPN | **TGW**（VGW では不可） |
| VPN/DX を単一 VPC に終端 | VGW |
| SD-WAN を GRE＋BGP で統合 | **TGW Connect** |
| リージョン間 TGW 接続（静的のみ） | **TGW Peering** |
| 往復対称が必要なステートフル検査 | **アプライアンスモード** |

関連: [VPC](vpc.md) / [Direct Connect](direct-connect.md) / [Site-to-Site VPN](site-to-site-vpn.md)

## よく問われる上限・注意点（ひっかけ）
- **重複 CIDR はピアリングも TGW も不可**（ひっかけ）。
- TGW Peering は**動的ルーティング・ECMP 非対応**（静的のみ）。Connect は逆に**静的非対応・伝播のみ**。
- アプライアンスモードのフロー固定は**同一 TGW アタッチメント経由のみ**。複数 TGW はフロー状態を共有しないため **Inspection VPC には TGW を1つだけ**接続。
- **AWS Network Firewall の TGW アタッチメント**はアプライアンスモード自動有効・静的ルーティングのみ・**サードパーティ FW 非対応**。
- **MTU**: VPC/DX/Connect/Peering 間 **8500**、**VPN は 1500**。PMTUD は VPC/Connect 受信のみ対応（VPN/DX/Peering 非対応）。MSS クランプは全パケット実施。
- アタッチメント / TGW = **5,000**、ルートテーブル / TGW = 20、経路数合計 = 10,000、Peering = 50。
- 帯域: VPC アタッチメント **最大 100 Gbps/AZ**、Connect peer **最大 5 Gbps**（4 peer で最大 20 Gbps）。
- DXGW: 1 DXGW に TGW 最大6、1 TGW に DXGW 最大20。
- TGW は**プライマリ経路のみ表示**。DX とVPN 同経路広告時は DX 優先表示、DX 断で初めて VPN 表示。
- **コスト**: アタッチメント時間課金＋データ処理量（GB）課金。リージョン間 Peering はデータ転送料も発生。
