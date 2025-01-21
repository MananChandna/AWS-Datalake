clarify_processor.run_explainability(
    data_config=data_config,
    model_config=model_config,
    explainability_config={
        "shap_config": {
            "baseline": "zero",  
            "num_samples": 100  
        }
    }
)
