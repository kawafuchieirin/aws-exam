---
service: cloudformation
domain_default: 2
source: README.md
source_sha256: 371f4d1304471d168cf5a5de82ba6b94a20aa99cb5600231437d8228ac973f8a
generated: 2026-05-24
---

## cloudformation-001
- type: single
- difficulty: easy
- domain: 2
- tags: [iac]

CloudFormation を使ってネットワーク基盤を構築する利点として最も適切なのはどれか。

- [ ] A. 命令的にリソースを 1 つずつ手作業で作成できる
- [x] B. テンプレートによる宣言的プロビジョニングで再現性・バージョン管理・レビューが可能
- [ ] C. 設定変更を行った API コールの実行者を記録できる
- [ ] D. リアルタイムのトラフィック量を監視できる

> **解説**: CloudFormation はテンプレート（JSON/YAML）で宣言的にリソースを定義し、再現性・バージョン管理・レビュー可能性が利点。実行者の記録は CloudTrail、トラフィック監視は CloudWatch/フローログの領域。
> **出典**: [cloudformation README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## cloudformation-002
- type: single
- difficulty: medium
- domain: 2
- tags: [iac]

ネットワークスタックで作成した VPC ID やサブネット ID を、別のアプリケーションスタックへ渡したい。定石の手段はどれか。

- [ ] A. パラメータストアに手動でコピーする
- [x] B. `Export` した出力値を `Fn::ImportValue` で参照するクロススタック参照
- [ ] C. 同一テンプレート内に全リソースをまとめる
- [ ] D. CloudTrail のイベントから ID を取得する

> **解説**: ネットワーク基盤を「ネットワークスタック」として分離し、`Export`/`Fn::ImportValue`（クロススタック参照）で VPC ID やサブネット ID をアプリ層へ渡すのが定石。階層化により責務分離と再利用が可能になる。
> **出典**: [cloudformation README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## cloudformation-003
- type: single
- difficulty: medium
- domain: 3
- tags: [iac, automation]

CloudFormation で管理している SG に、誰かがコンソールから手動でルールを追加した。テンプレートとの差分を検出する機能はどれか。

- [ ] A. スタックセット
- [x] B. ドリフト検出
- [ ] C. クロススタック参照
- [ ] D. 変更セット（Change Set）

> **解説**: ドリフト検出は実際のリソース構成とテンプレート定義の差分を検出し、手動変更された SG ルールやルートを発見できる。変更セットは適用前のプレビュー、スタックセットは複数展開の機能。
> **出典**: [cloudformation README #2 コアコンセプト](README.md#2-コアコンセプト)

## cloudformation-004
- type: single
- difficulty: medium
- domain: 4
- tags: [iac, multi-account]

組織内の全アカウントへ、フローログ有効化と標準 SG を含むネットワーク基盤を一括展開したい。最も適した機能はどれか。

- [ ] A. クロススタック参照
- [x] B. スタックセット（StackSets）
- [ ] C. ドリフト検出
- [ ] D. 変更セット

> **解説**: スタックセットは複数アカウント/リージョンへテンプレートを展開でき、標準ネットワーク基盤（フローログ有効化、標準 SG 等）の組織横断配布に適する。他の機能は単一スタック内/単一展開向け。
> **出典**: [cloudformation README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## cloudformation-005
- type: single
- difficulty: hard
- domain: 2
- tags: [iac, message-queue]

IGW を VPC にアタッチしてからその IGW を指すルートを作成する、という順序を保証したい。CloudFormation での手段はどれか。

- [ ] A. スタックセットで分割展開する
- [x] B. `DependsOn` や `!Ref`/`!GetAtt` による依存関係で順序を制御する
- [ ] C. ドリフト検出で順序を補正する
- [ ] D. CloudTrail で順序を記録する

> **解説**: リソース間の作成順序は `DependsOn` の明示や `!Ref`/`!GetAtt` の参照による暗黙の依存で制御する。これにより IGW アタッチ→ルート作成の順序が保証される。ドリフト検出や CloudTrail は順序制御の機能ではない。
> **出典**: [cloudformation README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## cloudformation-006
- type: single
- difficulty: medium
- domain: 3
- tags: [config-rules, iac, use-case-fit]

CloudFormation のドリフト検出と AWS Config の関係として正しいものはどれか。

- [ ] A. ドリフト検出があれば Config は不要
- [x] B. ドリフト検出（スポット的差分）と Config の継続監査は補完関係にある
- [ ] C. Config がドリフト検出の前提として必須
- [ ] D. 両者は同一機能であり併用すると競合する

> **解説**: ドリフト検出はテンプレートとの差分を見つける手段で、Config は構成の継続的な監査を行う。両者は補完関係にあり、手動変更（野良 SG ルール、ルート改ざん）の発見を異なるアプローチで支える。
> **出典**: [cloudformation README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## cloudformation-007
- type: single
- difficulty: easy
- domain: 2
- tags: [iac]

CloudFormation の「スタック」を最もよく表すのはどれか。

- [ ] A. 複数アカウントへ展開する単位
- [x] B. テンプレートから作られるリソース群の管理単位
- [ ] C. リソースのある時点の設定スナップショット
- [ ] D. SSM Automation による自動修復の単位

> **解説**: スタックはテンプレートから作られるリソース群で、ネットワーク基盤を 1 つの単位として作成・更新・削除できる。複数展開はスタックセット、設定スナップショットは Config の構成項目。
> **出典**: [cloudformation README #2 コアコンセプト](README.md#2-コアコンセプト)

## cloudformation-008
- type: single
- difficulty: easy
- domain: 2
- tags: [cost]

CloudFormation のコストについて正しいものはどれか。

- [ ] A. スタック数に応じた月額固定料金が発生する
- [x] B. CloudFormation 自体は無料（サードパーティ拡張除く）で、作成されるリソースの料金のみ発生
- [ ] C. テンプレートのデプロイ 1 回ごとに課金される
- [ ] D. ドリフト検出の実行回数に応じて課金される

> **解説**: CloudFormation 自体は無料で（サードパーティ拡張は除く）、課金は作成されるリソースの利用料のみ。スタック数やデプロイ回数、ドリフト検出回数に対する料金はない。
> **出典**: [cloudformation README #5 制約・コスト](README.md#5-制約コスト)

## cloudformation-009
- type: multi
- difficulty: hard
- domain: 2
- tags: [security-group, use-case-fit]

CloudFormation でネットワーク基盤を扱う際のベストプラクティスを 2 つ選べ。

- [x] A. VPC・サブネット等を「ネットワークスタック」として分離する
- [x] B. ネットワークスタックの出力を `Export`/`Fn::ImportValue` でアプリ層へ渡す
- [ ] C. 全リソースを 1 つの巨大テンプレートに集約して依存を排除する
- [ ] D. 認証情報をテンプレートにハードコードして再利用する
- [ ] E. 手動変更を前提とし、ドリフト検出は無効にする

> **解説**: ネットワーク基盤の階層化（ネットワークスタックの分離）とクロススタック参照による ID の受け渡しが定石。巨大テンプレートへの集約は保守性を損ない、認証情報のハードコードやドリフト無効化はアンチパターン。
> **出典**: [cloudformation README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)

## cloudformation-010
- type: single
- difficulty: medium
- domain: 1
- tags: [iac, use-case-fit]

緊急の障害対応で SG ルールを一度だけ即座に変更したい。CloudFormation と比較して適した手段はどれか。

- [ ] A. テンプレートを更新してスタックを再デプロイする
- [x] B. AWS CLI で命令的に変更する
- [ ] C. スタックセットで全アカウントへ展開する
- [ ] D. ドリフト検出を実行する

> **解説**: 一度きりの緊急対応や即時変更は命令的な CLI/SDK が向く。CloudFormation は再現性ある反復構築に適し、緊急時にテンプレート更新→再デプロイは迂遠。なお恒久対応はテンプレートへの反映が望ましい。
> **出典**: [cloudformation README #3 試験頻出ポイント](README.md#3-試験頻出ポイント)
