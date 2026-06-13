---
service: waf
domain_default: 4
source: README.md
source_sha256: 0ab4addd11f7d94d95cb337ff6145012741ac3a1104ea7d7f062276abe92ae54
generated: 2026-05-24
---

## waf-001
- type: single
- difficulty: medium
- domain: 4
- tags: [waf, route-table, edge-caching]

CloudFront ディストリビューションに WAF を適用する場合のスコープと作成リージョンについて正しいものはどれか。

- [ ] A. REGIONAL スコープで CloudFront と同一リージョン
- [x] B. CLOUDFRONT スコープで us-east-1（グローバル）に作成する
- [ ] C. REGIONAL スコープで us-east-1
- [ ] D. スコープは不要でどのリージョンでもよい

> **解説**: CloudFront 用の Web ACL は CLOUDFRONT スコープ（グローバル、us-east-1 で作成）。ALB/API Gateway/AppSync などは REGIONAL スコープでリソースと同一リージョンに作成する。
> **出典**: [waf README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## waf-002
- type: multi
- difficulty: medium
- domain: 4
- tags: [waf, firewall-manager]

AWS WAF の Web ACL を直接関連付けて保護できるリソースはどれか。3つ選べ。

- [x] A. Amazon CloudFront
- [x] B. Application Load Balancer（ALB）
- [x] C. Amazon API Gateway（REST API）
- [ ] D. Network Load Balancer（NLB）
- [ ] E. EC2 の Elastic IP

> **解説**: WAF の適用先は CloudFront / ALB / API Gateway(REST) / AppSync / Cognito / App Runner / Verified Access / Amplify。NLB（L4）や Elastic IP は WAF（L7）の適用先ではない。
> **出典**: [waf README #1 概要](README.md#1-概要)

## waf-003
- type: single
- difficulty: medium
- domain: 4
- tags: [waf, shield]

L7 の HTTP flood 攻撃に対する主要な対策ルールはどれか。

- [ ] A. 地理マッチルール
- [x] B. レートベースルール（一定時間の閾値超過 IP をブロック）
- [ ] C. SQLi ルール
- [ ] D. IP セットルール

> **解説**: レートベースルールは5分間（または1分）の閾値を超えた IP をブロックし、L7 flood/DDoS の主要対策となる。地理マッチや SQLi は別目的。
> **出典**: [waf README #2 主なルールタイプ](README.md#主なルールタイプ)

## waf-004
- type: single
- difficulty: medium
- domain: 3
- tags: [waf, quotas, well-architected]

新しいルールを本番投入する前に、誤検知の有無を安全に検証したい。WAF のどのアクションを使うか。

- [ ] A. Block
- [ ] B. Allow
- [x] C. Count
- [ ] D. CAPTCHA

> **解説**: Count はマッチしてもブロックせずメトリクスを記録するだけのアクションで、挙動を検証してから Block に切り替えるのがベストプラクティス。
> **出典**: [waf README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## waf-005
- type: single
- difficulty: hard
- domain: 4
- tags: [waf, api-endpoint]

API Gateway の HTTP API を WAF で保護したい。正しい説明はどれか。

- [ ] A. HTTP API に WAF を直接関連付けできる
- [x] B. WAF は REST API に適用可で、HTTP API は直接非対応のため CloudFront 経由などで対応する
- [ ] C. HTTP API は WAF 非対応なので保護できない
- [ ] D. HTTP API は Shield でのみ保護できる

> **解説**: WAF は API Gateway の REST API に適用できるが、HTTP API は直接非対応。前段に CloudFront を置くなどして保護する。
> **出典**: [waf README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## waf-006
- type: single
- difficulty: medium
- domain: 4
- tags: [waf, network-firewall]

Web ACL 内のルール評価順序について正しいものはどれか。

- [ ] A. 優先順位の降順で評価される
- [x] B. 優先順位の昇順で評価され、終端アクション（Allow/Block）で確定する
- [ ] C. ランダムな順序で評価される
- [ ] D. すべてのルールを評価してから多数決で決まる

> **解説**: Web ACL 内のルールは優先順位の昇順で評価され、Allow/Block の終端アクションで確定する。Count はマッチしても評価を継続する。
> **出典**: [waf README #3 アーキテクチャ / 仕組み](README.md#3-アーキテクチャ--仕組み)

## waf-007
- type: single
- difficulty: hard
- domain: 4
- tags: [waf, security-group]

WAF・Shield・Network Firewall の責務分担について正しいものはどれか。

- [ ] A. WAF が L3/L4 のボリューム攻撃を担当する
- [x] B. WAF は L7 のリクエスト内容、L3/L4 ボリューム攻撃は Shield、ネットワーク境界は Network Firewall が担当
- [ ] C. Network Firewall が L7 の HTTP 検査を担当する
- [ ] D. Shield が HTTP リクエストの内容を検査する

> **解説**: WAF はリクエスト内容（L7）を見る。L3/L4 のボリューム攻撃は Shield、VPC のネットワーク境界での検査は Network Firewall の領域。
> **出典**: [waf README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## waf-008
- type: single
- difficulty: medium
- domain: 4
- tags: [waf, shield]

Shield Advanced と WAF の関係について正しいものはどれか。

- [ ] A. WAF は Shield Advanced を内包し別途不要
- [x] B. Shield Advanced は WAF と統合し自動 L7 DDoS 緩和ルールを生成、SRT が WAF ルールを支援する
- [ ] C. WAF と Shield Advanced は併用できない
- [ ] D. Shield Advanced は WAF のログを生成するだけ

> **解説**: Shield Advanced は WAF と統合して自動 L7 DDoS 緩和ルールを生成し、SRT が WAF ルールの調整を支援する。
> **出典**: [waf README #5 他サービスとの連携](README.md#5-他サービスとの連携)

## waf-009
- type: single
- difficulty: medium
- domain: 3
- tags: [waf, monitoring]

WAF のログ配信先として正しいものはどれか。

- [ ] A. SNS トピックのみ
- [x] B. CloudWatch Logs / S3 / Kinesis Data Firehose
- [ ] C. EBS ボリュームのみ
- [ ] D. ログは出力できない

> **解説**: WAF ログは CloudWatch Logs / S3 / Kinesis Data Firehose に配信でき、フィールドの編集やフィルタも可能。
> **出典**: [waf README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)

## waf-010
- type: single
- difficulty: hard
- domain: 4
- tags: [waf, quotas, cost]

WCU（Web ACL Capacity Unit）について正しいものはどれか。

- [ ] A. 処理リクエスト数の単位である
- [x] B. ルールの計算コスト指標で、Web ACL あたりに既定上限（既定 1,500、引き上げ可）がある
- [ ] C. ログ保存量の単位である
- [ ] D. Web ACL の関連付け先リソース数の上限である

> **解説**: WCU はルールの計算コスト指標で、Web ACL あたり既定上限（既定 1,500、引き上げ可）がある。高 WCU のマネージドルールを盛りすぎないことがコスト最適化につながる。
> **出典**: [waf README #6 制約・上限・コスト](README.md#6-制約上限コスト)

## waf-011
- type: single
- difficulty: medium
- domain: 4
- tags: [waf]

既知の一般的な脆弱性（OWASP 系）を即時にカバーしたい。最も適切な方法はどれか。

- [ ] A. すべてのルールを自作する
- [x] B. AWS マネージドルールグループを適用し、誤検知は除外ルールで調整する
- [ ] C. Count モードだけで運用する
- [ ] D. 地理マッチで全リージョンを許可する

> **解説**: マネージドルールグループで既知脆弱性を即時カバーでき、誤検知が出れば除外ルールで調整する。Bot Control や Fraud Control など一部は追加料金がかかる。
> **出典**: [waf README #4 試験頻出ポイント](README.md#4-試験頻出ポイント)
