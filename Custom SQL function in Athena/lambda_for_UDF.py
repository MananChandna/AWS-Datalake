import json

def lambda_handler(event, context):
    records = event['records']
    results = []
    for record in records:
        payload = json.loads(record['data'])
        sentiment = payload.get('sentiment')
        score = payload.get('score', 1)
        result = {
            "sentiment": sentiment,
            "adjusted_score": score * 1.5  
        }
        results.append({
            "recordId": record['recordId'],
            "result": "Ok",
            "data": json.dumps(result)
        })
    return {"records": results}
