import boto3
import pprint


def describe_ec2_instances_in_region(region):
    """Returns full descriptions of Instances in an security-groups Region"""
    ec2client = boto3.client('ec2', region_name=region)
    response = ec2client.describe_instances()

    reservations = response['Reservations']

    return reservations


if __name__ == "__main__":
    instances = describe_ec2_instances_in_region('us-east-2')
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(instances)
