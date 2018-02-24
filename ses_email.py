import boto3
from botocore.exceptions import ClientError


def send_email_default(SUBJECT, BODY_TEXT):
    SENDER = '<sender email>'
    RECIPIENT = '<recipient email>'
    AWS_REGION = "us-east-1"
    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # response = client.send_email(
        client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])


if __name__ == "__main__":
    send_email_default('Test Email', 'This is a test\nThanks,\nAWS Security')
