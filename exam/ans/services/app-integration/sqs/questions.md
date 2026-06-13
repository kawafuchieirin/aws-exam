---
service: sqs
domain_default: 2
source: README.md
source_sha256: 51e789b999cc91f5bc1014ce1e099907742ac499a01790d73f763c53e0ff5438
generated: 2026-05-24
---

## sqs-001
- type: single
- difficulty: easy
- domain: 1
- tags: [message-queue, use-case-fit]

SQS の主な役割として正しいものはどれか。

- [ ] A. publish/subscribe でメッセージを複数の宛先へファンアウトする
- [x] B. 送信側と受信側を疎結合にし、メッセージをバッファリングする
- [ ] C. イベントパターンでマッチしたイベントをルーティングする
- [ ] D. メトリクスを収集してアラームを発報する

> **解説**: SQS はフルマネージドのメッセージキューで、プロデューサとコンシューマを疎結合にし、メッセージをバッファリングして耐障害性とスケーラビリティを高める。ファンアウトは SNS、イベントルーティングは EventBridge の役割。
> **出典**: [sqs README #1 概要](README.md#1-概要)

## sqs-002
- type: single
- difficulty: medium
- domain: 2
- tags: [privatelink, vpc-endpoint]

プライベートサブネットの EC2 が IGW・NAT・VPN なしで SQS キューに送受信したい。必要な構成はどれか。

- [ ] A. ゲートウェイ型 VPC エンドポイント（`com.amazonaws.<region>.sqs`）
- [x] B. インターフェイス型 VPC エンドポイント（`com.amazonaws.<region>.sqs`）
- [ ] C. NAT ゲートウェイ
- [ ] D. VPC ピアリング

> **解説**: SQS への接続はインターフェイス VPC エンドポイント（PrivateLink）で行い、サービス名は `com.amazonaws.<region>.sqs`（FIPS は `...sqs-fips`）。これによりプライベートサブネットから IGW/NAT/VPN なしで送受信できる。SQS にゲートウェイ型エンドポイントは提供されていない。
> **出典**: [sqs README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sqs-003
- type: single
- difficulty: medium
- domain: 2
- tags: [vpc-endpoint, use-case-fit]

SQS のインターフェイス VPC エンドポイントを使う際の必須設定として正しいものはどれか。

- [ ] A. レガシーエンドポイント（`queue.amazonaws.com`）を使う
- [x] B. プライベート DNS を有効化し、標準の `sqs.<region>.amazonaws.com` 形式を使う
- [ ] C. HTTP エンドポイントを明示的に指定する
- [ ] D. ゲートウェイ型エンドポイントのルートを追加する

> **解説**: VPC でプライベート DNS を有効化し、標準の `sqs.<region>.amazonaws.com` 形式のエンドポイントを使う。レガシーエンドポイント（`queue.amazonaws.com` 等）はプライベート DNS 非対応。接続は HTTPS のみサポートされる。
> **出典**: [sqs README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sqs-004
- type: single
- difficulty: hard
- domain: 4
- tags: [iam-policy, source-condition, encryption]

「このエンドポイント経由でなければ拒否」してデータ漏洩経路を遮断したい。キューのアクセスポリシーで使う条件キーはどれか。

- [ ] A. `aws:SourceIp`
- [x] B. `aws:sourceVpce`
- [ ] C. `aws:SecureTransport`
- [ ] D. `aws:PrincipalOrgID`

> **解説**: キューのアクセスポリシーで `aws:sourceVpce` を条件にすると、特定のエンドポイント経由でなければ拒否でき、データ漏洩経路を遮断できる。`SecureTransport` は HTTPS 強制、`SourceIp` は IP 制限で、エンドポイント単位の制御には使えない。
> **出典**: [sqs README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sqs-005
- type: single
- difficulty: easy
- domain: 4
- tags: [encryption, tls]

SQS の暗号化に関する記述として正しいものはどれか。

- [ ] A. 接続は HTTP のみサポートされる
- [x] B. 転送中は HTTPS 必須、保存時は SSE-SQS / SSE-KMS に対応
- [ ] C. 保存時暗号化はサポートされない
- [ ] D. 暗号化を有効にすると VPC エンドポイントが使えない

> **解説**: SQS は転送中暗号化として HTTPS が必須で、保存時暗号化は SSE-SQS / SSE-KMS に対応する。暗号化と VPC エンドポイント利用は両立する。
> **出典**: [sqs README #5 制約・上限・コスト](README.md#5-制約上限コスト)

## sqs-006
- type: single
- difficulty: medium
- domain: 3
- tags: [vpc-endpoint, least-privilege, message-queue]

特定キューに対する `sqs:SendMessage` のみを経路単位で許可する最小権限を実現したい。最も適切な手段はどれか。

- [ ] A. セキュリティグループのアウトバウンドルール
- [x] B. VPC エンドポイントのエンドポイントポリシー
- [ ] C. ネットワーク ACL の Deny ルール
- [ ] D. ルートテーブルのブラックホールルート

> **解説**: エンドポイントポリシーで「`sqs:SendMessage` を特定キューにのみ許可」のように、経路単位で API アクション・対象キューを限定し最小権限を実現できる。SG/NACL/ルートテーブルはレイヤ 3/4 の制御であり、API アクション単位の制御はできない。
> **出典**: [sqs README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sqs-007
- type: single
- difficulty: medium
- domain: 3
- tags: [message-queue, well-architected]

自動化の信頼性確保のために、重複防止と失敗メッセージの隔離を行いたい。SQS の機能の組み合わせとして正しいものはどれか。

- [ ] A. プライベート DNS と FIPS エンドポイント
- [x] B. 可視性タイムアウトとデッドレターキュー（DLQ）
- [ ] C. トピックポリシーとサブスクリプション
- [ ] D. イベントバスとルール

> **解説**: 可視性タイムアウトは処理中メッセージの重複取得を防ぎ、DLQ は規定回数失敗したメッセージを隔離して自動化の信頼性を確保する。トピック/サブスクリプションは SNS、イベントバス/ルールは EventBridge の概念。
> **出典**: [sqs README #2 コアコンセプト](README.md#2-コアコンセプト)

## sqs-008
- type: single
- difficulty: easy
- domain: 1
- tags: [message-queue, use-case-fit]

厳密な順序保証が必要なメッセージ処理に適した SQS キュータイプはどれか。

- [ ] A. Standard キュー
- [x] B. FIFO キュー
- [ ] C. デッドレターキュー
- [ ] D. 遅延キュー

> **解説**: FIFO キューは厳密な順序保証を提供する。Standard キューは高スループットだが順序は保証されない（ベストエフォート）。DLQ は失敗隔離用、遅延キューは配信遅延の設定であり順序保証の主機能ではない。
> **出典**: [sqs README #2 コアコンセプト](README.md#2-コアコンセプト)

## sqs-009
- type: multi
- difficulty: medium
- domain: 2
- tags: [vpc-endpoint, use-case-fit]

SQS へインターフェイス VPC エンドポイント経由でプライベートアクセスする際に満たすべき要件を2つ選べ。

- [x] A. プライベート DNS を有効化する
- [ ] B. レガシーエンドポイント（`queue.amazonaws.com`）を使う
- [x] C. HTTPS でアクセスする
- [ ] D. NAT ゲートウェイを併設する
- [ ] E. パブリック IP を EC2 に割り当てる

> **解説**: プライベートアクセスにはプライベート DNS の有効化と HTTPS でのアクセスが必要。レガシーエンドポイントはプライベート DNS 非対応であり、NAT やパブリック IP はインターネット経由となるため要件に反する。
> **出典**: [sqs README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)

## sqs-010
- type: multi
- difficulty: hard
- domain: 4
- tags: [least-privilege, vpc-endpoint, source-condition]

SQS でプライベートかつ最小権限・漏洩遮断を実現する設定として適切なものを2つ選べ。

- [x] A. エンドポイントポリシーで特定アクション・特定キューに限定する
- [ ] B. キューを Standard から FIFO に変更する
- [x] C. アクセスポリシーで `aws:sourceVpce` 条件を付け、特定エンドポイント経由以外を拒否する
- [ ] D. 可視性タイムアウトを 0 に設定する
- [ ] E. NAT ゲートウェイ経由のアクセスを許可する

> **解説**: エンドポイントポリシーでアクション/キューを限定し、アクセスポリシーの `aws:sourceVpce` 条件で経由元エンドポイントを縛ることで、最小権限と漏洩経路の遮断を両立できる。キュータイプ変更や可視性タイムアウトはセキュリティ制御ではなく、NAT 許可はプライベート化に反する。
> **出典**: [sqs README #3 試験頻出ポイント](README.md#3-試験頻出ポイントネットワーク観点)
