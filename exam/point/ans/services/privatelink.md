# AWS PrivateLink の要点

> 重要度: ◎ ／ 「特定サービスをプライベート公開」「CIDR 重複・一方向接続の解消」の定番解。設計/セキュリティ分野で超頻出。

## これは何
- VPC・AWSサービス・他アカウント・オンプレを、**IGW/NAT/ピアリング/TGWを経由せず**AWSバックボーン上のプライベートIP(ENI)で接続する技術。
- 消費側の **Interface VPCエンドポイント(ENI)** と、提供側の **エンドポイントサービス(NLB/GWLB背後)** で構成。
- 接続は本質的に**一方向(消費側→提供側)**。特定サービス1つだけを最小露出で公開できる。

## 試験頻出ポイント
- **Interfaceエンドポイント** = ENI+プライベートIPを消費側VPCに作成。**時間課金+データ処理課金**。大半のAWSサービス/自社/SaaS対応。
- **エンドポイントサービス**(提供側)のフロントは **NLBまたはGWLBが必須**。**ALBは直接指定不可**(NLBのターゲットにALBを置く構成は可)。名前は `com.amazonaws.vpce.<region>.vpce-svc-xxxx`。
- **CIDR完全重複でも接続可**。理由は**NLBがIP NAT**を行うため、消費側は自VPC内のエンドポイントENIのIPを宛先にするだけでよい。PrivateLink最大の利点。
- 提供側アプリが見る送信元IPは**NLBノードのプライベートIP**(消費側の実IPではない)。実IP/エンドポイントID取得は **Proxy Protocol v2** をNLBで有効化。
- **エンドポイントポリシー**=エンドポイントに付与するIAMリソースポリシーで、経路を最小権限に制限(例:特定バケットの `s3:GetObject` のみ)。
- 提供側で **接続承認(Acceptance required)** を有効化すると消費側の接続を手動承認。許可プリンシパルを明示登録。
- **プライベートDNS**でサービス正規名をENIのIPに解決。前提は VPCの **`enableDnsSupport`+`enableDnsHostnames`** 有効化。カスタムDNS名はTXTでドメイン所有権検証が必要。
- **Gatewayエンドポイント** = **S3/DynamoDB専用**・ルートテーブル(プレフィックスリスト)経由・**無料**。PrivateLinkではない。

## 比較・選択の判断（VPCピアリング/TGWとの違い）
| 要件 | 解答 |
|---|---|
| 相手VPC全体でなく特定サービス1つだけ公開 | PrivateLink |
| CIDRが完全重複している/一方向で十分 | PrivateLink(NLBがNAT) |
| VPC全体をIPレベルで双方向接続・少数VPC | VPCピアリング(重複CIDR不可) |
| 多数VPC/オンプレをハブ&スポークで集約 | Transit Gateway(重複CIDR不可) |
| 多数顧客VPCにスケール公開・ルート管理不要 | PrivateLink(1エンドポイントサービス) |
| S3/DynamoDBにVPC内からアクセス+コスト最小 | Gatewayエンドポイント(無料) |
| オンプレ(DX/VPN)からS3にプライベートアクセス | Interfaceエンドポイント(Gatewayは経路不可) |
| 集中型FW/IDSへ透過転送 | GWLB+GWLBe(GENEVE) |

## よく問われる上限・注意点（ひっかけ）
- **接続は消費側→提供側の一方向**。提供側から消費側へは開始できない(戻りトラフィックのみ)。
- **1つのNLBは1つのエンドポイントサービスにのみ**紐付け可(逆に1サービスは複数NLB可)。「1サービスにNLB1つだけ」は誤り。
- **Gatewayエンドポイントはオンプレから利用不可**(ルート起点がVPC内に必要)。オンプレ→S3はInterfaceを使う。
- ALBを直接エンドポイントサービスに指定する選択肢はひっかけ(NLB/GWLBのみ)。
- Interfaceエンドポイントは**クロスリージョン接続可(NLBベースのサービスのみ)**。Gatewayは不可。
- **GWLBエンドポイント(GWLBe)はAZ・サービスあたり1つ**。
- 上限(デフォルト): Interface 50/VPC、Gateway 20/リージョン、エンドポイントサービス 20/リージョン。帯域は既定10Gbps→最大100Gbpsへ自動スケール。
- コスト: Interfaceは時間課金+データ処理課金、**GatewayはS3/DynamoDBで無料**。コスト最小要件ではGatewayを選ぶ。

関連: [VPC](vpc.md) / [ELB](elastic-load-balancing.md) / [Route 53](route-53.md) / [Transit Gateway](transit-gateway.md)
