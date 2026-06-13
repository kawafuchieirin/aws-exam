# AWS CLI（ネットワーク自動化観点）

> カテゴリ: マネジメントとガバナンス / 重要度: △
> 最終更新: 2026-05-24

---

## 1. 概要

AWS CLI は AWS API をコマンドラインから呼び出すツール。ネットワーク観点では、VPC・SG・ルートテーブル・TGW・VPN 等の**命令的（imperative）な作成・変更・調査の自動化**に使う。宣言的な IaC（CloudFormation/Terraform）と対比される位置づけで問われる。

---

## 2. ネットワーク運用での使いどころ

| 用途 | 代表コマンド例 |
|---|---|
| トラブルシュート/調査 | `aws ec2 describe-security-groups`、`describe-route-tables`、`describe-network-interfaces` |
| 到達性解析の自動化 | `aws ec2 create-network-insights-path` / `start-network-insights-analysis`（Reachability Analyzer） |
| フローログ操作 | `aws ec2 create-flow-logs` |
| CloudTrail 設定 | `aws cloudtrail put-event-selectors`（ネットワークアクティビティイベント有効化） |
| ハイブリッド接続 | `aws directconnect describe-connections`、`aws ec2 describe-vpn-connections` |

---

## 3. 試験頻出ポイント

- **命令的 CLI/SDK vs 宣言的 IaC**: 一度きりの調査・緊急対応・スクリプト的処理は CLI、再現性ある環境構築は **CloudFormation 等の IaC**。
- フローログ・到達性解析・CloudTrail セレクター等、**コンソールで設定する内容は CLI/SDK でも自動化可能**。
- 認証情報はハードコードせず、**IAM ロール（EC2/インスタンスプロファイル）や名前付きプロファイル**を使う。
- ページネーション・`--query`（JMESPath）で大量のネットワークリソースを抽出・整形できる。

---

## 4. 他サービスとの連携

- **CloudFormation**: 宣言的 IaC との使い分け（[CloudFormation](../cloudformation/README.md)）。
- **VPC / TGW / Direct Connect**: 操作対象（[VPC](../../networking-content-delivery/vpc/README.md)）。

---

## 5. 制約・コスト

- CLI 自体は無料。API 呼び出しに伴う各サービスの料金のみ。API スロットリングに留意。

---

## 6. 出典

- [AWS CLI User Guide – AWS Docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [AWS CLI ec2 reference – AWS Docs](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/index.html)
