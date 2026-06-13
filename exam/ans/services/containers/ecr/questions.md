---
service: ecr
domain_default: 4
source: README.md
source_sha256: 9080909f91cb63c2b25e1e3bb9e2faff1ba8fb203eca1f6a8abee623faa60994
generated: 2026-05-24
---

## ecr-001
- type: single
- difficulty: medium
- domain: 1
- tags: [vpc-endpoint]

プライベートサブネットの ECS タスクが NAT Gateway を使わずに ECR からイメージを pull できるようにしたい。最低限必要な VPC エンドポイントの組み合わせはどれか。

- [ ] A. com.amazonaws.region.ecr.api（Interface）のみ
- [ ] B. com.amazonaws.region.ecr.dkr（Interface）のみ
- [x] C. ecr.api（Interface）+ ecr.dkr（Interface）+ S3（Gateway）
- [ ] D. com.amazonaws.region.ecr.api（Interface）+ NAT Gateway

> **解説**: NAT 無しのプライベート pull には3点が必須。ecr.api（認証・メタデータ）、ecr.dkr（Docker プロトコル）、そしてイメージレイヤー実体を格納する S3 への Gateway エンドポイント。api/dkr だけだと認証は通るがレイヤー取得で失敗する。
> **出典**: [ecr README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecr-002
- type: single
- difficulty: medium
- domain: 3
- tags: [vpc-endpoint, troubleshooting]

ecr.api と ecr.dkr の Interface エンドポイントを作成したが、認証は成功するのにイメージの pull がレイヤー取得で失敗する。最も可能性の高い原因はどれか。

- [ ] A. プライベート DNS が無効になっている
- [x] B. イメージレイヤー実体を取得する S3 の Gateway エンドポイントが無い
- [ ] C. ecr.dkr のセキュリティグループが 80 番ポートを許可していない
- [ ] D. リポジトリポリシーが pull を拒否している

> **解説**: ECR はイメージレイヤーの実体を S3 に格納するため、レイヤー取得には S3 への経路が必須。api/dkr だけでは認証・メタデータは通ってもレイヤー取得段階で失敗する典型的なひっかけ。
> **出典**: [ecr README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecr-003
- type: single
- difficulty: easy
- domain: 2
- tags: [vpc-endpoint, eni, tcp-udp]

ECR の Interface エンドポイント（ecr.api / ecr.dkr）に適用するセキュリティグループで許可すべきインバウンドポートはどれか。

- [ ] A. TCP 80
- [x] B. TCP 443
- [ ] C. TCP 53
- [ ] D. UDP 443

> **解説**: Interface エンドポイントは ENI + プライベート IP で動作し、ECR API 通信は HTTPS（TCP 443）。プライベートサブネットからの 443 インバウンドを許可する必要がある。
> **出典**: [ecr README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## ecr-004
- type: single
- difficulty: medium
- domain: 2
- tags: [vpc-endpoint, dns]

ECR の Interface エンドポイントで、既存の `*.dkr.ecr.region.amazonaws.com` ドメイン名をそのまま使ってエンドポイント経由で解決させたい。必要な設定はどれか。

- [x] A. エンドポイントのプライベート DNS を有効化する
- [ ] B. Route 53 にパブリックホストゾーンを作成する
- [ ] C. NAT Gateway にカスタム DNS を設定する
- [ ] D. S3 Gateway エンドポイントのプライベート DNS を有効化する

> **解説**: Interface エンドポイントでプライベート DNS を有効化すると、既存のサービスドメイン名がエンドポイントのプライベート IP へ透過的に解決される。アプリ側の設定変更が不要になる。S3 Gateway エンドポイントにはプライベート DNS の概念は無い。
> **出典**: [ecr README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecr-005
- type: single
- difficulty: hard
- domain: 4
- tags: [vpc-endpoint, least-privilege]

特定の ECR リポジトリのみへのアクセスに VPC エンドポイント経由のトラフィックを制限したい。最小権限を実現する手段はどれか。

- [ ] A. リポジトリのライフサイクルポリシーで制限する
- [x] B. VPC エンドポイントのエンドポイントポリシーで対象リポジトリのみ許可する
- [ ] C. NACL でリポジトリ ARN を指定して拒否する
- [ ] D. セキュリティグループでリポジトリ単位のルールを作る
> **解説**: エンドポイントポリシーで特定リポジトリのみを許可することで、エンドポイント経由のアクセスを最小権限化できる。NACL/SG は IP やポートの制御でリポジトリ ARN を扱えない。
> **出典**: [ecr README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecr-006
- type: single
- difficulty: easy
- domain: 4
- tags: [vpc-endpoint, iam-policy]

ECR のプライベートレジストリのアクセス制御について正しいものはどれか。

- [x] A. デフォルトでプライベートであり、IAM とリポジトリポリシーで制御する
- [ ] B. デフォルトでパブリックであり、明示的に非公開化が必要
- [ ] C. アクセス制御はセキュリティグループのみで行う
- [ ] D. NACL でリポジトリ単位の許可を設定する

> **解説**: ECR のプライベートレジストリはアカウント専用で既定でプライベート。アクセスは IAM ポリシーとリポジトリポリシーで制御する。
> **出典**: [ecr README #2 コアコンセプト](README.md#2-コアコンセプト)

## ecr-007
- type: single
- difficulty: medium
- domain: 1
- tags: [cost, nat, vpc-endpoint]

大量のイメージ pull を行うプライベートサブネット環境で、NAT Gateway 経由のデータ処理料を削減したい。最も効果的な対策はどれか。

- [ ] A. NAT Gateway を AZ ごとに増やす
- [x] B. ecr.api / ecr.dkr の Interface と S3 の Gateway エンドポイントを構成し NAT 経由を置き換える
- [ ] C. イメージを小さくするだけで十分
- [ ] D. パブリックサブネットに移して IGW を使う

> **解説**: NAT Gateway 経由の pull はデータ処理料が高い。VPC エンドポイント化（特に S3 Gateway は無料）で NAT 経由を置き換えるとトータルコストを削減できることが多い。
> **出典**: [ecr README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## ecr-008
- type: multi
- difficulty: hard
- domain: 1
- tags: [vpc-endpoint, eni]

ECR のプライベート pull に関わる VPC エンドポイントの特性として正しいものを2つ選べ。

- [x] A. ecr.api と ecr.dkr は Interface エンドポイントで ENI + プライベート IP として動作する
- [ ] B. ecr.dkr は Gateway エンドポイントで提供される
- [x] C. S3 のレイヤー取得用エンドポイントは Gateway 型で課金されない
- [ ] D. Interface エンドポイントの通信は UDP 53 を使う
- [ ] E. プライベート DNS は無効にしてもドメイン名がエンドポイントに解決される

> **解説**: ecr.api / ecr.dkr は Interface（PrivateLink）型で ENI とプライベート IP を持ち TCP 443 で通信する。S3 Gateway エンドポイントはルートテーブル経由で動き無料。プライベート DNS を有効化しないと既存ドメイン名は透過解決されない。
> **出典**: [ecr README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## ecr-009
- type: single
- difficulty: medium
- domain: 3
- tags: [awsvpc, iac]

EKS の Fargate プロファイルや ECS タスクがプライベートサブネットで動く際、コンテナイメージ取得の前提条件として ECR について正しいものはどれか。

- [x] A. ecr.api / ecr.dkr の Interface と S3 Gateway エンドポイント、または NAT が無いと pull に失敗する
- [ ] B. Fargate は ECR エンドポイント無しでも常に pull できる
- [ ] C. EKS は VPC CNI があれば ECR エンドポイントは不要
- [ ] D. ECS は bridge モードであれば ECR エンドポイントが不要になる

> **解説**: 実行環境（ECS/EKS/Fargate）に関わらず、プライベートサブネットからの ECR pull には3エンドポイント（api/dkr/S3）または NAT が必要。CNI やネットワークモードはこの前提を変えない。
> **出典**: [ecr README #5 他サービスとの連携](README.md#5-他サービスとの連携)

## ecr-010
- type: multi
- difficulty: medium
- domain: 1
- tags: [vpc-endpoint, iam-policy]

ECR の各 VPC エンドポイントの役割について正しいものを2つ選べ。

- [x] A. ecr.api は認証トークン取得や DescribeImages などのコントロールプレーン API を担う
- [x] B. ecr.dkr は docker push/pull の Docker Registry API を担う
- [ ] C. ecr.api がイメージレイヤーの実体を保存する
- [ ] D. ecr.dkr が S3 を経由せずレイヤー実体を直接配信する
- [ ] E. S3 Gateway エンドポイントは認証トークンの取得に使われる

> **解説**: ecr.api はコントロールプレーン API（認証トークン取得・DescribeImages 等）、ecr.dkr は Docker Registry API（push/pull）を担う。レイヤーの実体は S3 に格納され、S3 Gateway エンドポイント経由で取得する。
> **出典**: [ecr README #2 コアコンセプト](README.md#2-コアコンセプト)
</content>
</invoke>
