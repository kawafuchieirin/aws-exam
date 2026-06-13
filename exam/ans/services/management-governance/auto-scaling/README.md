# AWS Auto Scaling（ネットワーク観点）

> カテゴリ: マネジメントとガバナンス / 重要度: △
> 最終更新: 2026-05-24

---

## 1. 概要

AWS Auto Scaling（EC2 Auto Scaling グループ, ASG）は、需要に応じて EC2 インスタンスを自動増減させ、可用性とコスト効率を保つサービス。ネットワーク観点では、**複数 AZ/サブネットへのインスタンス分散**と **ELB/ターゲットグループとの連携**による高可用構成が問われる。

---

## 2. コアコンセプト

| 要素 | 役割 |
|---|---|
| **Auto Scaling グループ（ASG）** | インスタンス群を希望/最小/最大台数で維持 |
| **複数サブネット（AZ）指定** | ASG に複数 AZ のサブネットを割り当て、台数を均等分散 |
| **ELB/ターゲットグループ連携** | 起動インスタンスを自動登録、ELB ヘルスチェックで異常を判定 |
| **起動テンプレート** | サブネット・SG・ENI 設定を含むインスタンス定義 |

---

## 3. 試験頻出ポイント（ネットワーク）

- **マルチ AZ 分散**: ASG に**複数 AZ のサブネット**を指定すると、インスタンスを各 AZ に均等配置し、AZ 障害に耐える。AZ 追加時はリバランスで再配置される。
- **ELB との連携**: ASG に ALB/NLB のターゲットグループをアタッチすると、スケールアウト時にインスタンスを自動登録。**ELB ヘルスチェック**を ASG のヘルスチェックに採用すると、ネットワーク到達不能なインスタンスも置換対象になる（EC2 ステータスチェックだけでは検知できない）。
- ロードバランサーは**各 AZ で1サブネット**を有効化し、ASG のサブネットと AZ を一致させること。
- 起動テンプレートで**サブネット・SG・ENI/パブリック IP 割り当て**を制御。プライベートサブネット配置＋NAT GW でアウトバウンド、という構成が定石。
- スケーリングに伴い ENI・プライベート IP を消費するため、**サブネットの空き IP** がスケール上限を制約しないよう CIDR を設計する。

---

## 4. 他サービスとの連携

- **Elastic Load Balancing**: ターゲット登録・ヘルスチェック連携。
- **CloudWatch**: メトリクスアラームでスケーリングをトリガー（[CloudWatch](../cloudwatch/README.md)）。
- **VPC**: サブネット/AZ/SG/NAT 設計（[VPC](../../networking-content-delivery/vpc/README.md)）。

---

## 5. 制約・コスト

- Auto Scaling 自体は無料。起動した EC2・ELB・NAT GW 等の利用料が発生。
- サブネットの利用可能 IP がスケールの上限要因になり得る。

---

## 6. 出典

- [Auto Scaling groups – AWS Docs](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html)
- [Attach an Elastic Load Balancing load balancer to your Auto Scaling group – AWS Docs](https://docs.aws.amazon.com/autoscaling/ec2/userguide/attach-load-balancer-asg.html)
- [Add an Availability Zone – AWS Docs](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-add-az-console.html)
