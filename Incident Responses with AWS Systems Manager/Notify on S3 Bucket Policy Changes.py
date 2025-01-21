schemaVersion: "0.3"
description: "Send an SNS notification if an S3 bucket policy is modified."
assumeRole: "{{ AutomationAssumeRole }}"
parameters:
  BucketName:
    type: String
    description: "The name of the S3 bucket to monitor."
  TopicArn:
    type: String
    description: "The ARN of the SNS topic for notifications."
mainSteps:
  - name: checkBucketPolicy
    action: "aws:executeScript"
    inputs:
      Runtime: "python3.8"
      Handler: "monitor_bucket_policy"
      Script: |
        import boto3

        def monitor_bucket_policy(event, context):
            s3 = boto3.client('s3')
            sns = boto3.client('sns')

            try:
                policy = s3.get_bucket_policy(Bucket=event['BucketName'])
                message = f"Bucket policy for {event['BucketName']} was modified: {policy}"
                sns.publish(TopicArn=event['TopicArn'], Message=message)
            except Exception as e:
                sns.publish(TopicArn=event['TopicArn'], Message=f"Error: {str(e)}")
      InputPayload:
        BucketName: "{{ BucketName }}"
        TopicArn: "{{ TopicArn }}"
