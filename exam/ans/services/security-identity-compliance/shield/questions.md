---
service: shield
domain_default: 4
source: README.md
source_sha256: f36a3176f3a0f450b44959088a4147805e03cd6f16abbd791c2f495d6da8389b
generated: 2026-05-24
---

## shield-001
- type: single
- difficulty: easy
- domain: 4
- tags: [shield]

Shield Standard と Shield Advanced の違いとして正しいものはどれか。

- [ ] A. Standard は有料で L7 まで保護、Advanced は無料で L3/L4 のみ
- [x] B. Standard は無料で L3/L4 を自動緩和、Advanced は有料で L3/L4/L7・SRT 支援・コスト保護を提供
- [ ] C. どちらも有料で機能は同一
- [ ] D. Standard は申し込みが必要、Advanced は自動付帯

> **解説**: Standard は全 AWS 顧客に無料・常時オンで L3/L4 を自動緩和。Advanced は有料サブスクで L7 を含む高度な保護、SRT 支援、DDoS コスト保護、FMS 連携を提供する。
> **出典**: [shield README #2 コアコンセプト](README.md#2-コアコンセプト)

## shield-002
- type: multi
- difficulty: medium
- domain: 4
- tags: [shield, firewall-manager]

Shield Advanced が保護対象とできるリソースはどれか。3つ選べ。

- [x] A. Amazon CloudFront ディストリビューション
- [x] B. Elastic Load Balancing（ALB/NLB/CLB）
- [x] C. EC2 の Elastic IP
- [ ] D. Amazon S3 バケット
- [ ] E. Amazon RDS インスタンス

> **解説**: Shield Advanced の保護対象は CloudFront / Route 53 ホストゾーン / Global Accelerator（standard）/ ELB（ALB・NLB・CLB）/ EC2 の Elastic IP。S3 や RDS は保護対象ではない。
> **出典**: [shield README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## shield-003
- type: single
- difficulty: medium
- domain: 4
- tags: [shield, waf, alb]

L7（アプリケーション層）の DDoS 攻撃を自動緩和するために前提となる構成はどれか。

- [ ] A. Shield Standard のみ
- [x] B. Shield Advanced ＋ AWS WAF
- [ ] C. Network Firewall のステートレスルール
- [ ] D. NACL のレート制限

> **解説**: L7 緩和は Shield Advanced と WAF が前提。Advanced が WAF の自動緩和ルールを生成して L7 攻撃を緩和する。Standard は L3/L4 のみ。
> **出典**: [shield README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## shield-004
- type: single
- difficulty: medium
- domain: 4
- tags: [shield]

DDoS 攻撃によるオートスケールやデータ転送の課金急増を補償したい。どの機能が該当するか。

- [ ] A. Shield Standard のコスト保護
- [x] B. Shield Advanced の DDoS コスト保護（クレジット補償）
- [ ] C. AWS Budgets のアラート
- [ ] D. Savings Plans

> **解説**: DDoS コスト保護は Shield Advanced 限定の機能で、攻撃起因のスケール（ELB/CloudFront/Route 53 等）の課金急増分をクレジットで補償する。「攻撃時の予期せぬ課金を防ぐ」要件は Advanced。
> **出典**: [shield README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## shield-005
- type: single
- difficulty: easy
- domain: 4
- tags: [shield, use-case-fit]

SRT（Shield Response Team）について正しいものはどれか。

- [ ] A. Standard 加入者が無料で利用できる
- [x] B. Advanced 加入者が攻撃時に支援を受けられる専門チームである
- [ ] C. WAF のマネージドルールの名称である
- [ ] D. DDoS 攻撃を行う攻撃者グループである

> **解説**: SRT（旧称 DRT）は Shield Advanced 加入者が攻撃時にプロアクティブ対応を依頼できる専門チーム。Standard では利用できない。
> **出典**: [shield README #2 コアコンセプト](README.md#2-コアコンセプト)

## shield-006
- type: single
- difficulty: medium
- domain: 4
- tags: [shield, firewall-manager, multi-account]

組織内の全アカウントを Shield Advanced で保護し、新規アカウントも自動加入させたい。最適な手段はどれか。

- [ ] A. 各アカウントで個別に Advanced をサブスクする
- [x] B. Firewall Manager の Shield Advanced ポリシーで一括サブスク・自動加入させる
- [ ] C. SCP で Advanced を強制する
- [ ] D. Route 53 ヘルスチェックで一括加入する

> **解説**: Firewall Manager で組織全メンバーアカウントを Shield Advanced に一括サブスクライブでき、新規アカウントも自動加入する。SCP は許可上限を定めるだけでサブスクしない。
> **出典**: [shield README #5 他サービスとの連携](README.md#5-他サービスとの連携)

## shield-007
- type: single
- difficulty: medium
- domain: 1
- tags: [global-accelerator, nlb]

大規模な L3/L4 攻撃をエニーキャストの固定 IP で吸収しやすくするために前段に置くべきサービスはどれか。

- [ ] A. NAT Gateway
- [x] B. Global Accelerator（固定エニーキャスト IP）＋ Shield
- [ ] C. API Gateway
- [ ] D. VPC エンドポイント

> **解説**: Global Accelerator を前段に置くと固定エニーキャスト IP と Shield により大規模 L3/L4 攻撃を吸収しやすくなる。GA（standard）は Advanced の保護対象でもある。
> **出典**: [shield README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## shield-008
- type: single
- difficulty: medium
- domain: 4
- tags: [shield, security-group]

L7 のリクエスト内容を見た保護は WAF、L3/L4 のボリューム攻撃は Shield が担当する。Shield Standard の自動緩和が対象とするレイヤーはどれか。

- [ ] A. L7 のみ
- [x] B. L3 / L4
- [ ] C. L2 / L3
- [ ] D. すべてのレイヤー

> **解説**: Shield Standard は L3/L4 の一般的なネットワーク/トランスポート層 DDoS を自動緩和する。L7 緩和は Advanced ＋ WAF が必要。
> **出典**: [shield README #2 コアコンセプト](README.md#2-コアコンセプト)

## shield-009
- type: single
- difficulty: hard
- domain: 4
- tags: [shield, cost, pub-sub]

Shield Advanced の料金体系について正しいものはどれか。

- [ ] A. 保護リソース1つあたりの従量課金のみ
- [x] B. 固定サブスクリプション料（組織単位、1年コミット）＋データ転送従量
- [ ] C. 完全無料
- [ ] D. 攻撃を受けたときのみ課金される

> **解説**: Shield Advanced は組織単位・1年コミットの固定サブスクリプション料に加え、データ転送の従量課金がかかる。組織でサブスクすると複数アカウントをまとめて保護でき、FMS で新規アカウントも自動加入させられる。
> **出典**: [shield README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## shield-010
- type: single
- difficulty: medium
- domain: 3
- tags: [shield, health-check]

Shield Advanced の検出精度を高めるために連携できる機能はどれか。

- [ ] A. CloudWatch 異常検出のみ
- [x] B. Route 53 ヘルスチェックによるヘルスベース検出
- [ ] C. GuardDuty の脅威検出
- [ ] D. Config のルール評価

> **解説**: ヘルスベース検出は Route 53 ヘルスチェックと連携して検出精度を向上させる。
> **出典**: [shield README #2 コアコンセプト](README.md#2-コアコンセプト)
