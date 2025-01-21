schemaVersion: "0.3"
description: "Purge all messages from an SQS queue."
assumeRole: "{{ AutomationAssumeRole }}"
parameters:
  QueueUrl:
    type: String
    description: "The URL of the SQS queue to purge."
mainSteps:
  - name: purgeQueue
    action: "aws:executeScript"
    inputs:
      Runtime: "python3.8"
      Handler: "purge_queue"
      Script: |
        import boto3

        def purge_queue(event, context):
            client = boto3.client('sqs')
            response = client.purge_queue(QueueUrl=event['QueueUrl'])
            return {"Status": "Queue purged successfully"}
      InputPayload:
        QueueUrl: "{{ QueueUrl }}"
