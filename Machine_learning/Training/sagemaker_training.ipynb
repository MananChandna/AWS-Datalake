import sagemaker
import boto3
from sagemaker.pytorch import PyTorch
import os

s3_bucket = "manan-data-lake-bucket"
s3_cleaned_data = f"s3://{s3_bucket}/cleaned-data/train.csv"
s3_model_output = f"s3://{s3_bucket}/model-outputs/"

# Initialize SageMaker PyTorch Estimator for LSTM model
pytorch_estimator = PyTorch(
    entry_point="train.py",
    role="MachineLearningRole",
    instance_type="ml.m5.large",
    framework_version="1.8.1",
    py_version="py3",
    output_path=s3_model_output
)

pytorch_estimator.fit({"train": s3_cleaned_data})
