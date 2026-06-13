---
service: well-architected-tool
domain_default: 1
source: README.md
source_sha256: 137604eb117a0c967f07d45ed47d0106619aa61ef0feb4b598d2fe7de56111fe
generated: 2026-05-24
---

## well-architected-tool-001
- type: single
- difficulty: easy
- domain: 1
- tags: [well-architected]

AWS Well-Architected フレームワークの6つの柱に含まれないものはどれか。

- [ ] A. 信頼性
- [ ] B. セキュリティ
- [x] C. 拡張性（Scalability）
- [ ] D. コスト最適化

> **解説**: 6つの柱は運用上の優秀性・セキュリティ・信頼性・パフォーマンス効率・コスト最適化・持続可能性。拡張性は独立した柱ではない（パフォーマンス効率/信頼性で扱われる）。
> **出典**: [Well-Architected Tool README #1 概要](README.md#1-概要)

## well-architected-tool-002
- type: single
- difficulty: medium
- domain: 1
- tags: [well-architected, high-availability]

ネットワーク設計で NAT Gateway や VGW、接続が単一障害点になっていないかを点検したい。主にどの柱の観点か。

- [ ] A. コスト最適化の柱
- [x] B. 信頼性の柱
- [ ] C. 持続可能性の柱
- [ ] D. パフォーマンス効率の柱

> **解説**: マルチ AZ 冗長や単一障害点の排除、Direct Connect + VPN のバックアップ経路、クォータ管理は信頼性の柱の観点。
> **出典**: [Well-Architected Tool README #2 ネットワークに関わる主な観点](README.md#2-ネットワークに関わる主な観点)

## well-architected-tool-003
- type: single
- difficulty: medium
- domain: 4
- tags: [security-group]

セキュリティの柱でネットワーク設計を点検する際の観点として最も適切なものはどれか。

- [ ] A. NAT GW のデータ処理料の削減
- [x] B. 多層防御（SG＋NACL）・最小権限・トラフィック検査・境界保護・プライベート接続
- [ ] C. Enhanced Networking/EFA の選択
- [ ] D. リージョン間転送コストの最適化

> **解説**: セキュリティの柱は多層防御（SG＋NACL）、最小権限、トラフィック検査（Network Firewall/GWLB）、境界保護（WAF/Shield）、プライベート接続（PrivateLink/エンドポイント）を点検する。
> **出典**: [Well-Architected Tool README #2 ネットワークに関わる主な観点](README.md#2-ネットワークに関わる主な観点)

## well-architected-tool-004
- type: single
- difficulty: medium
- domain: 1
- tags: [enhanced-networking, monitoring]

パフォーマンス効率の柱でネットワーク機能の選択を点検する際の例として適切なものはどれか。

- [ ] A. SG と NACL の多層防御
- [x] B. Enhanced Networking/EFA、Global Accelerator、CloudFront の適切な選択
- [ ] C. マルチ AZ の NAT Gateway
- [ ] D. 未使用 EIP の削減

> **解説**: パフォーマンス効率は適切なネットワーク機能の選択（Enhanced Networking/EFA、Global Accelerator、CloudFront）を点検する。多層防御はセキュリティ、NAT マルチ AZ は信頼性、EIP 削減はコスト。
> **出典**: [Well-Architected Tool README #2 ネットワークに関わる主な観点](README.md#2-ネットワークに関わる主な観点)

## well-architected-tool-005
- type: single
- difficulty: medium
- domain: 1
- tags: [cost, nat]

コスト最適化の柱でネットワーク観点として点検する項目はどれか。

- [ ] A. SG＋NACL の多層防御
- [x] B. NAT GW データ処理料、リージョン間転送、未使用 EIP の削減
- [ ] C. マルチ AZ 冗長の確保
- [ ] D. トラフィック検査の導入

> **解説**: コスト最適化の柱は NAT GW のデータ処理料、リージョン間転送、未使用 EIP の削減を点検する。多層防御や冗長確保は他の柱。
> **出典**: [Well-Architected Tool README #2 ネットワークに関わる主な観点](README.md#2-ネットワークに関わる主な観点)

## well-architected-tool-006
- type: single
- difficulty: medium
- domain: 1
- tags: [well-architected, high-availability, direct-connect]

信頼性の柱が頻出テーマとして重視するネットワーク設計はどれか。

- [ ] A. 単一の Direct Connect 接続でコストを抑える
- [x] B. AZ ごとの NAT GW や冗長 Direct Connect/VPN による単一障害点の排除
- [ ] C. すべての通信をインターネット経由にする
- [ ] D. SG のルールを全開放にして接続性を確保する

> **解説**: 信頼性の柱はネットワークの単一障害点排除（AZ ごとの NAT GW、冗長 Direct Connect/VPN）とサービスクォータの管理を頻出テーマとして重視する。
> **出典**: [Well-Architected Tool README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## well-architected-tool-007
- type: single
- difficulty: easy
- domain: 1
- tags: [iam-policy, well-architected]

ANS 試験における Well-Architected Tool の位置づけとして最も適切なものはどれか。

- [ ] A. ツール自体の操作手順が細かく問われる
- [x] B. ツールよりも、Well-Architected の設計原則がネットワーク設計問題の背景知識として効く
- [ ] C. ネットワークの自動是正を行うツールである
- [ ] D. トラフィックの実測ツールである

> **解説**: 実際の試験は本ツール自体より、Well-Architected の設計原則がネットワーク設計問題の背景知識として効いてくる。自動是正や実測ツールではない。
> **出典**: [Well-Architected Tool README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## well-architected-tool-008
- type: single
- difficulty: easy
- domain: 3
- tags: [cost, use-case-fit]

Well-Architected レビューに取り込み可能な、別サービスのチェック結果はどれか。

- [ ] A. CloudTrail のイベント
- [x] B. Trusted Advisor のチェック結果
- [ ] C. VPC フローログ
- [ ] D. Health Dashboard のイベント

> **解説**: Well-Architected Tool は Trusted Advisor のチェック結果を WA レビューに取り込み可能。これにより推奨事項をレビューに反映できる。
> **出典**: [Well-Architected Tool README #4 他サービスとの連携](README.md#4-他サービスとの連携)

## well-architected-tool-009
- type: multi
- difficulty: hard
- domain: 1
- tags: [well-architected, security-group]

ネットワーク設計のレビューで信頼性の柱に該当する観点を2つ選べ。

- [x] A. マルチ AZ 冗長になっているか
- [x] B. 冗長 Direct Connect/VPN のバックアップ経路があるか
- [ ] C. 多層防御（SG＋NACL）になっているか
- [ ] D. Global Accelerator を使っているか
- [ ] E. 未使用 EIP を削減しているか

> **解説**: 信頼性の柱はマルチ AZ 冗長、単一障害点の排除、冗長 Direct Connect/VPN、クォータ管理を問う。多層防御はセキュリティ、Global Accelerator はパフォーマンス効率、EIP 削減はコスト最適化。
> **出典**: [Well-Architected Tool README #2 ネットワークに関わる主な観点](README.md#2-ネットワークに関わる主な観点)

## well-architected-tool-010
- type: multi
- difficulty: medium
- domain: 4
- tags: [security-group, well-architected, shield]

ネットワーク設計のレビューでセキュリティの柱に該当する観点を2つ選べ。

- [x] A. トラフィック検査（Network Firewall/GWLB）を行っているか
- [x] B. プライベート接続（PrivateLink/エンドポイント）を利用しているか
- [ ] C. AZ ごとに NAT Gateway を配置しているか
- [ ] D. リージョン間転送コストを最適化しているか
- [ ] E. CloudFront でキャッシュ効率を高めているか

> **解説**: セキュリティの柱は多層防御、最小権限、トラフィック検査、境界保護（WAF/Shield）、プライベート接続を点検する。NAT 配置は信頼性、転送コストはコスト最適化、CloudFront はパフォーマンス効率。
> **出典**: [Well-Architected Tool README #2 ネットワークに関わる主な観点](README.md#2-ネットワークに関わる主な観点)
