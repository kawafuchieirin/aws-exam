# ANS-C01 要点まとめ

> AWS Certified Advanced Networking – Specialty (ANS-C01) の「要点だけ」を集約するインデックス。
> このディレクトリ（`exam/point/ans/`）配下の Markdown が、そのまま要点文庫サイトへ公開されます。

## 使い方

- 1トピック = 1ファイル（例: `services/vpc.md`）で追加していく。
- ファイル先頭の `# 見出し` がサイトのページタイトルになる。
- サブディレクトリを切ってもOK（例: `services/`）。再帰的に取り込まれる。

## サービス別の要点

試験に出やすい主要サービスを重要度順にサービス別でまとめています（`services/` 配下）。
→ [サービス別 要点インデックス](services/README.md)

### 最重要（◎）

| サービス | 要点 |
|---|---|
| [Amazon VPC](services/vpc.md) | CIDR設計・SG/NACL・フローログ・エンドポイント |
| [AWS Transit Gateway](services/transit-gateway.md) | 大規模マルチVPC接続・ピアリングとの使い分け |
| [AWS Direct Connect](services/direct-connect.md) | 専用線・VIF種別・BGP制御・冗長設計 |
| [AWS Site-to-Site VPN](services/site-to-site-vpn.md) | 冗長トンネル・ルーティング・Accelerated VPN |
| [Amazon Route 53](services/route-53.md) | ルーティングポリシー・Resolver（ハイブリッドDNS） |
| [AWS PrivateLink](services/privatelink.md) | 特定サービスのプライベート公開・CIDR重複の解消 |
| [Elastic Load Balancing](services/elastic-load-balancing.md) | ALB/NLB/GWLB の使い分け |

### 重要（○）

| サービス | 要点 |
|---|---|
| [Amazon CloudFront](services/cloudfront.md) | エッジキャッシュ・セキュア配信 |
| [AWS Global Accelerator](services/global-accelerator.md) | Anycast固定IP・高速フェイルオーバー |
| [Amazon API Gateway](services/api-gateway.md) | エンドポイントタイプ・プライベートAPI |
| [AWS Network Firewall](services/network-firewall.md) | 集中インスペクション・ステートフル制御 |
| [AWS WAF](services/waf.md) | L7保護・適用先スコープ |
| [AWS Shield](services/shield.md) | DDoS保護・Standard/Advanced |
| [AWS Firewall Manager](services/firewall-manager.md) | Organizations横断の一元管理 |
| [AWS RAM](services/ram.md) | TGW/サブネット/Resolverルールの共有 |
| [Amazon CloudWatch](services/cloudwatch.md) | メトリクス・ログ・ネットワーク監視 |
| [AWS CloudTrail](services/cloudtrail.md) | API監査・構成変更追跡 |
| [AWS Organizations](services/organizations.md) | OU/SCP・マルチアカウント統制 |
| [Amazon EKS](services/eks.md) | VPC CNI・Pod IP消費・IP枯渇対策 |

> 実際の要点ノートを `exam/point/ans/` 配下に追加して push すると、自動でビルド・公開されます。
