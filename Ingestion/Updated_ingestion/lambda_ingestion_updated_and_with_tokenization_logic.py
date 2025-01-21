import boto3
import json
import os
import re
import uuid
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
comprehend_client = boto3.client('comprehend')
dynamodb = boto3.client('dynamodb')

def tokenize(value):
    try:
        response = dynamodb.get_item(
            TableName='TokenMapping',
            Key={'OriginalValue': {'S': value}}
        )
        if 'Item' in response:
            return response['Item']['Token']['S']
        else:
            token = str(uuid.uuid4())
            dynamodb.put_item(
                TableName='TokenMapping',
                Item={
                    'OriginalValue': {'S': value},
                    'Token': {'S': token}
                }
            )
            return token
    except Exception as e:
        print(f"Error in tokenizing value '{value}': {e}")
        return None  

class TweetStreamListener(StreamListener):
    def on_data(self, data):
        try:
            tweet = json.loads(data)
            tweet_text = tweet.get("text", "")
            clean_tweet = re.sub(r'http\S+|@\S+|#\S+', '', tweet_text) 

            sentiment_response = comprehend_client.detect_sentiment(
                Text=clean_tweet,
                LanguageCode='en'
            )
            sentiment = sentiment_response['Sentiment']

            user_id = tweet.get("user", {}).get("id_str", "")
            tokenized_user_id = tokenize(user_id)

            enriched_tweet = tweet.copy()
            enriched_tweet['sentiment'] = sentiment
            if tokenized_user_id:
                enriched_tweet['tokenized_user_id'] = tokenized_user_id

            s3_key = f"{S3_KEY_PREFIX}enriched_tweet_{tweet['id']}.json"
            s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=json.dumps(enriched_tweet))

            kinesis_client.put_record(
                StreamName=KINESIS_STREAM_NAME,
                Data=json.dumps(enriched_tweet),
                PartitionKey="partition_key"
            )
        except Exception as e:
            print(f"Error processing tweet: {e}")

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        return False

def lambda_handler(event, context):
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    stream = Stream(auth, TweetStreamListener())

    stream.filter(track=['positive', 'negative', 'neutral'])
