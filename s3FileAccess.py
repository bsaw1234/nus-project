 import botocore.session
 import boto3

def get_bucket_data(bucketname):
   
    session = botocore.session.get_session()
    accesskey=session.get_credentials().access_key
    secretkey=session.get_credentials().secret_key
    s3 = boto3.resource('s3',aws_access_key_id=accesskey, aws_secret_access_key=secretkey)
    bucket = s3.Bucket(bucketname)
    for obj in bucket.objects.all():
        key = obj.key
        body = obj.get()['Body'].read()
        print(body)

get_bucket_data('appbkp')
