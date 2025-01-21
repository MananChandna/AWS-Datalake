import boto3

sqs_client = boto3.client('sqs')
queue_url = 'https://sqs.ap-south-1.amazonaws.com/522814703979/data-ingestion-queue'

def publish_to_sqs(tweet):
    sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(tweet)
    )

enriched_tweet['sentiment'] = sentiment
publish_to_sqs(enriched_tweet)
