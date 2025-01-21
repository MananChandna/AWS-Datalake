CREATE FUNCTION AdjustSentimentScore(sentiment STRING, score DOUBLE)
RETURNS DOUBLE
USING 'arn:aws:lambda:ap-south-1:522814703979:function:YourLambdaFunction';
