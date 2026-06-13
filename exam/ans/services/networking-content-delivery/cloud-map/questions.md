---
service: cloud-map
domain_default: 1
source: README.md
source_sha256: 057b679b5da93478ffa91bb44834180504fe15b9981af6de7aac1680c4841c10
generated: 2026-05-24
---

## cloud-map-001
- type: single
- difficulty: medium
- domain: 1
- tags: [service-discovery, vpc-endpoint, routing-policy]

VPC 内のマイクロサービス間で `service.namespace.local` のような名前でプライベートに名前解決させたい。選ぶべき Cloud Map の名前空間種別はどれか。

- [x] A. プライベート DNS 名前空間
- [ ] B. パブリック DNS 名前空間
- [ ] C. HTTP 名前空間（API のみ）
- [ ] D. 名前空間は不要

> **解説**: プライベート DNS 名前空間を選ぶと、裏で Route 53 プライベートホストゾーンが自動生成され、VPC の DNS リゾルバ（VPC+2）で名前解決できる。VPC 内サービス間の名前解決の中核。
> **出典**: [cloud-map README #3 名前空間の種別](README.md#3-名前空間の種別最重要)

## cloud-map-002
- type: single
- difficulty: hard
- domain: 1
- tags: [vpc-endpoint, dns]

Cloud Map のプライベート DNS 名前空間のネットワーク観点での核心として正しいものはどれか。

- [ ] A. 内部で NAT Gateway を作成する
- [x] B. Route 53 プライベートホストゾーンが自動生成され、複数 VPC へ関連付けて共有できる
- [ ] C. インターネット越しの DNS 解決にのみ対応する
- [ ] D. DNS レコードを一切作らない

> **解説**: プライベート DNS 名前空間の実体は Route 53 プライベートホストゾーンで、Cloud Map が自動生成する。複数 VPC へ関連付けて共通の名前空間で発見を共有できる。
> **出典**: [cloud-map README #3 名前空間の種別](README.md#3-名前空間の種別最重要)

## cloud-map-003
- type: single
- difficulty: medium
- domain: 1
- tags: [service-discovery]

DNS キャッシュの影響を避け、DNS に依存せずヘルシーなインスタンスの IP/ポートをアプリから直接取得したい。適切な構成はどれか。

- [ ] A. プライベート DNS 名前空間 ＋ A レコード解決
- [ ] B. パブリック DNS 名前空間 ＋ CNAME
- [x] C. HTTP 名前空間 ＋ DiscoverInstances API
- [ ] D. Route 53 ヘルスチェックのみ

> **解説**: HTTP 名前空間は DNS レコードを作らず、DiscoverInstances API のみで発見する。アプリが直接 API を呼んでヘルシーなインスタンスを取得でき、DNS キャッシュの影響を避けられる。
> **出典**: [cloud-map README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloud-map-004
- type: single
- difficulty: medium
- domain: 2
- tags: [service-discovery]

Amazon ECS のサービスディスカバリを有効化したときの Cloud Map との関係として正しいものはどれか。

- [ ] A. ECS は Cloud Map を一切使わず独自の仕組みで発見する
- [x] B. 内部で Cloud Map を使い、タスクの起動/停止に合わせてインスタンスを自動登録/解除する
- [ ] C. タスクは手動で RegisterInstance を呼ぶ必要がある
- [ ] D. ECS サービスディスカバリはパブリック DNS 名前空間のみ対応する

> **解説**: ECS サービスディスカバリは内部で Cloud Map を使い、タスク起動/停止に合わせてサービスインスタンスを自動登録/解除する。プライベート DNS 名前空間にタスクが自動登録され `service.namespace.local` で相互解決できる。
> **出典**: [cloud-map README #7 よくある設計パターン](README.md#7-よくある設計パターン)

## cloud-map-005
- type: single
- difficulty: medium
- domain: 3
- tags: [health-check]

Cloud Map のヘルスチェックと発見結果について正しいものはどれか。

- [ ] A. ヘルスチェックは非対応で、登録されたすべてのインスタンスが返る
- [x] B. Route 53 ヘルスチェックまたはカスタムヘルスチェックを使い、ヘルシーなインスタンスのみが発見結果に返る
- [ ] C. ヘルスチェックは Route 53 のみ対応する
- [ ] D. カスタムヘルスチェックは自動で状態を判定する

> **解説**: Cloud Map は Route 53 ヘルスチェック（パブリックにルーティング可能な IP、追加課金）と、アプリ/サードパーティが UpdateInstanceCustomHealthStatus で報告するカスタムヘルスチェックの2種に対応する。いずれもヘルシーなインスタンスのみが発見結果に返る。
> **出典**: [cloud-map README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloud-map-006
- type: single
- difficulty: easy
- domain: 1
- tags: [multi-region]

Cloud Map の名前空間のスコープに関する説明として正しいものはどれか。

- [ ] A. グローバルリソースで全リージョンで共有される
- [x] B. リージョン固有で、マルチリージョンでは各リージョンに作成が必要
- [ ] C. アカウント全体で 1 つしか作れない
- [ ] D. AZ 固有である

> **解説**: 名前空間はリージョン固有。マルチリージョン構成では各リージョンに名前空間を作成する必要がある。
> **出典**: [cloud-map README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloud-map-007
- type: single
- difficulty: medium
- domain: 1
- tags: [dns, service-discovery]

Cloud Map のサービスがサポートする DNS レコード種別と、ポート情報も返せるレコードの組み合わせとして正しいものはどれか。

- [x] A. A / AAAA / SRV / CNAME をサポートし、SRV はポートも返せる
- [ ] B. A レコードのみサポートする
- [ ] C. MX / TXT のみサポートする
- [ ] D. CNAME のみサポートし、ポートは返せない

> **解説**: Cloud Map のサービスは A / AAAA / SRV / CNAME をサポートし、レコード種別はサービスに紐づく。SRV はホスト名に加えてポートも返せるため、ポート情報が必要な発見に向く。
> **出典**: [cloud-map README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloud-map-008
- type: single
- difficulty: medium
- domain: 1
- tags: [service-mesh, use-case-fit]

App Mesh の Virtual Node のサービスディスカバリ先として Cloud Map を使うとき、どのような利点があるか。

- [x] A. DNS と並ぶ発見手段として Cloud Map を指定でき、ヘルシーなインスタンスを発見できる
- [ ] B. App Mesh は Cloud Map を利用できない
- [ ] C. Cloud Map を使うと Envoy が不要になる
- [ ] D. Cloud Map はメッシュの BGP 経路を制御する

> **解説**: App Mesh の Virtual Node は発見方法として DNS または Cloud Map を選べる。Cloud Map を指定すると Cloud Map のサービスディスカバリ機能を活用できる。
> **出典**: [cloud-map README #5 他サービスとの連携](README.md#5-他サービスとの連携)

## cloud-map-009
- type: multi
- difficulty: hard
- domain: 1
- tags: [service-discovery, dns]

Cloud Map の名前空間種別について正しいものを 2 つ選べ。

- [x] A. パブリック DNS 名前空間は Route 53 パブリックホストゾーンを使い、登録済みドメイン名が必要
- [x] B. HTTP 名前空間は DiscoverInstances API のみで発見し、DNS レコードを作らない
- [ ] C. プライベート DNS 名前空間はインターネット越しの DNS クエリに対応する
- [ ] D. パブリック DNS 名前空間は DNS を一切使わない
- [ ] E. HTTP 名前空間は Route 53 プライベートホストゾーンを自動作成する

> **解説**: パブリック DNS 名前空間は Route 53 パブリックホストゾーンを使い登録ドメインが必要。HTTP 名前空間は API のみで DNS レコードを作らない。プライベート DNS は VPC 内の DNS クエリ用で、C/D/E は誤り。
> **出典**: [cloud-map README #3 名前空間の種別](README.md#3-名前空間の種別最重要)

## cloud-map-010
- type: single
- difficulty: easy
- domain: 3
- tags: [cost]

Cloud Map の課金体系について正しいものはどれか。

- [ ] A. 前払いの固定ライセンス料が必要
- [x] B. レジストリに登録したサービスインスタンス数と DiscoverInstances 等の API 呼び出し回数による従量課金
- [ ] C. VPC 数に応じた固定課金のみ
- [ ] D. 完全無料である

> **解説**: Cloud Map は前払いなしの従量課金で、登録したリソース（サービスインスタンス）数と DiscoverInstances 等の API 呼び出し回数で課金される。DNS 発見や Route 53 ヘルスチェックを使うと Route 53 の料金が別途発生する。
> **出典**: [cloud-map README #6 制約・上限・コスト](README.md#6-制約上限コスト)
