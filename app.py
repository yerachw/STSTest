import boto3

# The calls to AWS STS AssumeRole must be signed with the access key ID
# and secret access key of an existing IAM user or by using existing temporary
# credentials such as those from antoher role. (You cannot call AssumeRole
# with the access key for the root account.) The credentials can be in
# environment variables or in a configuration file and will be discovered
# automatically by the boto3.client() function. For more information, see the
# Python SDK documentation:
# http://boto3.readthedocs.org/en/latest/guide/sqs.html

# create an STS client object that represents a live connection to the
# STS service
sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.
assumedRoleObject = sts_client.assume_role(
    RoleArn="arn:aws:iam::613123897682:role/ststest",
    RoleSessionName="aec96c30-4784-11e6-bdf4-0800200c9a66",
    Policy='{"Version":"2012-10-17", "Statement": [ {"Effect": "Allow", "Action": ["s3:GetBucketLocation", "s3:ListAllMyBuckets"], "Resource": "arn:aws:s3:::*"}, {"Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": ["arn:aws:s3:::hasdemo"]}, {"Effect": "Allow", "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"], "Resource":["arn:aws:s3:::hasdemo/aec96c30-4784-11e6-bdf4-0800200c9a66/*"]} ]}'
)


# From the response that contains the assumed role, get the temporary
# credentials that can be used to make subsequent API calls
credentials = assumedRoleObject['Credentials']

# Use the temporary credentials that AssumeRole returns to make a
# connection to Amazon S3
s3_resource = boto3.resource(
    's3',
    aws_access_key_id = credentials['AccessKeyId'],
    aws_secret_access_key = credentials['SecretAccessKey'],
    aws_session_token = credentials['SessionToken'],
)

# Use the Amazon S3 resource object that is now configured with the
# credentials to access your S3 buckets.
for bucket in s3_resource.buckets.all():
    print(bucket.name)

data = open('/Users/roni/Pictures/IMG-20160211-WA0020.jpg', 'rb')
s3_resource.Bucket('hasdemo').put_object(Key='aec96c30-4784-11e6-bdf4-0800200c9a66/test.jpg', Body=data)