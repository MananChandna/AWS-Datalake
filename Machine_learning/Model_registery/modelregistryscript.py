from sagemaker.model import Model
from sagemaker.model import ModelPackage

model = Model(
    model_data="s3://manan-data-lake-bucket/model-outputs/model.tar.gz",
    role="MachineLearningRole",
    image_uri="522814703979.dkr.ecr.ap-south-1.amazonaws.com/sentiment-lstm"
)

model.register(
    content_types=["text/csv"],
    response_types=["application/json"],
    model_package_group_name="SentimentAnalysisGroup",
    approval_status="PendingManualApproval"
)
