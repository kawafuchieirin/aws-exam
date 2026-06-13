# インフラ & CI/CD セットアップ手順

「要点文庫」を AWS Amplify Hosting（Basic認証付き）で公開し、GitHub Actions から
キーレス（OIDC）で自動デプロイするための一式。

```
infra/
├─ amplify.tf           # Amplifyアプリ + 公開ブランチ + Basic認証
├─ iam_github_oidc.tf   # GitHub Actions用 OIDCプロバイダー + デプロイロール（最小権限）
├─ secrets.tf           # SOPS で暗号化した Basic認証情報を復号して参照
├─ secrets.sops.yaml    # Basic認証情報（age で暗号化済み・コミットOK）
├─ variables.tf / outputs.tf / providers.tf / versions.tf
└─ terraform.tfvars.example
```

## 構成の考え方

- **手動デプロイ方式**: Amplify にリポジトリを接続せず（`aws_amplify_app` に `repository` を指定しない）、
  ビルド〜デプロイはすべて GitHub Actions が担う。CI/CD を GitHub Actions に集約するため。
- **セキュア**:
  - 閲覧は Amplify ブランチの **Basic認証** で保護。資格情報は **SOPS + age で暗号化**して Git に置く（平文はコミットしない）。
  - GitHub Actions → AWS は **OIDC の一時クレデンシャル**。長期アクセスキーを Secrets に置かない。
  - デプロイロールは対象 Amplify アプリのみに権限を限定。

## 0. Basic認証情報（SOPS）の準備

Basic認証のユーザー名/パスワードは `infra/secrets.sops.yaml` に **age で暗号化**して格納する。
暗号化ルールはリポジトリ直下の `.sops.yaml`（age 公開鍵を記載・コミット済み）。

```bash
# 必要ツール（.mise.toml で管理）
mise install                       # sops / age を導入

# 鍵（初回のみ・既に作成済みなら不要）。秘密鍵は下記パスに保存しコミットしない。
#   macOS:  ~/Library/Application Support/sops/age/keys.txt
#   Linux:  ~/.config/sops/age/keys.txt （または環境変数 SOPS_AGE_KEY_FILE で指定）
# 新しい鍵を作る場合は公開鍵を .sops.yaml の age: に差し替えて再暗号化する。

# 値の編集（自動で復号→エディタ→保存時に再暗号化）
sops infra/secrets.sops.yaml
#   basic_auth_username: <任意のユーザー名>
#   basic_auth_password: <強いパスワード>
# エディタを明示したい場合は EDITOR を前置する:
#   EDITOR=vim sops infra/secrets.sops.yaml
```

> ⚠️ age 秘密鍵を紛失すると復号できなくなる。1Password 等にバックアップしておく。
> 別マシン/CI から apply する場合は、その秘密鍵を環境変数 `SOPS_AGE_KEY`（中身）または
> `SOPS_AGE_KEY_FILE`（パス）で渡す。

## 1. インフラを作成（ローカルから一度だけ）

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars   # Basic認証以外の値（任意で編集）

terraform init
terraform plan      # secrets.sops.yaml が自動復号され Amplify に渡る
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

```bash
sops infra/secrets.sops.yaml   # 復号→値を編集→保存で再暗号化
cd infra && terraform apply    # 新しい資格情報を Amplify に反映
```

## 状態管理について

デフォルトはローカル `terraform.tfstate`。個人運用なら十分。複数端末/CIから apply するなら
`versions.tf` の S3 バックエンド（コメントアウト済み）を有効化する。