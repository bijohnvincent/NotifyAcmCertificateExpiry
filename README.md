# NotifyAcmCertificateExpiry
This function is for notifying when a certificate in ACM is about to expire. Written for AWS Lambda with python 3.6 and boto3. You can add an AWS SNS topic in this function. If the certificate expires in less than the days given in the function, it will send notification to the given SNS topic. 

You may add a higher value as certificate expiry threshold and trigger the AWS Lambda function weekly using AWS CloudWatch Rules, so that you get notification earlier and will not spam your inbox.
Example Cron expression for CloudWatch event: 00 06 ? * MON *

## IAM policy for role
Add following policies to the IAM role you have attached to the Lambda in addition to the basic execution permission.

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
