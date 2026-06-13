---
service: ram
domain_default: 4
source: README.md
source_sha256: 684efa59969bf78e046b2792e0cd6885abe8515a7c479e259a198608493a5d66
generated: 2026-05-24
---

## ram-001
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-sharing, transit-gateway, multi-account]

複数の AWS アカウントの VPC を同一の Transit Gateway にアタッチして共有したい。標準的な手段はどれか。

- [ ] A. VPC ピアリングで全 VPC を接続する
- [x] B. AWS RAM で Transit Gateway を各アカウントに共有する
- [ ] C. アカウントごとに TGW を作成する
- [ ] D. PrivateLink で TGW を公開する

> **解説**: RAM は TGW を複数アカウントに共有し、同一ハブにアタッチさせる標準手段。アタッチメント自体は各アカウント所有のまま、TGW の所有権はオーナーが保持する。
> **出典**: [ram README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ram-002
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-sharing, ip-exhaustion]

複数アカウントのリソースを1つの VPC に集約し、IP アドレスを集約しつつネットワーク管理を集中したい。最も適切な方法はどれか。

- [ ] A. 各アカウントに VPC を作成しピアリングする
- [x] B. RAM による VPC 共有（サブネット共有）でサブネットをアプリアカウントに共有する
- [ ] C. すべてのリソースをオーナーアカウントに移動する
- [ ] D. Transit Gateway でルーティングのみ共有する

> **解説**: VPC 共有はオーナーが VPC/サブネットを所有・管理し、参加アカウントがサブネットに ENI/リソースを配置する。CIDR を分散させず IP を集約でき、ピアリング不要で同一 VPC 内通信が可能。
> **出典**: [ram README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ram-003
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-sharing, multi-account]

組織内アカウントへの RAM 共有を招待プロセスなしで即時利用可能にするにはどうするか。

- [ ] A. 各アカウントが招待を承諾する
- [x] B. Organizations 内共有を有効化する
- [ ] C. SCP で共有を許可する
- [ ] D. すべてのアカウントを同一 OU にまとめる

> **解説**: 組織内共有を有効化すると OU/組織への共有は招待プロセス不要で即時利用できる。組織外アカウントへの共有は招待＋承諾が必要。
> **出典**: [ram README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ram-004
- type: single
- difficulty: easy
- domain: 1
- tags: [vpc-sharing, multi-account]

RAM でリソースを共有したときの所有権について正しいものはどれか。

- [ ] A. コンシューマーに所有権が移転する
- [x] B. オーナーが所有権を保持したまま使用権だけを付与する
- [ ] C. 共有後はオーナーが操作できなくなる
- [ ] D. 所有権が両アカウントで共有される

> **解説**: オーナーは所有権を保持したまま、コンシューマーには使用権だけを付与する。コンシューマーは権限範囲内で自分のリソースのように操作できる。
> **出典**: [ram README #2 コアコンセプト](README.md#2-コアコンセプト)

## ram-005
- type: multi
- difficulty: medium
- domain: 1
- tags: [vpc-sharing]

RAM で共有可能なネットワーク関連リソースはどれか。3つ選べ。

- [x] A. Route 53 Resolver ルール
- [x] B. マネージド Prefix List
- [x] C. IPAM プール
- [ ] D. NAT Gateway
- [ ] E. インターネットゲートウェイ

> **解説**: RAM で共有可能なネットワークリソースには TGW、VPC サブネット、Route 53 Resolver ルール、マネージド Prefix List、IPAM プール、DNS Firewall ルールグループなどがある。NAT Gateway や IGW は RAM の共有対象ではない。
> **出典**: [ram README #2 主な共有可能ネットワークリソース](README.md#主な共有可能ネットワークリソース)

## ram-006
- type: single
- difficulty: medium
- domain: 4
- tags: [vpc-sharing, scp, privatelink]

RAM で共有されたリソースをコンシューマーが利用する際のアクセス制御について正しいものはどれか。

- [ ] A. 共有によりコンシューマー側の IAM/SCP は無効化される
- [x] B. コンシューマー側の IAM ポリシー・SCP は引き続き適用される
- [ ] C. オーナーの IAM ポリシーがコンシューマーに継承される
- [ ] D. RAM のマネージド権限のみが評価される

> **解説**: 共有後もコンシューマー側の IAM ポリシー・SCP は引き続き適用される。RAM のマネージド権限は共有時に付与される操作範囲を定めるが、コンシューマー側のガードレールを無効化しない。
> **出典**: [ram README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## ram-007
- type: single
- difficulty: easy
- domain: 1
- tags: [vpc-sharing, cost]

RAM の利用料金について正しいものはどれか。

- [ ] A. 共有1件あたり月額課金される
- [ ] B. 共有先アカウント数に応じて課金される
- [x] C. RAM 自体は無料で、共有したリソースの利用料は通常どおり発生する
- [ ] D. データ転送量に応じて課金される

> **解説**: RAM 自体は無料。共有したリソースの利用料は通常どおり発生する。VPC 共有によりアカウントごとの NAT GW/エンドポイント重複を削減できる点はコスト最適化に寄与する。
> **出典**: [ram README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## ram-008
- type: single
- difficulty: hard
- domain: 1
- tags: [vpc-sharing, multi-region]

グローバルリソースを RAM で共有する場合のホームリージョンはどこか。

- [ ] A. 共有元アカウントの任意のリージョン
- [x] B. us-east-1（バージニア北部）
- [ ] C. リージョンを問わず共有可能
- [ ] D. eu-west-1（アイルランド）

> **解説**: リージョナルリソースは同一リージョン内での共有に限られ、グローバルリソースの共有は us-east-1 がホームリージョンとなる。
> **出典**: [ram README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ram-009
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-sharing, route-table, iac]

複数アカウントの SG/ルートテーブルが参照する CIDR リストを一元的に更新・配布したい。最適な方法はどれか。

- [ ] A. 各アカウントで CIDR をハードコードする
- [x] B. マネージド Prefix List を RAM で共有し SG/RT から参照させる
- [ ] C. すべての CIDR を SCP に列挙する
- [ ] D. CIDR を Systems Manager パラメータで配布する

> **解説**: マネージド Prefix List を RAM で共有すると、SG/ルートテーブルが参照する CIDR を一元更新でき DRY を実現する。Prefix List を更新すれば参照先すべてに反映される。
> **出典**: [ram README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ram-010
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-sharing, dns]

ハイブリッド DNS の転送ルールを組織内の複数アカウントで再利用したい。最適な方法はどれか。

- [ ] A. 各アカウントで Resolver ルールを個別に作成する
- [x] B. Route 53 Resolver ルールを RAM で組織共有する
- [ ] C. 各 VPC に DNS サーバを立てる
- [ ] D. Prefix List で DNS 設定を配布する

> **解説**: Route 53 Resolver ルールを RAM で共有すると、ハイブリッド DNS の転送設定を組織で再利用でき設定を統一できる。
> **出典**: [ram README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)
