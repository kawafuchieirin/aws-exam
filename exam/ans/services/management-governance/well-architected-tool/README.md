# AWS Well-Architected Tool（ネットワーク観点）

> カテゴリ: マネジメントとガバナンス / 重要度: △
> 最終更新: 2026-05-24

---

## 1. 概要

AWS Well-Architected Tool は、ワークロードを **Well-Architected フレームワークの6つの柱**（運用上の優秀性・セキュリティ・信頼性・パフォーマンス効率・コスト最適化・持続可能性）に照らしてレビューし、リスクと改善項目を可視化するツール。ネットワーク観点では、主に**信頼性の柱**と**セキュリティの柱**でネットワーク設計を点検する。

---

## 2. ネットワークに関わる主な観点

| 柱 | ネットワーク観点の問い |
|---|---|
| **信頼性** | マルチ AZ 冗長か、NAT GW/VGW/接続が単一障害点になっていないか、Direct Connect + VPN のバックアップ経路があるか、上限（クォータ）を管理しているか |
| **セキュリティ** | 多層防御（SG＋NACL）、最小権限、トラフィック検査（Network Firewall/GWLB）、境界保護（WAF/Shield）、プライベート接続（PrivateLink/エンドポイント） |
| **パフォーマンス効率** | 適切なネットワーク機能の選択（Enhanced Networking/EFA、Global Accelerator、CloudFront） |
| **コスト最適化** | NAT GW データ処理料、リージョン間転送、未使用 EIP の削減 |

---

## 3. 試験頻出ポイント

- **信頼性の柱**: ネットワークの単一障害点排除（AZ ごとの NAT GW、冗長 Direct Connect/VPN）と**サービスクォータの管理**が頻出テーマ。
- **セキュリティの柱**: ネットワーク境界の保護と多層防御の評価。
- 実際の試験は本ツール自体より、**Well-Architected の設計原則がネットワーク設計問題の背景知識**として効いてくる。

---

## 4. 他サービスとの連携

- **Trusted Advisor**: チェック結果を WA レビューに取り込み可能（[Trusted Advisor](../trusted-advisor/README.md)）。
- **VPC / Direct Connect / Network Firewall**: レビュー対象のネットワーク設計（[VPC](../../networking-content-delivery/vpc/README.md)）。

---

## 5. 制約・コスト

- Well-Architected Tool 自体は無料。

---

## 6. 出典

- [AWS Well-Architected Tool – AWS Docs](https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html)
- [Reliability Pillar – AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
