from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql.functions import year, month, regexp_replace
import re

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

raw_data = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://manan-data-lake-bucket/raw-data/"]},
    format="json"
)

def clean_text(text):
    text = re.sub(r"http\S+|@\S+|#\S+|[^A-Za-z0-9 ]+", '', text.lower())
    return text

transformed_data = raw_data.toDF()
transformed_data = (
    transformed_data
    .withColumn("cleaned_text", clean_text(transformed_data["text"]))
    .withColumn("year", year(transformed_data["timestamp"]))
    .withColumn("month", month(transformed_data["timestamp"]))
    .withColumn(
        "user_id", 
        regexp_replace(transformed_data["user_id"], r"(\d{3})\d{4}(\d{3})", r"\1****\2")
    )
)

transformed_dynamic_frame = DynamicFrame.fromDF(transformed_data, glueContext, "transformed_data")

glueContext.write_dynamic_frame.from_options(
    frame=transformed_dynamic_frame,
    connection_type="s3",
    connection_options={
        "path": "s3://manan-data-lake-bucket/cleaned-data/",
        "partitionKeys": ["year", "month"]
    },
    format="parquet",
    format_options={"compression": "snappy"}
)
