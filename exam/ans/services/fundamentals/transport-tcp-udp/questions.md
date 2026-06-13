---
service: transport-tcp-udp
domain_default: 0
source: README.md
source_sha256: b6713eca89938255d2e95a5103e3d0c524ed539e7c75dc595addc978f5ebcd76
generated: 2026-05-24
---

## transport-tcp-udp-001
- type: single
- difficulty: easy
- domain: 0
- tags: [tcp-udp]

TCP と UDP の違いとして正しいものはどれか。

- [ ] A. UDP はコネクション型で再送制御を持つ
- [x] B. TCP はコネクション型で確認応答・再送・順序保証を持ち、UDP はコネクションレスでそれらを持たない
- [ ] C. TCP も UDP もコネクションレスである
- [ ] D. UDP はヘッダが大きく低速である

> **解説**: TCP はコネクション型で信頼性（確認応答・再送・順序保証）を提供。UDP はコネクションレスで軽量・低遅延だが信頼性は持たない。
> **出典**: [transport README #2 TCP vs UDP](README.md#2-tcp-vs-udp)

## transport-tcp-udp-002
- type: single
- difficulty: easy
- domain: 0
- tags: [tcp-udp]

TCP の接続確立（3way ハンドシェイク）の正しい順序はどれか。

- [x] A. SYN → SYN/ACK → ACK
- [ ] B. ACK → SYN → FIN
- [ ] C. SYN → FIN → ACK
- [ ] D. SYN/ACK → SYN → RST

> **解説**: クライアントが SYN、サーバが SYN/ACK、クライアントが ACK を返して接続が確立する。
> **出典**: [transport README #3 3way ハンドシェイク](README.md#3-3way-ハンドシェイクと接続終了)

## transport-tcp-udp-003
- type: single
- difficulty: medium
- domain: 0
- tags: [tcp-udp]

ネットワーク ACL（NACL）でインバウンドの HTTPS(443) を許可しているのに通信が成立しない。最も確認すべき設定はどれか。

- [ ] A. セキュリティグループのアウトバウンド 443 許可
- [x] B. NACL のアウトバウンドでエフェメラルポート（例: 1024-65535）が許可されているか
- [ ] C. インスタンスの MAC アドレス
- [ ] D. Route 53 のヘルスチェック設定

> **解説**: NACL はステートレスのため、戻りトラフィックはエフェメラルポート宛のアウトバウンド許可が別途必要。許可漏れが頻出の原因。
> **出典**: [transport README #4 エフェメラルポート](README.md#4-ポートとエフェメラルポート)

## transport-tcp-udp-004
- type: single
- difficulty: medium
- domain: 0
- tags: [mtu]

IPv4 で MTU が 1500 のとき、TCP の MSS は通常いくつか。

- [ ] A. 1500
- [x] B. 1460
- [ ] C. 1480
- [ ] D. 9001

> **解説**: MSS = MTU − IPヘッダ(20) − TCPヘッダ(20) = 1500 − 40 = 1460。
> **出典**: [transport README #6 MTU/MSS](README.md#6-mtu--mss-とフラグメンテーション)

## transport-tcp-udp-005
- type: single
- difficulty: hard
- domain: 0
- tags: [icmp, mtu]

ジャンボフレーム設定後、小さい通信は通るのに大きいデータ転送だけが固まる。PMTUD が機能していないと疑われる場合、遮断されている可能性が最も高いものはどれか。

- [x] A. ICMP Type3 Code4「Fragmentation Needed」
- [ ] B. ICMP Echo Reply（Type0）のみ
- [ ] C. TCP SYN パケット
- [ ] D. UDP/53 の DNS 応答

> **解説**: PMTUD は中継ルータが返す ICMP Type3 Code4 に依存する。これを遮断すると経路がブラックホール化し、MSS を超える大きいパケットだけ無応答になる。
> **出典**: [transport README #7 ICMP の役割](README.md#7-icmp-の役割頻出)

## transport-tcp-udp-006
- type: single
- difficulty: easy
- domain: 0
- tags: [tcp-udp]

DNS のクエリで一般的に使われるトランスポートとポートはどれか。

- [x] A. 通常は UDP/53、応答が大きい場合やゾーン転送では TCP/53
- [ ] B. 常に TCP/80
- [ ] C. 常に UDP/443
- [ ] D. 常に TCP/22

> **解説**: DNS は通常 UDP/53 を使い、応答が大きい場合（切り詰め）やゾーン転送では TCP/53 にフォールバックする。
> **出典**: [transport README #2 TCP vs UDP](README.md#2-tcp-vs-udp)

## transport-tcp-udp-007
- type: single
- difficulty: medium
- domain: 0
- tags: [nlb, tcp-udp]

NLB が同一の TCP コネクションを常に同じターゲットへ送る仕組みとして正しいものはどれか。

- [ ] A. ラウンドロビンでリクエストごとに分散する
- [x] B. フロー（5-tuple）のハッシュで同一フローを同一ターゲットへ送る
- [ ] C. クッキーによるスティッキーセッション
- [ ] D. パスベースルーティング

> **解説**: NLB は L4 でフローハッシュ（5-tuple）により同一フローを同一ターゲットへ送るため接続維持に有利。クッキーやパスは L7（ALB）の機能。
> **出典**: [transport README #5 フロー](README.md#5-フローコネクション追跡)

## transport-tcp-udp-008
- type: single
- difficulty: medium
- domain: 0
- tags: [mtu]

AWS におけるジャンボフレーム（MTU 9001）の利用について正しいものはどれか。

- [ ] A. インターネット宛のトラフィックでも常に 9001 が使える
- [x] B. 同一リージョンのインスタンス間では最大 9001 だが、インターネット宛や VPN 経由は 1500 に制限される
- [ ] C. ジャンボフレームは UDP でのみ有効
- [ ] D. ジャンボフレームを使うと MSS は変化しない

> **解説**: VPC 内/同一リージョンは最大 9001 だが、IGW 越え（インターネット宛）や VPN は 1500。経路に 1500 区間があれば PMTUD が必要。
> **出典**: [transport README #6 AWS の MTU 要点](README.md#6-mtu--mss-とフラグメンテーション)

## transport-tcp-udp-009
- type: multi
- difficulty: medium
- domain: 0
- tags: [tcp-udp, health-check, nlb]

セキュリティグループとネットワーク ACL の挙動について正しいものはどれか。2 つ選べ。

- [x] A. セキュリティグループはステートフルで戻りトラフィックを自動許可する
- [x] B. ネットワーク ACL はステートレスで、戻り用にエフェメラルポートのアウトバウンド許可が必要
- [ ] C. セキュリティグループは Deny ルールを持てる
- [ ] D. ネットワーク ACL はステートフルで戻りを自動許可する
- [ ] E. どちらも常にすべての戻りトラフィックを自動許可する

> **解説**: SG はステートフルで戻り自動許可・許可ルールのみ。NACL はステートレスで戻りに明示的なエフェメラルポート許可が必要。
> **出典**: [transport README #4 エフェメラルポート](README.md#4-ポートとエフェメラルポート)

## transport-tcp-udp-010
- type: multi
- difficulty: hard
- domain: 0
- tags: [icmp, mtu, health-check]

経路上の MTU ミスマッチによる通信障害の調査・対策として適切なものはどれか。2 つ選べ。

- [x] A. ICMP Type3 Code4 がファイアウォール/SG/NACL で遮断されていないか確認する
- [x] B. MSS クランプ（経路で MSS を下げる）を検討する
- [ ] C. すべてのトラフィックで MTU を 9001 に固定すれば解決する
- [ ] D. ICMP をすべて遮断すればブラックホール障害は解消する
- [ ] E. TCP の代わりに UDP を使えば MTU 問題は発生しない

> **解説**: PMTUD は ICMP Type3 Code4 に依存するため遮断を確認し、必要なら MSS クランプで経路の最小 MTU に合わせる。MTU を一律 9001 にするとインターネット/VPN 経路で破綻し、UDP でも大きいパケットは断片化問題を受ける。
> **出典**: [transport README #7 ICMP の役割](README.md#7-icmp-の役割頻出)
