# 本文件自动化处理 json 文件，添加属性等

import os
import json
json_input = "./question.json"
json_output = "./question1.json"

attributes = {
            "Teacher_Answer":"",
            "Student_Answer":"",
            "Comparative_Result":"",
            }

if __name__ == '__main__':
    with open(json_input, 'r',encoding='utf-8') as f:
        data = json.load(f)
    print("Start")
    for datum in data.values():
        for k,v in datum.items():
            for i in v.values():
                for attr, value in attributes.items():
                    i[attr] = value
    with open(json_output, 'w') as f:
        f.write(json.dumps(data,indent=4,ensure_ascii=False))
    print("Finished")
