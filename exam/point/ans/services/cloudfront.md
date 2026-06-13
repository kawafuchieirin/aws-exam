# Amazon CloudFront の要点

> 重要度: ○ ／ L7 のエッジキャッシュ＋セキュア配信。[Global Accelerator](global-accelerator.md) との使い分けが最頻出。

## これは何
- AWS グローバルの**エッジロケーション（POP）／リージョナルエッジキャッシュ**で静的・動的コンテンツを低レイテンシ配信する CDN。
- ビューワーを最寄り POP へルーティングし、ヒットなら即応答、ミスならオリジン（S3/カスタム/ALB/VPC オリジン）から取得してキャッシュ。
- TLS 終端・WAF 評価・署名検証・エッジ関数はすべて **POP** で実行。

## 試験頻出ポイント
- **オリジン保護は OAC 一択**（OAI はレガシー）。OAC は **SigV4 署名**・**SSE-KMS 対応**・**PUT/DELETE 対応**・全リージョン対応。OAI は非対応が多い。
- **S3 静的ウェブサイトエンドポイントは OAC/OAI 非対応**（カスタムオリジン扱い）。REST API エンドポイントなら OAC 可。
- OAC は S3 バケットポリシーで **`cloudfront.amazonaws.com`＋`AWS:SourceArn`** で特定ディストリビューションに限定。Object Ownership は **Bucket owner enforced（ACL 無効）**。
- **CloudFront Functions**: JS(ES5.1)・サブミリ秒・毎秒数百万・**Viewer Request/Response のみ**・ネットワーク不可。→ キャッシュキー正規化/ヘッダ操作/URL リライト/軽量トークン検証。
- **Lambda@Edge**: Node/Python・最大30秒・**Origin Request/Response も可**・**ネットワークアクセス可**・リクエストボディ参照可。→ 外部API/AWS SDK・オリジン選択・SSR。
- **Origin Groups**: プライマリ＋セカンダリの**2オリジン**でフェイルオーバー。対象メソッドは **GET/HEAD/OPTIONS のみ**。
- フェイルオーバー対象ステータス（選択式）: **400/403/404/416/429/500/502/503/504**。
- **署名付き URL**=個別ファイル。**署名付き Cookie**=複数ファイル（HLS 等）に URL を変えず一括制御。署名者は**トラステッドキーグループ推奨**。
- **WAF（CloudFront 用）は `us-east-1` の CLOUDFRONT スコープ**に作成。SQLi/XSS/レート/地理ブロックをエッジで評価。
- **証明書は ACM の `us-east-1`** で発行（CloudFront はグローバルだが証明書はバージニア北部）。
- **SNI は既定・無料**。SNI 非対応の旧クライアント用に**専用 IP(Dedicated IP) SSL は月額課金**。
- **Field-Level Encryption(FLE)**: 特定フィールド（PII/カード番号）をエッジで公開鍵暗号化しオリジンまで保持。最大10フィールド。
- **VPC オリジン**: プライベートサブネットの ALB/NLB/EC2 を非公開のまま配信。
- ログ: 標準ログ=S3/CloudWatch Logs/Data Firehose、**リアルタイムログ=Kinesis Data Streams**（即時分析向け）。
- **AWS オリジン→CloudFront 転送は無料**。Shield Standard は自動・無料。Price Class で配信範囲を絞りコスト最適化。

## 比較・選択の判断
| 要件 | 解答 |
|---|---|
| S3 を直接公開せず CloudFront 経由のみ（新規） | OAC |
| SSE-KMS 暗号化 S3 / PUT・DELETE | OAC（OAI 不可） |
| 超低遅延・毎秒数百万・Viewer での軽量処理 | CloudFront Functions |
| 外部API/SDK・ボディ参照・オリジン選択 | Lambda@Edge（Origin Request） |
| マルチリージョンのオリジン冗長化 | Origin Groups（プライマリ＋セカンダリ） |
| 個別ファイルへの限定配信 | 署名付き URL |
| 複数ファイル(HLS)を URL 不変で限定配信 | 署名付き Cookie |
| 機微フィールドをオリジンまで多重暗号化 | Field-Level Encryption |
| プライベート ALB/NLB を非公開配信 | VPC オリジン |
| 非HTTP(TCP/UDP)・固定IP・L4 高速フェイルオーバー | [Global Accelerator](global-accelerator.md) |
| ほぼリアルタイムなログ分析 | リアルタイムログ(Kinesis Data Streams) |

## よく問われる上限・注意点（ひっかけ）
- Origin Group は**2オリジン固定**（任意数を順に並べられない）。フェイルオーバー対象ステータスは**変更可能**（固定ではない）。
- **POST/PUT 等はフェイルオーバーしない**。OPTIONS をキャッシュ対象メソッドに含めないと OPTIONS もフェイルオーバーしない。
- Lambda@Edge を origin トリガーで使うとプライマリ・セカンダリ双方で**最大2回**発火しうる。
- WAF を「オリジンのリージョン」「主要視聴者のリージョン」に作るのは誤り。**必ず us-east-1（CLOUDFRONT）**。
- 証明書を東京等で発行するのは誤り。**ACM は us-east-1**。
- **SNI が無料、専用 IP が有料**（逆に問う設問に注意）。
- CloudFront のフェイルオーバーと **Route 53 ヘルスチェックの DNS フェイルオーバーは別物**。
- ビヘイビアの振り分けは最長一致でなく**評価順（優先度）で先頭一致**。
- Lambda@Edge スケールは **10,000 req/s/リージョン**。CloudFront Functions はメモリ 2MB・コード 10KB。デフォルト TTL は 24 時間。
