from sagemaker import ClarifyProcessor

clarify_processor = ClarifyProcessor(
    role="MachineLearningRole",
    instance_count=1,
    instance_type="ml.m5.xlarge",
    sagemaker_session=sagemaker.Session()
)
