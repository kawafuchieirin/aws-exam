import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';  // 変更ポイント
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import * as path from 'path';

export class TeststaticStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 静的ホスティング用S3バケットを作成
    const bucket = new s3.Bucket(this, 'SampleBucket', {
      versioned: true,
      publicReadAccess: false,
    });
    
    // CloudFront Origin Access Identity (OAI) を作成
    const cloudfrontOai = new cloudfront.OriginAccessIdentity(this, 'CloudFrontOAI');
  
    // 静的ホスティング用S3バケットに対して必要なアクセスポリシーを作成
    const bucketPolicy = new s3.BucketPolicy(this, 'WebsiteBucketPolicy', {
      bucket: bucket,
    });
    bucketPolicy.document.addStatements(
      new iam.PolicyStatement({
        actions: ['s3:GetObject'],
        effect: iam.Effect.ALLOW,
        principals: [new iam.CanonicalUserPrincipal(cloudfrontOai.cloudFrontOriginAccessIdentityS3CanonicalUserId)],
        resources: [`${bucket.bucketArn}/*`],
      })
    );

    // 静的ホスティング用S3バケットにOAIのアクセスを許可
    bucket.grantRead(cloudfrontOai);

    // CloudFrontディストリビューションを作成
    const distribution = new cloudfront.Distribution(this, 'WebsiteDistribution', {
      defaultBehavior: {
        origin: new origins.S3Origin(bucket, {   // 変更ポイント
          originAccessIdentity: cloudfrontOai,
        }),        
      },
      defaultRootObject: 'index.html',
      enableLogging: true, // ログ出力設定
      logBucket: new s3.Bucket(this, 'LogBucket', {
        objectOwnership: s3.ObjectOwnership.OBJECT_WRITER,
      }),
      logFilePrefix: 'distribution-access-logs/',
      logIncludesCookies: true,
    });

    // index.htmlを静的ホスティング用S3バケットにアップロード
    const indexHtmlPath = path.resolve(__dirname, '../source/index.html');
    new s3deploy.BucketDeployment(this, 'DeployIndexHtml', {
      sources: [s3deploy.Source.asset(path.dirname(indexHtmlPath))],
      destinationBucket: bucket,
      destinationKeyPrefix: '/',
    });

    // CloudFrontディストリビューションのDNS名を出力
    new cdk.CfnOutput(this, 'DistributionURL', {
      value: distribution.distributionDomainName,
    });
  }
}
