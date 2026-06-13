---
service: route-53
domain_default: 1
source: README.md
source_sha256: d67155f9d3b046299cd5ffed12cffbf44fc84bb3954d8a9ed1eaa40357c4b967
generated: 2026-05-24
---

## route-53-001
- type: single
- difficulty: easy
- domain: 2
- tags: [routing-policy, dns]

Zone Apex（例: `example.com`）を ALB に向けたい。適切なレコードはどれか。

- [ ] A. CNAME レコード
- [x] B. エイリアス（Alias）レコード
- [ ] C. NS レコード
- [ ] D. TXT レコード

> **解説**: CNAME は Zone Apex で使用できない。エイリアスは Zone Apex で使え、AWS リソース宛は無料で、リソースの IP 変化に自動追従する。Apex を ELB/CloudFront/S3 へ向けるなら必ずエイリアス。
> **出典**: [route-53 README #3 レコードとエイリアス](README.md#3-レコードとエイリアス)

## route-53-002
- type: single
- difficulty: hard
- domain: 1
- tags: [routing-policy]

ユーザーへの応答をリソースの地理的位置に基づいて返しつつ、特定リージョンへ流すトラフィック量を bias で手動調整したい。適切なルーティングポリシーはどれか。

- [ ] A. Geolocation
- [x] B. Geoproximity
- [ ] C. Latency
- [ ] D. IP-based

> **解説**: Geoproximity はリソースの地理的位置 + bias で範囲を拡縮し、トラフィック量を手動でシフトできる（Traffic Flow 必須）。Geolocation はユーザーの国/大陸/州で振り分けるもので bias はない。両者の違いは頻出。
> **出典**: [route-53 README #4 ルーティングポリシー](README.md#4-ルーティングポリシー8種最重要)

## route-53-003
- type: single
- difficulty: medium
- domain: 1
- tags: [routing-policy]

マルチリージョン構成でユーザーの応答速度を最優先し、実測レイテンシが最も低い AWS リージョンへ振り分けたい。適切なポリシーはどれか。

- [x] A. Latency（LBR）
- [ ] B. Geolocation
- [ ] C. Weighted
- [ ] D. Multivalue

> **解説**: Latency ルーティングはユーザーから最も低レイテンシの AWS リージョンへ向ける（リージョンベース・実測レイテンシ）。Geolocation はユーザーの地理的位置ベースで、必ずしも最速ではない。混同に注意。
> **出典**: [route-53 README #4 ルーティングポリシー](README.md#4-ルーティングポリシー8種最重要)

## route-53-004
- type: single
- difficulty: medium
- domain: 1
- tags: [routing-policy, failover, health-check]

Failover ルーティングポリシー（Active-Passive）の前提条件として正しいものはどれか。

- [ ] A. Multivalue と併用する必要がある
- [x] B. プライマリレコードにヘルスチェックの関連付けが必須
- [ ] C. プライマリとセカンダリは同一リージョンに置く必要がある
- [ ] D. ヘルスチェックは関連付け不可

> **解説**: Failover はプライマリにヘルスチェックが必須で、プライマリ Unhealthy 時にセカンダリへ切り替える。Simple はヘルスチェックを関連付けできない。DR やメンテナンスページ切替に使う。
> **出典**: [route-53 README #6 ヘルスチェックとフェイルオーバー](README.md#6-ヘルスチェックとフェイルオーバー)

## route-53-005
- type: single
- difficulty: hard
- domain: 3
- tags: [health-check, vpc-endpoint, monitoring]

プライベートサブネット内のリソースをヘルスチェックしてフェイルオーバーに使いたい。パブリックチェッカーから到達できない場合の正しい方法はどれか。

- [ ] A. パブリック IP を付与してエンドポイント監視する
- [x] B. CloudWatch メトリクスを発行し、CloudWatch アラーム連動（または Calculated）ヘルスチェックで監視する
- [ ] C. Multivalue ルーティングに切り替える
- [ ] D. ヘルスチェック間隔を 10 秒にする

> **解説**: プライベートリソースは世界中のパブリックチェッカーから到達できない。CloudWatch メトリクス + CloudWatch アラーム連動ヘルスチェック（または Calculated）で健全性を判定する。頻出の引っかけ。
> **出典**: [route-53 README #6 ヘルスチェックとフェイルオーバー](README.md#6-ヘルスチェックとフェイルオーバー)

## route-53-006
- type: single
- difficulty: hard
- domain: 2
- tags: [dns, security-group]

VPC 内のリソースがオンプレミスの `corp.example.com` を名前解決できるようにしたい。必要な構成はどれか。

- [ ] A. Inbound Endpoint のみ
- [x] B. Outbound Endpoint + 条件付き転送 Resolver Rule（オンプレ DNS へ転送）
- [ ] C. Private Hosted Zone のみ
- [ ] D. DNS Firewall の ALLOW ルール

> **解説**: AWS → オンプレの名前解決には Outbound Endpoint と条件付き転送（FORWARD）Resolver Rule を使い、指定ドメインの問い合わせをオンプレ DNS へ転送する。Inbound Endpoint はオンプレ → AWS の解決用で逆方向。
> **出典**: [route-53 README #7 Route 53 Resolver](README.md#7-route-53-resolverハイブリッド-dns超頻出)

## route-53-007
- type: single
- difficulty: medium
- domain: 2
- tags: [dns, security-group]

オンプレミスの DNS サーバが AWS の Private Hosted Zone の名前を解決できるようにしたい。必要な構成はどれか。

- [x] A. Inbound Endpoint を作り、オンプレからその IP へ転送する
- [ ] B. Outbound Endpoint を作る
- [ ] C. DNSSEC 署名を有効化する
- [ ] D. パブリックホストゾーンに同名レコードを作る

> **解説**: オンプレ → AWS の名前解決には Inbound Endpoint を使う。ENI に IP を割り当て、オンプレ DNS からその IP へ転送すると、PHZ 等の AWS 上の名前を解決できる。
> **出典**: [route-53 README #7 Route 53 Resolver](README.md#7-route-53-resolverハイブリッド-dns超頻出)

## route-53-008
- type: single
- difficulty: hard
- domain: 4
- tags: [network-firewall, security-group]

VPC からのアウトバウンド DNS クエリをドメインリストでフィルタし、マルウェアの C2 ドメインへの問い合わせを遮断したい。利用する機能はどれか。

- [ ] A. AWS WAF
- [ ] B. AWS Network Firewall
- [x] C. Route 53 Resolver DNS Firewall
- [ ] D. セキュリティグループ

> **解説**: Route 53 Resolver DNS Firewall は VPC からのアウトバウンド DNS クエリをドメインリストでフィルタ（ALLOW/BLOCK/ALERT）し、C2 ドメイン遮断やデータ流出防止に使う。DNS レイヤの保護は DNS Firewall であり、WAF や Network Firewall とは別物。
> **出典**: [route-53 README #8 DNSSEC / DNS Firewall / クエリログ](README.md#8-dnssec--dns-firewall--クエリログ)

## route-53-009
- type: single
- difficulty: medium
- domain: 1
- tags: [bgp, dns]

VPC 内からは内部 IP、外部からは公開 IP を返す split-horizon DNS を実現したい。正しい構成はどれか。

- [x] A. 同名のパブリックホストゾーンとプライベートホストゾーンを作る
- [ ] B. パブリックホストゾーンに 2 種類の A レコードを作る
- [ ] C. DNS Firewall でクエリを振り分ける
- [ ] D. Latency ルーティングを使う

> **解説**: 同名のパブリック PHZ とプライベート PHZ を作ると、VPC 内からはプライベート、外部からはパブリックの応答を返す split-horizon（split-view）DNS になる。PHZ には VPC の enableDnsSupport/enableDnsHostnames が必要。
> **出典**: [route-53 README #5 ホストゾーンと Split-Horizon DNS](README.md#5-ホストゾーンと-split-horizon-dns)

## route-53-010
- type: single
- difficulty: hard
- domain: 3
- tags: [high-availability, failover]

マルチリージョンアプリで、DNS フェイルオーバーよりも確実に、リカバリ先の容量を保証したリージョン退避を実現したい。最適なサービスはどれか。

- [ ] A. Route 53 Failover ルーティング単体
- [x] B. Amazon Application Recovery Controller (ARC)
- [ ] C. Geoproximity ルーティング
- [ ] D. DNS Firewall

> **解説**: ARC は Readiness Check でリカバリ先の容量/構成を継続監視し、Routing Control で確実なフェイルオーバースイッチを提供する。データプレーンは 5 リージョン構成で極めて高可用。DNS フェイルオーバーより確実な、容量保証のリージョン退避を問われたら ARC。
> **出典**: [route-53 README #9 Route 53 ARC](README.md#9-route-53-arcapplication-recovery-controller)

## route-53-011
- type: multi
- difficulty: hard
- domain: 1
- tags: [routing-policy]

Route 53 のルーティングポリシーに関して正しいものを 2 つ選べ。

- [x] A. Weighted は重み（0〜255）でトラフィックを比率配分し、Blue/Green やカナリアに使える
- [x] B. Multivalue は最大 8 件の正常レコードをランダム返却し、各値にヘルスチェックを付けられる
- [ ] C. Simple ポリシーはヘルスチェックを関連付けできる
- [ ] D. Multivalue は ALB のような高度な負荷分散を行う LB の代替である
- [ ] E. Geolocation は実測レイテンシで振り分ける

> **解説**: Weighted は 0〜255 の重みで比率配分し B/G・カナリア・A/B テストに使う。Multivalue は最大 8 件をランダム返却し各値を個別にヘルスチェックできるが、LB の代替ではない。Simple はヘルスチェック不可、Geolocation は地理的位置ベース（レイテンシは Latency）。
> **出典**: [route-53 README #4 ルーティングポリシー](README.md#4-ルーティングポリシー8種最重要)

## route-53-012
- type: multi
- difficulty: medium
- domain: 2
- tags: [dns, vpc-sharing, multi-account]

マルチアカウントでハイブリッド DNS を一元管理する構成として正しいものを 2 つ選べ。

- [x] A. Resolver Rule を AWS RAM で他アカウントに共有し、各 VPC に関連付ける
- [ ] B. 各アカウントで個別に Resolver Rule を重複作成するのが定石である
- [x] C. 多数 VPC への PHZ 関連付けは Route 53 Profiles が推奨（PHZ あたり関連付け上限 300）
- [ ] D. Resolver エンドポイントはアカウント間で物理的に共有される
- [ ] E. RAM 共有では Resolver クエリログを共有できない

> **解説**: Resolver Rule は RAM で他アカウントへ共有し各 VPC に関連付けて一元管理するのが定石。多数 VPC へ PHZ を束ねるには Route 53 Profiles が推奨（PHZ あたり VPC 関連付け上限 300）。個別重複作成は管理が破綻する。
> **出典**: [route-53 README #7 Route 53 Resolver](README.md#7-route-53-resolverハイブリッド-dns超頻出)
