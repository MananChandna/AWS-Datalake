import boto3
import json

sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    messages = sqs_client.receive_message(
        QueueUrl='https://sqs.ap-south-1.amazonaws.com/522814703979/data-ingestion-queue',
        MaxNumberOfMessages=10
    )

    for message in messages.get('Messages', []):
        tweet = json.loads(message['Body'])
        sqs_client.delete_message(
            QueueUrl='https://sqs.ap-south-1.amazonaws.com/522814703979/data-ingestion-queue',
            ReceiptHandle=message['ReceiptHandle']
        )
