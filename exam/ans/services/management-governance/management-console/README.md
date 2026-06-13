# AWS Management Console（ネットワーク観点）

> カテゴリ: マネジメントとガバナンス / 重要度: △
> 最終更新: 2026-05-24

---

## 1. 概要

AWS Management Console は、ブラウザから AWS サービスを操作する GUI。ネットワーク運用では、VPC・サブネット・ルートテーブル・SG/NACL の設定や、**Reachability Analyzer / Network Access Analyzer / フローログ**等の可視化ツールを対話的に扱う入口となる。手動操作のため再現性は IaC（CloudFormation）に劣るが、構成の確認・トラブルシュート・可視化には有用。

ネットワーク観点で押さえるべきは、**コンソールへのアクセス自体をネットワーク的に保護**できる点である。社内からのアクセスに限定したい場合、IAM の `aws:SourceIp` 条件や、AWS が提供する**コンソールへのインターフェイス VPC エンドポイント／プライベート接続**を組み合わせ、インターネットを経由しない管理アクセス経路を設計できる。なお、コンソールで実行した操作も裏では API コールであり、**CloudTrail の管理イベント**としてすべて記録される（[CloudTrail](../cloudtrail/README.md)）。

---

## 2. 出典

- [AWS Management Console – AWS Docs](https://docs.aws.amazon.com/awsconsolehelpdocs/latest/gsg/getting-started.html)
