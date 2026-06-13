---
service: health-dashboard
domain_default: 3
source: README.md
source_sha256: 67673ebfae46d3ed8cc2d3155e6a2496f0eb5a62c44fc5e1a46968846d9b83d2
generated: 2026-05-24
---

## health-dashboard-001
- type: single
- difficulty: easy
- domain: 3
- tags: [cloudtrail-events, monitoring]

自アカウントのリソースに影響する計画メンテナンスやスケジュール変更を確認したい。最も適切な情報源はどれか。

- [ ] A. Service Health Dashboard（公開）
- [x] B. AWS Health Dashboard - Your account（アカウント固有）
- [ ] C. Trusted Advisor のコスト最適化チェック
- [ ] D. CloudWatch メトリクスダッシュボード

> **解説**: 「Your account」はアカウント固有のイベント（計画メンテ・スケジュール変更・自リソースへの影響）を表示する。公開の Service Health は AWS 全体の稼働状況で、自リソース固有の情報は持たない。
> **出典**: [Health Dashboard README #2 コアコンセプト](README.md#2-コアコンセプト)

## health-dashboard-002
- type: single
- difficulty: medium
- domain: 3
- tags: [direct-connect, automation]

Direct Connect の計画メンテナンス通知を受け取った。ネットワーク運用上、これを起点に行うべき準備として最も適切なものはどれか。

- [ ] A. オンプレミスルーターを再起動する
- [x] B. 冗長接続（バックアップ経路）への切替え準備を行う
- [ ] C. VPC の CIDR を変更する
- [ ] D. SCP で Direct Connect を一時的に禁止する

> **解説**: Direct Connect の計画メンテナンス通知は、冗長接続への切替え準備のトリガーになる。メンテ中の単一障害点化を避けるため、バックアップ経路を確認・準備する。
> **出典**: [Health Dashboard README #3 試験頻出ポイント（ネットワーク）](README.md#3-試験頻出ポイントネットワーク)

## health-dashboard-003
- type: single
- difficulty: medium
- domain: 3
- tags: [event-routing, automation, pub-sub]

AWS Health のメンテナンス・障害イベントを起点に、運用チームへの即時通知や経路フェイルオーバーの自動対応を構成したい。最も適切なアーキテクチャはどれか。

- [ ] A. CloudWatch Logs のサブスクリプションフィルタを使う
- [x] B. EventBridge で Health イベントを受け、SNS 通知や Lambda 自動対応を起動する
- [ ] C. Config ルールで Health イベントを評価する
- [ ] D. Trusted Advisor の API を定期ポーリングする

> **解説**: AWS Health は EventBridge と連携でき、メンテ・障害イベントを起点に SNS 通知や Lambda による自動対応（経路フェイルオーバー、即時通知）を構成できる。
> **出典**: [Health Dashboard README #3 試験頻出ポイント（ネットワーク）](README.md#3-試験頻出ポイントネットワーク)

## health-dashboard-004
- type: single
- difficulty: medium
- domain: 4
- tags: [cost, health-check]

AWS Health API を使ってアカウント固有のイベントをプログラムから取得するための前提条件はどれか。

- [ ] A. 任意のサポートプランで利用可能
- [x] B. Business または Enterprise サポートプランが必要
- [ ] C. Organizations の管理アカウントである必要がある
- [ ] D. Direct Connect の契約が必要

> **解説**: アカウント固有イベントの取得・Health API のフルアクセスには Business / Enterprise サポートプランが前提。Basic/Developer では利用できない。
> **出典**: [Health Dashboard README #3 試験頻出ポイント（ネットワーク）](README.md#3-試験頻出ポイントネットワーク)

## health-dashboard-005
- type: single
- difficulty: easy
- domain: 3
- tags: [cloudtrail-events]

AWS Health のイベントタイプのうち、計画メンテナンスを表すものはどれか。

- [ ] A. issue
- [x] B. scheduledChange
- [ ] C. accountNotification
- [ ] D. costAnomaly

> **解説**: イベントタイプは issue（障害）/ scheduledChange（計画メンテ）/ accountNotification の3種。計画メンテは scheduledChange。
> **出典**: [Health Dashboard README #2 コアコンセプト](README.md#2-コアコンセプト)

## health-dashboard-006
- type: single
- difficulty: medium
- domain: 3
- tags: [troubleshooting, route-table]

VPN 接続が不安定になり、自社設定か AWS 側の問題か切り分けたい。一次情報源として最も適切なものはどれか。

- [ ] A. CloudTrail の管理イベント
- [x] B. AWS Health Dashboard のアカウント固有イベント
- [ ] C. Well-Architected Tool のレビュー
- [ ] D. VPC フローログのみ

> **解説**: AWS Health Dashboard は「AWS 側の問題か、自構成の問題か」を切り分ける一次情報源となる。AWS 側のメンテ・障害イベントが出ていればその影響を、なければ自構成を疑う。
> **出典**: [Health Dashboard README #3 試験頻出ポイント（ネットワーク）](README.md#3-試験頻出ポイントネットワーク)

## health-dashboard-007
- type: single
- difficulty: easy
- domain: 4
- tags: [cost]

AWS Health Dashboard の料金について正しいものはどれか。

- [x] A. Dashboard 自体は無料だが、Health API のフルアクセスは Business 以上のサポートが必要
- [ ] B. Dashboard の閲覧に月額料金がかかる
- [ ] C. イベント1件あたり従量課金される
- [ ] D. EventBridge 連携に追加のライセンスが必要

> **解説**: Health Dashboard 自体は無料。Health API のフルアクセスのみ Business 以上のサポートプランが必要となる。
> **出典**: [Health Dashboard README #5 制約・コスト](README.md#5-制約コスト)

## health-dashboard-008
- type: multi
- difficulty: hard
- domain: 3
- tags: [event-routing, monitoring, automation]

ハイブリッド接続の運用で AWS Health Dashboard を活用する方法として、正しいものを2つ選べ。

- [x] A. Direct Connect の計画メンテ通知を受けて冗長経路への切替え準備のトリガーにする
- [x] B. EventBridge で Health イベントを受け、Lambda による経路フェイルオーバーや SNS 通知を自動化する
- [ ] C. Health Dashboard で BGP のルーティングポリシーを直接編集する
- [ ] D. Health Dashboard が VPN トンネルを自動で再確立する
- [ ] E. Health Dashboard がオンプレミスルーターの設定を変更する

> **解説**: Health Dashboard は通知・検知の情報源であり、計画メンテ通知の活用や EventBridge 経由の自動化が正しい使い方。ルーティング編集やトンネル再確立、オンプレ機器変更などの能動的操作は行わない。
> **出典**: [Health Dashboard README #3 試験頻出ポイント（ネットワーク）](README.md#3-試験頻出ポイントネットワーク)
