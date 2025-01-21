SELECT sentiment, AdjustSentimentScore(sentiment, score) AS adjusted_score
FROM sentiment_table;
