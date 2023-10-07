import openai
import pandas as pd
import time
import os
import pandas as pd
import json
import tiktoken
questions_per_course=35

def generate(problems,questions_per_course,few_shots):
    for i in range(questions_per_course):
        print("Here")
        oneshot_question=problems[str(i+1)]['Problem description']
        oneshot_example={'Q':[problems[str(problems[str(i+1)]['similar questions'][i])]['Problem description'] for i in range(few_shots)],
                            'A':[problems[str(problems[str(i+1)]['similar questions'][i])]['Modeling'] for i in range(few_shots)]}
        if few_shots == 1:
            print("Running GPT-3 one-shot on "  + ' question ' + str(i+1) + '...')
        elif few_shots == 2:
            print("Running GPT-3  few-shot on "  + ' question ' + str(i+1) + '...')
        elif few_shots == 0:
                print("Running GPT-3 Zero-shot on "  + 'question ' + str(i+1) + '...')
        gpt3_CoT_input=''
        for j in range(few_shots):
            gpt3_CoT_input+='Q: ' + oneshot_example['Q'][j] + '\nA: '+oneshot_example['A'][j]  + '\n'
        gpt3_CoT_input+='Q: ' + oneshot_question + "\nA: "
        enc = tiktoken.get_encoding("gpt2")
        # 字节对编码过程，我的输出是[31373, 995]
        num = len(enc.encode(gpt3_CoT_input))
        problems[str(i+1)]['prompt_'+str(few_shots)] = gpt3_CoT_input
        problems[str(i+1)]['prompt_token_len_'+str(few_shots)] = num
    return problems


with open('problemsv6.json', 'r', encoding='utf-8') as fp:
# Load the JSON to a Python dict
    problems = json.load(fp)
try:

    problems = generate(problems,questions_per_course,0)
    problems = generate(problems,questions_per_course,1)
    problems = generate(problems,questions_per_course,2)
    with open('problemsv8.json', 'w', encoding='utf-8') as fp:  # Added encoding='utf-8'
        json.dump(problems, fp, indent=4)
    # problems=Few_shot_GPT(problems,questions_per_course,2)
except:
    print('------error--------')
    with open('problemsv8.json', 'w', encoding='utf-8') as fp:  # Added encoding='utf-8'
        json.dump(problems, fp, indent=4)

