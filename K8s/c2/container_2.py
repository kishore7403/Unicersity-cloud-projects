from flask import Flask,jsonify,request
import re

app= Flask(__name__)

def isFileInFormat(file, file_path):
    with open(file_path + "/" + file, 'r') as file_obj:
        lines = file_obj.readlines()
        if lines[0].strip() == "product, amount":
            for line in lines[1:]:
                parts = line.strip().split(", ")
                if len(parts) != 2 or not parts[1].isdigit():
                    return False
            return True
        else:
            return False
# def isFileInFormat(file,file_path):
#     with open(file_path+"/"+file,'r') as file_obj:
#         lines=file_obj.readlines()
#         if lines[0].strip()=="product, amount":
#             for line in lines[1:]:
#                 x=re.search('^\w+,\s\d+$',line.strip())
#                 if(x):
#                     pass
#                 else:
#                     return False
#             return True
#         else:
#             return False
def calculate_sum(file,product,file_path):
    total_sum=0
    with open(file_path+"/"+file,'r') as file_content:
        lines=file_content.readlines()
        for line in lines[1:]:
            item=line.split(", ")
            if item[0]==product:
                total_sum+=int(item[1])
    return str(total_sum)

@app.route('/findsum', methods=['POST'])
def find_sum():
    input_json = request.get_json()
    file = input_json['file']
    product=input_json['product']
    file_path="/kishoreganesh_PV_dir"

    if(isFileInFormat(file,file_path)):
        return jsonify({'file':file,'sum':calculate_sum(file,product,file_path)})
    else:
        return jsonify({'file':file,'error':"Input file not in CSV format."})


if __name__=="__main__":
    app.run(host='0.0.0.0',port=8080)

    #comment
    #comment