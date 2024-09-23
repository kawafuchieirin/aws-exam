from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC, DirectConnect, TransitGateway, Route53HostedZone, Route53
from diagrams.aws.compute import EC2
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users

with Diagram("Hybrid DNS Solution with AWS and On-Premises", show=False):
    with Cluster("オンプレミスネットワーク"):
        onprem_dns = Server("DNSサーバー")
        onprem_users = Users("ユーザー")
        
    direct_connect = DirectConnect("Direct Connect")
    transit_gateway = TransitGateway("Transit Gateway")

    with Cluster("AWS"):
        private_hosted_zone = Route53HostedZone("cloud.example.com\n(プライベートホストゾーン)")

        vpcs = []
        for i in range(1, 3):
            with Cluster(f"VPC {i}"):
                vpc = VPC(f"VPC {i}")
                ec2_instance = EC2(f"リソース {i}")
                resolver_inbound = Route53("Resolverインバウンドエンドポイント")

                # EC2インスタンスからResolverインバウンドエンドポイントへのDNSクエリ
                ec2_instance - Edge(label="DNSクエリ") - resolver_inbound

                # プライベートホストゾーンとVPCの関連付け
                private_hosted_zone - Edge(label="関連付け") - vpc

                # VPCのリストに追加
                vpcs.append((vpc, resolver_inbound))

            # VPCをTransit Gatewayに接続
            vpc - Edge(label="アタッチメント") - transit_gateway

    # 接続の定義
    onprem_users - Edge(label="DNSクエリ") - onprem_dns
    onprem_dns - Edge(label="DNSクエリ") - direct_connect - Edge(label="DX接続") - transit_gateway

    # Transit Gatewayから各ResolverインバウンドエンドポイントへのDNSクエリ
    for vpc, resolver_inbound in vpcs:
        transit_gateway - Edge(label="DNSクエリ") - resolver_inbound
