---
service: iam
domain_default: 4
source: README.md
source_sha256: d7690192ab9e59717592b06f656255b7793ed3cfff138c7fba2c101b081d33d2
generated: 2026-05-24
---

## iam-001
- type: single
- difficulty: medium
- domain: 4
- tags: [iam-policy, source-condition]

特定の VPC エンドポイント経由でのみ S3 バケットにアクセスを許可し、インターネット経由や他経路を遮断したい。最も適切な実装はどれか。

- [ ] A. エンドポイントポリシーに `aws:SourceVpc` を設定するだけ
- [x] B. S3 バケットポリシーで `aws:SourceVpce` が一致しない場合に Deny する
- [ ] C. セキュリティグループで S3 の IP を許可する
- [ ] D. IAM ユーザーポリシーで S3 アクセスを許可する

> **解説**: 「このバケットへどの経路を許すか」はリソース側のバケットポリシーで制御する。`aws:SourceVpce` 一致以外を Deny すれば指定エンドポイント経由のみ許可となる。条件キーは VPC エンドポイント経由のリクエストにのみ存在するため、インターネット経由は自動的に遮断される。
> **出典**: [iam README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## iam-002
- type: single
- difficulty: medium
- domain: 4
- tags: [source-condition, subnetting]

`aws:SourceVpce` 条件キーについて正しい説明はどれか。

- [ ] A. すべての AWS API リクエストに付与される
- [x] B. VPC エンドポイント経由のリクエストにのみ存在する
- [ ] C. インターネット経由のリクエストにのみ存在する
- [ ] D. オンプレミスからの VPN リクエストにのみ存在する

> **解説**: `aws:SourceVpc` / `aws:SourceVpce` / `aws:VpcSourceIp` は VPC エンドポイント経由のリクエストにのみ付与される。そのためこれらでの制限は暗黙的にエンドポイント経由の強制にもなる。
> **出典**: [iam README #2 コアコンセプト（ネットワーク関連）](README.md#2-コアコンセプトネットワーク関連)

## iam-003
- type: single
- difficulty: medium
- domain: 4
- tags: [vpc-endpoint]

VPC エンドポイントポリシーの役割として正しいものはどれか。

- [ ] A. ID ベースポリシーやリソースポリシーを上書きして許可を付与する
- [x] B. そのエンドポイント経由で通せるアクション/リソース/プリンシパルの範囲を絞る追加層である
- [ ] C. デフォルトで全アクセスを拒否する
- [ ] D. バケットポリシーの代わりに使う

> **解説**: エンドポイントポリシーは「このエンドポイントを通せる範囲」を絞る追加の層で、ID/リソースポリシーを上書きしない。デフォルトは全許可（Principal/Action/Resource すべて `*`）であり、絞る場合のみカスタムを付ける。
> **出典**: [iam README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## iam-004
- type: single
- difficulty: hard
- domain: 4
- tags: [vpc-endpoint, nacl]

VPC エンドポイントを作成したがエンドポイントポリシーを一切カスタマイズしていない。この状態でのエンドポイントポリシーの挙動はどれか。

- [ ] A. すべてのアクセスが拒否される
- [x] B. デフォルトで全許可（Principal `*`, Action `*`, Resource `*`）になる
- [ ] C. エンドポイントが作成できない
- [ ] D. 自動的に最小権限が適用される

> **解説**: エンドポイントポリシーはデフォルトで全許可。絞り込みたい場合のみカスタムポリシーを付与する。アクセス制御は他の層（リソース/ID ポリシー）と AND で評価される。
> **出典**: [iam README #3 仕組み / 評価フロー](README.md#3-仕組み--評価フロー)

## iam-005
- type: single
- difficulty: hard
- domain: 4
- tags: [vpc-endpoint, iam-policy]

S3/DynamoDB の Gateway エンドポイントのエンドポイントポリシーで、特定のプリンシパルだけに利用を限定したい。正しい方法はどれか。

- [ ] A. `Principal` フィールドに対象 IAM ロール ARN を列挙する
- [x] B. `Principal` は `*` 固定なので `aws:PrincipalArn` 条件で限定する
- [ ] C. Gateway エンドポイントではプリンシパル限定はできない
- [ ] D. SCP でのみ限定できる

> **解説**: Gateway エンドポイントのエンドポイントポリシーでは `Principal` は `*` 固定であり、プリンシパル限定は `aws:PrincipalArn` 条件で行う。
> **出典**: [iam README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## iam-006
- type: single
- difficulty: medium
- domain: 4
- tags: [scp, multi-account]

SCP（Service Control Policy）について正しい説明はどれか。

- [ ] A. メンバーアカウントに許可を付与する
- [x] B. アクセスの上限を定める（許可は付与しない）ガードレールである
- [ ] C. IAM ロールにアタッチして使う
- [ ] D. リソースベースポリシーの一種である

> **解説**: SCP は Organizations のアクセス上限を定めるもので、許可そのものは付与しない。例として「特定リージョン以外の API 呼び出しを Deny」「VPC エンドポイント削除を禁止」などのガードレールに使う。
> **出典**: [iam README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## iam-007
- type: multi
- difficulty: hard
- domain: 4
- tags: [use-case-fit, security-group]

VPC エンドポイント経由の S3 リクエストがアクセス成功するために満たすべき条件はどれか。3つ選べ。

- [x] A. エンドポイントポリシーで許可されている
- [x] B. リソースポリシー（バケットポリシー）で許可され明示 Deny がない
- [x] C. ID ベースポリシー＋SCP で許可され明示 Deny がない
- [ ] D. セキュリティグループでエフェメラルポートを許可している
- [ ] E. NACL でアウトバウンドを Deny している

> **解説**: アクセスは全レイヤーの評価の AND。エンドポイントポリシー、リソースポリシー、ID ポリシー＋SCP のいずれかで明示 Deny や許可不足があると失敗する。SG/NACL は L3/L4 のネットワーク制御でこの IAM 評価チェーンとは別軸。
> **出典**: [iam README #3 仕組み / 評価フロー](README.md#3-仕組み--評価フロー)

## iam-008
- type: single
- difficulty: medium
- domain: 4
- tags: [source-condition, quotas]

`aws:SourceVpc` などのネットワーク系条件キーの指定方法について正しいものはどれか。

- [ ] A. ワイルドカードで前方一致指定できる
- [ ] B. 数値比較演算子で範囲指定できる
- [x] C. システム生成 ID のため完全一致で指定する（ワイルドカード/数値演算子は不可）
- [ ] D. CIDR 表記で指定する

> **解説**: `aws:SourceVpc` 等はシステム生成 ID のため、ワイルドカードや数値演算子と併用できず完全一致で指定する。
> **出典**: [iam README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## iam-009
- type: single
- difficulty: easy
- domain: 4
- tags: [cost, quotas]

ANS 観点の IAM（エンドポイントポリシー/条件キー/SCP）の利用料金について正しいものはどれか。

- [ ] A. ポリシー数に応じて月額課金される
- [ ] B. 条件キー評価ごとに従量課金される
- [x] C. IAM・ポリシー・条件キーの利用は無料
- [ ] D. SCP のみ有料

> **解説**: IAM・ポリシー・条件キーの利用は無料。なおエンドポイントポリシーには最大 20,480 文字というサイズ上限がある。
> **出典**: [iam README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## iam-010
- type: single
- difficulty: medium
- domain: 4
- tags: [vpc-sharing, scp]

RAM で共有されたリソースをコンシューマーアカウントが利用する場合の権限について正しいものはどれか。

- [ ] A. 共有されると IAM ポリシーや SCP は一切適用されない
- [x] B. コンシューマー側の IAM ポリシー・SCP は引き続き適用される
- [ ] C. オーナーアカウントの SCP のみが適用される
- [ ] D. RAM が独自の権限ですべてを上書きする

> **解説**: RAM で共有されたリソースでも、コンシューマー側の IAM ポリシーや SCP は引き続き適用される。共有は使用権の付与であってガードレールを無効化しない。
> **出典**: [iam README #5 他サービスとの連携](README.md#5-他サービスとの連携)
