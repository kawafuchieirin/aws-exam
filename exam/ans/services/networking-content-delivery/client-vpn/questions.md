---
service: client-vpn
domain_default: 1
source: README.md
source_sha256: 649d2cb4a5cd04e14054c7570c720be99646b4d2bc31e6ba4b4a7d012e382367
generated: 2026-05-24
---

## client-vpn-001
- type: single
- difficulty: easy
- domain: 1
- tags: [client-vpn]

在宅勤務の個々の従業員が自宅 PC から VPC 内リソースへ安全に接続したい。最も適切なサービスはどれか。

- [x] A. AWS Client VPN
- [ ] B. AWS Site-to-Site VPN
- [ ] C. AWS Direct Connect
- [ ] D. Transit Gateway peering

> **解説**: Client VPN は個々のエンドユーザー（デバイス）単位のリモートアクセス VPN。Site-to-Site VPN は拠点間接続が目的。在宅勤務者の個別端末からの接続なら Client VPN を選ぶ。
> **出典**: [client-vpn README #1 概要](README.md#1-概要)

## client-vpn-002
- type: single
- difficulty: medium
- domain: 4
- tags: [iam-policy, client-vpn, console-security]

既存の IAM Identity Center（または Okta 等の外部 IdP）を使った SSO で Client VPN ユーザーを認証したい。選ぶべき認証方式はどれか。

- [ ] A. 相互証明書認証
- [ ] B. Active Directory 認証
- [x] C. SAML フェデレーション（SSO）
- [ ] D. IAM ユーザー名/パスワード

> **解説**: SSO 要件は SAML フェデレーション認証で実現する。IAM Identity Center や外部 IdP（Okta 等）と連携する。AD があれば AD 認証、IdP がなければ相互証明書という使い分け。
> **出典**: [client-vpn README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## client-vpn-003
- type: single
- difficulty: medium
- domain: 4
- tags: [iam-policy, tls]

Client VPN の認証方式に関わらず、必ず必要となるものはどれか。

- [x] A. ACM が管理するサーバ証明書
- [ ] B. クライアント証明書（全方式で必須）
- [ ] C. Active Directory
- [ ] D. SAML IdP

> **解説**: どの認証方式（相互証明書 / AD / SAML）でも、ACM が管理するサーバ証明書は必須。クライアント証明書は相互証明書認証のときのみ必要。
> **出典**: [client-vpn README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## client-vpn-004
- type: single
- difficulty: medium
- domain: 1
- tags: [client-vpn, cost]

クライアントの VPC/AWS 宛トラフィックのみを VPN 経由にし、その他の一般的なインターネット通信は端末から直接出させてデータ転送コストを削減したい。設定はどれか。

- [ ] A. フルトンネル（既定）
- [x] B. スプリットトンネルを有効化する
- [ ] C. 認可ルールを削除する
- [ ] D. クライアント CIDR を /12 にする

> **解説**: スプリットトンネルを有効化すると、エンドポイントのルートテーブルにある経路だけがクライアントへプッシュされ、該当宛先のみ VPN 経由になる。それ以外は端末から直接インターネットへ抜けるため、AWS からのアウトバウンド転送コストを削減でき経路も最適化される。
> **出典**: [client-vpn README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## client-vpn-005
- type: single
- difficulty: easy
- domain: 1
- tags: [client-vpn, landing-zone]

Client VPN の既定のトンネルモードと、その挙動として正しいものはどれか。

- [x] A. 既定はフルトンネルで、クライアントの全通信（0.0.0.0/0）が VPN 経由になる
- [ ] B. 既定はスプリットトンネルで、VPC 宛のみ VPN 経由になる
- [ ] C. 既定では一切のトラフィックがトンネルされない
- [ ] D. 既定では DNS のみがトンネルされる

> **解説**: 既定はフルトンネルで、クライアントのルートを 0.0.0.0/0 で上書きし全通信を VPN 経由にする。スプリットトンネルは明示的に有効化する必要がある。
> **出典**: [client-vpn README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## client-vpn-006
- type: single
- difficulty: hard
- domain: 3
- tags: [client-vpn, route-table, troubleshooting]

クライアントは認証に成功し IP も払い出されたが、特定の VPC 内サブネットへ疎通しない。疎通に必要な要素として正しいものはどれか。

- [ ] A. ルートテーブルの経路だけがあれば疎通する
- [ ] B. 認可ルールだけがあれば疎通する
- [x] C. エンドポイントルートテーブルの経路と、その宛先への認可ルールの両方が必要
- [ ] D. セキュリティグループのインバウンド許可だけで疎通する

> **解説**: Client VPN ではデフォルトで何も許可されない。宛先ネットワークへのルート（ルートテーブル）と、そのネットワークへのアクセスを許可する認可ルールの両方が揃って初めて疎通する。片方だけでは通らない（トラブルシュート頻出）。
> **出典**: [client-vpn README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## client-vpn-007
- type: single
- difficulty: medium
- domain: 1
- tags: [client-vpn, quotas]

Client VPN のクライアント CIDR（IPv4）の設定に関する制約として正しいものはどれか。

- [ ] A. AWS が自動で割り当て、ユーザーは指定できない
- [x] B. ユーザーが指定し、サイズは /22〜/12、関連付け先 VPC やローカルルートと重複してはならない
- [ ] C. /28〜/24 の範囲で指定する
- [ ] D. VPC CIDR と必ず一致させる

> **解説**: IPv4 のクライアント CIDR はユーザーが指定し、サイズは /22（1024 IP）〜/12。関連付けサブネットの VPC・ローカルルート・他関連付けと重複できない。IPv6 は AWS が自動割当。
> **出典**: [client-vpn README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## client-vpn-008
- type: single
- difficulty: medium
- domain: 1
- tags: [transit-gateway]

Client VPN から複数 VPC やオンプレ（DX/VPN 経由）へ集約して到達させたい。推奨される構成はどれか。

- [ ] A. 各 VPC ごとに別々の Client VPN エンドポイントを作る
- [x] B. エンドポイントを Transit Gateway に直接アタッチ（または関連付け VPC を TGW 経由）し、TGW ルートで集約到達させる
- [ ] C. VPC ピアリングのみで到達させる
- [ ] D. CloudFront を経由させる

> **解説**: Client VPN エンドポイントを Transit Gateway に直接アタッチ、または関連付け VPC を TGW 経由にすることで、複数 VPC や DX/VPN 経由のオンプレへ集約到達できる。グループ別に認可ルールで制御する。
> **出典**: [client-vpn README #7 よくある設計パターン](README.md#7-よくある設計パターン)

## client-vpn-009
- type: multi
- difficulty: hard
- domain: 4
- tags: [iam-policy, client-vpn, console-security]

Client VPN の認証方式の使い分けについて正しいものを 2 つ選べ。

- [x] A. 相互証明書認証はサーバ証明書とクライアント証明書（ともに ACM 管理）を使い、IdP がない小規模に向く
- [x] B. Active Directory 認証は AWS Directory Service を使い、AD Connector でオンプレ AD と連携して AD グループで認可できる
- [ ] C. SAML 認証ではサーバ証明書が不要になる
- [ ] D. 相互証明書認証では認可ルールが不要になる
- [ ] E. AD 認証はオンプレ AD と一切連携できない

> **解説**: 相互証明書認証は IdP がない小規模向け、AD 認証は AWS Directory Service（AD Connector でオンプレ AD 連携可）で AD グループ単位の認可が可能。どの方式でもサーバ証明書は必須で、認可ルールも必須。
> **出典**: [client-vpn README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## client-vpn-010
- type: single
- difficulty: medium
- domain: 3
- tags: [high-availability, multi-az]

Client VPN エンドポイントを可用性高く構成したい。推奨される方法はどれか。

- [ ] A. 単一サブネットを関連付ける
- [x] B. 複数 AZ のサブネットをエンドポイントに関連付ける
- [ ] C. クライアント CIDR を大きくする
- [ ] D. フルトンネルにする

> **解説**: 複数 AZ のサブネットを関連付けると冗長化できる（1 サブネット = 1 AZ）。単一サブネットでは AZ 障害に弱い。
> **出典**: [client-vpn README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## client-vpn-011
- type: single
- difficulty: hard
- domain: 4
- tags: [nat, public-ip, ipv6]

Client VPN における送信元 IP（SNAT）の挙動として正しいものはどれか。

- [x] A. IPv4 ではクライアント CIDR の送信元 IP が Client VPN ENI の IP に変換される（IPv6 は SNAT なしで元 IP が見える）
- [ ] B. IPv4・IPv6 ともに SNAT は行われない
- [ ] C. IPv4 では SNAT されず、IPv6 のみ SNAT される
- [ ] D. SNAT はセキュリティグループで明示的に有効化する必要がある

> **解説**: IPv4 ではクライアント CIDR の送信元 IP が Client VPN ENI の IP に SNAT される。IPv6 では SNAT が行われず元の IP が見える。アクセス元 IP のログ要件などで重要。
> **出典**: [client-vpn README #2 コアコンセプト](README.md#2-コアコンセプト)

## client-vpn-012
- type: single
- difficulty: medium
- domain: 3
- tags: [cost, transit-gateway, troubleshooting]

Client VPN のコスト最適化・運用上の注意として正しいものはどれか。

- [ ] A. 使わないターゲットネットワーク関連付けを残してもコストは発生しない
- [x] B. 関連付け（サブネット）ごとに時間課金が継続するため、使わない関連付けは削除する
- [ ] C. スプリットトンネルにするとデータ転送コストが増える
- [ ] D. 接続ログは課金対象外である

> **解説**: 課金はエンドポイント関連付け（サブネット）ごとの時間課金、アクティブ接続ごとの時間課金、データ転送、接続ログの CloudWatch Logs 等で発生する。使わない関連付けは課金が継続するため削除し、スプリットトンネルで不要なトラフィックを VPN に流さないのが最適化。
> **出典**: [client-vpn README #6 制約・上限・コスト](README.md#6-制約上限コスト)
