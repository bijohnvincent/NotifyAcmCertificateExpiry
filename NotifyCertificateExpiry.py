# Name          : notifyCertificateExpiry
# Author        : github.com/bijohnvincent
# Functionality : This function is for notifying when a certificate in ACM is about to expire
# Tested and working fine on: AWS Lambda with python 3.6 + boto3

#
#from botocore.vendored import requests
import boto3, datetime,  json, os, urllib3
from base64 import b64decode

# Enter number of days before you need notification about certificate expiry.
notifyIfExpiresAfter = int(os.environ['notifyIfExpiresAfter'])

# Set 'True' Only if you need notification on everytime this function runs. 
# If false function will notify only when your certificate is about to expire
# Idealy should be Flase
notifyEveryTime = eval(os.environ['notifyEveryTime'])


# Main function
def lambda_handler(event, context):
    notify = False
    message ="Hello,"
    acmClient = boto3.client('acm')
    
    # Initialise time
    now = datetime.datetime.now()
    
    # Get list of certificates in ACM
    certificateList = acmClient.list_certificates()["CertificateSummaryList"]
    
    for certificate in certificateList:
        certificateDetails = acmClient.describe_certificate(CertificateArn=certificate["CertificateArn"])["Certificate"]
        #print (certificateDetails)
        
        if 'NotAfter' in certificateDetails:
            certificateExpiresIn = certificateDetails['NotAfter'].replace(tzinfo=None) - now
            
            if certificateExpiresIn <= datetime.timedelta(days = notifyIfExpiresAfter):
                message += "\nCertificate with SAN " +repr(certificateDetails['SubjectAlternativeNames']) + \
                " expires in " + repr(certificateExpiresIn.days) + " days"
                
                notify = True
            else:
                if notifyEveryTime:
                    message += "\nCertificate with SAN " +repr(certificateDetails['SubjectAlternativeNames']) + \
                    " expires in " + repr(certificateExpiresIn.days) + " days"
                pass
        else:
            message += "\nCertificate with SAN " +repr(certificateDetails['SubjectAlternativeNames']) + \
                " has status: " + certificateDetails['Status']
        
    # Set apt subject for the notification
    if notify:
        snsSubject = 'Alert: Certificates Expiring Soon'
    else:
        snsSubject = 'AWS Certificate Manager update'

    # Send notification
    if notify or notifyEveryTime:
        # Send notification using SNS topic
        SnsClient = boto3.client('sns')
        response = SnsClient.publish(
            TopicArn= os.environ['SnsTopicArn'],
            Message= message,
            Subject= snsSubject,
            MessageStructure='string'
            )
            
        # If Slack web hook URL varible is provided, send notification to slack channel
        if os.environ['SlackWebhookUrl']:
            #print ("send Slack notification")
            slack_data = {'text': message}
            EncryptedSlackWebHookUrl = os.environ['SlackWebhookUrl']
            DecryptedSlackWebHookUrl = boto3.client('kms').decrypt(CiphertextBlob=b64decode(EncryptedSlackWebHookUrl))['Plaintext'].decode('utf-8')
            
            http = urllib3.PoolManager()
            response = http.request('POST',
                DecryptedSlackWebHookUrl, 
                body=json.dumps(slack_data),
                headers={'Content-Type': 'application/json'}
            )
            if response.status != 200:
                raise ValueError(
                    'Request to slack returned an error %s, the response is:\n%s'
                    % (response.status, response.data.decode('utf-8'))
                )
    else:
        message += "\nNo certificates expiring in " + repr (notifyIfExpiresAfter) + " days."
            
    print (message)
