import boto3


def get_regions(aws_region='us-east-1'):
    """Returns a list of all security-groups Regions"""
    ec2 = boto3.client('ec2', region_name=aws_region)
    response = ec2.describe_regions()

    regions = []

    for k in response['Regions']:
        regions.append(k['RegionName'])

    return regions


if __name__ == "__main__":
    for region in get_regions():
        print(region)
