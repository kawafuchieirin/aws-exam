# インフラ & CI/CD セットアップ手順

「要点文庫」を AWS Amplify Hosting（Basic認証付き）で公開し、GitHub Actions から
キーレス（OIDC）で自動デプロイするための一式。

```
infra/
├─ amplify.tf           # Amplifyアプリ + 公開ブランチ + Basic認証
├─ iam_github_oidc.tf   # GitHub Actions用 OIDCプロバイダー + デプロイロール（最小権限）
├─ variables.tf / outputs.tf / providers.tf / versions.tf
└─ terraform.tfvars.example
```

## 構成の考え方

- **手動デプロイ方式**: Amplify にリポジトリを接続せず（`aws_amplify_app` に `repository` を指定しない）、
  ビルド〜デプロイはすべて GitHub Actions が担う。CI/CD を GitHub Actions に集約するため。
- **セキュア**:
  - 閲覧は Amplify ブランチの **Basic認証** で保護（資格情報は Terraform 変数。コードにハードコードしない）。
  - GitHub Actions → AWS は **OIDC の一時クレデンシャル**。長期アクセスキーを Secrets に置かない。
  - デプロイロールは対象 Amplify アプリのみに権限を限定。

## 1. インフラを作成（ローカルから一度だけ）

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars   # 値を埋める（Basic認証のユーザー名/パス等）

# Basic認証情報は環境変数で渡してもよい（tfvarsに書かない場合）
# export TF_VAR_basic_auth_username='your-name'
# export TF_VAR_basic_auth_password='strong-password'

terraform init
terraform plan
terraform apply
```

> OIDCプロバイダー (`token.actions.githubusercontent.com`) がアカウントに既存なら、
> `create_oidc_provider = false` を設定して既存を参照する（重複作成は失敗するため）。

apply 後、出力された値を控える:

```bash
terraform output
# amplify_app_id, amplify_branch_name, site_url, github_deploy_role_arn
```

## 2. GitHub リポジトリ側の設定

Settings → Secrets and variables → Actions に登録する。

**Secrets**

| 名前 | 値 |
| :-- | :-- |
| `AWS_DEPLOY_ROLE_ARN` | `terraform output github_deploy_role_arn` |

**Variables**

| 名前 | 値 |
| :-- | :-- |
| `AWS_REGION` | 例: `ap-northeast-1` |
| `AMPLIFY_APP_ID` | `terraform output amplify_app_id` |
| `AMPLIFY_BRANCH` | 例: `main` |
| `SITE_URL` | `terraform output site_url`（正規URL/サイトマップ用） |

## 3. デプロイ

`bunko/**` または `exam/**`（原本ノート）を変更して `main` に push すると、
`.github/workflows/deploy.yml` が起動し、sync → ビルド → Amplify へデプロイする。
手動実行は Actions タブの「Run workflow」(`workflow_dispatch`)。

完了後、`SITE_URL` にアクセスするとブラウザが Basic認証を要求 → 設定したユーザー名/パスワードで閲覧。スマホでも同様。

## 認証情報を変更したいとき

`terraform.tfvars`（または環境変数）の `basic_auth_*` を変えて `terraform apply`。

## 状態管理について

デフォルトはローカル `terraform.tfstate`。個人運用なら十分。複数端末/CIから apply するなら
`versions.tf` の S3 バックエンド（コメントアウト済み）を有効化する。
