---
service: ec2
domain_default: 1
source: README.md
source_sha256: bede56e88bc73098c69ce24ccb6b811773fd167779d555daa244a813ae350bc9
generated: 2026-05-24
---

## ec2-001
- type: single
- difficulty: medium
- domain: 1
- tags: [enhanced-networking, placement-group]

密結合の HPC ワークロードで MPI/NCCL による集団通信を行い、ノード間で最低レイテンシ・高スループットが必要である。最も適切な構成はどれか。

- [ ] A. ENA を有効化し、Spread Placement Group に配置する
- [x] B. EFA を有効化し、Cluster Placement Group に配置する
- [ ] C. 複数 ENI を各インスタンスに付与し、Partition Placement Group に配置する
- [ ] D. セカンダリ IP を多数割り当て、Placement Group なしで配置する

> **解説**: EFA は ENA に OS バイパス機能を加えたアダプタで、MPI/NCCL の集団通信に最適。EFA の OS バイパスは同一 Cluster Placement Group 内でのみ有効なため、Cluster との併用が必須。Spread/Partition では低レイテンシ要件を満たせない。
> **出典**: [EC2 README #2 コアコンセプト](README.md#2-コアコンセプト)

## ec2-002
- type: single
- difficulty: easy
- domain: 1
- tags: [eni, failover, multi-az]

ENI（Elastic Network Interface）の付け替えに関する制約として正しいものはどれか。

- [ ] A. ENI はリージョンをまたいで別 AZ のインスタンスにアタッチできる
- [x] B. ENI は同一 AZ 内のサブネットにのみアタッチできる
- [ ] C. ENI は一度アタッチすると別インスタンスに付け替えできない
- [ ] D. ENI はインスタンス起動時にのみ作成できる

> **解説**: ENI は同一 AZ 内のサブネットにのみアタッチ可能で、AZ をまたげない。一方でインスタンス間での付け替えは可能で、フェイルオーバ用途に使える。AZ をまたぐ移動はできない点が頻出。
> **出典**: [EC2 README #3 アーキテクチャ](README.md#3-アーキテクチャ--仕組み)

## ec2-003
- type: single
- difficulty: medium
- domain: 1
- tags: [eni, enhanced-networking]

可用性向上のため 1 つの EC2 インスタンスに複数の ENI を追加した。ネットワーク帯域に関して正しいものはどれか。

- [ ] A. ENI を 2 つにすると総帯域は約 2 倍になる
- [ ] B. ENI を追加すると単一フローの上限帯域が上がる
- [x] C. ENI を追加してもインスタンスの総帯域は増えない
- [ ] D. ENI 追加により帯域はインスタンスタイプの制限を超えられる

> **解説**: ネットワーク帯域はインスタンスタイプ（サイズ）で決まり、ENI を追加しても総帯域は増えない。複数 ENI の主目的は IP/サブネット/SG の分離やフェイルオーバであって帯域増ではない。
> **出典**: [EC2 README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## ec2-004
- type: single
- difficulty: easy
- domain: 1
- tags: [placement-group, high-availability]

少数の重要なインスタンスを個別のハードウェアに分散させ、相関障害を避けたい。適切な Placement Group の種類はどれか。

- [ ] A. Cluster
- [x] B. Spread
- [ ] C. Partition
- [ ] D. Dedicated

> **解説**: Spread Placement Group は各インスタンスを個別のハードウェア（ラック）に分散配置し、単一ハードウェア障害の影響を局所化する。少数の重要インスタンスの可用性確保に適し、AZ あたり最大 7 インスタンスの制約がある。
> **出典**: [EC2 README #4 Placement Group](README.md#4-placement-group頻出)

## ec2-005
- type: single
- difficulty: medium
- domain: 1
- tags: [placement-group, quotas]

Spread Placement Group における AZ あたりのインスタンス数の上限として正しいものはどれか。

- [ ] A. AZ あたり最大 3 インスタンス
- [x] B. AZ あたり最大 7 インスタンス
- [ ] C. AZ あたり最大 7 パーティション
- [ ] D. 上限なし

> **解説**: Spread Placement Group は AZ あたり最大 7 インスタンスという制約がある。「最大 7 パーティション」は Partition Placement Group の制約であり混同しやすい。
> **出典**: [EC2 README #7 制約・上限・コスト](README.md#7-制約上限コスト)

## ec2-006
- type: single
- difficulty: medium
- domain: 1
- tags: [placement-group, event-routing]

Hadoop や Kafka、Cassandra といった大規模分散システムをデプロイし、ラック単位での障害分離を行いたい。適切な Placement Group はどれか。

- [ ] A. Cluster
- [ ] B. Spread
- [x] C. Partition
- [ ] D. なし（デフォルト配置）

> **解説**: Partition Placement Group はパーティション（ラック）単位でインスタンス群を分離し、パーティション障害が他に波及しないようにする。Hadoop/Kafka/Cassandra など大規模分散ワークロードに適する。グループあたり AZ ごと最大 7 パーティション。
> **出典**: [EC2 README #4 Placement Group](README.md#4-placement-group頻出)

## ec2-007
- type: single
- difficulty: hard
- domain: 1
- tags: [enhanced-networking, gwlb, placement-group]

2 つの EC2 インスタンス間で単一フローのスループットが 5 Gbps を超える必要がある。実現する構成はどれか。

- [ ] A. 異なる AZ に配置し ENI を 2 つずつ付与する
- [ ] B. リージョン内 VPC ピアリングで接続する
- [x] C. ENA 対応インスタンスを同一 Cluster Placement Group に配置する
- [ ] D. NAT Gateway を経由させてフローを集約する

> **解説**: 単一フローで 5 Gbps を超える通信は、原則として同一 Cluster Placement Group 内の ENA 対応インスタンスに限られる（Cluster は単一フロー最大 10 Gbps）。リージョン内ピア間など PG 外は 5 Gbps が上限の基本。ENI 追加では単一フロー帯域は上がらない。
> **出典**: [EC2 README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## ec2-008
- type: single
- difficulty: medium
- domain: 3
- tags: [enhanced-networking, config-rules]

小〜中サイズのインスタンスで、平常時は問題ないが持続的に高いネットワーク負荷をかけると徐々にスループットが低下する。最も妥当な説明はどれか。

- [ ] A. ENI のアタッチ数が上限に達したため
- [x] B. ベースライン帯域＋バーストのクレジットを使い切り、ベースライン帯域に律速されたため
- [ ] C. Placement Group が Spread になっているため
- [ ] D. EFA の OS バイパスが無効になったため

> **解説**: ネットワーク帯域はインスタンスサイズに比例し、小サイズはベースライン帯域＋バースト（クレジット制）で動作する。持続的な高負荷ではクレジットを使い切り、ベースライン帯域に律速される。サイズを上げるとベースラインが向上する。
> **出典**: [EC2 README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## ec2-009
- type: single
- difficulty: medium
- domain: 1
- tags: [mtu, subnetting]

EC2 インスタンス間でジャンボフレーム（MTU 9001）を利用する際の制約として正しいものはどれか。

- [ ] A. すべての経路で MTU 9001 が利用できる
- [x] B. 同一 VPC 内・一部経路でのみ有効で、IGW/VPN 経由は 1500 になる
- [ ] C. ジャンボフレームはインターネット経由でも 9001 を維持する
- [ ] D. MTU 9001 は EFA 利用時のみ有効

> **解説**: ジャンボフレーム（MTU 9001）は同一 VPC 内かつ一部経路でのみ有効。IGW やVPN を経由する通信は MTU 1500 に制限される。広域や外部経路では 1500 にフォールバックする点が頻出。
> **出典**: [EC2 README #5 試験頻出ポイント](README.md#5-試験頻出ポイント)

## ec2-010
- type: multi
- difficulty: hard
- domain: 1
- tags: [eni, security-group]

1 つの EC2 インスタンスに複数の ENI を付与する設計について、正しいものを 2 つ選べ。

- [x] A. 管理面とデータ面を別サブネット/別 SG に分離するデュアルホーム構成が可能
- [ ] B. ENI を AZ をまたいでアタッチできる
- [x] C. ENI を別インスタンスに付け替えてフェイルオーバを実現できる
- [ ] D. ENI を追加するとインスタンスの総ネットワーク帯域が増える
- [ ] E. 複数 ENI は EFA を有効化したインスタンスでのみ利用できる

> **解説**: 複数 ENI は異なるサブネット/SG に同時所属でき、管理/データ分離のデュアルホームに使える（A）。また ENI は付け替え可能でフェイルオーバ用途に使える（C）。ENI は AZ をまたげず（B 誤）、帯域は増えず（D 誤）、EFA とは無関係（E 誤）。
> **出典**: [EC2 README #2 コアコンセプト](README.md#2-コアコンセプト)

## ec2-011
- type: multi
- difficulty: medium
- domain: 1
- tags: [enhanced-networking]

拡張ネットワーキングと EFA に関する記述のうち、正しいものを 2 つ選べ。

- [x] A. 拡張ネットワーキングは SR-IOV により高 PPS・低レイテンシ・低 CPU を実現する
- [ ] B. EFA はインターネット越えの通信でも OS バイパスが有効
- [x] C. EFA は ENA に OS バイパスを加えたもので Cluster Placement Group が必須
- [ ] D. ENA を使うには追加のネットワーク料金が発生する
- [ ] E. ENA は最大 1 Gbps までしか対応しない

> **解説**: 拡張ネットワーキングは SR-IOV ベースで高 PPS・低レイテンシ（A）。EFA は ENA＋OS バイパスで Cluster Placement Group 必須（C）。EFA の OS バイパスは VPC 内・同一 PG でのみ有効でインターネット越えには使えない（B 誤）。ENA/EFA 自体に追加料金はなく（D 誤）、ENA は最大 100 Gbps 級（E 誤）。
> **出典**: [EC2 README #2 コアコンセプト](README.md#2-コアコンセプト)
