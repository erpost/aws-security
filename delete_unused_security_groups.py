import aws

for region in aws.get_regions():
    print(region)
    print(aws.get_security_groups_in_region(region))
