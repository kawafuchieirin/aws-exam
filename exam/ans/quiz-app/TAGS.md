# タグ統制語彙（Controlled Vocabulary）

> 問題バンク `questions.md` の `tags:` で使える**唯一の正規語**を定義する単一情報源。
> エンジンは `tag:<語>` を習熟度スコープに使う（`models.Question.scopes()`）。
> 新タグを足すときは必ずこの表に追記し、`synonym → canonical` のマップ（`tools/tag_map.py`）も更新する。

## 設計原則
- **サービス名はタグにしない**。サービスは `service:<name>` スコープで既に追跡されるため、タグは「サービス横断で共有される概念」に限定する（例: `cloudfront` は付けず、概念の `edge-caching` を付ける）。
- **概念レベル・フラット**。`bgp-as-path` のような細分はせず `bgp` に寄せ、ニュアンスは設問・解説で表現する。
- 1問あたり **1〜4 個**を目安に、最も中心的な概念を選ぶ。
- 基礎（`services/fundamentals/`）とサービス問題が**同じ canonical を共有**することで、「サービスで間違える→当該概念の習熟度が下がる→基礎問題が苦手モードに浮上」という降下連動が成立する。

## 語彙（テーマ別）

### プロトコル・トランスポート
`bgp` `dns` `tcp-udp` `tls` `ipsec` `http` `mtu` `icmp`

### アドレッシング
`cidr` `subnetting` `ipv6` `ip-exhaustion` `nat` `public-ip`

### 経路制御
`route-table` `longest-prefix` `blackhole` `route-propagation` `ecmp`

### 接続・ハイブリッド
`vpc-peering` `transit-gateway` `direct-connect` `vpn` `client-vpn` `privatelink` `vpc-endpoint` `vpc-sharing` `hybrid`

### ロードバランシング
`alb` `nlb` `gwlb` `cross-zone` `health-check` `target-type` `proxy-protocol`

### DNSルーティング（Route 53）
`routing-policy` `failover`

### セキュリティ
`security-group` `nacl` `stateful-stateless` `waf` `shield` `network-firewall` `firewall-manager` `encryption` `iam-policy` `scp` `least-privilege` `source-condition`

### 監視・運用
`flow-logs` `monitoring` `reachability-analyzer` `traffic-mirroring` `cloudtrail-events` `config-rules` `troubleshooting`

### コンピュート/コンテナのネットワーキング
`eni` `enhanced-networking` `placement-group` `awsvpc` `service-discovery` `service-mesh`

### コンテンツ配信・APIエッジ
`edge-caching` `oac` `global-accelerator` `api-endpoint` `vpc-link`

### アプリ統合
`pub-sub` `message-queue` `event-routing`

### ガバナンス・コスト・運用管理
`cost` `data-transfer` `multi-account` `landing-zone` `iac` `quotas` `well-architected` `auto-scaling` `console-security` `automation`

### 設計属性
`multi-az` `multi-region` `high-availability` `use-case-fit`

---
合計: 84語。`tools/tag_map.py` の `CANONICAL` がこの一覧と一致することを `tools/apply_tag_map.py` が検証する（不一致なら正規化を中断）。
