# AWS WAF の要点

> 重要度: ○ ／ ANS-C01 第4分野。L7（アプリ層）の保護サービス。適用先のスコープ（CloudFront=Global / その他=Regional）が即答ポイント。

## これは何
- HTTP/HTTPS リクエストを監視・制御する **L7 Web アプリケーションファイアウォール**。
- `Web ACL` にルールを定義し、リクエストを **Allow / Block / Count / CAPTCHA / Challenge** で処理する。
- SQLi・XSS・レート制限・地理ブロック・マネージドルール・Bot Control に対応。

## 試験頻出ポイント
- **適用先**: **CloudFront / ALB / API Gateway(REST) / AppSync / Cognito / App Runner / Verified Access / Amplify**。NLB(L4) や Elastic IP は不可。
- **スコープ**: **CloudFront＝CLOUDFRONT（Global、us-east-1 で作成）**、ALB/API GW/AppSync＝**REGIONAL（リソースと同一リージョン）**。
- **API Gateway は REST API に直接適用可。HTTP API は直接非対応** → 前段に CloudFront を置いて保護。
- **レートベースルール**が L7 HTTP flood の主要対策（5分/1分の閾値超過 IP をブロック）。
- **Count** はマッチしてもブロックせずメトリクス記録のみ。本番投入前の誤検知検証に使い、その後 **Block** へ切替がベストプラクティス。
- **マネージドルールグループ**（OWASP系・Bad Inputs・Bot Control）で既知脆弱性を即時カバー、誤検知は**除外ルール**で調整。
- ルールは**優先順位の昇順**で評価され、Allow/Block の**終端アクションで確定**（Count は継続）。
- **WAF ログ配信先**: **CloudWatch Logs / S3 / Kinesis Data Firehose**（フィールド編集・フィルタ可）。
- **WCU（Web ACL Capacity Unit）**: ルールの計算コスト指標。Web ACL あたり既定上限 **1,500**（引き上げ可）。
- **Shield Advanced** と統合し自動 L7 DDoS 緩和ルールを生成、SRT が WAF ルール調整を支援。
- **Firewall Manager** で Organizations 横断に Web ACL を一元適用・新規リソースへ自動付与。

## Shield/Network Firewallとの違い
| 観点 | 解答 |
|---|---|
| WAF | **L7**（HTTP リクエストの内容）を検査。SQLi/XSS/レート/Bot |
| [Shield](shield.md) | **L3/L4 のボリューム型 DDoS** 緩和。Advanced は WAF 統合で L7 も |
| Network Firewall | **VPC のネットワーク境界**でのトラフィック検査・フィルタ |

## よく問われる上限・注意点（ひっかけ）
- CloudFront 用 Web ACL を **REGIONAL で作る**のは誤り → **CLOUDFRONT スコープ・us-east-1** が正。
- **NLB は WAF 非対応**（L4）。Elastic IP も不可。
- **HTTP API への直接アタッチは不可**（REST API は可）。
- ルール評価は**降順ではなく昇順**。Count は終端アクションではない。
- 課金は **Web ACL 月額＋ルール数＋処理リクエスト数**。Bot Control / Fraud Control は**追加料金**。
- 高 WCU のマネージドルールを盛りすぎない（WCU 上限・コスト両面で注意）。
