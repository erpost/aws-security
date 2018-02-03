import boto3
import os
import aws
import logging
from logging.handlers import RotatingFileHandler

path = os.path.join(os.path.dirname(__file__), 'logs/')
logfile = os.path.join(path, 'cloud-monitor.log')

if os.path.isdir(path):
    pass
else:
    os.mkdir(path)

logger = logging.getLogger("Rotating Log")
log_formatter = logging.Formatter('%(asctime)s\t %(levelname)s %(message)s')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(logfile, maxBytes=5*1024*1024, backupCount=5)
handler.setFormatter(log_formatter)
logger.addHandler(handler)

cloudtrails_dict = {}
sendemail = False

for aws_region in aws.get_regions():

    client = boto3.client('cloudtrail', region_name=aws_region)
    cloudtrails = client.describe_trails()['trailList']

    for cloudtrail in cloudtrails:
        if aws_region == cloudtrail['HomeRegion']:
            status = client.get_trail_status(Name=cloudtrail['TrailARN'])
            if status['IsLogging'] is False:
                response = client.start_logging(Name=cloudtrail['TrailARN'])
                sendemail = True
                logger.warning('CloudTrail disabled: {}'.format(cloudtrail['TrailARN']))

if sendemail:
    subject = 'CloudTrail Disabled!'
    body_text = 'CloudTrail(s) were disabled and attempted to be re-enabled.  See logs for additional information.'
    aws.send_email(subject, body_text)
else:
    logger.info('No CloudTrail issues found')
