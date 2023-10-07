# ----------------------------
# |  GPT-4 work as a teather to |
# |
# |
# |
# |
# ----------------------------
import openai
import os
import json
import time
from prompt import TeacherPrompt
openai.api_base = "https://api.openai.com/v1/"
openai.api_key = "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"
gpt3_engine = "gpt-4"
gpt3_CoT_max_tokens =2000
engine_temperature = 0
engine_topP = 0
time_delay = 1
json_input = "./question.json"

messages = [
    {"role": "system", "content": TeacherPrompt},
    {"role": "user", "content": ""}
    ]

if __name__ == '__main__':
    print("Start Working")
    start = time.time()
    with open(json_input, 'r',encoding='utf-8') as f:
        data = json.load(f)
        print("Finishing loading")
    for datum in data.values():
        for k,v in datum.items():
            for i in v.values():
                question = f""" "Problem Description":"{i["Problem description"]}".
                                "Standard Answer":"{i["Teacher_Answer"]}".
                                "Student Answer":"{i["Student_Answer"]}".
                            """
                messages[-1]["content"] = question

                time.sleep(time_delay) #to avoid an openai.error.RateLimitError
                gpt3_CoT_output = openai.ChatCompletion.create(model = gpt3_engine,
                                                            messages = messages,
                                                            max_tokens = gpt3_CoT_max_tokens,
                                                            temperature = engine_temperature,
                                                            top_p = engine_topP)
                print('GPT-3 API call time: ' + str(time.time()-start) + '\n')
                print(i["Teacher_Answer"],i["Student_Answer"])
                print(gpt3_CoT_output["choices"][0]['message']['content'])
                i["Comparative_Result"] = gpt3_CoT_output["choices"][0]['message']['content']
                break
            break
        break
    with open("./question2.json", 'w') as f:
        f.write(json.dumps(data,indent=4,ensure_ascii=False))
    print("Finished")




