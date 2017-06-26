# NotifyAcmCertificateExpiry
This function is for notifying when a certificate in ACM is about to expire. 

Supports: python 3.6, boto3

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
