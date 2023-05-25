from flask import Flask,jsonify,request
from collections import OrderedDict
import re,json

app= Flask(__name__)

def isFileInFormat(file,file_path):
    with open(file_path+"/"+file,'r') as file:
        first_line=file.readline()
        if (first_line!="product,amount\n"):
            return False
        else:
            lines=file.readlines()
            for line in lines[1:]:
                x=re.search('^\w+,\d+$',line)
                if(x):
                    pass
                else:
                    return False
        return True
def claculate_sum(file,product,file_path):
    total_sum=0
    with open(file_path+"/"+file,'r') as file_content:
        lines=file_content.readlines()
        for line in lines[1:]:
            item=line.split(",")
            if item[0]==product:
                total_sum+=int(item[1])
    return total_sum

@app.route('/findsum', methods=['POST'])
def find_sum():
    input_json = request.get_json()
    file = input_json['file']
    product=input_json['product']
    file_path="/my_files"

    if(isFileInFormat(file,file_path)):
        return jsonify({'file':file,'sum':claculate_sum(file,product,file_path)})
    else:
        return jsonify({'file':file,'error':"Input file not in CSV format."})


if __name__=="__main__":
    app.run(host='0.0.0.0',port=8080)