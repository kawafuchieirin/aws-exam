variable "aws_region" {
  description = "リソースを作成するAWSリージョン"
  type        = string
  default     = "ap-northeast-1"
}

variable "app_name" {
  description = "Amplifyアプリ名"
  type        = string
  default     = "bunko"
}

variable "branch_name" {
  description = "公開するブランチ名（Amplify上のブランチ。手動デプロイ先）"
  type        = string
  default     = "main"
}

variable "github_repository" {
  description = "GitHub Actions の OIDC 信頼に使うリポジトリ（owner/repo 形式）"
  type        = string
  default     = "kawafuchieirin/aws-exam"
}

# Basic認証の資格情報は変数ではなく SOPS（infra/secrets.sops.yaml）で管理する。
# secrets.tf の data.sops_file 経由で local.basic_auth_username / password として参照。

variable "create_oidc_provider" {
  description = "GitHub Actions 用の OIDC プロバイダーを新規作成するか。アカウントに既存ならfalseにして既存を参照"
  type        = bool
  default     = true
}
