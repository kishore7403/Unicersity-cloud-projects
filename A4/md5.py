import json
import hashlib
import requests

def lambda_handler(event, context):
    text = event['input']['value']
    
    md5_hash = hashlib.md5()

  
    md5_hash.update(text.encode('utf-8'))

    md5_value = md5_hash.hexdigest()

    result = {
        "banner": "B00934548",
        "result": md5_value,
        "arn": context.invoked_function_arn,
        "action": event['input']['action'],
        "value": text
    }
    result_json = json.dumps(result)
    url = "https://v7qaxwoyrb.execute-api.us-east-1.amazonaws.com/default/end"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=result_json)


    if response.status_code == 200:
        print("Request successful.")
    else:
        print(f"Request failed:{response.status_code}")
        
    return result
