---
service: nat-and-load-balancing-concepts
domain_default: 0
source: README.md
source_sha256: 9f7ee5619bfc70d7f24bbb735958c54d775566dc5b340114b7bb311028bec57b
generated: 2026-05-24
---

## nat-and-load-balancing-concepts-001
- type: single
- difficulty: easy
- domain: 0
- tags: [nat]

NAT Gateway が行う変換として正しいものはどれか。

- [x] A. 送信元 IP とポートを書き換える SNAT + PAT（アウトバウンドのみ）
- [ ] B. 宛先 IP を書き換える DNAT（インバウンドのみ）
- [ ] C. MAC アドレスを書き換える
- [ ] D. TCP を UDP に変換する

> **解説**: NAT Gateway は送信元 IP とポートを多重化する SNAT + PAT で、プライベートサブネットのアウトバウンド通信を担う。新規インバウンド接続は受けない。
> **出典**: [nat README #2 NAT の種別](README.md#2-nat-の種別)

## nat-and-load-balancing-concepts-002
- type: single
- difficulty: easy
- domain: 0
- tags: [alb, nlb]

L7 で動作し、HTTP のパスやホストヘッダでルーティングできるロードバランサはどれか。

- [x] A. ALB（Application Load Balancer）
- [ ] B. NLB（Network Load Balancer）
- [ ] C. GWLB（Gateway Load Balancer）
- [ ] D. NAT Gateway

> **解説**: ALB は L7（アプリケーション層）で動作し、パス/ホスト/ヘッダ/メソッドによるルーティングや WAF 連携が可能。NLB は L4、GWLB は L3 透過。
> **出典**: [nat README #3 L4 vs L7](README.md#3-l4-vs-l7-ロードバランシング)

## nat-and-load-balancing-concepts-003
- type: single
- difficulty: medium
- domain: 0
- tags: [nlb, alb]

クライアントのソース IP をバックエンドにそのまま届ける（保持する）のはどれか。

- [ ] A. ALB（ソース IP を保持する）
- [x] B. NLB（基本的にソース IP を保持する）
- [ ] C. NAT Gateway
- [ ] D. Internet Gateway

> **解説**: NLB は基本的にクライアントのソース IP を保持する。ALB はリバースプロキシのため保持せず、`X-Forwarded-For` ヘッダで元の IP を渡す。
> **出典**: [nat README #6 ソース IP 保持](README.md#6-ソース-ip-保持と-proxy-protocol)

## nat-and-load-balancing-concepts-004
- type: single
- difficulty: medium
- domain: 0
- tags: [cross-zone, nlb, alb]

クロスゾーン負荷分散の既定の挙動として正しいものはどれか。

- [x] A. ALB は常に ON（無効化不可・無料）、NLB/GWLB は既定 OFF
- [ ] B. ALB も NLB も既定 OFF
- [ ] C. ALB は既定 OFF、NLB は常に ON
- [ ] D. どの LB もクロスゾーンは設定できない

> **解説**: ALB はクロスゾーン常時 ON（無料）。NLB/GWLB は既定 OFF で、有効化すると AZ 間データ転送料が発生する点が頻出。
> **出典**: [nat README #7 クロスゾーン負荷分散](README.md#7-ターゲットタイプとクロスゾーン負荷分散)

## nat-and-load-balancing-concepts-005
- type: single
- difficulty: medium
- domain: 0
- tags: [nat, stateful-stateless]

ステートフルとステートレスについて、AWS の例の対応として正しいものはどれか。

- [x] A. セキュリティグループはステートフル、ネットワーク ACL はステートレス
- [ ] B. セキュリティグループはステートレス、ネットワーク ACL はステートフル
- [ ] C. どちらもステートレス
- [ ] D. どちらもステートフル

> **解説**: SG はフローを追跡するステートフルで戻りを自動許可。NACL は個々のパケットを独立評価するステートレス。NAT Gateway もステートフル。
> **出典**: [nat README #2 ステートフル vs ステートレス](README.md#ステートフル-vs-ステートレスnatfw-共通)

## nat-and-load-balancing-concepts-006
- type: single
- difficulty: easy
- domain: 0
- tags: [health-check]

ロードバランサのヘルスチェックの目的として正しいものはどれか。

- [ ] A. ターゲットの課金額を計測する
- [x] B. Healthy なターゲットにのみトラフィックを送るため、定期的に死活を確認する
- [ ] C. クライアントのソース IP を書き換える
- [ ] D. TLS 証明書を自動更新する

> **解説**: ヘルスチェックは各ターゲットの死活を定期確認し、Healthy なターゲットにのみトラフィックを送るための仕組み。
> **出典**: [nat README #5 ヘルスチェック](README.md#5-ヘルスチェックと接続維持)

## nat-and-load-balancing-concepts-007
- type: single
- difficulty: medium
- domain: 0
- tags: [target-type, alb, nlb]

オンプレミスのサーバや別 VPC のリソースを直接ターゲットにできるターゲットタイプはどれか。

- [ ] A. instance
- [x] B. ip
- [ ] C. lambda
- [ ] D. alb

> **解説**: ip ターゲットタイプは IP アドレスを直接指せるため、オンプレ/別 VPC/コンテナをターゲットにでき、ハイブリッド構成で有用。
> **出典**: [nat README #7 ターゲットタイプ](README.md#7-ターゲットタイプとクロスゾーン負荷分散)

## nat-and-load-balancing-concepts-008
- type: single
- difficulty: hard
- domain: 0
- tags: [nat, high-availability]

複数 AZ のプライベートサブネットのアウトバウンドを AZ 障害に強く設計したい。最適なのはどれか。

- [ ] A. 1 つの NAT Gateway を全 AZ で共有する
- [x] B. AZ ごとに NAT Gateway を配置し、各 AZ のルートを自 AZ の NAT に向ける
- [ ] C. NAT Gateway をインバウンド受け入れに設定する
- [ ] D. Internet Gateway を AZ ごとに作る

> **解説**: NAT Gateway を共有すると、その AZ の障害で他 AZ もインターネット断になる。AZ ごとに配置し自 AZ のルートを向けるのがベストプラクティス。
> **出典**: [nat README #2 NAT の種別](README.md#2-nat-の種別)

## nat-and-load-balancing-concepts-009
- type: multi
- difficulty: medium
- domain: 0
- tags: [proxy-protocol, nlb, health-check]

NLB でクライアントの元 IP やヘルスチェックに関する記述として正しいものはどれか。2 つ選べ。

- [x] A. NLB が TLS 終端しない等で IP が失われる場合、Proxy Protocol v2 で元の送信元情報をバックエンドへ伝えられる
- [x] B. NLB の TCP ヘルスチェックは接続確立の可否で判定し、UDP ターゲットは別ポートの TCP/HTTP で代替監視するのが定石
- [ ] C. Proxy Protocol はバックエンドが未対応でも常に正しく解釈される
- [ ] D. NLB は HTTP のパスベースルーティングでヘルスチェックを行う
- [ ] E. NLB はクッキーによるスティッキーセッションでクライアント IP を保持する

> **解説**: Proxy Protocol v2 は L4 で元の送信元 IP/ポートを伝えるが、バックエンドが対応していないとヘッダがデータに混入し破損する。NLB の TCP チェックは接続可否、UDP は代替監視。
> **出典**: [nat README #6 Proxy Protocol](README.md#6-ソース-ip-保持と-proxy-protocol)

## nat-and-load-balancing-concepts-010
- type: multi
- difficulty: hard
- domain: 0
- tags: [gwlb, nat, stateful-stateless]

GWLB（Gateway Load Balancer）と NAT に関する記述として正しいものはどれか。2 つ選べ。

- [x] A. GWLB は L3 で透過的に動作し、全トラフィックをファイアウォール/IDS/IPS 等のアプライアンスへ GENEVE でカプセル化して送る
- [x] B. NAT Gateway は SNAT + PAT でアウトバウンド専用であり、新規インバウンド接続は受けない
- [ ] C. GWLB は HTTP のパスベースルーティングを行う L7 ロードバランサである
- [ ] D. NAT Gateway は DNAT によりインターネットからの新規インバウンド接続を受け付ける
- [ ] E. GWLB は単一の TCP コネクションのみを扱い UDP は扱えない

> **解説**: GWLB は L3 透過でセキュリティアプライアンスを挿入する用途（GENEVE カプセル化）。NAT Gateway は SNAT+PAT のアウトバウンド専用。GWLB は L7 ルーティングを行わず、全 IP トラフィックを扱う。
> **出典**: [nat README #3 L4 vs L7](README.md#3-l4-vs-l7-ロードバランシング)
