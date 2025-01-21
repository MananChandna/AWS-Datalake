schemaVersion: "0.3"
description: "Restart a failed SageMaker training job."
assumeRole: "{{ AutomationAssumeRole }}"
parameters:
  TrainingJobName:
    type: String
    description: "The name of the SageMaker training job to restart."
mainSteps:
  - name: restartSageMakerTraining
    action: "aws:executeScript"
    inputs:
      Runtime: "python3.8"
      Handler: "restart_training"
      Script: |
        import boto3

        def restart_training(event, context):
            client = boto3.client('sagemaker')
            response = client.create_training_job(
                TrainingJobName=event['TrainingJobName'],
                ...
            )
            return response
      InputPayload:
        TrainingJobName: "{{ TrainingJobName }}"
