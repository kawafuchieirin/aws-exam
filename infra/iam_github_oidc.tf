# GitHub Actions から AWS へ「キーレス」でアクセスするための OIDC 連携。
# 長期アクセスキーを GitHub Secrets に置かず、実行時に一時クレデンシャルを発行する。

data "aws_caller_identity" "current" {}

# OIDC プロバイダー。アカウントに既存（他リポで作成済み）なら create_oidc_provider=false で参照する。
resource "aws_iam_openid_connect_provider" "github" {
  count = var.create_oidc_provider ? 1 : 0

  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  # GitHub の OIDC は IAM 側で証明書チェーンを検証するため thumbprint は形式的な値で良い
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

data "aws_iam_openid_connect_provider" "github" {
  count = var.create_oidc_provider ? 0 : 1
  url   = "https://token.actions.githubusercontent.com"
}

locals {
  oidc_provider_arn = var.create_oidc_provider ? aws_iam_openid_connect_provider.github[0].arn : data.aws_iam_openid_connect_provider.github[0].arn
}

# GitHub Actions が assume するデプロイ用ロール。信頼ポリシーで対象リポジトリに限定する。
data "aws_iam_policy_document" "deploy_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [local.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # 当該リポジトリの「公開ブランチへの push / そのブランチ上の workflow_dispatch」のみ許可。
    # 末尾 :* のワイルドカードは PR コンテキストや任意ブランチも通すため使わない。
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repository}:ref:refs/heads/${var.branch_name}"]
    }
  }
}

resource "aws_iam_role" "deploy" {
  name               = "${var.app_name}-github-deploy"
  assume_role_policy = data.aws_iam_policy_document.deploy_assume.json
}

# Amplify 手動デプロイに必要な最小権限を、対象アプリに限定して付与。
data "aws_iam_policy_document" "deploy_permissions" {
  statement {
    sid    = "AmplifyManualDeploy"
    effect = "Allow"
    actions = [
      "amplify:CreateDeployment",
      "amplify:StartDeployment",
      "amplify:GetJob",
      "amplify:GetApp",
      "amplify:GetBranch",
      "amplify:ListJobs",
    ]
    resources = [
      aws_amplify_app.bunko.arn,
      "${aws_amplify_app.bunko.arn}/*",
    ]
  }
}

resource "aws_iam_role_policy" "deploy" {
  name   = "${var.app_name}-deploy"
  role   = aws_iam_role.deploy.id
  policy = data.aws_iam_policy_document.deploy_permissions.json
}
