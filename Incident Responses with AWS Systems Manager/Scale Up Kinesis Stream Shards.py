schemaVersion: "0.3"
description: "Automatically increase the shard count for a Kinesis data stream."
assumeRole: "{{ AutomationAssumeRole }}"
parameters:
  StreamName:
    type: String
    description: "The name of the Kinesis data stream."
  TargetShards:
    type: Integer
    description: "The new number of shards for the stream."
mainSteps:
  - name: scaleUpKinesis
    action: "aws:executeScript"
    inputs:
      Runtime: "python3.8"
      Handler: "scale_stream"
      Script: |
        import boto3

        def scale_stream(event, context):
            client = boto3.client('kinesis')
            response = client.update_shard_count(
                StreamName=event['StreamName'],
                TargetShardCount=event['TargetShards'],
                ScalingType='UNIFORM_SCALING'
            )
            return response
      InputPayload:
        StreamName: "{{ StreamName }}"
        TargetShards: "{{ TargetShards }}"
