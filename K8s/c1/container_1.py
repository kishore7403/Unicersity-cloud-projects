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

def validate_json(data):
    if data is None or 'file' not in data or not isinstance(data['file'], str) or data['file'] == '':
        return False
    return True

app= Flask(__name__)

@app.route('/calculate',methods=['POST'])
def calculate():
    input_json=request.get_json()
    file = input_json['file']
    if(file=="" or isFileNull(file) ):
        output_json = OrderedDict([('file', None),('error', "Invalid JSON input.")])
    # file_path="C:\\Users\\AVuser\\Desktop\\cloud 5409\\Kuberenetes Assignment\\K2"
    else:
        file_path="/kishoreganesh_PV_dir"
        product=input_json['product']
        if (isFileExist(file,file_path)):
            incoming_json=requests.post('http://combined-service:8080/findsum', json={'file': file,'product':product})
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

@app.route('/store-file',methods=['POST'])
def store_file():
    # try:
    #     input_json= request.get_json()
    # except Exception as e:
    #     return {
    #         "file": None,
    #         "error": "Invalid JSON input.12"
    #     }
    # try:
    #     file=input_json['file']
    # except:
    #     return {
    #             "file": None,
    #             "error": "Invalid JSON input."
    #         }
    input_json= request.get_json()
    file=input_json['file']
    if file==None:
        return OrderedDict([('file', file),('error',"Invalid JSON input.")])
    
   
    elif(file is not None):
        file_path="/kishoreganesh_PV_dir"
        # file_path="C:\\Users\\AVuser\\Desktop\\k8s"
        data=input_json['data']
        file_object = open(file_path+"/"+file, "w")
        file_object.write(data)
        file_object.close()
        return OrderedDict([('file', file),('message', "Success.")])

    else:
        return OrderedDict([('file', file),('error', "Error while storing the file to the storage.")])

    # json_data = json.dumps(output_json)
    # return  Response(json_data, mimetype='application/json')
    #comment
    #comment


if __name__=="__main__":
    app.run(host='0.0.0.0',port=6000)
