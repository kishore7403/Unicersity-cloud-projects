import json

def lambda_handler(event, context):
    # TODO implement
    input=event['input']
    input_json=json.loads(input) #conver str to dict
    return {
        "input":input_json
        }
