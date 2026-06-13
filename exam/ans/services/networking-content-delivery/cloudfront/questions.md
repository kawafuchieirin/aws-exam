---
service: cloudfront
domain_default: 1
source: README.md
source_sha256: 86a2da6f6b39d505debac65339bc6692d13df27e361645ef1c31f2353140c749
generated: 2026-05-24
---

## cloudfront-001
- type: single
- difficulty: medium
- domain: 4
- tags: [oac, vpc-endpoint, edge-caching]

S3 バケットを直接公開せず、CloudFront 経由のアクセスのみに限定したい。新規構築で推奨される方式はどれか。

- [x] A. OAC（Origin Access Control）でバケットポリシーにより `cloudfront.amazonaws.com` のみ許可する
- [ ] B. S3 バケットを公開し、バケットポリシーで全許可する
- [ ] C. OAI（Origin Access Identity）を新規に採用する
- [ ] D. S3 静的ウェブサイトエンドポイント＋IP 制限

> **解説**: 新規構築・移行は OAC 一択。OAC は SigV4 で署名し、SSE-KMS や PUT/DELETE にも対応し全リージョンで使える。OAI はレガシーで機能制限が多く、新規での採用は推奨されない。
> **出典**: [cloudfront README #5 オリジン保護: OAC](README.md#5-オリジン保護-oacoai-の後継)

## cloudfront-002
- type: multi
- difficulty: hard
- domain: 4
- tags: [oac, encryption]

OAC が OAI に対して持つ利点を 2 つ選べ。

- [x] A. SSE-KMS で暗号化された S3 オリジンに対応する
- [x] B. PUT/DELETE などの動的リクエストに対応する
- [ ] C. S3 静的ウェブサイトエンドポイントを保護できる
- [ ] D. ルートアカウントの署名鍵が必須になる
- [ ] E. 2023年1月以降の新リージョンに非対応

> **解説**: OAC は SSE-KMS や PUT/DELETE に対応し、全リージョンで使え SigV4 で署名する。S3 ウェブサイトエンドポイントは OAC/OAI ともに非対応（カスタムオリジン扱い）。新リージョン非対応なのは OAI 側。
> **出典**: [cloudfront README #5 オリジン保護: OAC](README.md#5-オリジン保護-oacoai-の後継)

## cloudfront-003
- type: single
- difficulty: hard
- domain: 2
- tags: [edge-caching]

オリジンへのリクエスト時に外部 API や AWS SDK を呼び出し、リクエストボディを参照してオリジンを動的に選択したい。適切なエッジ関数はどれか。

- [ ] A. CloudFront Functions
- [x] B. Lambda@Edge（Origin Request トリガー）
- [ ] C. CloudFront Functions（Viewer Response）
- [ ] D. WAF マネージドルール

> **解説**: Lambda@Edge は Origin Request/Response トリガーに対応し、ネットワークアクセス（外部 API・AWS SDK 連携）やリクエストボディ参照が可能。CloudFront Functions は Viewer イベントのみでネットワークアクセス・ボディ参照不可。
> **出典**: [cloudfront README #6 エッジ関数](README.md#6-エッジ関数-cloudfront-functions-vs-lambdaedge頻出)

## cloudfront-004
- type: single
- difficulty: medium
- domain: 2
- tags: [edge-caching, use-case-fit]

毎秒数百万リクエスト規模で、キャッシュキーの正規化や URL リライト/リダイレクトといった超低遅延・軽量処理を Viewer Request で行いたい。適切なエッジ関数はどれか。

- [x] A. CloudFront Functions
- [ ] B. Lambda@Edge
- [ ] C. Step Functions
- [ ] D. API Gateway オーソライザー

> **解説**: CloudFront Functions は JavaScript（ES5.1）でサブミリ秒・毎秒数百万リクエスト規模を捌け、キャッシュキー正規化・ヘッダ操作・URL リライト/リダイレクト・軽量トークン検証に向く。Viewer Request/Response のみのトリガー。
> **出典**: [cloudfront README #6 エッジ関数](README.md#6-エッジ関数-cloudfront-functions-vs-lambdaedge頻出)

## cloudfront-005
- type: single
- difficulty: hard
- domain: 3
- tags: [edge-caching, failover]

CloudFront の Origin Groups（オリジンフェイルオーバー）について正しいものはどれか。

- [ ] A. 任意の数のオリジンを並べて順にフェイルオーバーできる
- [x] B. プライマリとセカンダリの2オリジンで構成し、特定の HTTP ステータス（500/502/503/504 等）や接続失敗時にセカンダリへ切り替わる
- [ ] C. すべての HTTP メソッドがフェイルオーバー対象になる
- [ ] D. フェイルオーバー対象ステータスは固定で変更できない

> **解説**: Origin Group はプライマリ＋セカンダリの2オリジン構成。400/403/404/416/429/500/502/503/504 から選んだステータスや接続失敗/タイムアウト時にセカンダリへ切り替わる。フェイルオーバーするのは GET/HEAD/OPTIONS のみ。
> **出典**: [cloudfront README #4 Origin Groups](README.md#4-origin-groupsオリジンフェイルオーバー頻出)

## cloudfront-006
- type: single
- difficulty: hard
- domain: 3
- tags: [edge-caching, api-endpoint]

Origin Groups でフェイルオーバーの対象となる HTTP メソッドはどれか。

- [ ] A. POST / PUT / PATCH
- [x] B. GET / HEAD / OPTIONS
- [ ] C. DELETE のみ
- [ ] D. すべてのメソッド

> **解説**: フェイルオーバーするのは GET / HEAD / OPTIONS のみ。POST/PUT 等は対象外。なお OPTIONS をキャッシュ対象メソッドに含めていないと OPTIONS はフェイルオーバーしない。
> **出典**: [cloudfront README #4 Origin Groups](README.md#4-origin-groupsオリジンフェイルオーバー頻出)

## cloudfront-007
- type: single
- difficulty: medium
- domain: 4
- tags: [waf, multi-region]

CloudFront ディストリビューションに AWS WAF を関連付ける際、Web ACL を作成すべきスコープ/リージョンはどれか。

- [x] A. us-east-1（CLOUDFRONT スコープ）
- [ ] B. ディストリビューションの主要視聴者がいるリージョン
- [ ] C. 任意のリージョン（自動で全エッジへ展開）
- [ ] D. オリジンが存在するリージョン

> **解説**: CloudFront 用の WAF Web ACL は us-east-1 の CLOUDFRONT スコープに作成する必要がある。エッジで SQLi/XSS/レートベース/地理ブロック等を評価し、オリジンより手前で攻撃を遮断できる。
> **出典**: [cloudfront README #7 セキュリティ統合](README.md#7-セキュリティ統合-waf--shield--tls--署名--fle)

## cloudfront-008
- type: single
- difficulty: medium
- domain: 4
- tags: [tls, public-ip]

独自ドメインの TLS 配信でコストを抑えたい。SNI と専用 IP（Dedicated IP）SSL に関する説明として正しいものはどれか。

- [x] A. SNI は既定かつ無料で、1 つの IP を複数ディストリビューションで共有できる。専用 IP SSL は月額課金で SNI 非対応の旧クライアント向け
- [ ] B. SNI は有料で、専用 IP SSL が無料の既定である
- [ ] C. SNI も専用 IP SSL も無料である
- [ ] D. SNI を使うとカスタムドメインが使えない

> **解説**: SNI は既定・無料で 1 つの IP を複数ディストリビューションで共有する。SNI 非対応の旧クライアントを救う専用 IP（Dedicated IP）SSL は月額課金で追加コストが大きい。
> **出典**: [cloudfront README #7 セキュリティ統合](README.md#7-セキュリティ統合-waf--shield--tls--署名--fle)

## cloudfront-009
- type: single
- difficulty: medium
- domain: 4
- tags: [edge-caching]

HLS の複数セグメントファイルへ URL を変えずに一括でアクセス制限をかけたい。適切な仕組みはどれか。

- [ ] A. 署名付き URL（Canned ポリシー）
- [x] B. 署名付き Cookie
- [ ] C. OAC
- [ ] D. Field-Level Encryption

> **解説**: 署名付き Cookie は複数ファイル（HLS セグメント等）に一括でアクセス制御し、URL を変えたくない場合に向く。個別ファイルへのアクセスや URL を直接渡す場合は署名付き URL を使う。いずれもトラステッドキーグループ推奨。
> **出典**: [cloudfront README #7 セキュリティ統合](README.md#7-セキュリティ統合-waf--shield--tls--署名--fle)

## cloudfront-010
- type: single
- difficulty: hard
- domain: 1
- tags: [use-case-fit]

非 HTTP（TCP/UDP）のゲーム/VoIP トラフィックに、固定 IP と L4 の高速リージョンフェイルオーバーが必要。適切なサービスはどれか。

- [ ] A. CloudFront
- [x] B. AWS Global Accelerator
- [ ] C. CloudFront ＋ OAC
- [ ] D. API Gateway エッジ最適化

> **解説**: Global Accelerator は L4（TCP/UDP）で 2 つの静的 Anycast IP を提供し、TLS 終端せずパススルーする。非 HTTP・固定 IP・L4 高速フェイルオーバーに向く。キャッシュや HTTP/WAF/署名保護なら CloudFront。
> **出典**: [cloudfront README #9 CloudFront と Global Accelerator の使い分け](README.md#9-cloudfront-と-global-accelerator-の使い分け最頻出)

## cloudfront-011
- type: single
- difficulty: medium
- domain: 4
- tags: [encryption]

ビューワーが送信するクレジットカード番号などの特定フィールドを、エッジで暗号化したままオリジンまで運び、権限を持つ下流のみが復号できるようにしたい。使うべき機能はどれか。

- [x] A. Field-Level Encryption（FLE）
- [ ] B. OAC
- [ ] C. 署名付き Cookie
- [ ] D. TLS 1.3 セキュリティポリシー

> **解説**: FLE は特定フィールド（PII 等）をエッジで公開鍵暗号化し、オリジンまで暗号化したまま転送する。復号は権限を持つ下流コンポーネントの秘密鍵のみ。TLS の経路暗号化に加え機微フィールドを多重保護する（最大 10 フィールド）。
> **出典**: [cloudfront README #7 セキュリティ統合](README.md#7-セキュリティ統合-waf--shield--tls--署名--fle)

## cloudfront-012
- type: single
- difficulty: medium
- domain: 1
- tags: [edge-caching, api-endpoint]

インターネットに公開していないプライベートサブネットの ALB/NLB/EC2 を、CloudFront から非公開のまま配信したい。適切なオリジン構成はどれか。

- [x] A. VPC オリジン
- [ ] B. S3 静的ウェブサイトエンドポイント
- [ ] C. カスタムオリジン（パブリック ALB）
- [ ] D. MediaStore オリジン

> **解説**: VPC オリジンを使うと、プライベートサブネットの ALB/NLB/EC2 をインターネット公開せずに CloudFront から直接配信できる。パブリック ALB をカスタムオリジンにする方式とは異なり非公開を保てる。
> **出典**: [cloudfront README #2 コアコンセプト](README.md#2-コアコンセプト)

## cloudfront-013
- type: single
- difficulty: medium
- domain: 3
- tags: [monitoring]

CloudFront でほぼリアルタイムにリクエストを分析し、即時に異常検知へ流したい。適切なログ機能はどれか。

- [ ] A. 標準ログ（S3 出力）
- [x] B. リアルタイムログ（Kinesis Data Streams 経由）
- [ ] C. CloudTrail データイベント
- [ ] D. VPC Flow Logs

> **解説**: リアルタイムログは Kinesis Data Streams 経由でほぼリアルタイムにサンプリング配信され、即時分析に向く。標準ログ（v2）は S3 / CloudWatch Logs / Data Firehose へ出力されるが即時性ではリアルタイムログが上。
> **出典**: [cloudfront README #8 アクセスログとモニタリング](README.md#8-アクセスログとモニタリング)
