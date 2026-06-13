output "amplify_app_id" {
  description = "GitHub Actions の変数 AMPLIFY_APP_ID に設定する値"
  value       = aws_amplify_app.bunko.id
}

output "amplify_branch_name" {
  description = "デプロイ先ブランチ名"
  value       = aws_amplify_branch.main.branch_name
}

output "site_url" {
  description = "公開URL（Basic認証で保護）。GitHub Actions の変数 SITE_URL にも設定する"
  value       = "https://${aws_amplify_branch.main.branch_name}.${aws_amplify_app.bunko.default_domain}"
}

output "github_deploy_role_arn" {
  description = "GitHub Actions の Secret AWS_DEPLOY_ROLE_ARN に設定する値"
  value       = aws_iam_role.deploy.arn
}
