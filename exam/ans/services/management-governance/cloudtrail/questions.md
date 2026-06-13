---
service: cloudtrail
domain_default: 4
source: README.md
source_sha256: 84deb7384532d2ca9ba3169a61c4ca3c0922d852c17fcc89fb60be2c4cc96fa0
generated: 2026-05-24
---

## cloudtrail-001
- type: single
- difficulty: medium
- domain: 4
- tags: [cloudtrail-events, config-rules]

「誰がいつセキュリティグループのインバウンドルールを変更したか」を追跡したい。記録される CloudTrail イベント種別はどれか。

- [x] A. 管理イベント（Management Events）
- [ ] B. データイベント（Data Events）
- [ ] C. ネットワークアクティビティイベント
- [ ] D. VPC フローログ

> **解説**: SG 変更（`AuthorizeSecurityGroupIngress` 等）やルート変更、VPC/サブネット作成などコントロールプレーンの構成変更は管理イベントに記録され、既定でオン。データイベントはデータプレーン操作、フローログはトラフィックメタデータで実行者は分からない。
> **出典**: [cloudtrail README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloudtrail-002
- type: single
- difficulty: medium
- domain: 3
- tags: [cloudtrail-events, monitoring]

90 日を超えてネットワーク構成変更の監査ログを保持し、横断的に分析したい。適切な手段はどれか。

- [ ] A. イベント履歴をコンソールで閲覧し続ける
- [x] B. 証跡（S3）または CloudTrail Lake を利用する
- [ ] C. データイベントを有効化する
- [ ] D. VPC フローログを CloudWatch Logs に送る

> **解説**: イベント履歴は直近 90 日のみ無料で閲覧可能。長期保持や横断分析が必要なら証跡を作成して S3 に配信するか、CloudTrail Lake で SQL 分析する。フローログは構成変更の監査用ではない。
> **出典**: [cloudtrail README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloudtrail-003
- type: single
- difficulty: hard
- domain: 4
- tags: [cloudtrail-events, vpc-endpoint]

VPC エンドポイント経由の API アクセスで、特に拒否（`VpceAccessDenied`）された試みを監査したい。最も適切な機能はどれか。

- [ ] A. VPC フローログ
- [ ] B. 管理イベント
- [x] C. ネットワークアクティビティイベント
- [ ] D. CloudWatch メトリクス

> **解説**: VPC エンドポイント経由の API コール（特に拒否）の監査は、フローログ（IP メタデータのみ）では不可能で、ネットワークアクティビティイベントが担う。組織外の認証情報がエンドポイントを使おうとする試みの検知に有効。既定オフ・追加課金。
> **出典**: [cloudtrail README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloudtrail-004
- type: single
- difficulty: medium
- domain: 3
- tags: [monitoring]

想定外の SG 全開放（`0.0.0.0/0`）を即時に検知・通知する仕組みを構築したい。正しい連携の流れはどれか。

- [ ] A. CloudTrail → S3 → Athena でバッチ集計
- [x] B. CloudTrail → CloudWatch Logs → メトリクスフィルター → アラーム → SNS
- [ ] C. Config ルール → ドリフト検出 → スタック再デプロイ
- [ ] D. VPC フローログ → Logs Insights → ダッシュボード

> **解説**: リアルタイム検知は CloudTrail を CloudWatch Logs に連携し、メトリクスフィルターで特定 API パターンを抽出してアラーム→SNS で即時通知する。S3+Athena はバッチ分析でリアルタイム性に欠ける。
> **出典**: [cloudtrail README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloudtrail-005
- type: single
- difficulty: medium
- domain: 4
- tags: [cloudtrail-events, multi-account]

AWS Organizations 配下の全メンバーアカウントの監査ログを単一バケットに集約したい。最も適した手段はどれか。

- [ ] A. 各アカウントで個別に証跡を作成し手動でコピーする
- [x] B. 管理アカウントで組織証跡（Organization Trail）を作成する
- [ ] C. データイベントを全アカウントで有効化する
- [ ] D. CloudTrail Lake を各アカウントで個別に作成する

> **解説**: 組織証跡を Organizations の管理アカウントで作成すると、全メンバーアカウントのイベントを単一バケットに自動集約できる。個別作成・手動コピーは運用負荷が高く漏れも生じやすい。
> **出典**: [cloudtrail README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## cloudtrail-006
- type: single
- difficulty: hard
- domain: 4
- tags: [cloudtrail-events]

ネットワークアクティビティイベントを有効化する際の正しい設定はどれか。

- [ ] A. 基本のイベントセレクターで `eventCategory = Management` を指定する
- [x] B. 高度なイベントセレクターで `eventCategory = NetworkActivity` と `eventSource` を指定する
- [ ] C. データイベントセレクターで S3 バケット ARN を指定する
- [ ] D. Config ルールで `vpc-flow-logs-enabled` を有効化する

> **解説**: ネットワークアクティビティイベントは高度なイベントセレクターで `eventCategory = NetworkActivity` と `eventSource`（例 `ec2.amazonaws.com`）を指定して有効化する。さらに `errorCode = VpceAccessDenied` と `vpcEndpointId` で特定エンドポイントの拒否のみ抽出可能。
> **出典**: [cloudtrail README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## cloudtrail-007
- type: single
- difficulty: medium
- domain: 3
- tags: [cloudtrail-events, route-table]

CloudTrail の守備範囲として正しいものはどれか。

- [ ] A. パケットの中身やトラフィック流量の記録
- [x] B. コントロールプレーンの API 操作監査
- [ ] C. インスタンス間のレイテンシ計測
- [ ] D. BGP セッションの状態監視

> **解説**: CloudTrail はコントロールプレーンの操作監査を担う。トラフィックの中身やフロー量は VPC フローログ/トラフィックミラーリング、レイテンシ計測や BGP 状態は CloudWatch メトリクスの領域。
> **出典**: [cloudtrail README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloudtrail-008
- type: single
- difficulty: medium
- domain: 4
- tags: [cloudtrail-events]

新規リージョンを追加した際も自動的に API 操作を記録対象に含めたい。設定はどれか。

- [ ] A. リージョンごとに単一リージョン証跡を都度作成する
- [x] B. マルチリージョン証跡を有効にする
- [ ] C. データイベントを有効化する
- [ ] D. イベント履歴の保持期間を延長する

> **解説**: マルチリージョン証跡を有効にすると、新規リージョン追加時も自動的に記録対象になる。単一リージョン証跡の都度作成は漏れの原因。イベント履歴の保持延長は別の話。
> **出典**: [cloudtrail README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## cloudtrail-009
- type: single
- difficulty: easy
- domain: 4
- tags: [cloudtrail-events, use-case-fit]

AWS Config と CloudTrail の役割分担として正しいものはどれか。

- [ ] A. Config は API コールを記録し、CloudTrail は構成状態を記録する
- [x] B. Config は構成の状態を記録し、CloudTrail は変更を行った API コールを記録する
- [ ] C. 両者ともトラフィックの中身を記録する
- [ ] D. 両者ともメトリクスのアラームを生成する

> **解説**: Config は「リソースが今どういう設定か・どう変化したか」を記録し、CloudTrail は「変更を行った API コール（誰が・いつ）」を記録する。両者は補完関係にある。
> **出典**: [cloudtrail README #5 他サービスとの連携](README.md#5-他サービスとの連携)

## cloudtrail-010
- type: multi
- difficulty: hard
- domain: 4
- tags: [cost, cloudtrail-events]

CloudTrail のコストについて正しいものを 2 つ選べ。

- [x] A. 管理イベントの 1 証跡コピー目は無料である
- [x] B. データイベントとネットワークアクティビティイベントは既定オフで追加課金される
- [ ] C. イベント履歴のコンソール閲覧（90 日）は課金される
- [ ] D. 管理イベントは常に全コピーが無料である
- [ ] E. マルチリージョン証跡を有効にすると別途リージョン数分の固定料金が発生する

> **解説**: 管理イベントは 1 コピー目が無料で、追加証跡コピーは課金。データイベント/ネットワークアクティビティイベントは既定オフ・追加課金。イベント履歴の 90 日閲覧は無料。マルチリージョン化自体に固定料金はない。
> **出典**: [cloudtrail README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## cloudtrail-011
- type: single
- difficulty: medium
- domain: 4
- tags: [cloudtrail-events, config-rules]

ネットワーク構成変更の追跡を目的とする場合、データイベントの扱いとして適切なのはどれか。

- [ ] A. ネットワーク構成変更はデータイベントに記録されるため必ず有効化する
- [x] B. ネットワーク構成変更の追跡には基本的に不要なので有効化しなくてよい
- [ ] C. データイベントなしでは SG 変更を記録できない
- [ ] D. データイベントを有効化しないとイベント履歴が見られない

> **解説**: データイベントは S3 オブジェクトや Lambda 実行などデータプレーン操作を記録し、高頻度・既定オフ・追加課金。ネットワーク構成変更（管理イベント）の追跡には基本不要で、有効化はコスト増を招くだけ。
> **出典**: [cloudtrail README #2 コアコンセプト](README.md#2-コアコンセプト)
