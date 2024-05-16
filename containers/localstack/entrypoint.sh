#!/bin/bash

set -eu

# 設定
LOCALSTACK_HOME=/etc/localstack/init/ready.d
AWSLOCAL_ACCOUNT_ID=000000000000
ROLE_NAME=role01
FUNC_NAME=func01
QUEUE_NAME=queue01.fifo

ENV_VARIABLES=LAMBDA_TOKEN=${LAMBDA_TOKEN},
ENV_VARIABLES+=AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION},
ENV_VARIABLES+=AWS_S3_ENDPOINT_URL=${AWS_S3_ENDPOINT_URL},
ENV_VARIABLES+=AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID},
ENV_VARIABLES+=AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY},
ENV_VARIABLES+=AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}

# バケットを作成
awslocal s3 mb s3://${AWS_STORAGE_BUCKET_NAME}

# 実行ロールを作成
awslocal iam create-role \
--role-name ${ROLE_NAME} \
--assume-role-policy-document file://${LOCALSTACK_HOME}/role.json

awslocal iam attach-role-policy \
--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole \
--role-name ${ROLE_NAME}

# Lambda 関数を作成
cp -p ${LOCALSTACK_HOME}/function.py .
chmod 755 function.py
zip function.zip function.py
awslocal lambda create-function \
    --function-name ${FUNC_NAME} \
    --zip-file fileb://function.zip \
    --handler function.lambda_handler \
    --runtime python3.12 \
    --timeout 900 \
    --memory-size 1024 \
    --role arn:aws:iam::${AWSLOCAL_ACCOUNT_ID}:role/${ROLE_NAME} \
    --environment Variables="{${ENV_VARIABLES}}"


# AmazonSQSキューを作成
awslocal sqs create-queue \
    --queue-name ${QUEUE_NAME} \
    --attributes FifoQueue=true,ContentBasedDeduplication=true

# イベントソースを設定
awslocal lambda create-event-source-mapping \
--function-name ${FUNC_NAME}  \
--batch-size 1 \
--event-source-arn arn:aws:sqs:${AWS_DEFAULT_REGION}:${AWSLOCAL_ACCOUNT_ID}:${QUEUE_NAME}
