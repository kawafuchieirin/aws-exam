# AWS Shield の要点

> 重要度: ○ ／ ANS-C01 第4分野。DDoS 保護（L3/L4/L7）の Standard と Advanced の違い・保護対象が頻出。

## これは何
- **DDoS 攻撃から AWS リソースを保護**するサービス。ネットワーク/トランスポート層（L3/L4）とアプリ層（L7）に対応。
- **Standard**（全ユーザー無料・自動適用）と **Advanced**（有料・高度保護＋SRT 支援＋コスト保護）の2階層。

## 試験頻出ポイント
- **Standard は L3/L4 を無料・常時オンで自動緩和**。申し込み不要。
- **Advanced は L3/L4/L7 を保護**。L7 緩和は **WAF が前提**（Advanced が WAF の自動緩和ルールを生成）。
- **Advanced の保護対象（暗記）**: **CloudFront** / **Route 53 ホストゾーン** / **Global Accelerator（standard）** / **ELB（ALB・NLB・CLB）** / **EC2 の Elastic IP**。
- **DDoS コスト保護**: 攻撃起因のオートスケール/データ転送の課金急増分を**クレジットで補償**（Advanced 限定）。「攻撃時の予期せぬ課金を防ぐ」→ Advanced。
- **SRT（Shield Response Team、旧 DRT）**: Advanced 加入者が攻撃時にプロアクティブ支援を依頼できる専門チーム。
- **Firewall Manager** で組織全アカウントを Advanced に一括サブスク・新規アカウント自動加入。
- **ヘルスベース検出**: Route 53 ヘルスチェックと連携し検出精度を向上。
- **Global Accelerator を前段**に置くと固定エニーキャスト IP ＋ Shield で大規模 L3/L4 攻撃を吸収しやすい。

## Standard vs Advanced
| 観点 | Standard | Advanced |
|---|---|---|
| 対象レイヤー | L3 / L4 | L3 / L4 / **L7** |
| コスト | **無料**（全 AWS 利用に自動付帯） | 有料（固定サブスク＋データ転送従量） |
| 申し込み | 不要・常時オン | 明示的なサブスクが必要 |
| L7 緩和 | なし | あり（**WAF 連携**が前提） |
| SRT 支援 | なし | あり |
| DDoS コスト保護 | なし | あり（クレジット補償） |
| FMS 一括適用 | — | あり |

## よく問われる上限・注意点（ひっかけ）
- **S3 / RDS は Advanced の保護対象ではない**（保護対象タイプは限定列挙）。
- **L7 緩和を Standard で実現できない**。Standard は L3/L4 のみ → L7 は Advanced ＋ [WAF](waf.md)。
- **Advanced の料金は固定サブスク（組織単位・1年コミット）＋データ転送従量**。「攻撃時のみ課金」「完全無料」は誤り。
- **SCP は Advanced をサブスクしない**。組織一括サブスク・自動加入は [Firewall Manager](firewall-manager.md)。
- SRT は **Advanced 限定**。Standard では利用不可。
- Global Accelerator は **standard accelerator** が保護対象（custom routing ではない点に注意）。
