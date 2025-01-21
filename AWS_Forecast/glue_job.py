from pyspark.sql.functions import date_format

cleaned_data = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://manan-data-lake-bucket/cleaned-data/"]},
    format="parquet"
).toDF()

forecast_data = cleaned_data.groupBy("timestamp", "sentiment").count().withColumnRenamed("count", "value")
forecast_data = forecast_data.withColumn("metric", forecast_data["sentiment"])
forecast_data = forecast_data.withColumn("timestamp", date_format(forecast_data["timestamp"], "yyyy-MM-dd HH:mm:ss"))

forecast_data.write.csv("s3://manan-data-lake-bucket/forecast-data/", header=True)
