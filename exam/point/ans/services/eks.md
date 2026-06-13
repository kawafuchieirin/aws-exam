# Amazon EKS の要点（ネットワーク観点）

> 重要度: ○ ／ ANS-C01 では「Pod が VPC の実 IP を持つ」VPC CNI モデルと、それに起因する **IPv4 枯渇対策** の選択が頻出。

## これは何
- マネージド Kubernetes。ネットワークの核心は **Amazon VPC CNI プラグイン**。
- 各 Pod に **VPC 内のルーティング可能な実 IP** を割り当てる（オーバーレイ無し）。
- VPC ネイティブ通信が可能になる反面、**Pod ごとに VPC の IP を消費**するため大規模クラスタで IP 枯渇が論点。

## 試験頻出ポイント
- **VPC CNI** = Pod が VPC の実 IP を持つ（オーバーレイ無し）。ノードの ENI にセカンダリ IP/プレフィックスを束ねて配布。これが IP 枯渇の根本原因。
- **Pod は VPC ネイティブ IP** なので、**ピアリング / TGW / Direct Connect 越しに Pod へ直接到達可能**（CIDR 重複は不可）。
- **max-pods** = **(ENI 数 × ENI あたり IP 数) − 予約**。**インスタンスタイプ依存**（既定上限 110/ノード、変更可）。
- **IP 枯渇対策**は要件で選ぶ:
  - Pod 密度を上げたい → **プレフィックス委任**（ENI に **/28**(IPv4)・**/80**(IPv6)、`ENABLE_PREFIX_DELEGATION=true`、**Linux のみ**）。
  - RFC1918 を温存/別空間へ逃がす → **セカンダリ CIDR（例 100.64.0.0/10）+ カスタムネットワーキング（ENIConfig CRD）**。
  - 恒久解（AWS 推奨）→ **IPv6 クラスタ**。
- **AWS Load Balancer Controller**: **Ingress → ALB**、**Service type=LoadBalancer → NLB**。
  - **ip ターゲットモード**: LB が **Pod IP へ直接転送**（ホップ削減、**Fargate 必須**）。SG は**各 Pod の ENI**で選択。
  - **instance ターゲットモード**: NodePort 経由で kube-proxy が転送。SG は**ノードのプライマリ ENI**。
- **Security Groups for Pods**: **trunk ENI（ノードに1つ）+ branch ENI（Pod ごと）** で **Pod 単位に SG** を適用。Pod から RDS 等への最小権限アクセスで正解になりやすい。
- プライベートサブネットの Pod がインターネットへ出る場合は **NAT Gateway 経由**（`AWS_VPC_K8S_CNI_EXTERNALSNAT` の挙動に注意）。

## 比較・選択の判断
| 要件 | 解答 |
|---|---|
| Pod 密度を上げ RFC1918 を温存 | **プレフィックス委任**（/28） |
| プライマリ CIDR を使い切った／別空間へ逃がす | **セカンダリ CIDR + カスタムネットワーキング** |
| IPv4 枯渇の恒久・根本解決 | **IPv6 クラスタ** |
| Pod 単位で SG を適用したい | **Security Groups for Pods**（trunk/branch ENI） |
| LB が Pod IP へ直接転送／Fargate | **ip ターゲットモード** |
| Kubernetes Ingress を公開 | **ALB**（LB Controller） |
| Service type=LoadBalancer を公開 | **NLB**（LB Controller） |

## よく問われる上限・注意点（ひっかけ）
- VPC CNI は**オーバーレイではない**（VXLAN・ノード IP 共有は誤答）。Pod は固有 VPC IP を持つ。
- **プレフィックス委任は Linux のみ**（Windows のみは誤答）。CNI **v1.9.0 以上**、既存ノードへの混在は非推奨で**新規ノードグループで移行**。
- **IPv6 はクラスタ作成時に選択**。**後から IPv4↔IPv6 の変更は不可**。外部 IPv4 へは送信側 NAT で到達。
- **セカンダリ CIDR / IPv6 自体は無料**（別途料金は誤答）。
- カスタムネットワーキングは**ノードあたり Pod 数がやや減る**ことがある（「必ず増える」は誤答）。
- **Fargate はノードが無いため ip モード必須**（instance モードは不可）。
- NACL での Pod 個別制御は不適。Pod 単位の SG 制御は **Security Groups for Pods** が正解。

関連: [VPC](vpc.md)（セカンダリ CIDR・サブネット・NAT・ルーティングの基盤）
