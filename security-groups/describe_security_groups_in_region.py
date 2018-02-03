import boto3
import pprint


def describe_security_groups_in_region(region):
    """Returns full descriptions of Security Groups in an security-groups Region"""

    client = boto3.client('ec2', region_name=region)
    response = client.describe_security_groups()

    sgs = response['SecurityGroups']

    return sgs


if __name__ == "__main__":
    security_groups = describe_security_groups_in_region('us-east-2')
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(security_groups)
