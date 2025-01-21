from sagemaker.model import ModelPackage

model_package = ModelPackage(
    role="MachineLearningRole",
    model_package_arn=latest_model_package_arn
)

predictor = model_package.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large"
)
