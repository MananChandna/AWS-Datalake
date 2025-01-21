schemaVersion: "0.3"
description: "Redeploy a Lambda function that has failed."
assumeRole: "{{ AutomationAssumeRole }}"
parameters:
  FunctionName:
    type: String
    description: "The name of the Lambda function to redeploy."
mainSteps:
  - name: redeployLambda
    action: "aws:executeScript"
    inputs:
      Runtime: "python3.8"
      Handler: "redeploy_function"
      Script: |
        import boto3

        def redeploy_function(event, context):
            client = boto3.client('lambda')
            response = client.publish_version(
                FunctionName=event['FunctionName']
            )
            return {"Version": response['Version']}
      InputPayload:
        FunctionName: "{{ FunctionName }}"
