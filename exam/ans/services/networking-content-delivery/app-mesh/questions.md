---
service: app-mesh
domain_default: 1
source: README.md
source_sha256: ff9169b9d9a0b11b2c0c290d374d39c8009b84d687140dde8c6128fe7a7279c0
generated: 2026-05-24
---

## app-mesh-001
- type: single
- difficulty: medium
- domain: 1
- tags: [service-mesh]

AWS App Mesh のデータプレーンとして各サービスに併設され、実際のトラフィック転送を担うコンポーネントはどれか。

- [ ] A. ALB
- [x] B. Envoy サイドカープロキシ
- [ ] C. NAT Gateway
- [ ] D. Route 53 Resolver

> **解説**: App Mesh は Envoy プロキシベースのサービスメッシュで、各サービスにサイドカーとして Envoy を配置する。Envoy がメッシュ設定（コントロールプレーン）を読み取り、実際のルーティング（データプレーン）を実行する。
> **出典**: [app-mesh README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## app-mesh-002
- type: single
- difficulty: medium
- domain: 1
- tags: [service-mesh, routing-policy, monitoring]

App Mesh で v1 に 90%、v2 に 10% の割合でトラフィックを振り分けるカナリアデプロイを行いたい。設定するコンポーネントはどれか。

- [ ] A. Virtual Service の発見名
- [ ] B. Virtual Node のリスナー
- [x] C. Virtual Router のルートで重み付けを設定する
- [ ] D. Virtual Gateway のポート

> **解説**: Virtual Router のルートで複数の Virtual Node への重み付け（例 v1:90% / v2:10%）を設定することで、カナリア/ブルーグリーンデプロイを実現する。メッシュ設定の更新だけで切り替わりアプリ再デプロイは不要。
> **出典**: [app-mesh README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## app-mesh-003
- type: single
- difficulty: hard
- domain: 4
- tags: [use-case-fit, service-discovery, automation]

App Mesh に関する最重要の制約として、新規設計で考慮すべきものはどれか。

- [ ] A. 追加料金が高額である
- [x] B. 2026年9月30日でサポート終了予定で、Amazon ECS Service Connect への移行が推奨されている
- [ ] C. EKS では利用できない
- [ ] D. L4 トラフィックしか制御できない

> **解説**: AWS は 2026年9月30日で App Mesh のサポートを終了する予定。以降はコンソール/リソースにアクセスできなくなり、ECS Service Connect への移行が推奨される。新規採用は避けるべき。
> **出典**: [app-mesh README #1 概要](README.md#1-概要)

## app-mesh-004
- type: single
- difficulty: medium
- domain: 1
- tags: [service-mesh, service-discovery]

Virtual Node のサービス発見方法として指定できるものはどれか。

- [x] A. DNS または AWS Cloud Map
- [ ] B. ARP のみ
- [ ] C. IAM ロール
- [ ] D. セキュリティグループタグ

> **解説**: Virtual Node の発見方法には DNS または AWS Cloud Map を指定できる。Cloud Map を使うとヘルシーなインスタンスへの発見が可能。
> **出典**: [app-mesh README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## app-mesh-005
- type: single
- difficulty: medium
- domain: 1
- tags: [vpn, security-group]

メッシュ外のクライアントからのトラフィックを受け入れる入口（Ingress）として機能するコンポーネントはどれか。

- [ ] A. Virtual Node
- [ ] B. Virtual Service
- [x] C. Virtual Gateway
- [ ] D. Mesh

> **解説**: Virtual Gateway はメッシュ境界の Envoy で、メッシュ外クライアントからのトラフィックの受け口（Ingress）となる。これをメッシュ内ルーティングへ橋渡しする。
> **出典**: [app-mesh README #2 コアコンセプト](README.md#2-コアコンセプト)

## app-mesh-006
- type: multi
- difficulty: hard
- domain: 1
- tags: [service-mesh, alb, message-queue]

App Mesh の Virtual Router のルートで実現できる L7 トラフィック制御を 2 つ選べ。

- [x] A. HTTP ヘッダ / URL パス / gRPC メソッド名による条件分岐
- [x] B. リトライポリシー（回数・間隔・対象エラー）
- [ ] C. TCP ポート番号の NAT 変換
- [ ] D. BGP コミュニティによる経路制御
- [ ] E. IPsec トンネルの暗号化設定

> **解説**: Virtual Router のルートでは HTTP ヘッダ・URL パス・gRPC サービス/メソッド名による振り分けや重み付けルーティング、リトライポリシーといった L7 制御ができる。NAT・BGP・IPsec はメッシュの機能ではない。
> **出典**: [app-mesh README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## app-mesh-007
- type: single
- difficulty: medium
- domain: 3
- tags: [monitoring]

App Mesh の可観測性について正しいものはどれか。

- [x] A. Envoy がメトリクス・ログ・分散トレーシングを出力し、CloudWatch / X-Ray / Prometheus / Grafana 等と連携する
- [ ] B. 可観測性はアプリのコードを大幅に改修しないと得られない
- [ ] C. メトリクスは VPC Flow Logs だけで取得する
- [ ] D. トレーシングは非対応である

> **解説**: Envoy がメトリクス・ログ・分散トレーシングを出力し、CloudWatch・X-Ray・Prometheus・Grafana 等と連携してサービス間通信を end-to-end で可視化できる。アプリ改修なしで得られる。
> **出典**: [app-mesh README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## app-mesh-008
- type: single
- difficulty: easy
- domain: 1
- tags: [use-case-fit, awsvpc]

App Mesh を利用する前提として必要なものはどれか。

- [ ] A. オンプレミスの物理サーバのみ
- [x] B. AWS Fargate / ECS / EKS / EC2 上の Kubernetes や Docker のいずれかで稼働するサービス
- [ ] C. Lambda 関数だけ
- [ ] D. S3 バケット

> **解説**: App Mesh の利用には Fargate / ECS / EKS / EC2 上の Kubernetes / Docker on EC2 のいずれかで稼働中のサービスが必要。Envoy サイドカーをそれらのタスク/Pod に追加してメッシュへ参加させる。
> **出典**: [app-mesh README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## app-mesh-009
- type: single
- difficulty: medium
- domain: 2
- tags: [monitoring, iac]

App Mesh のカナリアデプロイがアプリケーションの観点で優れている理由として正しいものはどれか。

- [ ] A. ルーティング変更のたびにアプリとプロキシの再デプロイが必要になる
- [x] B. メッシュ設定の更新だけでルーティングを切り替えられ、アプリやプロキシの再デプロイが不要
- [ ] C. アプリのソースコードにルーティングロジックを埋め込む必要がある
- [ ] D. DNS の TTL 切れを待たないと切り替わらない

> **解説**: App Mesh ではルーティング制御をインフラ層（メッシュ設定）に外出しできるため、メッシュ設定の更新だけでルーティングを切り替えられ、アプリやプロキシの再デプロイが不要。これがカナリアに有効。
> **出典**: [app-mesh README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## app-mesh-010
- type: single
- difficulty: medium
- domain: 3
- tags: [cost, service-mesh]

App Mesh のコスト・オーバーヘッドに関する説明として正しいものはどれか。

- [ ] A. App Mesh 自体に高額な固定料金がかかる
- [x] B. App Mesh 自体の追加料金はなく、ECS/EKS/EC2/Fargate のコンピュートと Envoy のリソース消費、出力先（CloudWatch/X-Ray）の料金が発生する
- [ ] C. Envoy サイドカーは CPU/メモリを一切消費しない
- [ ] D. データ転送は全て無料である

> **解説**: App Mesh 自体の追加料金はない。利用するコンピュートと Envoy が消費するリソース、出力先の料金が発生する。Envoy サイドカー追加により各タスク/Pod の CPU・メモリと若干のレイテンシオーバーヘッドが増える。
> **出典**: [app-mesh README #6 制約・上限・コスト](README.md#6-制約上限コスト)
