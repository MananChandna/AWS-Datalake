# AWS-Datalake-Code-Components
This repository is only meant to store the pipeline code components of my aws datalake
<!DOCTYPE html>
<html>
<head>
 AWS Data Lake Project - Sentiment Analysis on Twitter Data
</head>
<body>

<h1>AWS Data Lake Project - Real-Time Sentiment Analysis on Twitter Data</h1>

<p>This project demonstrates the end-to-end setup of a secure AWS-based data lake that ingests real-time Twitter data, processes it for sentiment analysis, and uses Amazon SageMaker to train an LSTM model to predict sentiment (positive, negative, neutral) in tweets.</p>

<h2>Project Structure</h2>
<pre>
project/
├── ingestion/
│   └── lambda_ingestion.py
├── transformation/
│   └── glue_etl_job.py
├── analytics/
│   └── athena_queries.sql
├── machine_learning/
│   ├── sagemaker_training.ipynb
│   └── train.py
├── policies/
│   ├── KMS_policy.json
│   └── S3_bucket_policy.json
└── README.md
</pre>

<h2>File Descriptions</h2>

<h3>1. Data Ingestion (Kinesis & Lambda)</h3>
<ul>
  <li><strong>File:</strong> <code>ingestion/lambda_ingestion.py</code></li>
  <li><strong>Description:</strong> Lambda function collects tweets in real-time from Twitter's API based on specific keywords, processes each tweet, and writes it to S3 for further processing. Also sends data to a Kinesis stream for real-time processing.</li>
  <li><strong>Core Functions:</strong>
    <ul>
      <li>Fetches tweets based on keywords, removes URLs, and writes raw JSON data to the <code>/raw-data</code> folder in S3.</li>
    </ul>
  </li>
</ul>

<h3>2. Data Transformation (AWS Glue)</h3>
<ul>
  <li><strong>File:</strong> <code>transformation/glue_etl_job.py</code></li>
  <li><strong>Description:</strong> Glue ETL script processes and cleans raw tweet data by removing mentions, hashtags, URLs, and special characters, performing text normalization and tokenization. The cleaned data is stored in the <code>/cleaned-data</code> directory in S3 for model training.</li>
  <li><strong>Core Functions:</strong>
    <ul>
      <li>Standardizes text and removes unwanted characters to prepare for analysis.</li>
      <li>Writes cleaned data to the <code>/cleaned-data</code> directory in S3.</li>
    </ul>
  </li>
</ul>

<h3>3. Data Analytics (Amazon Athena)</h3>
<ul>
  <li><strong>File:</strong> <code>analytics/athena_queries.sql</code></li>
  <li><strong>Description:</strong> SQL queries for analyzing the cleaned data stored in S3. Queries calculate the daily sentiment distribution and identify top contributors for each sentiment category.</li>
  <li><strong>Example Queries:</strong>
    <ul>
      <li>Get average sentiment count per day.</li>
      <li>Identify users who contribute most tweets to each sentiment category.</li>
    </ul>
  </li>
</ul>

<h3>4. Machine Learning (Amazon SageMaker)</h3>
<ul>
  <li><strong>Files:</strong>
    <ul>
      <li><code>machine_learning/sagemaker_training.ipynb</code> - Jupyter notebook for SageMaker training and deployment of an LSTM model.</li>
      <li><code>machine_learning/train.py</code> - Script used within SageMaker to train the LSTM model.</li>
    </ul>
  </li>
  <li><strong>Description:</strong> The notebook trains an LSTM model on the cleaned tweet data to predict sentiment. The trained model is deployed for real-time sentiment analysis on new tweets.</li>
  <li><strong>Output:</strong> Model artifacts are stored in the <code>/model-outputs</code> directory in S3, encrypted using KMS.</li>
</ul>

<h3>5. Policies</h3>
<ul>
  <li><strong>Folder:</strong> <code>policies/</code></li>
  <li><strong>Files:</strong>
    <ul>
      <li><code>KMS_policy.json</code> - Defines permissions for KMS encryption, enabling secure data storage.</li>
      <li><code>S3_bucket_policy.json</code> - Enforces server-side encryption for all S3 objects and restricts access by IAM roles.</li>
    </ul>
  </li>
</ul>

<h2>Setup Instructions</h2>

<h3>1. IAM Roles</h3>
<ul>
  <li>Create and configure IAM roles as specified:
    <ul>
      <li><strong>DataIngestionRole</strong> - For Kinesis and Lambda, grants access to Twitter API, S3, and Kinesis.</li>
      <li><strong>DataProcessingRole</strong> - For Glue, grants S3 read/write access and Glue Data Catalog permissions.</li>
      <li><strong>AnalyticsRole</strong> - For Athena, grants access to query <code>/cleaned-data</code>.</li>
      <li><strong>MachineLearningRole</strong> - For SageMaker, grants access to train and store models in S3.</li>
    </ul>
  </li>
</ul>

<h3>2. S3 Bucket Configuration</h3>
<ul>
  <li>Create the main S3 bucket, <code>manan-data-lake-bucket</code>, with folders <code>/raw-data</code>, <code>/cleaned-data</code>, <code>/processed-data</code>, and <code>/model-outputs</code>.</li>
  <li>Apply the S3 bucket policy to enforce encryption and access restrictions as per <code>S3_bucket_policy.json</code>.</li>
</ul>

<h3>3. Kinesis and Lambda Setup</h3>
<ul>
  <li>Set up the Kinesis data stream and configure the Lambda function to use <code>lambda_ingestion.py</code> to process incoming Twitter data in real-time.</li>
</ul>

<h3>4. Glue ETL Job</h3>
<ul>
  <li>Set up AWS Glue Crawler to create a schema in the Data Catalog for <code>/raw-data</code>.</li>
  <li>Deploy <code>glue_etl_job.py</code> to clean and transform data, outputting results to <code>/cleaned-data</code>.</li>
</ul>

<h3>5. SageMaker Training and Deployment</h3>
<ul>
  <li>Upload <code>sagemaker_training.ipynb</code> and <code>train.py</code> to SageMaker.</li>
  <li>Run the notebook to train and deploy the LSTM model for real-time sentiment analysis.</li>
</ul>

<h2>Data Security and Encryption</h2>
<p>Each AWS service in this project uses role-based access control to limit permissions. S3 data is encrypted at rest with KMS, and the project uses IAM policies to enforce strict access. The model output in SageMaker is also encrypted using KMS before being stored in S3.</p>

<h2>Troubleshooting Tips</h2>
<ul>
  <li><strong>Lambda Kinesis Access Error:</strong> Ensure DataIngestionRole includes permissions for Kinesis and S3.</li>
  <li><strong>Glue ETL Schema Issues:</strong> Verify that the Glue Crawler points to <code>/raw-data</code> and data formats are consistent.</li>
  <li><strong>Athena Query Errors:</strong> Confirm that Glue Catalog schema aligns with Athena queries.</li>
  <li><strong>SageMaker Model Storage Error:</strong> Check MachineLearningRole permissions for S3 output path.</li>
</ul>

</body>
</html>
