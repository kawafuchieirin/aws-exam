# Amplify Hosting アプリ。repository を指定しないことで「手動デプロイ」モードになり、
# ビルド/デプロイは GitHub Actions 側で行う（CI/CD を GitHub Actions に寄せる構成）。
resource "aws_amplify_app" "bunko" {
  name     = var.app_name
  platform = "WEB" # 静的サイト（Astro/Starlight の出力）

  # SPA ではなくマルチページ静的サイトのため、未知パスは Starlight の 404 を返す。
  custom_rule {
    source = "/<*>"
    target = "/404.html"
    status = "404"
  }
}

# 公開ブランチ。Basic認証はブランチ単位で有効化する。
resource "aws_amplify_branch" "main" {
  app_id      = aws_amplify_app.bunko.id
  branch_name = var.branch_name
  framework   = "Web"
  stage       = "PRODUCTION"

  enable_basic_auth      = true
  basic_auth_credentials = base64encode("${local.basic_auth_username}:${local.basic_auth_password}")

  # 手動デプロイ運用のため自動ビルドは無効
  enable_auto_build = false

  lifecycle {
    # 認証情報は機密。Terraform の差分ログに平文を出さない
    ignore_changes = []
  }
}
