import boto3

sm_client = boto3.client("sagemaker")
response = sm_client.list_model_packages(
    ModelPackageGroupName="SentimentAnalysisGroup",
    ModelApprovalStatus="Approved"
)

latest_model_package_arn = response["ModelPackageSummaryList"][0]["ModelPackageArn"]
print(latest_model_package_arn)
