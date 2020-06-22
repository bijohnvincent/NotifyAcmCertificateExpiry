# NotifyAcmCertificateExpiry
This function is for notifying when a certificate in ACM is about to expire. Written for AWS Lambda with python 3.6 and boto3. You can add an AWS SNS topic in this function. If the certificate expires in less than the days given in the function, it will send notification to the given SNS topic. 

Compared to AWS Config notification, this won't fill your email inbox with notifications and you can use a different SNS topic than you use for AWS Config. Email will be more readable compared to notification by Config. Also will be completely free.
Optionally you can add a Slack notification (using Slack webhook)

You may add a higher value as certificate expiry threshold and trigger the AWS Lambda function weekly using AWS CloudWatch Rules, so that you get notification earlier and will not spam your inbox.
Example Cron expression for CloudWatch event: 00 06 ? * MON *

Set following Lambda environment variables
* SlackWebhookUrl  (Note: Encrypt this environment variable)
* SnsTopicArn
* notifyEveryTime
* notifyIfExpiresAfter

![NotifyAcmCertificateExpiry](https://github.com/bijohnvincent/NotifyAcmCertificateExpiry/blob/master/image.png)

Tested and working fine on: AWS Lambda with python 3.7 + boto3

## IAM policy for role
Add following policies to the IAM role to which you have attached to the Lambda in addition to the Lambda basic execution policy.

### ACM permission
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "acm:ListCertificates",
                    "acm:DescribeCertificate"
                ],
                "Resource": [
                    "*"
                    ]
            }
        ]
    }
### SNS permission
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sns:Publish"
                ],
                "Resource": [
                    "<ARN of your SNS topic>"
                ]
            }
        ]
    }

#### Following KMS policy is required if Slack notification is required. (webhook URL is encrypted for security)
### KMS permission
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": [
                    "<ARN of your KMS key used for encrypting Lambda environment variable 'SlackWebhookUrl'>"
                ]
            }
        ]
    }
