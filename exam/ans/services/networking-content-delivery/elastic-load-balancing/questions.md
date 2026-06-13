---
service: elastic-load-balancing
domain_default: 1
source: README.md
source_sha256: 0810f6e6934d95aca1bd46aef80e08443ae262264860810084a23fa1f2e654f4
generated: 2026-05-24
---

## elastic-load-balancing-001
- type: single
- difficulty: medium
- domain: 1
- tags: [use-case-fit, gwlb]

サードパーティのファイアウォール/IDS アプライアンス群に、すべてのパケットを透過的に通して検査させたい。最も適切なロードバランサはどれか。

- [ ] A. ALB（HTTP ヘッダでルーティング）
- [ ] B. NLB（TCP/UDP パススルー）
- [x] C. GWLB（GENEVE 6081 で仮想アプライアンスへ）
- [ ] D. CLB（レガシー L4/L7）

> **解説**: GWLB は L3 で動作し、GENEVE（ポート 6081）で全パケットをカプセル化して仮想アプライアンス（FW/IDS/IPS）へ透過的に送る。集中型インスペクションの定番。ALB/NLB はアプライアンス挿入を目的としたカプセル化を行わない。CLB は新規採用しない。
> **出典**: [elastic-load-balancing README #3 ロードバランサ4種比較](README.md#3-ロードバランサ-4-種比較最重要)

## elastic-load-balancing-002
- type: single
- difficulty: medium
- domain: 1
- tags: [cross-zone, nlb, stateful-stateless]

NLB で AZ ごとのターゲット数が大きく異なる（AZ-a に 2 台、AZ-b に 8 台）。AZ-a のターゲットに負荷が偏っている。原因として正しいものはどれか。

- [ ] A. ALB と異なり NLB はヘルスチェックを行わないため
- [x] B. NLB のクロスゾーン負荷分散がデフォルトで OFF のため、各ノードが自 AZ 内のターゲットのみへ分散している
- [ ] C. NLB はスティッキーセッションが常時 ON のため
- [ ] D. NLB は最低 2 AZ を必須としないため

> **解説**: NLB はクロスゾーン負荷分散がデフォルト OFF。各 LB ノードは自 AZ 内のターゲットのみへ分散するため、AZ ごとのターゲット数が偏ると負荷も偏る（AZ-a は各 25%、AZ-b は各 6.25%）。クロスゾーンを ON にするか各 AZ のターゲット数を揃える。
> **出典**: [elastic-load-balancing README #5 クロスゾーン負荷分散](README.md#5-クロスゾーン負荷分散最頻出暗記必須)

## elastic-load-balancing-003
- type: single
- difficulty: hard
- domain: 1
- tags: [cross-zone, cost, data-transfer]

NLB のクロスゾーン負荷分散を ON にした場合のコスト面の注意点として正しいものはどれか。

- [ ] A. クロスゾーン ON でも追加課金は一切発生しない
- [x] B. AZ をまたぐ転送に対しデータ転送課金（$0.01/GB）が発生する
- [ ] C. LCU が NLCU の 2 倍になる
- [ ] D. NLB の時間課金が AZ 数に比例して増える

> **解説**: NLB はクロスゾーン ON 時に AZ 間データ転送 $0.01/GB が発生する。ALB/CLB は同シナリオで非課金。この差は「コスト最小でクロスゾーン分散」を問う設問の引っかけになる。
> **出典**: [elastic-load-balancing README #10 制約・上限・コスト](README.md#10-制約上限コスト)

## elastic-load-balancing-004
- type: single
- difficulty: medium
- domain: 1
- tags: [target-type, eni, alb]

Lambda 関数をロードバランサのターゲットとして登録できるのはどの種別か。

- [x] A. ALB のみ
- [ ] B. NLB のみ
- [ ] C. GWLB のみ
- [ ] D. ALB と NLB の両方

> **解説**: lambda ターゲットタイプは ALB のみ対応（サーバーレス Web の実現）。NLB のみが対応するのは alb ターゲット（NLB 背後に ALB を置く構成）。GWLB は GENEVE のみ。
> **出典**: [elastic-load-balancing README #4 ターゲットグループ](README.md#4-ターゲットグループ)

## elastic-load-balancing-005
- type: single
- difficulty: hard
- domain: 1
- tags: [nlb, use-case-fit]

ファイアウォールのホワイトリスト用に固定 IP（EIP）が必要だが、同時に L7 のパス/ホストルーティングと WAF も使いたい。最適な構成はどれか。

- [ ] A. ALB に EIP を関連付ける
- [ ] B. CLB に EIP を関連付け、ルールでルーティングする
- [x] C. NLB（静的 IP）を前段に置き、ターゲットを ALB にする
- [ ] D. GWLB を前段に置き、ターゲットを ALB にする

> **解説**: ALB は静的 IP を持てず DNS 名のみ。NLB は AZ ごとに静的 IP/EIP を関連付け可能で、alb ターゲットタイプにより背後に ALB を置ける。これで固定 IP と L7 ルーティング/WAF を両立する定番構成。
> **出典**: [elastic-load-balancing README #11 よくある設計パターン](README.md#11-よくある設計パターン)

## elastic-load-balancing-006
- type: single
- difficulty: medium
- domain: 2
- tags: [tls, nlb, well-architected]

クライアントからターゲットまでエンドツーエンドで TLS 暗号化を維持し、ターゲット側で証明書を管理・復号したい。適切な構成はどれか。

- [ ] A. ALB の HTTPS リスナーで終端する
- [ ] B. NLB の TLS リスナーで終端する
- [x] C. NLB の TCP リスナーで TLS パススルーにする
- [ ] D. GWLB で GENEVE 終端する

> **解説**: TLS パススルーは NLB の TCP リスナーで実現し、NLB は復号せず素通しするためターゲットが復号する。ALB の HTTPS や NLB の TLS リスナーは LB で終端してしまう。エンドツーエンド暗号化や相互 TLS が必須なときはパススルー。
> **出典**: [elastic-load-balancing README #7 TLS 終端 vs パススルー](README.md#7-tls-終端-vs-パススルーproxy-protocolsni)

## elastic-load-balancing-007
- type: single
- difficulty: hard
- domain: 3
- tags: [proxy-protocol, privatelink]

NLB の背後で動くアプリが、PrivateLink エンドポイント経由のアクセスでクライアントの実 IP を取得できない。解決策として正しいものはどれか。

- [ ] A. NLB のクロスゾーン負荷分散を ON にする
- [x] B. NLB で Proxy Protocol v2 を有効化する
- [ ] C. ターゲットタイプを instance から ip に変更する
- [ ] D. ALB に切り替えて X-Forwarded-For を使う

> **解説**: NLB は送信元 IP を保持するが、PrivateLink エンドポイント経由や ALB ターゲットの場合は実 IP が NLB ノード IP に置き換わる。実 IP やエンドポイント ID が必要なときは Proxy Protocol v2 を有効化し、TCP ペイロード先頭に実 IP/ポートを付与する。
> **出典**: [elastic-load-balancing README #7 TLS 終端 vs パススルー](README.md#7-tls-終端-vs-パススルーproxy-protocolsni)

## elastic-load-balancing-008
- type: single
- difficulty: medium
- domain: 2
- tags: [tls]

1 つの HTTPS リスナーで複数ドメインの証明書を提供し、ClientHello に応じて適切な証明書を選択したい。利用する機能はどれか。

- [ ] A. Proxy Protocol v2
- [x] B. SNI（Server Name Indication）
- [ ] C. クロスゾーン負荷分散
- [ ] D. スティッキーセッション

> **解説**: SNI により ALB/NLB は 1 つの HTTPS/TLS リスナーに複数証明書を載せ、ClientHello の SNI に応じて証明書を選択できる（マルチテナント）。証明書は ACM で発行・自動更新する。
> **出典**: [elastic-load-balancing README #7 TLS 終端 vs パススルー](README.md#7-tls-終端-vs-パススルーproxy-protocolsni)

## elastic-load-balancing-009
- type: single
- difficulty: easy
- domain: 4
- tags: [waf, alb, security-group]

AWS WAF（WebACL）を直接関連付けできるロードバランサはどれか。

- [x] A. ALB
- [ ] B. NLB
- [ ] C. GWLB
- [ ] D. すべての ELB 種別

> **解説**: WAF 連携は ALB のみ可能。NLB/GWLB/CLB は WAF と直接連携できない。L7 のリクエスト検査が前提のため ALB が対象になる。
> **出典**: [elastic-load-balancing README #3 ロードバランサ4種比較](README.md#3-ロードバランサ-4-種比較最重要)

## elastic-load-balancing-010
- type: single
- difficulty: medium
- domain: 1
- tags: [cross-zone, alb, target-type]

ALB のクロスゾーン負荷分散について正しいものはどれか。

- [ ] A. デフォルト OFF で LB レベルで ON にできる
- [x] B. LB レベルでは常に ON で無効化できないが、ターゲットグループ単位で OFF にできる
- [ ] C. 完全に無効化できない
- [ ] D. AZ 間データ転送課金が発生する

> **解説**: ALB はクロスゾーンが LB レベルで常に ON（無効化不可）だが、ターゲットグループ単位でのみ OFF にできる。ALB/CLB はクロスゾーン分散による AZ 間データ転送課金は発生しない（NLB は発生）。
> **出典**: [elastic-load-balancing README #5 クロスゾーン負荷分散](README.md#5-クロスゾーン負荷分散最頻出暗記必須)

## elastic-load-balancing-011
- type: multi
- difficulty: hard
- domain: 1
- tags: [nlb, use-case-fit]

NLB の特徴として正しいものを 2 つ選べ。

- [x] A. AZ ごとに静的 IP / EIP を関連付けできる
- [ ] B. HTTP ヘッダ/パスに基づくコンテンツルーティングができる
- [x] C. instance/ip ターゲットでクライアントの送信元 IP を保持する
- [ ] D. AWS WAF を直接関連付けできる
- [ ] E. クロスゾーン負荷分散がデフォルトで ON である

> **解説**: NLB は L4 で動作し、AZ ごとに静的 IP/EIP を関連付けでき、instance/ip ターゲットで送信元 IP を保持する。コンテンツルーティングと WAF は ALB の機能。クロスゾーンは NLB ではデフォルト OFF。
> **出典**: [elastic-load-balancing README #3 ロードバランサ4種比較](README.md#3-ロードバランサ-4-種比較最重要)

## elastic-load-balancing-012
- type: multi
- difficulty: hard
- domain: 2
- tags: [awsvpc, alb, target-type]

EKS の AWS Load Balancer Controller に関して正しいものを 2 つ選べ。

- [x] A. Ingress リソースから ALB を、Service (type: LoadBalancer) から NLB を自動プロビジョニングする
- [ ] B. CLB のみをプロビジョニングする
- [x] C. IP モードでは Pod の IP を直接ターゲット登録し、instance モードより低レイテンシ
- [ ] D. ターゲットタイプや SSL 設定はコントローラの環境変数のみで制御する
- [ ] E. GWLB を Pod ごとに自動生成する

> **解説**: AWS Load Balancer Controller は Ingress→ALB、Service(LoadBalancer)→NLB を自動生成する。IP モードは VPC CNI を前提に Pod IP を直接登録し instance モードより効率的。各種設定はアノテーションで制御し、IngressGroup で複数 Ingress を 1 ALB に集約できる。
> **出典**: [elastic-load-balancing README #8 AWS Load Balancer Controller](README.md#8-aws-load-balancer-controllereks)
