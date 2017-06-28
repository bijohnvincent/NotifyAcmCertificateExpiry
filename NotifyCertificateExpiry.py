# Name          : notifyCertificateExpiry
# Author        : Bijohn Vincent
# Functionality : This function is for notifying when a certificate imported in ACM is about to expire
# Tested and working fine on: AWS Lambda with python 3.6 + boto3

#Import modules
import boto3, datetime

########################### Add your SNS ARN ################################
SnsTopicArn = "SNS ARN"
#############################################################################

# Enter number of days before you need notification about certificate expiry.
notifyIfExpiresAfter = 40

# Set 'True' Only if you need notification on everytime this function runs. 
# If false function will notify only when your certificate is about to expire
# Idealy should be Flase
notifyEveryTime = False


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
        
    # Set apt subject for the notification
    if notify:
        snsSubject = 'Alert: Certificates Expiring Soon'
    else:
        snsSubject = 'AWS Certificate Manager update'
    
    # Send notification using SNS topic
    if notify or notifyEveryTime:
        SnsClient = boto3.client('sns')
        response = SnsClient.publish(
            TopicArn= SnsTopicArn,
            Message= message,
            Subject= snsSubject,
            MessageStructure='string'
            )
    else:
        message += "\nNo certificates expiring in " + repr (notifyIfExpiresAfter) + " days."
    print (message)
