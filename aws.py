import boto3
from botocore.exceptions import ClientError


def get_regions(aws_region='us-east-1'):
    """Returns a list of all security-groups Regions"""
    ec2 = boto3.client('ec2', region_name=aws_region)
    response = ec2.describe_regions()

    regions = []

    for k in response['Regions']:
        regions.append(k['RegionName'])

    return regions


def get_security_groups_in_region(aws_region):
    """Returns a list of all Security Groups (excluding Default) in an security-groups Region"""

    client = boto3.client('ec2', region_name=aws_region)
    response = client.describe_security_groups()

    sgs = response['SecurityGroups']

    security_groups = []

    for sg in sgs:
        if sg['GroupName'] != 'default':
            security_groups.append(sg['GroupId'])

    return security_groups


def get_all_security_groups():
    """Returns a list of all Security Groups (excluding Default) in all security-groups Regions"""
    security_groups = []

    for aws_region in get_regions():
        client = boto3.client('ec2', region_name=aws_region)
        response = client.describe_security_groups()

        sgs = response['SecurityGroups']
        for sg in sgs:
            if sg['GroupName'] != 'default':
                security_groups.append(sg['GroupId'])

    return security_groups


def get_ec2_security_groups_in_region(aws_region):
    """Returns a list of all Security Groups (excluding Default) in an security-groups Region"""
    sgs_in_use_ec2 = []

    ec2client = boto3.client('ec2', region_name=aws_region)
    response = ec2client.describe_instances()
    reservations = response['Reservations']

    for i in range(len(reservations)):
        instances = reservations[i]['Instances'][0]
        sgs = instances['SecurityGroups']

        for sg in sgs:
            sgs_in_use_ec2.append(sg['GroupId'])
        i += 1

    return sgs_in_use_ec2


def send_email(SUBJECT, BODY_TEXT):
    SENDER = 'cloud-security@tpat.xyz'
    RECIPIENT = 'cloud-security-notifications@tpat.xyz'
    AWS_REGION = "us-east-1"
    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
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
    print('#' * 75)
    print('All Regions\n')
    for region in get_regions('us-east-1'):
        print(region)
    print('\n' + '#' * 75)

    print('Security Groups (excluding Default) in one Region\n')
    for security_group in get_security_groups_in_region('us-east-1'):
        print(security_group)
    print('\n' + '#' * 75)

    print('Security Groups (excluding Defaults) in all Regions\n')
    for security_group in get_all_security_groups():
        print(security_group)
    print('\n' + '#' * 75)

    print('Security Groups used by EC2 in one Region\n')
    for security_group in get_ec2_security_groups_in_region('us-east-2'):
        print(security_group)
    print('\n' + '#' * 75)
