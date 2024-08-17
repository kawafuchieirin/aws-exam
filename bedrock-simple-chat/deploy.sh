#!/bin/bash

# 環境変数
account_id=412420079063


# DockerでECRにログイン
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin $account_id.dkr.ecr.ap-northeast-1.amazonaws.com

# ビルド（コンテナ化）
docker build -t bsc .

# コンテナへ「最新版」タグを付与
docker tag bsc:latest $account_id.dkr.ecr.ap-northeast-1.amazonaws.com/bsc:latest

# コンテナをECRへプッシュ（登録）
docker push $account_id.dkr.ecr.ap-northeast-1.amazonaws.com/bsc:latest
