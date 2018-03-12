from logging.handlers import RotatingFileHandler

import boto3
import os
import aws
import logging


# Removes World-accessible permissions

path = os.path.expanduser('~/python-logs')
logfile = os.path.expanduser('~/python-logs/security.log')

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

alert = False

boto3.setup_default_session()
s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)
