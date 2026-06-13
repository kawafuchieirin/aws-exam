---
service: auto-scaling
domain_default: 1
source: README.md
source_sha256: 50ad3f6c8f67d011dc7bf2b201594f698f2a5a23eef5854a9d772e7da65fd282
generated: 2026-05-24
---

## auto-scaling-001
- type: single
- difficulty: easy
- domain: 1
- tags: [multi-az, high-availability]

EC2 Auto Scaling グループ（ASG）を AZ 障害に耐える構成にしたい。最も適切な設定はどれか。

- [ ] A. 単一 AZ の 1 サブネットを指定し、希望台数を増やす
- [x] B. 複数 AZ のサブネットを ASG に指定し、インスタンスを各 AZ へ分散させる
- [ ] C. 起動テンプレートで Elastic IP を全インスタンスに割り当てる
- [ ] D. ルートテーブルにブラックホールルートを設定する

> **解説**: ASG に複数 AZ のサブネットを指定すると、インスタンスが各 AZ に均等配置され、AZ 障害時も他 AZ で稼働を継続できる。単一 AZ では AZ 障害で全滅する。EIP やルートは可用性分散の手段ではない。
> **出典**: [auto-scaling README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク)

## auto-scaling-002
- type: single
- difficulty: medium
- domain: 3
- tags: [health-check, troubleshooting]

ネットワーク到達不能になったインスタンスを ASG が検知して自動置換できるようにしたい。ASG のヘルスチェックとして何を採用すべきか。

- [ ] A. EC2 ステータスチェックのみ
- [x] B. ELB ヘルスチェックを ASG のヘルスチェックに採用する
- [ ] C. CloudTrail の管理イベント
- [ ] D. VPC フローログのステータスフィールド

> **解説**: EC2 ステータスチェックはハイパーバイザ/インスタンスレベルの正常性のみを見るため、アプリやネットワーク到達不能を検知できない。ELB ヘルスチェックを ASG に採用すると、ターゲットグループのヘルスチェック失敗インスタンスも置換対象になる。
> **出典**: [auto-scaling README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク)

## auto-scaling-003
- type: single
- difficulty: medium
- domain: 1
- tags: [alb, subnetting]

ALB をアタッチした ASG で、スケールアウトしたインスタンスが ELB のトラフィックを受けられないことがある。確認すべき設定はどれか。

- [ ] A. ASG の希望台数が最大台数を超えていないか
- [x] B. ロードバランサーが有効化している AZ と ASG のサブネットの AZ が一致しているか
- [ ] C. 起動テンプレートに EIP が設定されているか
- [ ] D. NAT Gateway がインスタンスと同じサブネットにあるか

> **解説**: ロードバランサーは各 AZ で 1 サブネットを有効化する必要があり、ASG が起動するサブネットの AZ と LB の有効 AZ が一致していないと、その AZ のインスタンスへトラフィックが流れない。AZ の一致が定石。
> **出典**: [auto-scaling README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク)

## auto-scaling-004
- type: single
- difficulty: medium
- domain: 1
- tags: [auto-scaling, subnetting]

セキュリティ要件上、ASG のインスタンスはインターネットからの直接アクセスを禁止しつつ、アウトバウンド通信は許可したい。定石の構成はどれか。

- [ ] A. パブリックサブネットに配置し、SG でインバウンドを全拒否する
- [x] B. プライベートサブネットに配置し、NAT Gateway 経由でアウトバウンドを行う
- [ ] C. パブリックサブネットに配置し、起動テンプレートでパブリック IP を無効化する
- [ ] D. プライベートサブネットに配置し、Internet Gateway を直接アタッチする

> **解説**: ASG はプライベートサブネットに配置し、アウトバウンドは NAT Gateway を経由するのがネットワークの定石。起動テンプレートでサブネット・SG・パブリック IP 割り当てを制御する。IGW はサブネットに直接アタッチできない。
> **出典**: [auto-scaling README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク)

## auto-scaling-005
- type: single
- difficulty: hard
- domain: 3
- tags: [ip-exhaustion, quotas]

ASG が最大台数までスケールアウトせず、新規インスタンスの起動が失敗する。ネットワーク観点で最も疑うべき原因はどれか。

- [ ] A. 起動テンプレートのバージョンが古い
- [x] B. サブネットの利用可能 IP アドレスが枯渇している
- [ ] C. CloudWatch アラームの評価期間が短い
- [ ] D. ELB のアイドルタイムアウトが短すぎる

> **解説**: スケーリングで ENI・プライベート IP を消費するため、サブネットの空き IP が不足すると新規インスタンスを起動できず、スケール上限を制約する。CIDR は将来のスケールを見込んで設計する必要がある。
> **出典**: [auto-scaling README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク)

## auto-scaling-006
- type: single
- difficulty: medium
- domain: 3
- tags: [monitoring, auto-scaling]

需要に応じて ASG の台数を増減させるトリガーとして、一般的に何を用いるか。

- [ ] A. CloudTrail の管理イベント
- [x] B. CloudWatch メトリクスアラーム
- [ ] C. Config ルールの非準拠通知
- [ ] D. VPC フローログの REJECT 集計

> **解説**: ASG のスケーリングは CloudWatch メトリクスアラーム（CPU 使用率やリクエスト数など）でトリガーするのが一般的。CloudTrail/Config/フローログは監査・監視用途でスケーリングの起点ではない。
> **出典**: [auto-scaling README #4 他サービスとの連携](README.md#4-他サービスとの連携)

## auto-scaling-007
- type: single
- difficulty: easy
- domain: 1
- tags: [target-type, service-discovery]

ASG に ALB のターゲットグループをアタッチした場合、スケールアウト時のインスタンス登録はどうなるか。

- [ ] A. 手動でターゲットグループに登録する必要がある
- [x] B. 起動したインスタンスが自動的にターゲットグループへ登録される
- [ ] C. NLB のみ自動登録され、ALB は手動登録になる
- [ ] D. 登録には Config の修復アクションが必要

> **解説**: ASG にターゲットグループをアタッチすると、スケールアウト時に起動インスタンスが自動でターゲットグループへ登録され、スケールイン時には登録解除される。手動登録は不要。
> **出典**: [auto-scaling README #2 コアコンセプト](README.md#2-コアコンセプト)

## auto-scaling-008
- type: multi
- difficulty: hard
- domain: 1
- tags: [multi-az, alb, use-case-fit]

ASG と ELB を用いた高可用ネットワーク構成のベストプラクティスとして正しいものを 2 つ選べ。

- [ ] A. AZ をまたぐ単一サブネットを 1 つだけ ASG に指定する
- [x] B. ASG に複数 AZ のサブネットを指定してインスタンスを分散する
- [x] C. ロードバランサーは各 AZ で 1 サブネットを有効化し、ASG の AZ と一致させる
- [ ] D. ELB ヘルスチェックは無効にし、EC2 ステータスチェックのみに統一する
- [ ] E. すべてのインスタンスに NAT Gateway を直接アタッチする

> **解説**: 高可用構成では ASG に複数 AZ のサブネットを指定して分散し、ロードバランサーの有効 AZ を ASG の AZ と一致させる。サブネットは AZ をまたげない。ELB ヘルスチェックは到達不能検知のため有効にすべきで、NAT Gateway はインスタンスに直接アタッチするものではない。
> **出典**: [auto-scaling README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク)

## auto-scaling-009
- type: single
- difficulty: easy
- domain: 1
- tags: [cost]

AWS Auto Scaling のコストについて正しいものはどれか。

- [ ] A. ASG の管理台数に応じた月額固定料金が発生する
- [x] B. Auto Scaling 自体は無料で、起動した EC2・ELB・NAT GW 等の利用料が発生する
- [ ] C. スケーリングイベント 1 回ごとに API 課金される
- [ ] D. 複数 AZ 構成にすると ASG の追加料金が発生する

> **解説**: Auto Scaling 自体は無料で、課金されるのは起動した EC2 インスタンスや連携する ELB・NAT Gateway 等の利用料のみ。ASG の台数や AZ 数に対する追加料金はない。
> **出典**: [auto-scaling README #5 制約・コスト](README.md#5-制約コスト)

## auto-scaling-010
- type: single
- difficulty: medium
- domain: 3
- tags: [auto-scaling]

稼働中の ASG に新しい AZ のサブネットを追加した。インスタンス配置はどうなるか。

- [ ] A. 追加した AZ には次回スケールアウトまでインスタンスが配置されない
- [x] B. リバランスにより既存インスタンスが各 AZ へ再配置される
- [ ] C. 既存インスタンスがすべて再起動される
- [ ] D. AZ を追加しても配置は変わらず手動移行が必要

> **解説**: ASG に AZ を追加すると、AZ リバランスによりインスタンスが各 AZ へ均等になるよう再配置される。これにより新 AZ も含めた分散が維持される。
> **出典**: [auto-scaling README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク)
