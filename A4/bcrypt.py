import json
import bcrypt
import requests

def lambda_handler(event, context):
    
    text = event['input']['value']
    bytes = text.encode('utf-8')
    salt = bcrypt.gensalt()
    bcrypt_value = bcrypt.hashpw(bytes, salt)
    
    result = {
        "banner": "B00934548",
        "result": bcrypt_value.decode('utf-8'),  
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
        print(f"Request failed: {response.status_code}")

    return result