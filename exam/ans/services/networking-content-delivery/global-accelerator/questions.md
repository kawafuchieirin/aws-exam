---
service: global-accelerator
domain_default: 1
source: README.md
source_sha256: 890ebe413339b2645def413784bfd8e2c6d4457813e376ee6f56c81bb6567306
generated: 2026-05-24
---

## global-accelerator-001
- type: single
- difficulty: medium
- domain: 1
- tags: [use-case-fit, nlb]

オンラインゲームの非 HTTP（UDP）トラフィックを、固定 IP を維持したまま複数リージョンへ最適ルーティングし、リージョン障害時に高速フェイルオーバーしたい。最適なサービスはどれか。

- [x] A. AWS Global Accelerator
- [ ] B. Amazon CloudFront
- [ ] C. Route 53 Latency ルーティング
- [ ] D. ALB のクロスリージョン構成

> **解説**: Global Accelerator は L4（TCP/UDP）で動作し、2 つの静的 Anycast IP を提供、非 HTTP プロトコル（ゲーム/IoT/VoIP/MQTT）に対応し、リージョン障害から固定 IP のまま数十秒で高速フェイルオーバーする。CloudFront は L7・キャッシュ前提で UDP に向かない。
> **出典**: [global-accelerator README #7 CloudFront との使い分け](README.md#7-cloudfront-との使い分け最頻出)

## global-accelerator-002
- type: single
- difficulty: medium
- domain: 1
- tags: [global-accelerator, security-group]

Global Accelerator が提供する静的 IP について正しいものはどれか（IPv4、デフォルト）。

- [ ] A. リージョンごとに 1 個ずつ
- [x] B. 2 個の静的 Anycast IP を 2 つのネットワークゾーンから 1 個ずつ提供
- [ ] C. 常に 4 個
- [ ] D. エンドポイントごとに動的に割り当て

> **解説**: GA は IPv4 で 2 個の静的 Anycast IP を、2 つのネットワークゾーンから 1 個ずつ提供する。片方の IP がクライアント網でブロックされても、もう一方へリトライできる。デュアルスタックでは計 4 個（IPv4×2＋IPv6×2）。
> **出典**: [global-accelerator README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## global-accelerator-003
- type: single
- difficulty: hard
- domain: 1
- tags: [global-accelerator, routing-policy]

トラフィックダイヤルとエンドポイント重みの違いとして正しいものはどれか。

- [x] A. トラフィックダイヤルはエンドポイントグループ（リージョン）単位の流量割合、重みはエンドポイント単位の比率
- [ ] B. トラフィックダイヤルはエンドポイント単位、重みはグループ単位
- [ ] C. どちらもグループ単位で同義
- [ ] D. どちらもリスナー単位の設定

> **解説**: トラフィックダイヤルはエンドポイントグループ（=リージョン）単位の流量割合（0–100%）で、Blue/Green や段階移行に使う。エンドポイント重み（0–255）はグループ内のエンドポイント間の比率。両者の粒度の違いが頻出論点。
> **出典**: [global-accelerator README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## global-accelerator-004
- type: single
- difficulty: medium
- domain: 1
- tags: [global-accelerator, iam-policy]

同一クライアントを常に同一エンドポイントへ送り、セッションを維持したい。設定すべきクライアントアフィニティはどれか。

- [ ] A. None（5 タプル）
- [x] B. Source IP（2 タプル）
- [ ] C. クッキーベース
- [ ] D. ラウンドロビン

> **解説**: クライアントアフィニティ Source IP（2 タプル＝送信元 IP＋宛先 IP）にすると、同一クライアントを同一エンドポイントへ固定できる。既定の None は 5 タプルでハッシュしリクエストごとに分散する。
> **出典**: [global-accelerator README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## global-accelerator-005
- type: single
- difficulty: hard
- domain: 1
- tags: [global-accelerator]

ゲームプレイヤーを特定の EC2 インスタンス（プライベート IP）へ決定論的に割り当てたい。利用すべきアクセラレーター種別はどれか。

- [ ] A. Standard アクセラレーター
- [x] B. Custom routing アクセラレーター
- [ ] C. CloudFront ディストリビューション
- [ ] D. Route 53 Multivalue ルーティング

> **解説**: Custom routing はユーザーを決定論的に特定の宛先（VPC サブネット内 EC2 のプライベート IP）へ IP/ポートマッピングで割り当てる。ゲームセッション固定が代表用途。Standard はヘルス・位置・重みで最適な NLB/ALB/EC2/EIP へルーティングする。
> **出典**: [global-accelerator README #3 アーキテクチャ/仕組み](README.md#3-アーキテクチャ仕組み)

## global-accelerator-006
- type: single
- difficulty: hard
- domain: 3
- tags: [failover, routing-policy, dns]

リージョン障害時のフェイルオーバーで、Global Accelerator が Route 53 フェイルオーバーより優れる点はどれか。

- [ ] A. DNS の TTL を 0 にできる
- [x] B. DNS の TTL に依存せず、固定 IP のまま数十秒で自動フェイルオーバーできる
- [ ] C. キャッシュを保持したまま切り替わる
- [ ] D. L7 のパスルーティングを維持できる

> **解説**: GA はヘルスチェックで不健全リージョンを検知すると数十秒で自動フェイルオーバーする。Route 53 フェイルオーバーは DNS の TTL（クライアント/リゾルバのキャッシュ）に依存して切替が遅れがちだが、GA は固定 IP のまま切り替わるためクライアントは IP/DNS を変えなくてよい。
> **出典**: [global-accelerator README #5 ヘルスチェックと高速フェイルオーバー](README.md#5-ヘルスチェックと高速フェイルオーバー頻出)

## global-accelerator-007
- type: single
- difficulty: hard
- domain: 1
- tags: [vpn, transit-gateway]

Accelerated Site-to-Site VPN を有効化できる条件として正しいものはどれか。

- [ ] A. VGW に直接アタッチした VPN
- [x] B. Transit Gateway にアタッチした VPN（TGW VPN）
- [ ] C. Client VPN エンドポイント
- [ ] D. Direct Connect の Transit VIF

> **解説**: Accelerated Site-to-Site VPN は Global Accelerator のエッジを基盤に VPN トラフィックを AWS バックボーンへ載せる機能で、Transit Gateway にアタッチする VPN でのみ有効化できる。VGW 直アタッチの VPN では不可。
> **出典**: [global-accelerator README #6 Accelerated Site-to-Site VPN 基盤](README.md#6-accelerated-site-to-site-vpn-基盤)

## global-accelerator-008
- type: single
- difficulty: medium
- domain: 3
- tags: [vpc-endpoint, health-check]

Standard アクセラレーターのエンドポイントとして指定できないものはどれか。

- [ ] A. ALB
- [ ] B. NLB
- [ ] C. EC2 / EIP
- [x] D. API Gateway を直接エンドポイントに指定

> **解説**: Standard アクセラレーターのエンドポイントは NLB/ALB/EC2/EIP。API Gateway は直接エンドポイントにできず、NLB＋VPC リンク等を介して固定 IP を提供する構成になる。ALB/NLB はそのリソース自身のヘルスチェック結果を GA が尊重し、EC2/EIP は GA のヘルスチェックを使う。
> **出典**: [global-accelerator README #8 他サービスとの連携](README.md#8-他サービスとの連携)

## global-accelerator-009
- type: single
- difficulty: medium
- domain: 1
- tags: [use-case-fit, edge-caching, waf]

静的/動的 Web コンテンツをエッジでキャッシュし、WAF と署名付き URL で保護したい。最適なサービスはどれか。

- [ ] A. Global Accelerator
- [x] B. Amazon CloudFront
- [ ] C. Route 53 Geolocation
- [ ] D. NLB の TLS リスナー

> **解説**: キャッシュ・HTTP・WAF が必要なら CloudFront（L7・エッジキャッシュ・TLS 終端）。Global Accelerator は L4・キャッシュなし・固定 IP で、非 HTTP や L4 高速フェイルオーバーが要件のときに選ぶ。
> **出典**: [global-accelerator README #7 CloudFront との使い分け](README.md#7-cloudfront-との使い分け最頻出)

## global-accelerator-010
- type: single
- difficulty: medium
- domain: 3
- tags: [health-check, monitoring]

Global Accelerator のヘルスチェックに関するデフォルト値として正しいものはどれか。

- [ ] A. 間隔は 60 秒固定
- [x] B. 間隔は既定 30 秒（10/30 秒から選択）、異常しきい値は既定 3 回
- [ ] C. 異常しきい値は 1 回固定
- [ ] D. 正常しきい値は 10 回固定

> **解説**: ヘルスチェック間隔は 10 秒または 30 秒（既定 30 秒）。異常しきい値は既定 3 回（範囲 2–10）、正常しきい値は既定 2 回（範囲 2–10）。
> **出典**: [global-accelerator README #5 ヘルスチェックと高速フェイルオーバー](README.md#5-ヘルスチェックと高速フェイルオーバー頻出)

## global-accelerator-011
- type: multi
- difficulty: hard
- domain: 1
- tags: [use-case-fit]

Global Accelerator が CloudFront と異なる点として正しいものを 2 つ選べ。

- [x] A. L4（TCP/UDP）で動作する
- [ ] B. エッジでコンテンツをキャッシュする
- [x] C. 2 つの静的 Anycast IP をエントリポイントとして提供する
- [ ] D. TLS をエッジで終端する
- [ ] E. HTTP/HTTPS にのみ対応する

> **解説**: GA は L4 で動作し、2 つの静的 Anycast IP を提供し、TLS を終端せずパススルーし、非 HTTP も扱える。キャッシュ・TLS 終端・HTTP 中心は CloudFront の特徴。
> **出典**: [global-accelerator README #7 CloudFront との使い分け](README.md#7-cloudfront-との使い分け最頻出)

## global-accelerator-012
- type: multi
- difficulty: medium
- domain: 4
- tags: [nlb, public-ip, shield]

Global Accelerator の静的 Anycast IP に関して正しいものを 2 つ選べ。

- [x] A. アクセラレーターが存在する限り IP を保持し、delete すると失効する
- [ ] B. アクセラレーターを disable すると即座に IP が失効する
- [x] C. BYOIP（IPv4）で自社の IP を持ち込める
- [ ] D. IP は AWS Shield Advanced の保護対象外である
- [ ] E. IP はリージョンごとに異なる

> **解説**: 静的 Anycast IP はアクセラレーター存在中は保持され（disable でも保持）、delete で失効する。BYOIP（IPv4）で自社 IP を持ち込め、Shield Advanced の DDoS 保護対象でもある。Anycast なので全リージョンで同一 IP が広告される。
> **出典**: [global-accelerator README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)
