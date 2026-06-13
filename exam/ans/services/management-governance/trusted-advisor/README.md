# AWS Trusted Advisor（ネットワーク観点）

> カテゴリ: マネジメントとガバナンス / 重要度: △
> 最終更新: 2026-05-24

---

## 1. 概要

AWS Trusted Advisor は、アカウントをベストプラクティスに照らして**自動チェック・推奨事項**を提示するサービス。**コスト最適化・パフォーマンス・セキュリティ・耐障害性・サービス上限・運用上の優秀性**の柱で評価する。ネットワーク観点では、**サービスクォータ（上限）への接近**や、**セキュリティグループの過度な開放**の検出が問われる。

---

## 2. コアコンセプト（チェックカテゴリ）

| カテゴリ | ネットワーク関連の代表チェック |
|---|---|
| **セキュリティ** | SG の過度に許可的なルール（特定ポートの全開放）、ELB のセキュリティ設定 |
| **サービス上限（クォータ）** | VPC 数、EIP 数、Internet Gateway 数、VPN 接続数などが上限に接近していないか |
| **耐障害性** | 単一 AZ 構成、ELB の最適化、マルチ AZ 化の推奨 |
| **コスト最適化** | アイドルなロードバランサー、未関連付け EIP（課金対象）の検出 |

---

## 3. 試験頻出ポイント

- **サービス上限チェック**: EIP・VPC・IGW・VPN 接続などのクォータ逼迫を事前検知。上限引き上げ申請の判断材料。
- **セキュリティ**: SG の無制限アクセス（22/3389 等の全開放）の検出。ただし詳細な継続監査は **Config** や **Firewall Manager** の領域。
- **未関連付け EIP** は課金されるため、コスト最適化チェックで検出される。
- フルチェック（全カテゴリ）は **Business / Enterprise サポート**プランが必要。

---

## 4. 他サービスとの連携

- **Service Quotas / Health Dashboard**: 上限管理・通知（[Health Dashboard](../health-dashboard/README.md)）。
- **Config / Firewall Manager**: 継続的な SG 準拠監査は Config 側（[Config](../config/README.md)）。

---

## 5. 制約・コスト

- Basic/Developer サポートは一部チェックのみ。全チェックは Business 以上。
- Trusted Advisor 自体に追加料金はない（サポートプランに含まれる）。

---

## 6. 出典

- [AWS Trusted Advisor – AWS Docs](https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html)
- [Trusted Advisor check reference – AWS Docs](https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor-check-reference.html)
