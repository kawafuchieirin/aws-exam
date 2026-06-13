# Elastic Load Balancing の要点

> 重要度: ◎ ／ 4種（ALB/NLB/GWLB/CLB）の使い分けとクロスゾーン・送信元IP保持・TLS挙動は ANS-C01 最頻出。

## これは何
- 受信トラフィックを複数AZの複数ターゲット（EC2/IP/Lambda/コンテナ/仮想アプライアンス）へ自動分散するマネージドLB。
- ヘルスチェックで健全なターゲットのみへルーティングし、需要に応じ自動スケール。
- 種別は **ALB（L7）/ NLB（L4）/ GWLB（L3+GENEVE）/ CLB（旧世代）** の4つ。

## 試験頻出ポイント
- **使い分け**: HTTPヘッダ/パス/ホストルーティング・**WAF**連携→**ALB**。静的IP(EIP)/UDP/超低レイテンシ/送信元IP保持→**NLB**。FW/IDS/IPS等の**仮想アプライアンスを透過挿入**→**GWLB**（GENEVE 6081）。
- **クロスゾーン負荷分散デフォルト**: **ALB=常時ON（LBレベルで無効化不可、TG単位でのみOFF可）**、**NLB/GWLB=OFF**、CLB=コンソールON/API・CLIはOFF。
- **送信元IP保持**: NLB は instance/ip ターゲットで**クライアントIPを透過**。ALB/CLB は保持せず **X-Forwarded-For** で伝達。
- **静的IP/EIP**: **NLB のみ**AZごとに関連付け可。ALB は DNS名のみ。
- **ターゲットタイプの限定**: **lambda は ALB のみ**、**alb ターゲット（NLB背後にALB）は NLB のみ**。
- **WAF直接連携は ALB のみ**（NLB/GWLB/CLB 不可）。
- **TLS終端 vs パススルー**: ALB の HTTPS・NLB の TLS リスナー＝LBで終端。**NLB の TCP リスナー＝パススルー（ターゲットが復号）**でエンドツーエンド暗号化/相互TLS。
- **Proxy Protocol v2**: NLB/CLB で有効化。**PrivateLinkエンドポイント経由やALBターゲット**で実IPがNLBノードIPに化ける場合に、実IP・ポート（PrivateLinkならEndpoint ID）を付与。
- **SNI**: 1つの HTTPS/TLS リスナーに複数証明書を載せ ClientHello で選択（マルチテナント）。証明書は **ACM** で発行・自動更新。
- **AWS Load Balancer Controller（EKS）**: Ingress→ALB、Service(type:LoadBalancer)→NLB を自動生成。**IPモード**は Pod IP を直接登録（VPC CNI 前提）で instance モードより低レイテンシ。IngressGroup で複数Ingressを1ALBに集約。
- **SG**: ALB/NLB は付与可、**GWLB は不可**。

## ALB / NLB / GWLB 比較
| 観点 | ALB | NLB | GWLB |
|---|---|---|---|
| OSI層 | L7（アプリ） | L4（トランスポート） | L3 + GENEVE |
| プロトコル | HTTP/HTTPS（gRPC/WebSocket） | TCP/UDP/TCP_UDP/TLS | IP（GENEVE 6081） |
| 主用途 | Webアプリ・コンテンツルーティング | 超低レイテンシ・高スループット・静的IP | FW/IDS/IPS等の仮想アプライアンス連携 |
| ターゲット | instance/ip/lambda/alb | instance/ip/alb | instance/ip |
| 静的IP/EIP | なし | **AZごとに可** | なし |
| 送信元IP保持 | しない（XFF） | **保持** | 保持（GENEVE） |
| TLS | 終端可 | 終端/パススルー両対応 | - |
| クロスゾーン既定 | **常時ON** | **OFF** | **OFF** |
| WAF連携 | **可** | 不可 | 不可 |
| SG | 可 | 可 | 不可 |
| MTU | 9001 | 9001 | **8500** |

## よく問われる上限・注意点（ひっかけ）
- **NLBクロスゾーンON時のみ AZ間データ転送 $0.01/GB が発生**。ALB/CLB は同シナリオ非課金（「コスト最小でクロスゾーン分散」の引っかけ）。
- **NLBで負荷が偏る** → クロスゾーンが**デフォルトOFF**で各ノードが自AZ内のみへ分散するため。ON にするか各AZのターゲット数を揃える。
- ALB のクロスゾーンは「OFFにできる」と思わせるが **LBレベルでは無効化不可**（TG単位でのみOFF）。
- **ALB は最低2 AZ 必須**。NLB は静的IPを持てるがALBは持てない（ALBにEIPを付ける選択肢は誤り）。
- ACM証明書は ELB/CloudFront/API Gateway で利用可だが **EC2へエクスポート不可**。
- 主な上限（既定）: ALB/NLB 50/リージョン、ALBルール 100/LB、ALBターゲット 1,000/LB、NLBターゲット 500/AZ、SNI証明書 25/リスナー。
- 課金は LB時間 + **LCU(ALB)/NLCU(NLB)/GLCU(GWLB)**。
- 静的IP+L7+WAF両立の定番は **NLB（前段・静的IP）→ ターゲットをALB** にする構成。

関連: [VPC](vpc.md) ／ [Route 53](route-53.md) ／ [PrivateLink](privatelink.md) ／ [Global Accelerator](global-accelerator.md)
