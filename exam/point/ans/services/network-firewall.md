# AWS Network Firewall の要点

> 重要度: ○ ／ ANS-C01 第4分野の主役。集中インスペクション VPC + Transit Gateway 構成と、ステートフル/ステートレスの違いが頻出。

## これは何
- VPC 境界（IGW/NAT/VPN/DX の手前）でトラフィックを検査する**マネージドなステートフル FW 兼 IDS/IPS**。
- L3/L4 のステートレス検査と、**Suricata 互換**ルールによる L7 ステートフル検査の両方を持つ。
- アウトバウンドのドメインフィルタや East-West / North-South の集中検査に使う。

## 試験頻出ポイント
- **2つのエンジン**: ステートレス（5タプル・単一パケット・高速・AWS 独自形式）／ステートフル（フロー文脈・**Suricata 互換**・DPI/ドメインフィルタ）。
- **アクション**: ステートレス=Pass / Drop / **Forward to stateful**。ステートフル=**Pass / Drop / Alert / Reject**。
- ステートレスで `Forward to stateful` したトラフィックのみステートフル検査・ログ記録される。
- **ファイアウォールエンドポイントは自サブネットのトラフィックを検査できない** → AZ ごとに**専用サブネット**を用意し、保護対象は別サブネットへ。ルートテーブルを書き換えて誘導。
- **集中構成では TGW を appliance mode** にして対称ルーティング。AZ をまたぐと戻りパケットが別 AZ に行きステートフル検査が壊れるため必須。
- **アウトバウンドドメインフィルタ**: ステートフルルールで **`tls.sni` / `http.host`** を評価し、許可ドメインのみ Pass・他は Drop（IP ベースの SG/NACL では不可）。
- **ログ**: ステートフルのみ（フロー/アラート/TLS）。ステートレスはメトリクスのみ。配信先は CloudWatch Logs / S3 / Kinesis Data Firehose。
- **集中 egress の配置順**: **Network Firewall → NAT GW → IGW**（変換前に検査して送信元 IP の可視性を確保）。
- **デプロイ構成**: 集中型（TGW ハブで全フローを Inspection VPC へ／East-West・North-South を一箇所で検査）vs 分散型（各 VPC に配置・小規模で単純だが管理点増）。

## SG/NACL/WAFとの違い
| 観点 | 解答 |
|---|---|
| Network Firewall | VPC 境界の L3〜L7 FW + IDS/IPS。ドメイン/SNI/HTTP Host フィルタ、Suricata ルール |
| セキュリティグループ | ENI 単位のステートフル許可リスト。IP/ポート。ドメイン制御不可 |
| NACL | サブネット単位のステートレス許可/拒否。IP/ポート。ドメイン制御不可 |
| [WAF](waf.md) | L7（HTTP/HTTPS）特化。CloudFront/ALB/API GW に付与。VPC 境界の汎用検査ではない |
| [GWLB](#) | 自前/サードパーティ仮想アプライアンスを GENEVE で透過挿入。NWFW はマネージドエンジン |

## よく問われる上限・注意点（ひっかけ）
- 「Forward to stateless」というアクションは**存在しない**（逆方向のみ Forward to stateful）。
- ステートレスはログ不可（メトリクスのみ）。「ステートレスもフローログ出力可」は誤り。
- SG/NACL でドメイン名フィルタはできない → ドメイン制御はステートフルルール。
- サードパーティ製アプライアンス（Palo Alto 等）が要件なら **GWLB**。NWFW はホストできない。
- 課金は**エンドポイント時間（AZ ごと）＋ 処理データ量（GB）**。AZ を増やすほど課金増、クロス AZ 検査はデータ転送料増。ログ量も配信先コストに影響。
- ルールグループには**キャパシティ上限**があり、ステートレス/ステートフルで別管理。
- ステートフルエンジンは Suricata 7.x 系互換。
- 関連: [Route 53 Resolver DNS Firewall](#) は DNS レイヤーのブロックで補完（NWFW は IP/TLS/HTTP レイヤー）。
