# ANS-C01 サービス別 要点インデックス

> AWS Certified Advanced Networking – Specialty (ANS-C01) で**試験に出やすい主要サービス**を、
> サービス別に「要点だけ」へ凝縮したノート群。原本の詳細ノート（`exam/ans/services/`）から抽出。

重要度: **◎=最重要** / **○=重要**（周辺サービス △ は本インデックス対象外）

## ネットワークとコンテンツ配信

| 重要度 | サービス | 要点 |
|---|---|---|
| ◎ | [Amazon VPC](vpc.md) | CIDR設計・SG/NACL・フローログ・VPCエンドポイント |
| ◎ | [AWS Transit Gateway](transit-gateway.md) | 大規模マルチVPC・ハイブリッド接続のハブ |
| ◎ | [AWS Direct Connect](direct-connect.md) | 専用線・VIF種別・BGP制御・冗長/SLA |
| ◎ | [AWS Site-to-Site VPN](site-to-site-vpn.md) | 冗長トンネル・ECMP・Accelerated VPN |
| ◎ | [Amazon Route 53](route-53.md) | ルーティングポリシー・Resolver |
| ◎ | [AWS PrivateLink](privatelink.md) | プライベート公開・CIDR重複解消 |
| ◎ | [Elastic Load Balancing](elastic-load-balancing.md) | ALB/NLB/GWLB の使い分け |
| ○ | [Amazon CloudFront](cloudfront.md) | エッジキャッシュ・セキュア配信 |
| ○ | [AWS Global Accelerator](global-accelerator.md) | Anycast固定IP・高速フェイルオーバー |
| ○ | [Amazon API Gateway](api-gateway.md) | エンドポイントタイプ・プライベートAPI |

## セキュリティ・アイデンティティ・コンプライアンス

| 重要度 | サービス | 要点 |
|---|---|---|
| ○ | [AWS Network Firewall](network-firewall.md) | 集中インスペクション・ステートフル制御 |
| ○ | [AWS WAF](waf.md) | L7保護・適用先スコープ |
| ○ | [AWS Shield](shield.md) | DDoS保護・Standard/Advanced |
| ○ | [AWS Firewall Manager](firewall-manager.md) | Organizations横断の一元管理 |
| ○ | [AWS RAM](ram.md) | TGW/サブネット/Resolverルールの共有 |

## 管理とガバナンス

| 重要度 | サービス | 要点 |
|---|---|---|
| ○ | [Amazon CloudWatch](cloudwatch.md) | メトリクス・ログ・ネットワーク監視 |
| ○ | [AWS CloudTrail](cloudtrail.md) | API監査・構成変更追跡 |
| ○ | [AWS Organizations](organizations.md) | OU/SCP・マルチアカウント統制 |

## コンテナ

| 重要度 | サービス | 要点 |
|---|---|---|
| ○ | [Amazon EKS](eks.md) | VPC CNI・Pod IP消費・IP枯渇対策 |
