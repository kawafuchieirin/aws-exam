# AWS Control Tower（ネットワーク観点）

> カテゴリ: マネジメントとガバナンス / 重要度: △
> 最終更新: 2026-05-24

---

## 1. 概要

AWS Control Tower は、ベストプラクティスに沿った**マルチアカウント環境（ランディングゾーン）を自動構築・運用**するサービス。Organizations・SCP・Config・CloudTrail を内部で組み合わせ、**ガードレール（コントロール）**でガバナンスを強制する。ネットワーク観点では、ランディングゾーン構築時の**ネットワーク基盤の標準化**と、ネットワーク変更を制限するガードレールが問われる。

---

## 2. コアコンセプト

| 要素 | 役割 |
|---|---|
| **ランディングゾーン** | 安全なマルチアカウントの初期構成（管理/ログアーカイブ/監査アカウント等） |
| **ガードレール（コントロール）** | 予防的（SCP）・発見的（Config ルール）・プロアクティブ（CloudFormation Hooks） |
| **Account Factory** | 標準化されたアカウントの払い出し（VPC 構成のカスタマイズ可） |

---

## 3. 仕組みとネットワークガードレール

- ランディングゾーンを敷くと、**ログアーカイブ／監査アカウント**が作られ、組織証跡や Config が自動構成される。
- **Account Factory** で新規アカウントを払い出す際、VPC の CIDR・サブネット・リージョンを標準化できる（不要なデフォルト VPC の削除等も可能）。
- ネットワーク関連のガードレール例:
  - 「インターネットゲートウェイの VPC へのアタッチを禁止」（予防的）
  - 「VPC フローログが有効かを検出」（発見的）
  - 「承認外リージョンの利用を禁止」

---

## 4. 試験頻出ポイント

- Control Tower は **Organizations + SCP + Config + CloudTrail のオーケストレーション**。ゼロから自前構築する代わりに標準化されたガバナンスを得る。
- **予防的ガードレール＝SCP**、**発見的ガードレール＝Config ルール**という対応を押さえる。
- Account Factory による VPC 標準化で、CIDR 重複や野良 VPC を防止。

---

## 5. 他サービスとの連携

- **Organizations / SCP**: 土台（[Organizations](../organizations/README.md)）。
- **Config / CloudTrail**: 発見的ガードレールと監査（[Config](../config/README.md) / [CloudTrail](../cloudtrail/README.md)）。
- **VPC**: Account Factory が払い出す基盤（[VPC](../../networking-content-delivery/vpc/README.md)）。

---

## 6. 制約・上限・コスト

- Control Tower 自体は無料。配下の Config・CloudTrail・S3 等の利用料が発生。

---

## 7. 出典

- [What is AWS Control Tower? – AWS Docs](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html)
- [Controls in AWS Control Tower – AWS Docs](https://docs.aws.amazon.com/controltower/latest/controlreference/controls.html)
