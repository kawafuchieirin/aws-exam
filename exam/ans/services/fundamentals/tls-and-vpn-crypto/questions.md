---
service: tls-and-vpn-crypto
domain_default: 0
source: README.md
source_sha256: d629607411c32c9266c061dc596e5f4e7d11796689bf973f925a703de6313fdb
generated: 2026-05-24
---

## tls-and-vpn-crypto-001
- type: single
- difficulty: easy
- domain: 0
- tags: [encryption]

TLS や IPsec が「非対称暗号で鍵交換し、実データは対称暗号で暗号化する」ハイブリッド方式を採る主な理由はどれか。

- [ ] A. 非対称暗号は対称暗号より安全性が高いから
- [x] B. 対称暗号は高速でバルクデータの暗号化に向くから
- [ ] C. 対称暗号は鍵配送が不要だから
- [ ] D. 非対称暗号は大量データの暗号化に向くから

> **解説**: 非対称暗号は計算コストが高く少量データ（鍵交換・署名）向き、対称暗号は高速でバルクデータ向き。両者を組み合わせ、非対称で安全に共有したセッション鍵を使って対称暗号で本データを暗号化する。
> **出典**: [TLS/VPN README #2 対称 vs 非対称](README.md#2-対称暗号-vs-非対称暗号)

## tls-and-vpn-crypto-002
- type: single
- difficulty: easy
- domain: 0
- tags: [tls, encryption]

サーバ証明書を提示するとき、サーバが送るべき証明書として最も適切なものはどれか。

- [ ] A. ルート CA 証明書のみ
- [x] B. サーバ証明書と中間 CA 証明書（チェーン）
- [ ] C. クライアント証明書
- [ ] D. 自己署名のルート証明書のみ

> **解説**: ルート CA はクライアントのトラストストアに事前格納されている。サーバは検証経路をつなぐためにサーバ証明書と中間 CA 証明書まで提示する必要がある。チェーン不備は証明書エラーの典型原因。
> **出典**: [TLS/VPN README #3 PKI・証明書チェーン](README.md#3-pki証明書チェーンルート-ca)

## tls-and-vpn-crypto-003
- type: single
- difficulty: medium
- domain: 0
- tags: [tls]

TLS 1.3 が TLS 1.2 と比べて改善した点として正しいものはどれか。

- [ ] A. RSA 鍵交換を必須化して互換性を高めた
- [x] B. ハンドシェイクを 1-RTT に短縮し、常に PFS を提供する
- [ ] C. SNI を必ず平文で送るよう統一した
- [ ] D. CBC モードの暗号を推奨に格上げした

> **解説**: TLS 1.3 はハンドシェイクを 1-RTT（再接続で 0-RTT）に短縮し、(EC)DHE のみを使うため常に PFS を持つ。脆弱な RSA 鍵交換や CBC 系は廃止された。
> **出典**: [TLS/VPN README #4 TLS ハンドシェイク](README.md#4-tls-ハンドシェイク12-と-13)

## tls-and-vpn-crypto-004
- type: single
- difficulty: medium
- domain: 0
- tags: [tls]

1 つの ALB で複数ドメインの証明書を出し分けたい。これを可能にする TLS の仕組みはどれか。

- [ ] A. OCSP ステープリング
- [x] B. SNI（Server Name Indication）
- [ ] C. セッション再開（Session Resumption）
- [ ] D. クライアント証明書認証

> **解説**: SNI は ClientHello に接続先ホスト名を載せ、サーバ側が複数証明書を出し分けられる拡張。ALB は SNI に基づく複数証明書をサポートする。
> **出典**: [TLS/VPN README #5 SNI](README.md#5-sniserver-name-indication)

## tls-and-vpn-crypto-005
- type: single
- difficulty: medium
- domain: 0
- tags: [encryption, tls]

PFS（前方秘匿性）に関する説明として正しいものはどれか。

- [ ] A. サーバ秘密鍵が漏洩しても、その鍵で過去の通信を復号できないようにする
- [ ] B. RSA 鍵交換を使うと PFS が得られる
- [ ] C. PFS はクライアント証明書がある場合のみ有効になる
- [x] D. ECDHE 等のセッションごとの使い捨て鍵で実現する

> **解説**: PFS はセッションごとに使い捨ての (EC)DHE 鍵を生成し、長期秘密鍵が将来漏洩しても過去の通信を復号できないようにする性質。RSA 鍵交換は PFS を提供しない。A の記述も PFS の効果として正しいが、設問が求める「実現方法」を最も的確に述べているのは D。
> **出典**: [TLS/VPN README #8 PFS](README.md#8-pfsperfect-forward-secrecy前方秘匿性)

## tls-and-vpn-crypto-006
- type: single
- difficulty: medium
- domain: 0
- tags: [ipsec, vpn]

AWS Site-to-Site VPN が使う IPsec のモードとして正しいものはどれか。

- [ ] A. トランスポートモード（ペイロードのみ暗号化）
- [x] B. トンネルモード（元の IP パケット全体を暗号化し新ヘッダを付与）
- [ ] C. AH のみを使い暗号化はしない
- [ ] D. モードは使わず L7 で暗号化する

> **解説**: ゲートウェイ間（拠点間）の VPN ではトンネルモードを使い、元の IP パケット全体を暗号化して新しい IP ヘッダで包む。トランスポートモードはホスト間の End-to-End 用途。
> **出典**: [TLS/VPN README #7 IPsec](README.md#7-ipsecvpn-の中核)

## tls-and-vpn-crypto-007
- type: single
- difficulty: medium
- domain: 0
- tags: [ipsec]

IPsec の ESP と AH の違いについて正しいものはどれか。

- [ ] A. AH は暗号化と完全性の両方を提供する
- [x] B. ESP は暗号化・完全性・認証を提供し、AH は完全性・認証のみで暗号化しない
- [ ] C. ESP は認証を提供せず暗号化のみ行う
- [ ] D. AH は NAT と相性が良く実運用で最も使われる

> **解説**: ESP は暗号化＋完全性＋認証を提供し実運用の主役。AH は完全性・認証のみで暗号化しない。AH は IP ヘッダも保護するため NAT と相性が悪い。
> **出典**: [TLS/VPN README #7 ESP vs AH](README.md#7-ipsecvpn-の中核)

## tls-and-vpn-crypto-008
- type: single
- difficulty: hard
- domain: 0
- tags: [direct-connect, encryption]

Direct Connect の専用線で機密データを送る。暗号化に関する正しい理解はどれか。

- [ ] A. Direct Connect は専用線なので自動的に暗号化されている
- [x] B. Direct Connect 自体は暗号化されず、必要なら VPN（IPsec）を重ねるか MACsec を使う
- [ ] C. Direct Connect では TLS が常に強制される
- [ ] D. 専用線のため暗号化は一切不可能

> **解説**: Direct Connect は専用接続だがそれ自体は暗号化されない。機密性が必要なら DX 上に IPsec VPN を重ねるか、対応ロケーションで L2 の MACsec を使う。
> **出典**: [TLS/VPN README #9 VPN の暗号](README.md#9-vpn-の暗号aws-文脈での整理)

## tls-and-vpn-crypto-009
- type: multi
- difficulty: medium
- domain: 0
- tags: [ipsec, vpn]

AWS Site-to-Site VPN の IKE / IPsec パラメータとして正しいものを 2 つ選べ。

- [x] A. IKE Phase 1 で双方を認証し、安全な管理用トンネルを確立する
- [x] B. IKE Phase 2 で実データ用の SA（暗号鍵）を確立し、PFS をここで有効化できる
- [ ] C. IKE Phase 1 で実データの暗号鍵を直接配布しトンネルは作らない
- [ ] D. Site-to-Site VPN は単一トンネルのみで冗長構成を持たない
- [ ] E. Phase 2 は Phase 1 のトンネルなしに単独で実行される

> **解説**: IKE Phase1 で相互認証し安全な管理トンネル（ISAKMP SA）を確立、Phase2 でその上に IPsec SA を交渉し PFS を効かせる。Site-to-Site VPN は冗長な 2 トンネルを持つ。
> **出典**: [TLS/VPN README #7 IKE 2 フェーズ](README.md#7-ipsecvpn-の中核)

## tls-and-vpn-crypto-010
- type: multi
- difficulty: easy
- domain: 0
- tags: [tls, edge-caching, client-vpn]

TLS / 暗号化の AWS での扱いについて正しいものを 2 つ選べ。

- [x] A. CloudFront はエッジで TLS を終端でき、最小 TLS バージョンや SNI を設定できる
- [x] B. Client VPN は OpenVPN ベースで TLS により通信を保護する
- [ ] C. ECDHE ではなく RSA 鍵交換のスイートを選ぶと PFS が得られる
- [ ] D. ALB は L4 で動作するため TLS を扱えない
- [ ] E. AH を使えば通信ペイロードが暗号化される

> **解説**: CloudFront はエッジで TLS を終端し最小 TLS バージョンや SNI を制御できる。Client VPN は OpenVPN ベースで TLS により保護される。PFS は ECDHE 系で得られ、ALB は L7 で TLS を扱え、AH は暗号化しない。
> **出典**: [TLS/VPN README #9 VPN の暗号](README.md#9-vpn-の暗号aws-文脈での整理)
