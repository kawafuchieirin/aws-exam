---
service: osi-and-encapsulation
domain_default: 0
source: README.md
source_sha256: f89bdf44ef1d4049c8e0423c303ffc409a9e6d9ab087767afa394b62f051dcac
generated: 2026-05-24
---

## osi-and-encapsulation-001
- type: single
- difficulty: easy
- domain: 0
- tags: [alb, nlb]

OSI 参照モデルにおける ELB の動作層の対応として正しいものはどれか。

- [ ] A. ALB は L4、NLB は L7
- [x] B. ALB は L7、NLB は L4
- [ ] C. ALB も NLB も L3
- [ ] D. ALB は L2、NLB は L3

> **解説**: ALB は HTTP ヘッダ/パス/ホストを扱う L7、NLB は TCP/UDP のポートを扱う L4。GWLB は L3 で動作する。ELB の使い分けはこの層の理解が前提。
> **出典**: [OSI README #1 概要](README.md#1-概要)

## osi-and-encapsulation-002
- type: single
- difficulty: easy
- domain: 0
- tags: [tcp-udp]

OSI 各層の PDU（呼称）の対応として正しいものはどれか。

- [ ] A. L3 = フレーム、L2 = パケット
- [x] B. L4 = セグメント、L3 = パケット、L2 = フレーム
- [ ] C. L4 = パケット、L3 = フレーム
- [ ] D. すべての層で「パケット」と呼ぶ

> **解説**: L4 はセグメント（TCP）/データグラム（UDP）、L3 はパケット、L2 はフレーム。混同を狙うひっかけが頻出する。
> **出典**: [OSI README #5 PDU](README.md#5-pduprotocol-data-unit-の呼び方)

## osi-and-encapsulation-003
- type: single
- difficulty: easy
- domain: 0
- tags: [tcp-udp]

各層が宛先の識別に使う情報の対応として正しいものはどれか。

- [ ] A. L4 = IP アドレス、L3 = ポート番号
- [x] B. L4 = ポート番号、L3 = IP アドレス、L2 = MAC アドレス
- [ ] C. L2 = IP アドレス、L3 = MAC アドレス
- [ ] D. すべての層で MAC アドレスを使う

> **解説**: L4 はポート番号でプロセスを、L3 は IP アドレスでホストを、L2 は MAC アドレスで隣接ノードを識別する。AWS では即答できることが重要。
> **出典**: [OSI README #2 対応表](README.md#2-osi-7-階層と-tcpip-4-階層の対応)

## osi-and-encapsulation-004
- type: single
- difficulty: medium
- domain: 0
- tags: [http, mtu]

パケットを送信する際のカプセル化の順序として正しいものはどれか。

- [ ] A. L2 ヘッダ → L3 ヘッダ → L4 ヘッダの順に上位へ付与する
- [x] B. L7 データに L4 → L3 → L2 の順でヘッダを付与していく
- [ ] C. すべてのヘッダを同時に 1 つ付与する
- [ ] D. 受信側と同じく L1 から L7 の順に付与する

> **解説**: 送信時は L7 データに対し L4（ポート）→ L3（IP）→ L2（MAC）の順でヘッダを付与（カプセル化）する。受信時は逆順に剥がす（デカプセル化）。
> **出典**: [OSI README #4 カプセル化](README.md#4-カプセル化とデカプセル化)

## osi-and-encapsulation-005
- type: single
- difficulty: medium
- domain: 0
- tags: [use-case-fit]

同一サブネット内で IP アドレスから MAC アドレスを解決するプロトコルはどれか。また、その有効範囲はどれか。

- [ ] A. DNS。範囲はインターネット全体
- [x] B. ARP。範囲は同一ブロードキャストドメイン内のみ
- [ ] C. ARP。範囲はルータを越えて任意のネットワーク
- [ ] D. ICMP。範囲は同一サブネットのみ

> **解説**: ARP は同一ブロードキャストドメイン内で IP → MAC を解決する。ルータ（L3 境界）を越えないため、別ネットワーク宛はデフォルトゲートウェイの MAC に送られルータが転送する。
> **出典**: [OSI README #6 MAC と ARP](README.md#6-mac-アドレスと-arp)

## osi-and-encapsulation-006
- type: single
- difficulty: medium
- domain: 0
- tags: [use-case-fit]

スイッチとルータの違いについて正しいものはどれか。

- [ ] A. スイッチは IP アドレスでルーティングし、ルータは MAC で転送する
- [x] B. スイッチは L2 で MAC により転送し、ルータは L3 で IP によりネットワーク間をルーティングする
- [ ] C. スイッチもルータもブロードキャストを遮断する
- [ ] D. ルータはブロードキャストを転送しドメインを統合する

> **解説**: スイッチは L2 で MAC アドレステーブルに基づき転送、ルータは L3 で IP によりネットワーク間をルーティングする。ルータはブロードキャストを遮断しドメインを分割する。
> **出典**: [OSI README #7 スイッチ vs ルータ](README.md#7-スイッチ-vs-ルータブロードキャストドメイン)

## osi-and-encapsulation-007
- type: single
- difficulty: medium
- domain: 0
- tags: [gwlb, target-type]

セキュリティアプライアンス（IDS/IPS 等）にトラフィックを透過的に振り向けたい。GWLB が動作する層とカプセル化方式の組み合わせとして正しいものはどれか。

- [ ] A. L7 で HTTP ヘッダにより振り分ける
- [ ] B. L4 で TCP ポートにより振り分ける
- [x] C. L3 で動作し GENEVE でカプセル化してアプライアンスに渡す
- [ ] D. L2 で MAC により振り分ける

> **解説**: GWLB は L3 で動作し、GENEVE（UDP 6081）でトラフィックをカプセル化してアプライアンス群に透過的に振り向ける。ALB（L7）/ NLB（L4）とは層が異なる。
> **出典**: [OSI README #9 AWS サービスとの接続](README.md#9-aws-サービスとの接続)

## osi-and-encapsulation-008
- type: single
- difficulty: hard
- domain: 0
- tags: [mtu, icmp]

ジャンボフレーム（MTU 9001）を設定後、Internet Gateway 経由の一部通信が無応答になった。最も疑うべき原因はどれか。

- [ ] A. セキュリティグループに Deny ルールがある
- [x] B. 経路の MTU 1500 区間に対し PMTUD 用の ICMP（Type3 Code4）が遮断されパスがブラックホール化している
- [ ] C. ルートテーブルにブラックホールルートが追加された
- [ ] D. ARP テーブルが破損している

> **解説**: IGW 経由は MTU 1500。経路最小 MTU は PMTUD で調整されるが、"Fragmentation Needed"（ICMP Type3 Code4）を遮断するとサイズ超過パケットが黙って破棄されブラックホール化する。ICMP を通す必要がある。
> **出典**: [OSI README #8 MTU](README.md#8-mtu-とフラグメンテーション)

## osi-and-encapsulation-009
- type: multi
- difficulty: medium
- domain: 0
- tags: [alb, nlb]

ELB の層と特性について正しいものを 2 つ選べ。

- [x] A. ALB は L7 で動作しパス/ホストベースルーティングや HTTP ヘッダ判定ができる
- [x] B. NLB は L4 で動作し TCP/UDP を超低レイテンシで処理する
- [ ] C. ALB は L4 で動作しポート番号のみで判断する
- [ ] D. NLB は L7 で HTTP パスベースルーティングができる
- [ ] E. GWLB は L7 で動作する

> **解説**: ALB は L7（HTTP コンテキストを扱う）、NLB は L4（TCP/UDP・低レイテンシ）。GWLB は L3。層と機能の対応を取り違えるひっかけに注意。
> **出典**: [OSI README #3 各層の役割](README.md#3-各層の役割試験で問われる粒度)

## osi-and-encapsulation-010
- type: multi
- difficulty: easy
- domain: 0
- tags: [use-case-fit, mtu]

ブロードキャストドメインと VPC の特性について正しいものを 2 つ選べ。

- [x] A. ブロードキャストドメインはルータ（L3 境界）で分割される
- [x] B. VPC のサブネットは従来の L2 ブロードキャスト/マルチキャストを基本的に流さない
- [ ] C. ルータはブロードキャストを転送するためドメインが統合される
- [ ] D. スイッチは L3 で IP によりブロードキャストを遮断する
- [ ] E. VPC では任意の L2 ブロードキャストが自由に届く

> **解説**: ブロードキャストドメインはルータで分割される。VPC サブネットはブロードキャスト/マルチキャスト非対応（従来の L2 ブロードキャストは流れない）。スイッチは L2 でブロードキャストを転送する。
> **出典**: [OSI README #7 ブロードキャストドメイン](README.md#7-スイッチ-vs-ルータブロードキャストドメイン)
