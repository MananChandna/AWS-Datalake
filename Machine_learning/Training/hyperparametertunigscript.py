from sagemaker.tuner import HyperparameterTuner, ContinuousParameter, IntegerParameter

hyperparameter_ranges = {
    'learning_rate': ContinuousParameter(0.0001, 0.1),
    'batch_size': IntegerParameter(16, 128)
}

tuner = HyperparameterTuner(
    estimator=estimator,
    objective_metric_name='validation:accuracy',
    hyperparameter_ranges=hyperparameter_ranges,
    max_jobs=20,
    max_parallel_jobs=5
)

tuner.fit({'train': 's3://manan-data-lake-bucket/cleaned-data/'})
