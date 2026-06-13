---
service: network-firewall
domain_default: 4
source: README.md
source_sha256: ea5accc86c9b76f07357413556c286f944c950df9b3f625da7b82f587a30569e
generated: 2026-05-24
---

## network-firewall-001
- type: single
- difficulty: medium
- domain: 4
- tags: [network-firewall]

AWS Network Firewall の検査エンジンについて正しい説明はどれか。

- [ ] A. ステートレスエンジンのみを持ち単一パケットを評価する
- [x] B. ステートレス（5タプル）とステートフル（Suricata 互換）の両エンジンを持つ
- [ ] C. ステートフルエンジンのみで L3/L4 検査はできない
- [ ] D. L7 検査はできず L3/L4 のみ

> **解説**: Network Firewall は L3/L4 のステートレス検査と、Suricata 互換ルールによる L7 ステートフル検査の両方を行うマネージドファイアウォール兼 IDS/IPS。
> **出典**: [network-firewall README #1 概要](README.md#1-概要)

## network-firewall-002
- type: single
- difficulty: hard
- domain: 4
- tags: [network-firewall, direct-connect]

集中インスペクション VPC を設計する際、ファイアウォールエンドポイントを配置するサブネットに関する重要な制約はどれか。

- [ ] A. エンドポイントは保護対象リソースと同じサブネットに置く必要がある
- [x] B. エンドポイントは自分のいるサブネットのトラフィックを検査できないため専用サブネットにする
- [ ] C. 1 VPC に1つのファイアウォールサブネットしか作れない
- [ ] D. ファイアウォールサブネットはパブリックサブネットでなければならない

> **解説**: ファイアウォールエンドポイントは自サブネットのトラフィックを検査できない。よって専用サブネットを用意し、保護対象は別サブネットに配置してルートテーブルで誘導する。
> **出典**: [network-firewall README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## network-firewall-003
- type: single
- difficulty: hard
- domain: 4
- tags: [transit-gateway]

Transit Gateway 経由の集中インスペクションで、ステートフル検査の戻りパケットが別 AZ に流れて検査が壊れる問題を防ぐにはどうするか。

- [ ] A. ステートレスルールのみを使う
- [x] B. Transit Gateway の appliance mode を有効化して対称ルーティングにする
- [ ] C. AZ を1つだけにする
- [ ] D. ECMP を有効化する

> **解説**: TGW 経由でステートフル検査が AZ をまたぐと戻りが別 AZ に行き検査が壊れる。appliance mode を有効化するとフローを同一 AZ の同一エンドポイントへ対称ルーティングできる。
> **出典**: [network-firewall README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## network-firewall-004
- type: single
- difficulty: medium
- domain: 4
- tags: [network-firewall, data-transfer]

アウトバウンド通信を「許可されたドメインのみ」に限定したい（例: S3 など既知ドメインのみ）。Network Firewall でどう実現するか。

- [ ] A. ステートレスルールで宛先 IP を許可リスト化する
- [x] B. ステートフルルールで `tls.sni` / `http.host` を使い許可ドメインのみ Pass、それ以外を Drop する
- [ ] C. NACL でドメインを Deny する
- [ ] D. セキュリティグループでドメイン名を許可する

> **解説**: アウトバウンドのドメインフィルタはステートフルルールで `tls.sni` / `http.host` を評価し、許可ドメインのみ Pass しそれ以外を Drop する。IP ベースの SG/NACL ではドメイン単位の制御はできない。
> **出典**: [network-firewall README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## network-firewall-005
- type: single
- difficulty: medium
- domain: 3
- tags: [monitoring]

Network Firewall のログ出力について正しいものはどれか。

- [ ] A. ステートレスエンジンもフローログを出力できる
- [x] B. ステートフルエンジンのみフロー/アラート/TLS ログを出力でき、ステートレスはメトリクスのみ
- [ ] C. どちらのエンジンもログは出せない
- [ ] D. ログは CloudWatch Logs にのみ配信できる

> **解説**: ログ出力はステートフルエンジンのみ（フロー/アラート/TLS）。ステートレスはメトリクスのみ。配信先は CloudWatch Logs / S3 / Kinesis Data Firehose。
> **出典**: [network-firewall README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## network-firewall-006
- type: single
- difficulty: hard
- domain: 1
- tags: [gwlb, use-case-fit]

サードパーティ製の仮想アプライアンス（例: Palo Alto）で検査したい要件がある。Network Firewall と GWLB の使い分けで正しいものはどれか。

- [ ] A. Network Firewall でサードパーティアプライアンスを直接ホストできる
- [x] B. GWLB で自前/サードパーティアプライアンスを GENEVE で透過挿入する
- [ ] C. GWLB は AWS マネージドエンジンのみ対応する
- [ ] D. 両者は完全に同一機能で違いはない

> **解説**: Network Firewall はマネージドな AWS 製エンジン。GWLB は自前/サードパーティの仮想アプライアンスを GENEVE で透過挿入する仕組み。特定ベンダ製品が必要なら GWLB を選ぶ。
> **出典**: [network-firewall README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## network-firewall-007
- type: multi
- difficulty: medium
- domain: 4
- tags: [network-firewall]

Network Firewall のステートフルエンジンで指定できるアクションはどれか。3つ選べ。

- [x] A. Pass
- [x] B. Drop
- [x] C. Alert
- [ ] D. Forward to stateless
- [ ] E. Encrypt

> **解説**: ステートフルエンジンのアクションは Pass / Drop / Alert / Reject。ステートレス側が `Forward to stateful` でステートフルへ渡す（逆方向の「Forward to stateless」は存在しない）。Encrypt はアクションではない。
> **出典**: [network-firewall README #2 ステートレス vs ステートフル](README.md#ステートレス-vs-ステートフル)

## network-firewall-008
- type: single
- difficulty: medium
- domain: 4
- tags: [network-firewall]

ステートレスルールで `Forward to stateful` したトラフィックについて正しいものはどれか。

- [ ] A. ログには記録されず破棄される
- [x] B. ステートフルエンジンで検査・ログ記録される
- [ ] C. 自動的に Pass される
- [ ] D. 再度ステートレスエンジンへ戻る

> **解説**: ステートレスで `Forward to stateful` したトラフィックだけがステートフルエンジンで検査され、フロー/アラート/TLS ログに記録される。
> **出典**: [network-firewall README #2 ステートレス vs ステートフル](README.md#ステートレス-vs-ステートフル)

## network-firewall-009
- type: single
- difficulty: medium
- domain: 3
- tags: [cost, data-transfer]

Network Firewall のコスト最適化について正しいものはどれか。

- [ ] A. エンドポイント数に関係なく定額課金される
- [x] B. エンドポイントは AZ ごとに課金されるため必要 AZ 数を見極め、クロス AZ 検査のデータ転送料に注意する
- [ ] C. ログ量はコストに影響しない
- [ ] D. ステートフル検査は無料

> **解説**: 課金はエンドポイント時間（AZ ごと）＋処理データ量。クロス AZ 検査はデータ転送料が増え、ログ量が多いと配信先コストも増大する。アラートログのみに絞る選択肢もある。
> **出典**: [network-firewall README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## network-firewall-010
- type: single
- difficulty: medium
- domain: 1
- tags: [transit-gateway, event-routing]

集中インスペクションと分散インスペクションの選択について正しいものはどれか。

- [ ] A. 集中型は TGW 不要で管理点が最少になる
- [x] B. 分散型は各 VPC に FW を配置し小規模・少数 VPC で単純だが管理点が増える
- [ ] C. 分散型では East-West 検査ができない
- [ ] D. 集中型は VPC が少ないほど有利

> **解説**: 分散型は各 VPC に Network Firewall を配置し、VPC 数が少ない小規模構成では単純だが管理点が増える。集中型は TGW をハブに全フローを Inspection VPC へ誘導し East-West/North-South を一箇所で検査する。
> **出典**: [network-firewall README #7 よくある設計パターン](README.md#7-よくある設計パターン)

## network-firewall-011
- type: single
- difficulty: hard
- domain: 1
- tags: [data-transfer, nat]

集中 egress 構成でインスペクション後にアドレス変換を行う場合の正しい配置順はどれか。

- [ ] A. NAT GW → Network Firewall → IGW
- [x] B. Network Firewall → NAT GW → IGW
- [ ] C. IGW → NAT GW → Network Firewall
- [ ] D. NAT GW → IGW → Network Firewall

> **解説**: 集中 egress では FW → NAT GW → IGW の順に配置し、インスペクションの後にアドレス変換を行う。NAT を先にすると送信元 IP が失われ検査・ログの可視性が下がる。
> **出典**: [network-firewall README #5 他サービスとの連携](README.md#5-他サービスとの連携)
