# AWS CloudFormation（ネットワーク IaC 観点）

> カテゴリ: マネジメントとガバナンス / 重要度: △
> 最終更新: 2026-05-24

---

## 1. 概要

AWS CloudFormation は、テンプレート（JSON/YAML）で AWS リソースを**宣言的にプロビジョニング**する IaC サービス。ネットワーク観点では、VPC・サブネット・ルートテーブル・SG・TGW・VPN・エンドポイント等を**再現性をもって一括構築**し、ドリフトを検出する用途が問われる。

---

## 2. コアコンセプト

| 要素 | 役割 | ネットワーク観点 |
|---|---|---|
| **テンプレート** | リソース定義（宣言的） | VPC/サブネット/RT/SG/TGW を一括定義 |
| **スタック** | テンプレートから作られるリソース群 | ネットワーク基盤を単位として管理 |
| **スタックセット** | 複数アカウント/リージョンへ展開 | 標準ネットワーク基盤をマルチアカウント配布 |
| **クロススタック参照（Export/ImportValue）** | スタック間で値共有 | ネットワークスタックの VPC ID/サブネット ID をアプリスタックへ渡す |
| **ドリフト検出** | 実構成とテンプレートの差分検出 | 手動変更された SG ルールやルートの検出 |

---

## 3. 試験頻出ポイント

- **宣言的 IaC**: 再現性・バージョン管理・レビュー可能性が利点。命令的な CLI/SDK と対比（[AWS CLI](../aws-cli/README.md)）。
- **ネットワーク基盤の階層化**: VPC・サブネット等の「ネットワークスタック」を分離し、`Export`/`Fn::ImportValue` でアプリ層へ ID を渡すのが定石。
- **ドリフト検出**: コンソールやコマンドで手動変更（野良 SG ルール、ルート改ざん）を発見。Config の継続監査と補完関係。
- **スタックセット**で組織横断の標準ネットワーク（フローログ有効化、標準 SG 等）を一括展開。
- 依存関係（`DependsOn`、`!Ref`/`!GetAtt`）で IGW アタッチ→ルート作成の順序を制御。

---

## 4. 他サービスとの連携

- **Organizations / Control Tower**: スタックセットや Account Factory で標準ネットワークを展開（[Organizations](../organizations/README.md)）。
- **Config**: ドリフト/準拠の補完（[Config](../config/README.md)）。
- **VPC / TGW**: 構築対象（[VPC](../../networking-content-delivery/vpc/README.md)）。

---

## 5. 制約・コスト

- CloudFormation 自体は無料（サードパーティ拡張除く）。作成されるリソースの料金のみ。

---

## 6. 出典

- [What is AWS CloudFormation? – AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [Detecting unmanaged configuration changes (drift) – AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)
