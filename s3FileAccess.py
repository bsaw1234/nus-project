import boto3 as boto3

s3 = boto3.resource('s3',aws_access_key_id='AKIAR5SIOW5FPO6A7IFA', aws_secret_access_key='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')
bucket = s3.Bucket('bsaw-client-info')
for obj in bucket.objects.all():
    key = obj.key
    body = obj.get()['Body'].read()
    print(body)
