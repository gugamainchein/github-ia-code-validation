# /bin/bash

export API_NAME="github-ia-back-end"
export STAGE="v1"
export AWS_DEFAULT_REGION="us-east-1"
export ACCOUNT_ID=""

if ! aws s3 ls s3://$API_NAME-$AWS_DEFAULT_REGION-$ACCOUNT_ID; then
    aws s3 mb s3://$API_NAME-$AWS_DEFAULT_REGION-$ACCOUNT_ID
    aws s3api put-bucket-tagging --bucket $API_NAME-$AWS_DEFAULT_REGION-$ACCOUNT_ID --tagging 'TagSet=[{Key=owner,Value=gustavo.mainchein},{Key=project,Value=study}]'
    aws s3api put-bucket-versioning --bucket $API_NAME-$AWS_DEFAULT_REGION-$ACCOUNT_ID --versioning-configuration Status=Enabled
fi

python3 -m venv venv

source venv/bin/activate

mkdir -p src/layers/common/python/lib/python3.12/site-packages

pip install --upgrade pip

pip install --no-cache-dir -r layers/common/requirements.txt -t src/layers/common/python/lib/python3.12/site-packages

sls deploy --stage=$STAGE --param="API_NAME=$API_NAME"

rm -rf src/layers

deactivate

rm -rf venv