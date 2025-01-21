schemaVersion: "0.3"
description: "Restart a failed AWS Glue job automatically."
assumeRole: "{{ AutomationAssumeRole }}"
parameters:
  JobName:
    type: String
    description: "The name of the Glue job to restart."
mainSteps:
  - name: restartGlueJob
    action: "aws:executeScript"
    inputs:
      Runtime: "python3.8"
      Handler: "restart_job"
      Script: |
        import boto3

        def restart_job(event, context):
            client = boto3.client('glue')
            response = client.start_job_run(JobName=event['JobName'])
            return {"JobRunId": response['JobRunId']}
      InputPayload:
        JobName: "{{ JobName }}"
