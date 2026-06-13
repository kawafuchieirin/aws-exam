# AWS Site-to-Site VPN の要点

> 重要度: ◎ ／ ANS-C01 第1分野（ハイブリッド接続）の最頻出。冗長トンネル・ECMP・Accelerated VPN・VGW vs TGW が定番。

## これは何
- オンプレと VPC を**インターネット経由の IPsec 暗号化トンネル**で接続するサービス。
- 1接続に**冗長のため自動で2本のトンネル**を内包し、別々の AWS 側エンドポイントに終端。
- [Direct Connect](direct-connect.md) より安価・即時開通だが、インターネット品質に依存。DX のバックアップとして頻出。

## 試験頻出ポイント
- **2トンネル冗長**: 各トンネルは別 AWS エンドポイントに終端。高可用には**CGW 側で両トンネルを設定**するのが前提。
- **静的 vs 動的(BGP)**: 静的は手動・BGP 不要だが**ECMP 不可**。動的は BGP 必須で自動フェイルオーバ・**ECMP 可**。可能なら BGP 推奨。
- **VGW 終端 vs TGW 終端**: VGW は**単一 VPC のみ**。TGW は多数 VPC ハブで **ECMP / Accelerated VPN / Private IP VPN over DX / IPv6** を解放。
- **ECMP（帯域集約）**: 標準トンネルの上限を超えるには**複数 VPN 接続を ECMP で束ねる**。要件は **TGW で「VPN ECMP support」有効化＋動的ルーティング(BGP)**。約 1.25 Gbps × 接続数。
- **Accelerated VPN**: **AWS グローバルネットワーク(Global Accelerator 基盤)** 経由でインターネット混雑を回避しレイテンシ改善。**TGW 終端のみ**、アクセラレータ2基を自動管理（追加課金）。
- **VPN CloudHub**: **単一 VGW に複数 CGW(拠点)を BGP 接続**し、拠点間を AWS 経由でハブ＆スポーク疎通。各拠点は**異なる ASN** を使用。
- **Private IP VPN over DX**: DX の **Transit VIF 上にプライベート IP で IPsec**。インターネット非経由で暗号化＋プライベート。**TGW 終端**。
- **Large Bandwidth Tunnel**: 1トンネルで最大 **5 Gbps / 400,000 pps**（TGW / Cloud WAN 終端）。

## 比較・選択の判断
| 要件 | 解答 |
|---|---|
| 単一 VPC へ手軽に暗号化接続 | VGW 終端 |
| 多数 VPC 集約・帯域集約・高速化 | **TGW 終端** |
| 標準トンネル上限超の帯域が必要 | **複数 VPN を TGW＋BGP で ECMP 束ね** |
| インターネット混雑を回避し低遅延化 | **Accelerated VPN（TGW のみ）** |
| 拠点同士を AWS 経由でメッシュ接続 | **VPN CloudHub（VGW、各拠点別 ASN）** |
| DX 上をインターネット非経由で暗号化 | **Private IP VPN over DX（TGW）** |
| BGP 非対応の CGW 機器 | 静的ルーティング |
| DX プライマリ＋安価なバックアップ | DX＋Site-to-Site VPN（TGW で DX 伝播優先） |

## よく問われる上限・注意点（ひっかけ）
- **トンネルは常に2本**。終端の種類に関係なく増減しない（「4本にする」は誤答）。
- **ECMP は静的では不可・VGW では不可**。TGW＋動的(BGP) が必須。
- **Accelerated / Private IP VPN over DX / IPv6 は VGW 不可**、TGW 終端のみ。
- 標準トンネル帯域は**最大 1.25 Gbps / 140,000 pps**。トンネルを増やすのではなく接続を束ねる。
- **MTU 1446 バイト（MSS 1406）**。**ジャンボフレーム非対応・PMTUD 非対応** → **MSS クランプ必須**（MTU 9001 は誤答）。
- **IPv6 は TGW / Cloud WAN のみ**。1接続で IPv4 と IPv6 を**同時利用不可**。
- **CGW ASN は 2-byte（1〜65535）**、VGW ASN は 4-byte（1〜2147483647）。
- **DX 優先**: TGW ルート評価で **DX 伝播 > VPN 伝播**。同一プレフィックス広告時は DX 正常なら DX のみ採用、DX 断で VPN へ自動切替。
- **コスト**: ①VPN 接続時間課金（プロビジョニング中ずっと課金）＋②データ転送。Accelerated は**アクセラレータ2基分**が追加。
- 上限: VPN 接続/リージョン=50、VPN 接続/VGW=10、Accelerated VPN/リージョン=10。
