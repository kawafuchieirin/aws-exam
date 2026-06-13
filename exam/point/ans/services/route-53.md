# Amazon Route 53 の要点

> 重要度: ◎ ／ ANS-C01 のDNS分野の中核。ルーティングポリシー・ヘルスチェック・Resolver（ハイブリッドDNS）は確実に得点したい。

## これは何
- AWS のマネージドな**権威DNS**・**ドメイン登録**・**DNSヘルスチェック**サービス。
- **Route 53 Resolver** で VPC ↔ オンプレ間の**再帰DNS解決（ハイブリッドDNS）**を実現する。

## 試験頻出ポイント
- **8種のルーティングポリシー**（Simple/Weighted/Latency/Failover/Geolocation/Geoproximity/IP-based/Multivalue）の使い分け。
- **エイリアスレコード**: Zone Apex で使え、AWSリソース宛は**無料**、IP変化に**自動追従**。CNAME は **Zone Apex 不可**。
- **Split-horizon DNS**: 同名のパブリックPHZ + プライベートPHZ で内外を出し分け。PHZ には VPC の **`enableDnsSupport`/`enableDnsHostnames` 両方 true** が必要。
- **Route 53 Resolver** は VPC CIDR の **+2 アドレス**に存在。
  - **Inbound Endpoint**: オンプレ → AWS の名前解決（オンプレDNSがPHZ等を解決する受け口）。
  - **Outbound Endpoint**: AWS → オンプレの名前解決。**条件付き転送 Resolver Rule（FORWARD）**と組で使う。
- **Resolver Rule は AWS RAM で共有**してマルチアカウントのハイブリッドDNSを一元管理（定石）。
- **ヘルスチェック**: エンドポイント監視 / **Calculated（子HC集約）** / **CloudWatchアラーム連動**。
- **プライベートサブネット内リソース**はパブリックチェッカー不達 → **CloudWatchメトリクス + アラーム連動/Calculated** で監視（頻出ひっかけ）。
- **Failover はプライマリにヘルスチェック必須**。
- **DNS Firewall**: VPCの**アウトバウンドDNSクエリ**をドメインリストでフィルタ（ALLOW/BLOCK/ALERT）。WAF/Network Firewall とは別物。
- **DNSSEC**: パブリックホストゾーンの署名で改ざん防止。KMS非対称鍵(ECC_NIST_P256)使用、**KSKはゾーンあたり最大2**、親ゾーンに**DSレコード**登録が必要。署名・検証は**無料**。
- **Route 53 ARC**: DNSフェイルオーバーより確実な**容量保証のリージョン退避**。Readiness Check + Routing Control、データプレーンは**5リージョン構成**。

## ルーティングポリシーの即答表
| 要件 | ポリシー |
|---|---|
| 単一リソースへ単純に応答 | Simple（HC関連付け不可） |
| 重み(%)で配分・Blue/Green・カナリア | Weighted（0〜255） |
| 実測レイテンシ最小のリージョンへ | Latency |
| Active-Passive のDR・障害切替 | Failover（プライマリにHC必須） |
| ユーザーの国/大陸/州で振り分け・地域制限 | Geolocation |
| リソースの位置 + **bias** でトラフィック量を手動調整 | Geoproximity（Traffic Flow必須） |
| 送信元IPの**CIDR**で振り分け | IP-based |
| 最大8件をランダム返却 + 各値HC | Multivalue（LBの代替ではない） |

> 混同注意: Latency=リージョン実測 / Geolocation=ユーザー位置 / Geoproximity=リソース位置+bias。

## よく問われる上限・注意点（ひっかけ）
- **Zone Apex を ELB/CloudFront/S3 に向ける → 必ずエイリアス**（CNAME不可）。
- **Multivalue は LB の代替ではない**（最大8件・ランダム）。
- **Geolocation は `Default` レコードがないと未マッチが `NoAnswer`**。最具体マッチ優先（州 > 国 > 大陸 > Default）。
- ヘルスチェック間隔: 標準 **30秒** / Fast **10秒**（追加課金）。失敗しきい値既定 **3回**。
- **Resolver エンドポイント / リージョン = 4**、エンドポイントあたり IP = **6**。
- **PHZ あたり関連付け VPC = 300**（超過は **Route 53 Profiles** 推奨）。
- ホストゾーン/アカウント = 500、レコード/ゾーン = 10,000、HC/アカウント = 200、Calculated の子HC = 255。
- 関連: [VPC](vpc.md)（VPC+2リゾルバ・NAT64連携）、[ELB](elb.md)（エイリアス）、[PrivateLink](privatelink.md)（プライベートDNS名）。
