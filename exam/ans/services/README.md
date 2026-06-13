# ANS-C01 主要サービス要点集（インデックス）

> AWS Certified Advanced Networking - Specialty (ANS-C01) 試験対策。
> 試験ガイド「範囲内の AWS サービスと機能」全サービスを、1サービス1ディレクトリで詳細化。
> 各 README は AWS 公式ドキュメント/Blog を参照し出典 URL を明記、Mermaid 図でトポロジ・設計パターンを図解。
> 出典: AWS公式「ANS-C01 試験ガイド」バージョン 2.0 ／ 最終更新: 2026-05-24

---

## 試験概要

| 項目 | 内容 |
|---|---|
| 対象 | AWS / ハイブリッドネットワークを大規模に設計・実装・管理・保護するスペシャリスト |
| 実務経験目安 | ネットワーク 5年以上 ＋ クラウド/ハイブリッド 2年以上 |
| 採点問題数 | 50問（＋採点外15問） |
| 合格スコア | 750 / 1000（補整スコアリング、総合点で合否） |

### コンテンツ分野と配点

| 分野 | タイトル | 配点 |
|---|---|---|
| 第1分野 | ネットワーク設計 | **30%** |
| 第2分野 | ネットワーク実装 | 26% |
| 第3分野 | ネットワークの管理と運用 | 20% |
| 第4分野 | ネットワークセキュリティ・コンプライアンス・ガバナンス | 24% |

> 設計（30%）が最重量。次いでセキュリティ（24%）。「どのサービスをどう組み合わせるか」の判断力が中心。

---

## サービス索引（重要度順）

重要度: ◎=最重要 / ○=重要 / △=周辺・ネットワーク観点に限定

### ネットワークとコンテンツ配信

| 重要度 | サービス | 資料 |
|---|---|---|
| ◎ | Amazon VPC | [vpc](networking-content-delivery/vpc/README.md) |
| ◎ | AWS Transit Gateway | [transit-gateway](networking-content-delivery/transit-gateway/README.md) |
| ◎ | AWS Direct Connect | [direct-connect](networking-content-delivery/direct-connect/README.md) |
| ◎ | AWS Site-to-Site VPN | [site-to-site-vpn](networking-content-delivery/site-to-site-vpn/README.md) |
| ◎ | Amazon Route 53 | [route-53](networking-content-delivery/route-53/README.md) |
| ◎ | AWS PrivateLink | [privatelink](networking-content-delivery/privatelink/README.md) |
| ◎ | Elastic Load Balancing | [elastic-load-balancing](networking-content-delivery/elastic-load-balancing/README.md) |
| ○ | Amazon CloudFront | [cloudfront](networking-content-delivery/cloudfront/README.md) |
| ○ | AWS Global Accelerator | [global-accelerator](networking-content-delivery/global-accelerator/README.md) |
| ○ | Amazon API Gateway | [api-gateway](networking-content-delivery/api-gateway/README.md) |
| △ | AWS Client VPN | [client-vpn](networking-content-delivery/client-vpn/README.md) |
| △ | AWS Cloud Map | [cloud-map](networking-content-delivery/cloud-map/README.md) |
| △ | AWS App Mesh | [app-mesh](networking-content-delivery/app-mesh/README.md) |

### セキュリティ・アイデンティティ・コンプライアンス

| 重要度 | サービス | 資料 |
|---|---|---|
| ○ | AWS Network Firewall | [network-firewall](security-identity-compliance/network-firewall/README.md) |
| ○ | AWS WAF | [waf](security-identity-compliance/waf/README.md) |
| ○ | AWS Shield | [shield](security-identity-compliance/shield/README.md) |
| ○ | AWS Firewall Manager | [firewall-manager](security-identity-compliance/firewall-manager/README.md) |
| ○ | AWS RAM | [ram](security-identity-compliance/ram/README.md) |
| △ | AWS IAM（NW観点） | [iam](security-identity-compliance/iam/README.md) |

### マネジメントとガバナンス

| 重要度 | サービス | 資料 |
|---|---|---|
| ○ | Amazon CloudWatch | [cloudwatch](management-governance/cloudwatch/README.md) |
| ○ | AWS CloudTrail | [cloudtrail](management-governance/cloudtrail/README.md) |
| ○ | AWS Organizations | [organizations](management-governance/organizations/README.md) |
| △ | AWS Config | [config](management-governance/config/README.md) |
| △ | AWS Control Tower | [control-tower](management-governance/control-tower/README.md) |
| △ | AWS Trusted Advisor | [trusted-advisor](management-governance/trusted-advisor/README.md) |
| △ | AWS Health Dashboard | [health-dashboard](management-governance/health-dashboard/README.md) |
| △ | AWS Well-Architected Tool | [well-architected-tool](management-governance/well-architected-tool/README.md) |
| △ | AWS CLI | [aws-cli](management-governance/aws-cli/README.md) |
| △ | AWS CloudFormation | [cloudformation](management-governance/cloudformation/README.md) |
| △ | マネジメントコンソール | [management-console](management-governance/management-console/README.md) |
| △ | AWS Auto Scaling | [auto-scaling](management-governance/auto-scaling/README.md) |

### コンピュート

| 重要度 | サービス | 資料 |
|---|---|---|
| △ | Amazon EC2 | [ec2](compute/ec2/README.md) |
| △ | EC2 Auto Scaling | [ec2-auto-scaling](compute/ec2-auto-scaling/README.md) |
| △ | AWS Lambda | [lambda](compute/lambda/README.md) |

### コンテナ

| 重要度 | サービス | 資料 |
|---|---|---|
| ○ | Amazon EKS | [eks](containers/eks/README.md) |
| △ | Amazon ECS | [ecs](containers/ecs/README.md) |
| △ | Amazon ECR | [ecr](containers/ecr/README.md) |
| △ | AWS Fargate | [fargate](containers/fargate/README.md) |

### アプリケーション統合 / ストレージ / コスト管理

| 重要度 | サービス | 資料 |
|---|---|---|
| △ | Amazon EventBridge | [eventbridge](app-integration/eventbridge/README.md) |
| △ | Amazon SNS | [sns](app-integration/sns/README.md) |
| △ | Amazon SQS | [sqs](app-integration/sqs/README.md) |
| △ | Amazon S3 | [s3](storage/s3/README.md) |
| △ | AWS Cost Explorer | [cost-explorer](cost-management/cost-explorer/README.md) |

> サーバーレスカテゴリ（API Gateway / Lambda / Fargate / EventBridge / SNS / SQS / S3）は重複のため各サービスを上記の主カテゴリに一元配置しています。

---

## サービス選択 早見表（即答用）

| 要件 | 解答 |
|---|---|
| 多数VPC＋ハイブリッドを集中管理 | Transit Gateway |
| 少数VPCで低遅延・低コスト | VPCピアリング |
| CIDR重複したまま単一サービスへ接続 | PrivateLink |
| オンプレへ専用・安定帯域 | Direct Connect |
| DXのコスト効率の良いバックアップ | Site-to-Site VPN |
| DX上を暗号化したい | Private IP VPN over DX（Transit VIF） |
| L7ルーティング・WAF | ALB |
| 静的IP・超低遅延・TLSパススルー | NLB |
| サードパーティFW/IDSを透過挿入 | Gateway Load Balancer |
| マネージドなVPCファイアウォール | Network Firewall |
| 非HTTPの低遅延グローバルルーティング | Global Accelerator |
| 静的/動的コンテンツのCDN配信 | CloudFront |
| オンプレ↔AWSの相互名前解決 | Route 53 Resolver（in/outbound endpoint） |
| 加重/レイテンシ/フェイルオーバーDNS | Route 53 ルーティングポリシー |
| マルチアカウントでTGW/サブネット/Resolver共有 | RAM |
| 構成ミスの到達性検証 | Reachability Analyzer |
| パケット中身の解析 | VPCトラフィックミラーリング |
| トラフィックメタデータ・ACCEPT/REJECT | VPCフローログ |
| 組織横断のFW/WAFポリシー強制 | Firewall Manager |

---

## 横断的な頻出概念（サービス非依存）

### ルーティング / BGP
- **静的 vs 動的（BGP）**: 動的は障害時の自動収束・経路集約が利点。DXは必須、VPNは選択。
- **BGP属性によるトラフィック制御**: インバウンド（AWS→オンプレ広告制御）= AS_PATHプリペンド / more-specific / BGPコミュニティ（`7224:7100/7200/7300`=local/regional/global）。アウトバウンド（オンプレルータ側）= LOCAL_PREF / MED。
- **ロンゲストプレフィックスマッチ**が最優先。
- AWS のルート評価: 最長一致 → 静的/伝播 → DX → VPN の順。

### レイヤー1/2・MTU
- VLAN（802.1Q）、LAG（リンク集約）、ジャンボフレーム。
- MTU: VPC内9001 / VPN・IGW経由1500。経路最小MTUにPMTUDで調整。ICMPを遮断するとブラックホール化。

### カプセル化・暗号化
- GRE（TGW Connect / SD-WAN）、IPsec（VPN）、GENEVE（6081、GWLB↔アプライアンス）、MACsec（DXのL2暗号化）、TLS/ACM（転送中暗号化）。

### 設計パターン
- **集中型インスペクション**: インスペクションVPC＋TGW＋Network Firewall/GWLB で全トラフィック検査。
- **境界VPC / 3層アーキテクチャ**: パブリック/アプリ/DB層の分離。
- **共有サービスVPC**: DNS Resolver・AD・監視を集約し RAM/PHZ で共有。
- **ハブ＆スポーク**: TGW中心（旧トランジットVPCより推奨）。

---

> **学習のコツ**: 本試験は「サービス単体の暗記」より「複数サービスを組み合わせた設計判断」と「制約・上限・コストのトレードオフ」が問われます。特に **TGW × DX × VPN × Route 53 Resolver × PrivateLink** のハイブリッド構成、および **インスペクションVPCによる集中セキュリティ** のパターンを図で描けるようにしておくことを推奨します。各サービスの詳細は上記索引のリンクから参照してください。
