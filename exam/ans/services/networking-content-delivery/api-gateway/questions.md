---
service: api-gateway
domain_default: 1
source: README.md
source_sha256: 9bb3837aaf682f28555af13753a7419a67bb9117b6cfa8ce2dad79336ccc77ee
generated: 2026-05-24
---

## api-gateway-001
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-endpoint, api-endpoint]

VPC 内の EC2 とオンプレミス（Direct Connect 経由）からのみ呼び出せ、インターネットには一切公開しない REST API を構築したい。最も適切なエンドポイントタイプはどれか。

- [ ] A. エッジ最適化エンドポイント
- [ ] B. リージョナルエンドポイント
- [x] C. プライベートエンドポイント（プライベート API）
- [ ] D. WebSocket エンドポイント

> **解説**: プライベート API は `execute-api` の Interface VPC エンドポイント（PrivateLink）経由でのみアクセスでき、インターネットに公開されない。VPC 内および DX/VPN 経由のオンプレからアクセスできる。エッジ最適化/リージョナルはパブリックに公開される。
> **出典**: [api-gateway README #4 プライベート API](README.md#4-プライベート-api最頻出)

## api-gateway-002
- type: single
- difficulty: easy
- domain: 1
- tags: [vpc-endpoint, edge-caching]

地理的に世界中へ分散したクライアントへ向けて REST API を低レイテンシで公開したい。既定かつ最適なエンドポイントタイプはどれか。

- [x] A. エッジ最適化エンドポイント
- [ ] B. リージョナルエンドポイント
- [ ] C. プライベートエンドポイント
- [ ] D. ローカルエンドポイント

> **解説**: エッジ最適化は内部で AWS 管理の CloudFront を経由して最寄り POP からリクエストを処理するため、地理的に分散したクライアントに向く。REST API の既定タイプでもある。同一リージョン/EC2 からの呼び出しならリージョナルが向く。
> **出典**: [api-gateway README #3 エンドポイントタイプ](README.md#3-エンドポイントタイプネットワーク観点の中核)

## api-gateway-003
- type: single
- difficulty: medium
- domain: 4
- tags: [api-endpoint, iam-policy]

プライベート API で、特定の VPC エンドポイント（VPCe）からの呼び出しだけを許可したい。必須となる制御はどれか。

- [ ] A. セキュリティグループのインバウンドルールのみ
- [x] B. API のリソースポリシーで `aws:SourceVpce` 条件を指定する
- [ ] C. WAF の IP セットによる制限のみ
- [ ] D. ステージのスロットリング設定

> **解説**: プライベート API ではリソースポリシーが必須で、`aws:SourceVpc` / `aws:SourceVpce` 条件により特定の VPC や VPC エンドポイントのみを許可する。さらに VPC エンドポイントポリシーで二段の制御が可能。
> **出典**: [api-gateway README #4 プライベート API](README.md#4-プライベート-api最頻出)

## api-gateway-004
- type: single
- difficulty: medium
- domain: 1
- tags: [api-endpoint, use-case-fit]

API キー単位のレート制限・使用プラン・クォータによるクライアント単位課金が要件にある。どの API タイプを選ぶべきか。

- [x] A. REST API
- [ ] B. HTTP API
- [ ] C. WebSocket API
- [ ] D. GraphQL API

> **解説**: 使用プラン + API キーによるクライアント単位のレート制限・クォータは REST API のみの機能。HTTP API は軽量・低コストだがこれらの管理機能を持たない。
> **出典**: [api-gateway README #6 スロットリング](README.md#6-スロットリング頻出)

## api-gateway-005
- type: multi
- difficulty: hard
- domain: 1
- tags: [vpc-endpoint, api-endpoint]

エンドポイントタイプと API タイプの対応について正しいものを 2 つ選べ。

- [x] A. プライベート API は REST API のみ対応する
- [x] B. HTTP API と WebSocket API はリージョナルエンドポイントのみ対応する
- [ ] C. HTTP API はエッジ最適化エンドポイントに対応する
- [ ] D. WebSocket API はプライベートエンドポイントに対応する
- [ ] E. エッジ最適化は HTTP API の既定タイプである

> **解説**: プライベートとエッジ最適化は REST API のみ対応する。HTTP API・WebSocket API はリージョナルのみ。よって C/D/E は誤り。
> **出典**: [api-gateway README #3 エンドポイントタイプ](README.md#3-エンドポイントタイプネットワーク観点の中核)

## api-gateway-006
- type: single
- difficulty: medium
- domain: 2
- tags: [vpc-link, api-endpoint]

REST API から VPC 内のプライベートな ELB バックエンドへインターネットを経由せず統合したい。REST API の VPC リンクの接続先として正しいものはどれか。

- [x] A. NLB（Network Load Balancer）
- [ ] B. ALB（Application Load Balancer）
- [ ] C. Classic Load Balancer のみ
- [ ] D. CloudFront ディストリビューション

> **解説**: REST API の VPC リンクは NLB を接続先とする。一方 HTTP API の VPC リンクは ALB / NLB / Cloud Map に接続できる。タイプによって接続先が異なる点が頻出。
> **出典**: [api-gateway README #5 カスタムドメインと VPC 統合](README.md#5-カスタムドメインと-vpc-統合)

## api-gateway-007
- type: single
- difficulty: hard
- domain: 4
- tags: [api-endpoint, tls]

プライベート API の TLS とプロトコルに関する制約として正しいものはどれか。

- [ ] A. TLS 1.0 から 1.3 まで自由に選択できる
- [x] B. TLS 1.2 のみ対応し、HTTP/2 リクエストは HTTP/1.1 に強制される
- [ ] C. TLS は不要でプレーン HTTP のみ
- [ ] D. mTLS 必須でクライアント証明書がないと接続できない

> **解説**: プライベート API は TLS 1.2 のみ対応する。HTTP/2 リクエストは HTTP/1.1 に強制され、IP タイプはデュアルスタックのみ（IPv4 のみ指定不可）という制約がある。
> **出典**: [api-gateway README #4 プライベート API](README.md#4-プライベート-api最頻出)

## api-gateway-008
- type: single
- difficulty: medium
- domain: 3
- tags: [api-endpoint]

クライアントが `429 Too Many Requests` を受け取った。原因切り分けのためにスロットルの適用順（優先される順）として正しいものはどれか。

- [x] A. 使用プラン → ステージ/メソッド → アカウント単位 → リージョン全体
- [ ] B. リージョン全体 → アカウント単位 → ステージ → 使用プラン
- [ ] C. ステージ → アカウント単位 → 使用プラン → リージョン全体
- [ ] D. アカウント単位 → 使用プラン → リージョン全体 → ステージ

> **解説**: API Gateway はトークンバケットで制御し、使用プラン（クライアント/メソッド単位）が最優先、続いてステージ/メソッド、アカウント単位（リージョン）、最後にリージョン全体の上限の順で評価される。429 の切り分けにはどのレベルかを特定する。
> **出典**: [api-gateway README #6 スロットリング](README.md#6-スロットリング頻出)

## api-gateway-009
- type: single
- difficulty: medium
- domain: 1
- tags: [api-endpoint, multi-region, routing-policy]

複数リージョンに同名のカスタムドメインを持つリージョナル API を展開し、最寄り/健全なリージョンへ振り分ける耐障害構成にしたい。組み合わせとして適切なものはどれか。

- [ ] A. エッジ最適化 API ＋ CloudFront のオリジングループ
- [x] B. リージョナル API ＋ Route 53 のレイテンシ/フェイルオーバールーティング
- [ ] C. プライベート API ＋ Transit Gateway
- [ ] D. WebSocket API ＋ Global Accelerator のみ

> **解説**: リージョナルのカスタムドメインはそのリージョン固有のため、複数リージョンに同名ドメインを設定し Route 53 のレイテンシ/フェイルオーバールーティングでマルチリージョン API を実現できる。固定 IP 要件があれば Global Accelerator を併用する。
> **出典**: [api-gateway README #5 カスタムドメインと VPC 統合](README.md#5-カスタムドメインと-vpc-統合)

## api-gateway-010
- type: single
- difficulty: medium
- domain: 4
- tags: [api-endpoint, tls]

エッジ最適化エンドポイントのカスタムドメインに使う ACM 証明書はどのリージョンで発行する必要があるか。

- [x] A. us-east-1（バージニア北部）
- [ ] B. API をデプロイしたリージョン
- [ ] C. 任意のリージョン（自動レプリケートされる）
- [ ] D. ap-northeast-1（東京）固定

> **解説**: エッジ最適化のカスタムドメインは内部で CloudFront を使うため ACM 証明書は us-east-1 で発行する必要がある。リージョナルはそのリージョンの ACM 証明書を使う。
> **出典**: [api-gateway README #5 カスタムドメインと VPC 統合](README.md#5-カスタムドメインと-vpc-統合)

## api-gateway-011
- type: single
- difficulty: hard
- domain: 1
- tags: [api-endpoint, vpc-endpoint]

プライベート API でプライベート DNS を有効化した。これに伴う挙動として正しいものはどれか。

- [ ] A. パブリック API のデフォルトエンドポイントも引き続き VPC からアクセスできる
- [x] B. `Host` / `x-apigw-api-id` ヘッダなしで VPC 内から呼べるが、パブリック API のデフォルトエンドポイントへ VPC からアクセスできなくなる
- [ ] C. インターネット経由のアクセスも自動的に有効になる
- [ ] D. リソースポリシーが不要になる

> **解説**: プライベート DNS を有効化すると専用ヘッダなしで VPC 内から呼べる一方、有効化中はパブリック API のデフォルトエンドポイントに VPC からアクセスできなくなる（必要ならプライベートホストゾーンで個別解決）。
> **出典**: [api-gateway README #4 プライベート API](README.md#4-プライベート-api最頻出)

## api-gateway-012
- type: single
- difficulty: easy
- domain: 1
- tags: [api-endpoint, cost, routing-policy]

Lambda / HTTP プロキシ統合が中心で、低コスト・低レイテンシを最優先したい。高度な API 管理機能（API キー使用プラン等）は不要。適切な API タイプはどれか。

- [ ] A. REST API
- [x] B. HTTP API
- [ ] C. WebSocket API
- [ ] D. プライベート REST API

> **解説**: HTTP API は REST API より最大 71% 安く、最大 60% 低レイテンシで、Lambda/HTTP プロキシ向き。高度な管理機能（使用プラン・API キー）が不要ならコスト最適。
> **出典**: [api-gateway README #2 コアコンセプト](README.md#2-コアコンセプト)
