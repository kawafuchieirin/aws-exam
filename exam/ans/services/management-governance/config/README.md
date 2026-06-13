# AWS Config（ネットワーク準拠監査観点）

> カテゴリ: マネジメントとガバナンス / 重要度: △
> 最終更新: 2026-05-24

---

## 1. 概要

AWS Config は AWS リソースの**構成（設定状態）を継続的に記録・評価**し、コンプライアンスを判定するサービス。CloudTrail が「変更した API コール」を記録するのに対し、Config は「リソースが今どういう設定か・過去どう変化したか」を記録する。ネットワーク観点では **SG / NACL / ルートテーブル等の構成準拠監査**と、**Firewall Manager の前提**として問われる。

---

## 2. コアコンセプト

| 要素 | 役割 |
|---|---|
| **構成項目（Configuration Item）** | あるリソースの時点ごとの設定スナップショット |
| **構成履歴 / タイムライン** | リソースの変更履歴を時系列で追跡 |
| **Config ルール（マネージド/カスタム）** | 望ましい設定かを自動評価（準拠/非準拠） |
| **コンフォーマンスパック** | 関連ルール＋是正をまとめてデプロイ |
| **アグリゲーター** | 複数アカウント/リージョンの結果を集約（組織統合） |
| **修復（Remediation）** | SSM Automation で非準拠を自動是正 |

---

## 3. 仕組みとネットワーク準拠ルール

Config が SG/NACL 等の変更を検知 → ルールで評価 → 非準拠なら通知/自動修復、という流れ。

代表的なネットワーク関連マネージドルール:

| ルール | 検査内容 |
|---|---|
| `restricted-ssh` | SG が SSH(22) を `0.0.0.0/0`・`::/0` に開放していないか |
| `vpc-sg-open-only-to-authorized-ports` | `0.0.0.0/0` 開放の SG が許可ポートのみか |
| `vpc-sg-port-restriction-check` | 22/3389 等の制限ポートを全開放していないか |
| `vpc-default-security-group-closed` | デフォルト SG がトラフィックを許可していないか |
| `vpc-flow-logs-enabled` | VPC でフローログが有効か |
| `eip-attached` / `vpc-network-acl-unused-check` | 未使用 EIP・未使用 NACL の検出 |

---

## 4. 試験頻出ポイント

- **「設定が望ましい状態か」の継続監査は Config、「誰が変更したか」は CloudTrail**。両者は補完関係。
- SG/NACL の不適切な全開放（22/3389）の検出 → 該当マネージドルール＋ **SSM 自動修復**でポート閉塞。
- **AWS Firewall Manager の前提**として Config の有効化が必要。
- 組織アグリゲーターで全アカウントのネットワーク準拠状況を一元把握。

---

## 5. 他サービスとの連携

- **CloudTrail**: 変更の「実行者」を補完（[CloudTrail](../cloudtrail/README.md)）。
- **Organizations / Firewall Manager**: 組織集約・前提（[Organizations](../organizations/README.md)）。
- **Systems Manager Automation**: 非準拠の自動修復。
- **VPC**: 監査対象の SG/NACL/フローログは [VPC](../../networking-content-delivery/vpc/README.md)。

---

## 6. 制約・上限・コスト

- 課金は**記録された構成項目数**＋**ルール評価回数**＋コンフォーマンスパック評価に基づく。
- 記録対象リソースタイプは選択可能（全記録はコスト増）。

---

## 7. 出典

- [restricted-ssh – AWS Config Docs](https://docs.aws.amazon.com/config/latest/developerguide/restricted-ssh.html)
- [vpc-sg-open-only-to-authorized-ports – AWS Config Docs](https://docs.aws.amazon.com/config/latest/developerguide/vpc-sg-open-only-to-authorized-ports.html)
- [vpc-sg-port-restriction-check – AWS Config Docs](https://docs.aws.amazon.com/config/latest/developerguide/vpc-sg-port-restriction-check.html)
