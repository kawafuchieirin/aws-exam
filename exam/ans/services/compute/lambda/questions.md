---
service: lambda
domain_default: 1
source: README.md
source_sha256: 91af54310cde2410014c6aae46e3c97a18c859ae4ca4581a8981195ee8d3d699
generated: 2026-05-24
---

## lambda-001
- type: single
- difficulty: medium
- domain: 1
- tags: [eni, nat]

VPC に接続した Lambda 関数から外部のインターネット API を呼び出せない。正しい解決策はどれか。

- [ ] A. 関数をパブリックサブネットに配置する
- [x] B. プライベートサブネットに配置し、NAT Gateway 経由でアウトバウンドさせる
- [ ] C. 関数に Elastic IP を割り当てる
- [ ] D. セキュリティグループのインバウンドを全開放する

> **解説**: VPC 接続した Lambda 実行環境にはパブリック IP が付かないため、パブリックサブネットに置いてもインターネットへ出られない。プライベートサブネットに置き、NAT Gateway 経由でアウトバウンドさせるのが正解。AWS サービスへは VPC エンドポイントも使える。
> **出典**: [Lambda README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## lambda-002
- type: single
- difficulty: medium
- domain: 1
- tags: [eni, auto-scaling]

現行アーキテクチャの VPC 接続 Lambda における Hyperplane ENI の特徴として正しいものはどれか。

- [ ] A. 同時実行 1 つにつき 1 つの ENI が作成される
- [x] B. 同一の SG:サブネットの組を使う関数は同じ Hyperplane ENI を共有する
- [ ] C. ENI は関数ごとに専有され共有されない
- [ ] D. ENI 数が同時実行数の上限を律速する

> **解説**: 現行の Hyperplane ENI は SG:サブネットの組み合わせ単位で作成・共有される。同一アカウントで同じ SG:サブネットの組を使う関数は同じ ENI を共有するため ENI が爆発的に増えず、スケールは ENI 数に律速されない。旧来の「同時実行ごとに ENI 作成」とは異なる。
> **出典**: [Lambda README #3 アーキテクチャ](README.md#3-アーキテクチャ--仕組み)

## lambda-003
- type: single
- difficulty: hard
- domain: 3
- tags: [ip-exhaustion, eni, subnetting]

多数の Lambda 関数で "exceeded the maximum limit for HyperPlane elastic network interfaces" エラーが発生した。根本対策として適切なものはどれか。

- [ ] A. 同時実行数（予約済み同時実行）を増やす
- [x] B. 関数が使う SG:サブネットの組み合わせ数を減らし、十分大きいサブネット CIDR を割り当てる
- [ ] C. すべての関数を VPC 外に出す前にメモリを増やす
- [ ] D. NAT Gateway を追加する

> **解説**: このエラーは SG:サブネットの組み合わせが多すぎる、またはサブネットの IP 不足が原因。対策は SG:サブネットの組を減らすこと、十分大きいサブネット CIDR を割り当てること。Hyperplane 化により IP 消費は同時実行数とは独立している。
> **出典**: [Lambda README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## lambda-004
- type: single
- difficulty: medium
- domain: 4
- tags: [vpc-endpoint, privatelink, cost]

VPC 接続 Lambda から AWS サービスへアクセスする際、NAT Gateway のコストを回避しつつプライベートに接続したい。適切な手段はどれか。

- [ ] A. インターネット Gateway を直接利用する
- [x] B. VPC エンドポイント（PrivateLink / Gateway エンドポイント）を利用する
- [ ] C. パブリックサブネットに移動する
- [ ] D. Elastic IP を付与する

> **解説**: AWS サービスへは VPC エンドポイント（Interface = PrivateLink、S3/DynamoDB は Gateway エンドポイント）を使えば、NAT Gateway を経由せずプライベートに接続でき、NAT のコストを回避できる。セキュリティ面でも有利。
> **出典**: [Lambda README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## lambda-005
- type: single
- difficulty: easy
- domain: 1
- tags: [awsvpc, subnetting, security-group]

Lambda 関数を VPC 内リソース（RDS 等）にアクセスさせるための設定として正しいものはどれか。

- [ ] A. RDS のパブリックアクセスを有効にするだけでよい
- [x] B. 関数にサブネットとセキュリティグループを指定して VPC 接続する
- [ ] C. 関数に Elastic IP を割り当てる
- [ ] D. Lambda は既定で VPC 内にあるので設定不要

> **解説**: Lambda は既定で VPC 外（AWS 管理ネットワーク）で動作する。VPC 内リソースへアクセスするには、関数にサブネットとセキュリティグループを指定して VPC 接続する。これにより Hyperplane ENI が作成される。
> **出典**: [Lambda README #2 コアコンセプト](README.md#2-コアコンセプト)

## lambda-006
- type: single
- difficulty: hard
- domain: 3
- tags: [eni, hybrid, auto-scaling]

各 Hyperplane ENI が扱える接続数と、それを超えた場合の挙動として正しいものはどれか。

- [ ] A. 約 1,000 接続で上限に達し、それ以上は接続が拒否される
- [x] B. 約 65,000 接続/ポートを扱い、超過時は Lambda が自動で ENI を追加スケールする
- [ ] C. 接続数に上限はなく無制限である
- [ ] D. 約 65,000 接続を超えると関数がエラー終了する

> **解説**: 各 Hyperplane ENI は最大約 65,000 接続/ポートを扱う。これを超過すると Lambda が自動で ENI を追加してスケールするため、接続増に追従できる。拒否やエラー終了ではない。
> **出典**: [Lambda README #3 アーキテクチャ](README.md#3-アーキテクチャ--仕組み)

## lambda-007
- type: single
- difficulty: medium
- domain: 4
- tags: [security-group, vpc-endpoint, hybrid]

VPC 接続した Lambda から RDS へ接続する際のセキュリティグループ設定として正しいものはどれか。

- [ ] A. Lambda には SG を指定できないため RDS 側のみ設定する
- [x] B. Lambda に指定した SG を、RDS 側 SG のインバウンドで許可する
- [ ] C. RDS の SG をすべての IP に開放する
- [ ] D. Lambda の SG で RDS の MAC アドレスを許可する

> **解説**: VPC 接続 Lambda にはお客様が指定した SG が適用される。RDS など宛先リソース側の SG で、その Lambda の SG を送信元として許可する必要がある。SG 参照（SG-to-SG）で最小権限を実現できる。
> **出典**: [Lambda README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## lambda-008
- type: single
- difficulty: medium
- domain: 3
- tags: [auto-scaling, eni, enhanced-networking]

現行アーキテクチャで VPC 接続 Lambda のコールドスタート遅延が大幅に改善した理由として正しいものはどれか。

- [ ] A. 実行ごとに専用 ENI を作成するようになったため
- [x] B. ENI 作成が実行パスから外れ、Hyperplane ENI を事前共有するようになったため
- [ ] C. VPC 接続が廃止されたため
- [ ] D. NAT Gateway がコールドスタートを肩代わりするため

> **解説**: 旧来は同時実行ごとに ENI を作成し、これがコールドスタートの遅延要因だった。現行では ENI 作成が実行パスから外れ、SG:サブネット組ごとに共有される Hyperplane ENI を使うため、VPC 接続のコールドスタートが大幅に改善した。
> **出典**: [Lambda README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## lambda-009
- type: single
- difficulty: easy
- domain: 1
- tags: [dns, routing-policy]

VPC 内 Lambda の名前解決はどのように行われるか。

- [ ] A. パブリック DNS リゾルバ（8.8.8.8）を直接利用する
- [x] B. VPC リゾルバ（VPC CIDR の基底 +2 のアドレス）で名前解決する
- [ ] C. Lambda は名前解決を行えない
- [ ] D. NAT Gateway が DNS を代理する

> **解説**: VPC 接続した Lambda は VPC リゾルバ（VPC の CIDR 基底アドレス +2、いわゆる VPC+2）で名前解決する。これは VPC 内の他リソースと同じ仕組み。
> **出典**: [Lambda README #5 他サービスとの連携](README.md#5-他サービスとの連携)

## lambda-010
- type: multi
- difficulty: medium
- domain: 1
- tags: [eni, security-group, monitoring]

VPC 接続 Lambda のアウトバウンド通信について、正しいものを 2 つ選べ。

- [x] A. VPC 接続すると既定でインターネットへ出られない
- [ ] B. パブリックサブネットに置けば自動でパブリック IP が付与され外部へ出られる
- [x] C. AWS サービスへは VPC エンドポイント（PrivateLink）でプライベート接続できる
- [ ] D. インターネットへ出るには Internet Gateway を関数に直接アタッチする
- [ ] E. アウトバウンドには必ず Elastic IP が必要

> **解説**: VPC 接続 Lambda は既定でインターネットへ出られない（A）。外部へは NAT Gateway 経由、AWS サービスへは VPC エンドポイント（PrivateLink）でプライベート接続できる（C）。実行環境にパブリック IP は付かず（B 誤）、IGW を直接アタッチはできず（D 誤）、EIP は必須ではない（E 誤）。
> **出典**: [Lambda README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## lambda-011
- type: multi
- difficulty: hard
- domain: 4
- tags: [ip-exhaustion, cost, vpc-endpoint]

VPC 接続 Lambda の IP 消費とコスト最適化について、正しいものを 2 つ選べ。

- [x] A. Hyperplane ENI がサブネットの IP を消費し、SG:サブネット組が多いほど増える
- [ ] B. IP 消費は同時実行数に比例して増える
- [x] C. S3/DynamoDB へは Gateway エンドポイント、他 AWS サービスは Interface エンドポイントで NAT コストを回避できる
- [ ] D. VPC 接続自体に追加のネットワーク料金が発生する
- [ ] E. NAT Gateway は時間課金のみでデータ処理料はかからない

> **解説**: Hyperplane ENI はサブネットの IP を消費し、SG:サブネットの組が多いほど増える（A）。S3/DynamoDB は Gateway エンドポイント、他 AWS サービスは Interface エンドポイントで NAT コストを回避できる（C）。IP 消費は同時実行数と非連動（B 誤）、VPC 接続自体は追加料金なし（D 誤）、NAT は時間＋データ処理料が発生する（E 誤）。
> **出典**: [Lambda README #6 制約・上限・コスト](README.md#6-制約上限コスト)
