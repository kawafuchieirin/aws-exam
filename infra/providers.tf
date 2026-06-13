provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = "bunko"
      ManagedBy = "terraform"
    }
  }
}
