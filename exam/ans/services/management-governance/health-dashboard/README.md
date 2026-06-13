# AWS Health Dashboard（ネットワーク観点）

> カテゴリ: マネジメントとガバナンス / 重要度: △
> 最終更新: 2026-05-24

---

## 1. 概要

AWS Health Dashboard は、**AWS 側のサービスイベント・計画メンテナンス・自アカウントに影響するイベント**を通知するサービス。「Service Health Dashboard（全体的なサービス状況）」と「**AWS Health Dashboard - Your account（アカウント固有）**」があり、後者は **AWS Health API / EventBridge** と連携して自動通知できる。ネットワーク観点では、**Direct Connect のメンテナンス通知**や**VPN/ネットワーク機器の計画メンテ**の検知が問われる。

---

## 2. コアコンセプト

| 要素 | 内容 |
|---|---|
| **Service Health（公開）** | AWS 全体のサービス稼働状況 |
| **Your account（アカウント固有）** | 自リソースに影響するイベント・計画メンテ・スケジュール変更 |
| **AWS Health API** | イベントをプログラムから取得（Business 以上） |
| **イベントタイプ** | issue（障害）/ scheduledChange（計画メンテ）/ accountNotification |

---

## 3. 試験頻出ポイント（ネットワーク）

- **Direct Connect の計画メンテナンス**通知をアカウント固有イベントとして受信。冗長接続への切替え準備のトリガーになる。
- **EventBridge 連携**でメンテナンス・障害イベントを起点に SNS 通知や Lambda 自動対応（例: 経路フェイルオーバー、運用チームへの即時通知）を構成。
- アカウント固有イベントの取得・API 利用は **Business / Enterprise サポート**が前提。
- 「AWS 側の問題か、自構成の問題か」の切り分けの一次情報源。

---

## 4. 他サービスとの連携

- **EventBridge / SNS**: イベント駆動の通知・自動化。
- **Direct Connect / VPN**: メンテ対象のハイブリッド接続（冗長設計の判断材料）。
- **Trusted Advisor**: サービス上限等の別観点（[Trusted Advisor](../trusted-advisor/README.md)）。

---

## 5. 制約・コスト

- Health Dashboard 自体は無料。Health API のフルアクセスは Business 以上のサポートプランが必要。

---

## 6. 出典

- [AWS Health Dashboard – AWS Docs](https://docs.aws.amazon.com/health/latest/ug/aws-health-dashboard-status.html)
- [AWS Health concepts – AWS Docs](https://docs.aws.amazon.com/health/latest/ug/aws-health-concepts-and-terms.html)
