---
service: ec2-auto-scaling
domain_default: 1
source: README.md
source_sha256: 6c0772432488cb4ad32d07fe6c622a8e704ff01edef74581cfd1c6b1b1f3ec9b
generated: 2026-05-24
---

## ec2-auto-scaling-001
- type: single
- difficulty: easy
- domain: 1
- tags: [multi-az, high-availability, subnetting]

単一 AZ のサブネットだけを指定して構成された Auto Scaling Group がある。可用性を高めるための最も適切な変更はどれか。

- [ ] A. インスタンスタイプを大型化する
- [x] B. 複数 AZ のサブネットを ASG に追加し、インスタンスを均等分散させる
- [ ] C. ヘルスチェックを EC2 ステータスチェックに固定する
- [ ] D. 起動テンプレートを複数登録する

> **解説**: ASG のサブネット指定が AZ 指定に相当する。単一 AZ のみだとその AZ 障害でサービス全停止する。複数 AZ のサブネットを与えると EC2 Auto Scaling が均等分散し、単一 AZ 障害でも他 AZ で稼働継続できる。
> **出典**: [EC2 Auto Scaling README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ec2-auto-scaling-002
- type: single
- difficulty: medium
- domain: 3
- tags: [health-check, alb, troubleshooting]

ASG 配下のインスタンスでアプリが HTTP 500 を返す不健全状態になっても、インスタンスが置き換えられない。原因として最も妥当なものはどれか。

- [ ] A. ターゲットグループが IP ターゲットになっている
- [x] B. ASG のヘルスチェックが EC2 ステータスチェックのみで ELB ヘルスチェックが無効
- [ ] C. AZ リバランスが無効になっている
- [ ] D. 起動テンプレートが古い

> **解説**: ASG のデフォルトは EC2 ステータスチェックのみで、これは OS/ハードウェアレベルの健全性しか見ない。HTTP 500 のようなアプリ層の不健全を検知して置換するには、ELB ヘルスチェックを ASG で有効化する必要がある。
> **出典**: [EC2 Auto Scaling README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ec2-auto-scaling-003
- type: single
- difficulty: easy
- domain: 1
- tags: [target-type, service-discovery, alb]

ASG とターゲットグループの連携について正しいものはどれか。

- [ ] A. インスタンスは手動でターゲットグループに登録する必要がある
- [x] B. ASG にターゲットグループをアタッチすると、起動時に自動登録・終了時に自動解除される
- [ ] C. ターゲットグループは ASG ごとに最大 1 つしかアタッチできない
- [ ] D. ターゲットグループ連携にはヘルスチェックを無効化する必要がある

> **解説**: ASG にターゲットグループをアタッチすると、スケールアウトで起動したインスタンスは自動登録され、スケールインで終了するインスタンスは自動解除される。手動登録は不要。
> **出典**: [EC2 Auto Scaling README #2 コアコンセプト](README.md#2-コアコンセプト)

## ec2-auto-scaling-004
- type: single
- difficulty: medium
- domain: 3
- tags: [auto-scaling, enhanced-networking]

ASG の AZ リバランス（再均等化）の挙動として正しいものはどれか。

- [ ] A. 先に古いインスタンスを終了してから新規を起動する
- [x] B. 先に新規インスタンスを起動してから古いものを終了するため一時的に希望容量を超えることがある
- [ ] C. 希望容量を絶対に超えないよう同時置換する
- [ ] D. リバランスは AZ 障害時のみ実行される

> **解説**: AZ リバランスは可用性を優先し、先にインスタンスを起動してから古いものを終了する。このため一時的に希望容量（DesiredCapacity）を超えることがある。容量計画でこの挙動を考慮する必要がある。
> **出典**: [EC2 Auto Scaling README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ec2-auto-scaling-005
- type: single
- difficulty: medium
- domain: 1
- tags: [target-type, eni]

ASG とターゲットグループを連携する際の登録方式として、ASG が自動連携する標準的な方式はどれか。

- [ ] A. IP アドレス登録
- [x] B. インスタンス ID 登録
- [ ] C. Lambda ターゲット登録
- [ ] D. ENI 登録

> **解説**: ターゲットグループはインスタンス ID 登録で ASG と連携し、スケール時に自動で登録/解除される。IP 登録は手動寄りの運用となり ASG の自動連携には向かない。
> **出典**: [EC2 Auto Scaling README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ec2-auto-scaling-006
- type: single
- difficulty: easy
- domain: 1
- tags: [alb, subnetting, use-case-fit]

ELB と ASG を組み合わせる際の AZ 設計の原則として正しいものはどれか。

- [ ] A. ELB と ASG は異なる AZ をカバーさせるべき
- [x] B. ELB がカバーする AZ と同じ AZ を ASG のサブネットでカバーするべき
- [ ] C. ASG は ELB が使う AZ の半分だけをカバーすべき
- [ ] D. ELB は単一 AZ、ASG は複数 AZ にすべき

> **解説**: ELB がトラフィックを分散できるのは、その ELB が有効化している AZ にバックエンドが存在する場合。ASG のサブネット（AZ）を ELB と同じ AZ に揃えるのが原則で、揃っていないとトラフィックが流れない AZ が生じる。
> **出典**: [EC2 Auto Scaling README #3 アーキテクチャ](README.md#3-アーキテクチャ--仕組み)

## ec2-auto-scaling-007
- type: single
- difficulty: medium
- domain: 4
- tags: [health-check, vpc-link, use-case-fit]

EC2 Auto Scaling Group がサポートするヘルスチェックタイプとして該当しないものはどれか。

- [ ] A. EC2 ステータスチェック
- [ ] B. ELB ヘルスチェック
- [ ] C. VPC Lattice ヘルスチェック
- [x] D. Route 53 ヘルスチェック

> **解説**: ASG のヘルスチェックタイプは EC2 / ELB / VPC Lattice / カスタムがサポートされる。Route 53 のヘルスチェックは DNS フェイルオーバ用であり、ASG のヘルスチェックタイプには含まれない。
> **出典**: [EC2 Auto Scaling README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## ec2-auto-scaling-008
- type: single
- difficulty: medium
- domain: 3
- tags: [cost, data-transfer]

マルチ AZ で ASG を運用する際のコストに関して正しいものはどれか。

- [ ] A. EC2 Auto Scaling 機能自体に時間課金が発生する
- [ ] B. マルチ AZ 配置では AZ 間データ転送が完全無料になる
- [x] C. EC2 Auto Scaling 自体は無料だが、AZ 間データ転送料に留意する必要がある
- [ ] D. ELB を使うと EC2 Auto Scaling が有料になる

> **解説**: EC2 Auto Scaling 機能そのものは無料で、課金は起動される EC2・ELB・データ転送に対して発生する。マルチ AZ 配置では AZ 間データ転送料が発生するため、設計時に留意が必要。
> **出典**: [EC2 Auto Scaling README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## ec2-auto-scaling-009
- type: multi
- difficulty: medium
- domain: 1
- tags: [health-check, alb, high-availability]

ASG のヘルスチェックと可用性設計について正しいものを 2 つ選べ。

- [x] A. ELB ヘルスチェックを有効化するとアプリ層の不健全（HTTP 500 等）を検知して置換できる
- [ ] B. デフォルトのヘルスチェックは ELB ヘルスチェックである
- [x] C. 不健全と判定されたインスタンスは終了され、必要に応じて別 AZ で再起動される
- [ ] D. ヘルスチェックは ASG が単一 AZ の場合のみ機能する
- [ ] E. ELB ヘルスチェックを有効化すると EC2 ステータスチェックは使えなくなる

> **解説**: ELB ヘルスチェックでアプリ層の不健全を検知でき（A）、不健全インスタンスは終了して別 AZ で再起動され可用性を維持する（C）。デフォルトは EC2 ステータスチェック（B 誤）、AZ 数に依存せず機能し（D 誤）、EC2 と ELB は併用可能（E 誤）。
> **出典**: [EC2 Auto Scaling README #2 コアコンセプト](README.md#2-コアコンセプト)

## ec2-auto-scaling-010
- type: multi
- difficulty: hard
- domain: 1
- tags: [multi-az, multi-region, routing-policy]

広域（マルチリージョン）での高可用性を含む ASG 可用性設計について、正しいものを 2 つ選べ。

- [x] A. ASG に複数 AZ のサブネットを指定すると EC2 Auto Scaling が均等分散する
- [ ] B. ASG は単独でリージョンをまたいでインスタンスを分散できる
- [x] C. マルチリージョン構成では Route 53 の DNS ルーティングと組み合わせる
- [ ] D. ASG は AZ 障害時に自動でリージョンを切り替える
- [ ] E. AZ リバランスはリージョン間で容量を移動する機能である

> **解説**: ASG は複数 AZ のサブネット指定で均等分散する（A）。リージョンをまたぐ広域可用性は ASG 単独では実現できず、Route 53 の DNS ルーティングと組み合わせる（C）。ASG はリージョンをまたがず（B/D 誤）、AZ リバランスはリージョン間移動ではない（E 誤）。
> **出典**: [EC2 Auto Scaling README #5 他サービスとの連携](README.md#5-他サービスとの連携)
