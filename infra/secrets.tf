# SOPS で暗号化した secrets.sops.yaml を復号して参照する。
# 復号には age 秘密鍵が必要:
#   - ローカル: ~/.config/sops/age/keys.txt を自動検出
#   - 別マシン/CI: 環境変数 SOPS_AGE_KEY または SOPS_AGE_KEY_FILE で渡す
data "sops_file" "secrets" {
  source_file = "${path.module}/secrets.sops.yaml"
}

locals {
  basic_auth_username = data.sops_file.secrets.data["basic_auth_username"]
  basic_auth_password = data.sops_file.secrets.data["basic_auth_password"]
}
