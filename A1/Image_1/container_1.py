from flask import Flask,request,Response
from collections import OrderedDict
import json,os,requests

def isFileNull(file_name):
    return file_name==None

def isFileExist(file_name,file_path):
    file_path=file_path+"/"+file_name
    return os.path.exists(file_path)

# def getsum(file,product):
#     total_sum=requests.post('http://localhost:5000/findsum', json={'file': file,'product':product})
#     return total_sum.json()['sum']


app= Flask(__name__)

@app.route('/calculate',methods=['POST'])
def calculate():
    input_json=request.get_json()
    file = input_json['file']
    product=input_json['product']
    file_path="/my_files"

    if(file=="" or isFileNull(file)):
        output_json = OrderedDict([('file', None),('error', "Invalid JSON input.")])
    else:
        if (isFileExist(file,file_path)):
            incoming_json=requests.post('http://container_2:8080/findsum', json={'file': file,'product':product})
            try:
                sum=incoming_json.json()['sum']
                output_json = OrderedDict([('file', file),('sum',sum)])
            except:
                error=incoming_json.json()['error']
                output_json = OrderedDict([('file', file),('error',error)])                
        else:
            output_json = OrderedDict([('file', file),('error',"File not found.")])
    
    json_data = json.dumps(output_json)

    return  Response(json_data, mimetype='application/json')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=6000)