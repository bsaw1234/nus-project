import boto3 as boto3

s3 = boto3.resource('s3',aws_access_key_id='AKIA2I4L5O2NZ532672T', aws_secret_access_key='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')
bucket = s3.Bucket('bsaw-client-info')
for obj in bucket.objects.all():
    key = obj.key
    body = obj.get()['Body'].read()
    print(body)