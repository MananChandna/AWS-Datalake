SELECT date_format(timestamp, '%Y-%m-%d') AS date, sentiment, COUNT(*) AS sentiment_count
FROM cleaned_data_table
GROUP BY date, sentiment
ORDER BY date;

SELECT user_id, sentiment, COUNT(*) AS tweet_count
FROM cleaned_data_table
GROUP BY user_id, sentiment
ORDER BY tweet_count DESC
LIMIT 10;
