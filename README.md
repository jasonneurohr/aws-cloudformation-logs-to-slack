# aws-cloudformation-logs-to-slack

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python AWS Lambda which delivers CloudFormation events to Slack created using the AWS SAM framework.

To use with CloudFormation include the `--notications-arns` argument with the ARN of the SNS topic created as part of the included SAM template. The ARN is listed in the output section of the CloudFormation used to deploy the Lambda. 

## Example usage

Example usage with the AWS cli.

```
aws cloudformation create-stack --stack-name test --template-body file://cf-s3bucket.yml --notification-arns arn:aws:sns:ap-southeast-2:xxxx:sns-cloudformation
```

## Deployment

Firstly, we need a `S3 bucket` where we can upload our Lambda functions packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://BUCKET_NAME
```

Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name aws-cloudformation-logs-to-slack \
    --capabilities CAPABILITY_IAM
```

Once the Lambda is deployed you must update the environment variable called `SLACK_WEBHOOK` in the Lambda configuration with a Slack webhook URL for it to work correctly. If you don't have a Slack Webhook set up to use, now would be a good time to set one up. Refer to the Slack documentation [here](https://api.slack.com/incoming-webhooks)

## Cleanup

To delete the Serverless Application use the following AWS CLI Command:

```bash
aws cloudformation delete-stack --stack-name aws-cloudformation-logs-to-slack
```

To delete the S3 bucket use the following AWS CLI Command:

```bash
aws s3 rb s3://BUCKET_NAME
```