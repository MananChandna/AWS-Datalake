from sagemaker.pytorch import PyTorch

estimator = PyTorch(
    entry_point="train.py",
    role="MachineLearningRole",
    instance_count=1,
    instance_type="ml.m5.large",
    use_spot_instances=True,
    max_wait=3600 
)
