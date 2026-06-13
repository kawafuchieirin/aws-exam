# AWS Organizations の要点

> 重要度: ○ ／ RAM・Firewall Manager・組織証跡など、マルチアカウントのネットワーク統制すべての前提基盤。SCP によるガードレールが頻出。

## これは何
- 複数 AWS アカウントを**一元統制・課金集約**するサービス。
- **OU（組織単位）**でアカウントを階層化し、**SCP** で許可の上限（ガードレール）を設定する。
- RAM 共有・Firewall Manager・Config 組織アグリゲーター・組織証跡の有効化起点。

## 試験頻出ポイント
- **SCP はガードレール（許可の上限）であり、許可を付与しない**。実効権限は **SCP（上限）∩ IAM（付与）** の AND。
- **SCP は管理アカウント自身には効かない**。運用は委任管理者など別アカウントへ分離する。
- SCP は **OU 階層に沿って上位のものも継承**される。
- **ネットワーク向け SCP の典型**: 承認外リージョン禁止、**IGW/VPC ピアリング/VPN の作成禁止**（例: `ec2:CreateInternetGateway` を Deny）、特定 SG ルール変更禁止、デフォルト VPC 削除保護。
- **RAM × Organizations**: 組織内共有を有効にすると、**招待の承諾なしに**サブネット/TGW を共有できる。各アカウントが自前 VPC/TGW を作らず集約基盤を利用 → **IP 効率化・管理集中**。
- **Firewall Manager の前提**: **Organizations 有効化 + 委任管理者の指定 + AWS Config 有効化**。新規アカウント追加時も自動でポリシー適用。
- **委任管理者（delegated administrator）** で Firewall Manager・RAM・IPAM 等を専用アカウントで運用し、権限を分離。
- 監査・監視の集約: **組織証跡（CloudTrail）+ クロスアカウント CloudWatch オブザーバビリティ + Config 組織アグリゲーター**。

## 比較・選択の判断
| 要件 | 解答 |
|---|---|
| 全アカウントで IGW 作成を一律禁止 | SCP で `ec2:CreateInternetGateway` を **Deny**（IAM 個別変更は抜け漏れる） |
| 自前 VPC/TGW を作らず集約基盤で IP 効率化 | [RAM](ram.md) でサブネット/TGW を共有 |
| 全アカウントへセキュリティポリシーを一括展開 | Firewall Manager（Org + 委任管理者 + Config が前提） |
| 管理権限を集中させず運用を専用アカウントへ | 委任管理者の指定 |
| 承認外リージョンの利用を禁止 | SCP で Deny |
| ランディングゾーンとガードレールを自動構築 | [Control Tower](control-tower.md)（Organizations が土台） |

## RAM で共有できるネットワークリソース
- Transit Gateway、VPC サブネット、Route 53 解決ルール、Prefix List など。
- **共有不可**: IAM ロール、EC2 インスタンス、CloudTrail 証跡。

## よく問われる上限・注意点（ひっかけ）
- SCP は**許可を付与しない**（「SCP で管理者権限を付与」「IAM を上書きして許可」は誤り）。
- SCP は**管理アカウントには効かない**（「全アカウントに必ず適用」は誤り）。
- SCP は **OU/アカウントあたり最大 5 ポリシー**、OU 階層は**ルート配下 最大 5 階層**。
- **Organizations 自体は無料**。コストは RAM 共有リソース・Firewall Manager・Config 等の利用料。月額割引などの選択肢は誤り。
- コスト最適化は VPC/TGW 共有による **NAT GW・エンドポイントの重複削減**であって、Organizations の料金とは無関係。
- Firewall Manager は **Config 必須**（「Control Tower のみ」「サポートプランのみ」は誤り）。
