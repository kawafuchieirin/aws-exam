# Amazon VPC の要点

> 重要度: ◎ ／ ANS-C01 全分野の土台。CIDR 設計・SG/NACL・フローログ・エンドポイントは単独でも他サービスの前提でも頻出。

## これは何
- AWS 上に論理分離した**仮想ネットワーク**を構築するサービス。
- CIDR で定義した IP 空間にサブネット・ルートテーブル・ゲートウェイ・セキュリティ制御を配置し、オンプレ同等のネットワークをソフトウェア定義で実現。

## 試験頻出ポイント
- **プライマリ CIDR は変更不可**。拡張は**セカンダリ CIDR** で対応（/16〜/28）。
- サブネット先頭4＋末尾1の**計5アドレスは AWS 予約**。AZ をまたげない。
- ローカル DNS リゾルバは **VPC+2**（10.0.0.0/16 → 10.0.0.2）。
- **SG=ステートフル/許可のみ/ENI 単位**、**NACL=ステートレス/許可+拒否/サブネット単位**。
- **特定 IP のブロックは NACL の Deny ルール**（SG は Deny 不可）。
- NACL はステートレスなので**エフェメラルポート(1024–65535)の戻り許可**を忘れると不通。
- ルートは**ロンゲストプレフィックスマッチ**。明示関連付けが無ければメイン RT。
- **NAT GW は AZ ごとに作り、各 AZ のルートを自 AZ の NAT に向ける**（共有すると AZ 障害で他 AZ 断）。
- NAT GW に **SG は付けられない**。Public NAT=EIP 必須/インターネット、Private NAT=EIP 不要/オンプレ・他 VPC（CIDR 重複緩和）。
- **VGW 経由(VPN/DX)から NAT GW へはルーティング不可、TGW なら可能**。ピアリング越しの NAT インバウンドも不可。
- フローログは**メタデータのみ**（中身は記録しない＝**中身はトラフィックミラーリング**）。出力先は **CloudWatch Logs / S3 / Data Firehose**。
- NAT/セカンダリ IP の**実宛先は `pkt-dstaddr`**（`dstaddr` はプライマリ IP が出る）。
- **到達性の静的解析は Reachability Analyzer**（実トラフィック不要）。意図しない経路検出は Network Access Analyzer。
- 拡張ネットワーキング: 高スループット一般用途=**ENA**、密結合 HPC/分散学習(OS バイパス)=**EFA**、通常=ENI。

## 比較・選択の判断
| 要件 | 解答 |
|---|---|
| 特定 IP をサブネット単位で拒否 | NACL の Deny ルール |
| インスタンス単位の細かい許可制御 | セキュリティグループ |
| S3/DynamoDB にプライベート接続・無料 | Gateway エンドポイント |
| その他 AWS/自社サービスにプライベート接続 | Interface エンドポイント (PrivateLink) |
| 重複 CIDR のまま単一サービスへ片方向接続 | PrivateLink |
| 重複 CIDR で双方向通信 | Private NAT or 再アドレッシング |
| パケットの中身を解析 (IDS/IPS) | トラフィックミラーリング |
| 2点間の到達可否を静的検証 | Reachability Analyzer |
| OS バイパスの超低レイテンシ (HPC) | EFA |

## よく問われる上限・注意点（ひっかけ）
- **ピアリング・TGW は重複 CIDR を許容しない**（重複時は PrivateLink/Private NAT/再アドレッシング）。
- プライマリ CIDR は後から拡大変更できない。予約 5 アドレスは再利用不可。
- NAT GW 帯域は 5→100 Gbps へ自動スケール、**1 IPv4 あたりユニーク宛先ごと最大 55,000 同時接続**（最大 8 IPv4 で拡張）。
- IGW 経由インターネット・S2S VPN・ピアリングのリージョン間は **MTU 1500**。VPC 内は最大 9001。
- **PMTUD の ICMP(Type3 Code4)を遮断するとブラックホール化**して無応答 → ICMP を通す。
- フローログに**記録されない**: Amazon DNS 宛、DHCP、169.254.169.254、Windows ライセンス認証、ミラーリング対象。集約間隔は最短 1 分。
- コスト発生: NAT GW(時間+データ処理)、Interface エンドポイント、ミラーリング、各 Analyzer、IPAM。**Gateway エンドポイント・SG・NACL・IGW は無料**。
- コスト最適化: S3/DynamoDB は **Gateway エンドポイント**で NAT を経由させない。
- 主な上限: リージョンあたり VPC 5、VPC あたり CIDR 5(最大50)・サブネット 200・RT 200。

## 関連
- [Transit Gateway](transit-gateway.md) / [PrivateLink](privatelink.md) / [Direct Connect](direct-connect.md) / [Route 53 Resolver](route53.md)
