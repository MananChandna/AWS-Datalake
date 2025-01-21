import boto3
import json
import os
import re
from tweepy import OAuthHandler, Stream, StreamListener

TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
S3_BUCKET = "manan-data-lake-bucket"
S3_KEY_PREFIX = "raw-data/"
KINESIS_STREAM_NAME = "data-ingestion-stream"

s3_client = boto3.client('s3')
kinesis_client = boto3.client('kinesis')

class TweetStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        tweet_text = tweet.get("text", "")
        clean_tweet = re.sub(r'http\S+|@\S+|#\S+', '', tweet_text)  

        s3_key = f"{S3_KEY_PREFIX}tweet_{tweet['id']}.json"
        s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=json.dumps(tweet))

        kinesis_client.put_record(
            StreamName=KINESIS_STREAM_NAME,
            Data=data,
            PartitionKey="partition_key"
        )

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        return False

def lambda_handler(event, context):
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    stream = Stream(auth, TweetStreamListener())
    
    stream.filter(track=['positive', 'negative', 'neutral'])
