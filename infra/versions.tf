terraform {
  required_version = ">= 1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60"
    }
    # SOPS で暗号化した secrets.sops.yaml を apply 時に復号する。
    sops = {
      source  = "carlpett/sops"
      version = "~> 1.1"
    }
  }

  # 状態ファイルはデフォルトでローカル(terraform.tfstate)。
  # チーム運用やCIからのapplyに進む場合は S3 + DynamoDB バックエンドへ移行する。
  # backend "s3" {
  #   bucket         = "<your-tfstate-bucket>"
  #   key            = "bunko/terraform.tfstate"
  #   region         = "ap-northeast-1"
  #   dynamodb_table = "<your-tflock-table>"
  #   encrypt        = true
  # }
}
