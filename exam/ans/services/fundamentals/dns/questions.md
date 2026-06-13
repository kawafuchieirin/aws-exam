---
service: dns
domain_default: 0
source: README.md
source_sha256: ec5018bcc99c0018d7cd3fa2eeda4ed30b71e605276330d8af8313eb9fbf934b
generated: 2026-05-24
---

## dns-001
- type: single
- difficulty: easy
- domain: 0
- tags: [dns]

クライアント（スタブリゾルバ）が再帰リゾルバに対して行う問い合わせの種類はどれか。

- [x] A. 再帰問い合わせ（最終的な答えをまるごと要求する）
- [ ] B. 反復問い合わせ（次に聞くべきサーバを要求する）
- [ ] C. ゾーン転送（AXFR）
- [ ] D. 権威応答のみを要求する問い合わせ

> **解説**: クライアントはリゾルバに「最終的な答えを返して」と依頼する再帰問い合わせを行う。リゾルバが上位（ルート/TLD/権威）に対して行うのが反復問い合わせ。
> **出典**: [DNS README #3 再帰と反復](README.md#3-名前解決フロー再帰と反復)

## dns-002
- type: single
- difficulty: easy
- domain: 0
- tags: [dns]

Zone Apex（例: `example.com`）を AWS の ELB に向けたい。標準的な CNAME が使えない理由として正しいものはどれか。

- [ ] A. CNAME は IPv6 を表現できないため
- [x] B. Zone Apex には SOA/NS が必須で、CNAME と併存できないため
- [ ] C. CNAME は TTL を設定できないため
- [ ] D. CNAME は AWS リソースを指せないため

> **解説**: RFC 上、Apex には SOA と NS が必要で、CNAME は同名の他レコードと併存できない。Apex には Route 53 の ALIAS を使う。
> **出典**: [DNS README #4 CNAME と ALIAS](README.md#cname-と-alias-の違いaws-文脈で頻出)

## dns-003
- type: single
- difficulty: medium
- domain: 0
- tags: [dns]

逆引き（IP → 名前）に使われるレコードと特殊ドメインの組み合わせとして正しいものはどれか。

- [ ] A. A レコード / `in-addr.arpa`
- [x] B. PTR レコード / `in-addr.arpa`（IPv4）・`ip6.arpa`（IPv6）
- [ ] C. CNAME レコード / `reverse.arpa`
- [ ] D. NS レコード / `ptr.arpa`

> **解説**: 逆引きは PTR レコードを `in-addr.arpa`（IPv4）/`ip6.arpa`（IPv6）に置き、IP を逆順に並べる。
> **出典**: [DNS README #6 正引き/逆引き](README.md#6-ゾーン委任と正引き逆引き)

## dns-004
- type: single
- difficulty: medium
- domain: 0
- tags: [dns, failover]

DNS フェイルオーバーで切り替えを「より速く」反映させるための定石はどれか。

- [ ] A. レコードの TTL を長く（例: 86400 秒）設定しておく
- [x] B. 切替前にレコードの TTL を短く（例: 60 秒）下げておく
- [ ] C. SOA のシリアル番号を 0 に固定する
- [ ] D. CNAME を A レコードに変換する

> **解説**: TTL の間リゾルバは応答をキャッシュするため、TTL を短くしておくと旧キャッシュの残存が短くなり切替が速く反映される。
> **出典**: [DNS README #5 TTL](README.md#5-ttlキャッシュ生存時間)

## dns-005
- type: single
- difficulty: medium
- domain: 0
- tags: [dns]

MX レコードの優先度（preference）について正しいものはどれか。

- [x] A. 値が小さいほど優先される
- [ ] B. 値が大きいほど優先される
- [ ] C. 値は無視され、ランダムに選ばれる
- [ ] D. 値は TTL を表す

> **解説**: MX の優先度は数値が小さいほど優先。複数の同値があれば負荷分散される。
> **出典**: [DNS README #4 レコード種別](README.md#4-レコード種別頻出)

## dns-006
- type: single
- difficulty: easy
- domain: 0
- tags: [dns, hybrid]

VPC 内のインスタンスが内部名を解決する際に既定で問い合わせる、VPC CIDR の +2 アドレスにあるものはどれか。

- [ ] A. オンプレミスの権威 DNS サーバ
- [ ] B. ルートネームサーバ
- [x] C. VPC の Route 53 Resolver（再帰リゾルバ）
- [ ] D. Internet Gateway の DNS プロキシ

> **解説**: VPC には CIDR の +2 アドレスに Amazon 提供 DNS（Route 53 Resolver）が存在し、再帰リゾルバとして名前解決を担う。ハイブリッド DNS の土台。
> **出典**: [DNS README #7 AWS サービスとの接続](README.md#7-aws-サービスとの接続)

## dns-007
- type: single
- difficulty: medium
- domain: 0
- tags: [dns]

サブドメイン `dev.example.com` を別チームの DNS サーバに委任したい。`example.com` ゾーンに置くべきレコードはどれか。

- [ ] A. CNAME レコード
- [x] B. `dev` の NS レコード（委任先ネームサーバを指定）
- [ ] C. SOA レコード
- [ ] D. TXT レコード

> **解説**: ゾーンの委任は親ゾーンに子の NS レコードを置くことで行う。`example.com` 内に `dev` の NS を置くと下位ゾーンへ委任される。
> **出典**: [DNS README #6 ゾーン委任](README.md#6-ゾーン委任と正引き逆引き)

## dns-008
- type: single
- difficulty: hard
- domain: 0
- tags: [dns]

新しい A レコードを追加したのに一部のクライアントでしばらく解決できない。最も可能性の高い原因はどれか。

- [ ] A. SOA レコードが存在しない
- [ ] B. レコードのタイプが AAAA だった
- [x] C. 直前の NXDOMAIN（不在）応答がネガティブキャッシュとして残っている
- [ ] D. 権威サーバが再帰問い合わせを行っている

> **解説**: 不在応答（NXDOMAIN）は SOA の最小 TTL に従ってネガティブキャッシュされるため、レコード追加直後でもキャッシュが切れるまで引けないことがある。
> **出典**: [DNS README #3 キャッシュ](README.md#キャッシュ)

## dns-009
- type: multi
- difficulty: medium
- domain: 0
- tags: [dns, failover, health-check]

Route 53 の ALIAS レコードが標準的な CNAME に対して持つ利点はどれか。2 つ選べ。

- [x] A. Zone Apex（`example.com`）に設定できる
- [x] B. AWS リソース宛のクエリ課金がなく、リソースの IP 変化に自動追従する
- [ ] C. 任意の外部ドメイン名（他社の FQDN）を直接指せる
- [ ] D. DNSSEC 署名が不要になる
- [ ] E. 反復問い合わせを再帰問い合わせに変換できる

> **解説**: ALIAS は Route 53 独自で Zone Apex に使え、AWS リソース宛は無料・自動追従。外部任意ドメインを指すのは CNAME の役割で、ALIAS は AWS リソース/同一ゾーンの別レコードを指す。
> **出典**: [DNS README #4 CNAME と ALIAS](README.md#cname-と-alias-の違いaws-文脈で頻出)

## dns-010
- type: multi
- difficulty: hard
- domain: 0
- tags: [dns, failover, hybrid]

DNS の名前解決フローと役割について正しいものはどれか。2 つ選べ。

- [x] A. リゾルバはルート→TLD→権威の順に反復問い合わせをたどって解決する
- [x] B. 権威サーバは委任（NS）または権威応答を返し、自分では再帰しない
- [ ] C. クライアントはルートサーバに直接反復問い合わせする
- [ ] D. TTL を 0 にすれば、すべてのリゾルバで確実にキャッシュされない
- [ ] E. DNS フェイルオーバーは TTL に関係なく全クライアントへ即座に反映される

> **解説**: リゾルバが反復で上位をたどり、権威サーバは委任/権威応答を返すのみ。クライアントはリゾルバに再帰依頼する。TTL は実装により最小値が強制され完全には信用できず、フェイルオーバーはキャッシュ残存で遅延する。
> **出典**: [DNS README #3 再帰と反復](README.md#3-名前解決フロー再帰と反復)
