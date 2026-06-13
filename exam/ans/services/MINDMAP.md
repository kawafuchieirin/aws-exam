# ANS-C01 リソース相関マインドマップ

> AWS Certified Advanced Networking - Specialty の主要リソースを「どう繋がり・どう依存し合うか」で整理。
> 試験は単体暗記より **組み合わせ設計判断** が問われるため、本資料は相関関係に特化。
> 各サービス詳細は [services/README.md](README.md) のインデックスを参照。

---

## 1. 全体マインドマップ（俯瞰）

```mermaid
mindmap
  root((ANS-C01<br/>ネットワーク))
    接続性
      VPC
        Subnet / Route Table
        IGW / NAT GW / EIGW
        NACL / Security Group
        VPC Peering
      Transit Gateway
        TGW Attachment
        TGW Route Table
        TGW Peering
        TGW Connect GRE/SD-WAN
      ハイブリッド
        Direct Connect
          Private VIF
          Transit VIF
          Public VIF
          DX Gateway
        Site-to-Site VPN
          VGW
          Customer GW
        Client VPN
      PrivateLink
        Interface Endpoint
        Gateway Endpoint
        Endpoint Service
    トラフィック分散
      ELB
        ALB L7
        NLB L4
        GWLB GENEVE
      Global Accelerator
      CloudFront
      API Gateway
    DNS / 検出
      Route 53
        Public / Private HZ
        Resolver in/out
        ルーティングポリシー
        ヘルスチェック
      Cloud Map
      App Mesh
    セキュリティ
      WAF
      Shield
      Network Firewall
      Firewall Manager
      IAM
    監視 / 運用
      CloudWatch
      VPC Flow Logs
      CloudTrail
      Reachability Analyzer
      Traffic Mirroring
    ガバナンス / 共有
      Organizations
      RAM
      Config / Control Tower
```

---

## 2. コア接続性の相関図（VPC を中心に）

```mermaid
flowchart TB
    subgraph onprem[オンプレミス / 他組織]
        CGW[Customer Gateway<br/>ルータ]
        ONP[オンプレ拠点]
    end

    subgraph aws[AWS]
        TGW{{Transit Gateway<br/>ハブ}}
        DXGW[Direct Connect<br/>Gateway]

        subgraph vpcA[VPC A]
            SNA[Subnet/RT]
            EP[Interface Endpoint]
        end
        subgraph vpcB[VPC B]
            SNB[Subnet/RT]
        end
        subgraph svcvpc[サービス提供VPC]
            NLBe[NLB] --> EPS[Endpoint Service]
        end
    end

    ONP --- CGW
    CGW -- IPsec/BGP --> VPN[Site-to-Site VPN]
    ONP -- 専用線/BGP --> DX[Direct Connect]

    DX -- Private VIF --> DXGW
    DX -- Transit VIF --> TGW
    DXGW --> TGW
    VPN --> TGW

    TGW === vpcA
    TGW === vpcB
    vpcA <-- VPC Peering --> vpcB

    EP -. PrivateLink .-> EPS

    classDef hub fill:#f96,stroke:#333,stroke-width:2px;
    class TGW hub;
```

**読み解きポイント**
- **TGW がハブ**: 多数 VPC ＋ ハイブリッドを集中管理。スポーク間は TGW ルートテーブルで制御。
- **VPC Peering** は少数 VPC・低コスト・推移的ルーティング不可（A↔B↔C で A↔C は不可）。
- **PrivateLink** は CIDR 重複していても単一サービスへ到達可能（NLB 裏付け）。
- **DX の VIF 使い分け**: Private VIF→単一/少数VPC、Transit VIF→TGW経由で多数VPC、Public VIF→AWSパブリックサービス。

---

## 3. ハイブリッド接続の選択フロー

```mermaid
flowchart TD
    Q1{安定した専用帯域が必要?}
    Q1 -- はい --> DX[Direct Connect]
    Q1 -- いいえ/即時 --> VPN[Site-to-Site VPN]

    DX --> Q2{冗長/バックアップは?}
    Q2 -- 低コスト冗長 --> VPNb[VPN を DX バックアップに]
    Q2 -- DX上を暗号化 --> PIPVPN[Private IP VPN over DX<br/>Transit VIF]

    DX --> Q3{接続先VPC数は?}
    Q3 -- 少数 --> PVIF[Private VIF + DXGW]
    Q3 -- 多数/集中管理 --> TVIF[Transit VIF + TGW]

    VPN --> Q4{接続先は?}
    Q4 -- 単一VPC --> VGW[VGW アタッチ]
    Q4 -- 多数VPC --> TGWa[TGW アタッチ]
```

---

## 4. エッジ → アプリ層のトラフィック相関

```mermaid
flowchart LR
    USER([クライアント])
    USER --> GA[Global Accelerator<br/>静的Anycast IP / 非HTTP低遅延]
    USER --> CF[CloudFront<br/>CDN / 静的+動的]

    CF --> WAF[AWS WAF]
    WAF -.保護.-> SHLD[Shield Advanced]

    CF --> ALB
    GA --> NLB
    APIGW[API Gateway] --> ALB

    subgraph elb[Elastic Load Balancing]
        ALB[ALB L7]
        NLB[NLB L4 静的IP]
        GWLB[GWLB GENEVE]
    end

    ALB --> TG[Target Group]
    NLB --> TG
    TG --> EC2[EC2]
    TG --> ECS[ECS/Fargate]
    TG --> LMB[Lambda]

    GWLB -. 透過挿入 .-> APPL[サードパーティFW/IDS]

    NLB --> EPS2[PrivateLink Endpoint Service]
```

**読み解きポイント**
- **WAF は ALB / CloudFront / API Gateway に紐付け**。Shield Advanced はそれらに加えて Global Accelerator / EIP も保護。
- **NLB は PrivateLink の裏付け**（Endpoint Service）になる唯一の ELB。
- **GWLB は GENEVE(6081)** でセキュリティアプライアンスへ透過的に挿入。

---

## 5. DNS / 名前解決の相関

```mermaid
flowchart TB
    subgraph onp[オンプレDNS]
        ONDNS[社内DNSサーバ]
    end
    subgraph r53[Route 53]
        PUB[Public Hosted Zone]
        PHZ[Private Hosted Zone]
        RIN[Resolver Inbound EP]
        ROUT[Resolver Outbound EP]
        RULE[Resolver Rule]
        HC[Health Check]
    end

    ONDNS -- AWS名を解決 --> RIN
    ROUT -- オンプレ名を転送 --> ONDNS
    RULE --> ROUT
    PHZ -- VPC関連付け --> VPCx[VPC]
    PUB --> POL[ルーティングポリシー<br/>加重/レイテンシ/フェイルオーバー/地理]
    HC --> POL

    RAM2[RAM] -. PHZ/Resolverルール共有 .-> ACCTS[他アカウントVPC]
```

**読み解きポイント**
- **Inbound EP** = オンプレ → AWS の名前解決、**Outbound EP + Rule** = AWS → オンプレ。双方向で「ハイブリッドDNS」。
- **PHZ と Resolver ルールは RAM で共有** し、共有サービス VPC に集約するのが定石。

---

## 6. セキュリティ・ガバナンスの相関

```mermaid
flowchart TB
    ORG[Organizations] --> FM[Firewall Manager]
    FM -- 一括ポリシー強制 --> WAFr[WAF]
    FM --> SHLDr[Shield Advanced]
    FM --> NFW[Network Firewall]
    FM --> SGp[Security Group ポリシー]

    ORG --> RAM3[RAM<br/>TGW/Subnet/Resolver共有]
    ORG --> CT[Control Tower / Config]

    subgraph insp[インスペクションVPC]
        NFW
        GWLBi[GWLB]
    end
    TGWc{{Transit Gateway}} -- 全トラフィック誘導 --> insp
```

**読み解きポイント**
- **集中型インスペクション**: TGW で全トラフィックをインスペクション VPC に誘導 → Network Firewall / GWLB で検査。
- **Firewall Manager は Organizations 配下に組織横断ポリシーを強制**（新規アカウントにも自動適用）。

---

## 7. 監視・トラブルシュートの相関

```mermaid
flowchart LR
    VPCm[VPC] --> FL[VPC Flow Logs<br/>メタデータ ACCEPT/REJECT]
    VPCm --> TM[Traffic Mirroring<br/>パケット中身]
    FL --> CW[CloudWatch Logs]
    FL --> S3l[S3]
    TM --> APPLm[解析アプライアンス/IDS]

    RA[Reachability Analyzer<br/>到達性の構成検証] -. 設定ベース .-> VPCm
    CW --> ALM[CloudWatch Alarm]
    CTr[CloudTrail<br/>API監査] --> S3l
```

**読み解きポイント**
- **Flow Logs = メタデータ**（誰が誰へ・許可/拒否）、**Traffic Mirroring = パケット実体**。用途で使い分け。
- **Reachability Analyzer** は実トラフィックを流さず構成から到達性を検証（SG/NACL/RT のミス検出）。

---

## 8. 共有・マルチアカウント（RAM 中心）

```mermaid
flowchart TB
    RAMc((RAM))
    RAMc --> TGWs[Transit Gateway 共有]
    RAMc --> SUBs[Subnet 共有<br/>VPC Sharing]
    RAMc --> RSLVs[Resolver Rule 共有]
    RAMc --> PHZs[Private Hosted Zone 関連付け]
    RAMc --> PFXs[Prefix List 共有]
    ORGr[Organizations] -. 信頼関係 .-> RAMc
```

---

## まとめ：暗記すべき相関の最重要ペア

| 起点 | 相関先 | 関係の本質 |
|---|---|---|
| Transit Gateway | VPC / VPN / DX(Transit VIF) | ハブ＆スポークの中心。スポーク間制御は TGW ルートテーブル |
| PrivateLink | NLB / Endpoint Service | CIDR重複でも単一サービスへ到達（NLB裏付け） |
| Direct Connect | DXGW(Private VIF) / TGW(Transit VIF) | 接続VPC数で VIF を選択 |
| WAF | ALB / CloudFront / API Gateway | L7保護の貼り付け先 |
| Shield Advanced | CloudFront / GA / NLB / EIP | DDoS保護対象 |
| Route 53 Resolver | オンプレDNS（in/out EP） | ハイブリッドDNSの双方向 |
| Firewall Manager | Organizations / WAF / NFW / SG | 組織横断ポリシー強制 |
| RAM | TGW / Subnet / Resolver / PHZ | マルチアカウント共有の起点 |
| GWLB | セキュリティアプライアンス(GENEVE) | 透過的インスペクション挿入 |
| VPC Flow Logs | CloudWatch / S3 | トラフィックメタデータの可視化 |
```
