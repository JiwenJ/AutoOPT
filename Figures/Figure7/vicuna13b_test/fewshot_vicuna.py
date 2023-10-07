import openai
import pandas as pd
import time

import os
import pandas as pd


os.environ["OPENAI_API_KEY"] = ""
openai.api_key = os.getenv('OPENAI_API_KEY')
few_shots=2
import json
openai.api_base = "http://127.1.1.1:8000/v1"  
gpt3_time_delay = 1
CoT = "Let's think step by step."
gpt3_engine = "gpt-3.5-turbo"
gpt3_CoT_max_tokens =2000
engine_temperature = 0
engine_topP = 0
questions_per_course=35

def Few_shot_GPT(problems,questions_per_course,few_shots):
    for i in range(questions_per_course):
        if problems[str(i+1)]['GPT3.5_M@1']==0:
            oneshot_question=problems[str(i+1)]['Problem description']
            #oneshot
            oneshot_example={'Q':[problems[str(problems[str(i+1)]['similar questions'][i])]['Problem description'] for i in range(few_shots)],
                                'A':[problems[str(problems[str(i+1)]['similar questions'][i])]['Modeling'] for i in range(few_shots)]}

            print("Running GPT-3 CoT few-shot on "  + ' question ' + str(i+1) + '...')
            start = time.time()
            time.sleep(gpt3_time_delay) #to avoid an openai.error.RateLimitError
            gpt3_CoT_input=''
            for i in range(few_shots):
                gpt3_CoT_input+='Q: ' + oneshot_example['Q'][i] + '\nA: '+oneshot_example['A'][i]  + '\n'
            gpt3_CoT_input+='Q: ' + oneshot_question + "\nA: "
            prompt='''
            Imagine you are an expert in optimization and mathematical modeling.
            I will give you a practical optimization problem and you are supposed to establish a mathematical model of it correctly.
            First you should model the problem by defining the decision variables,
            objective function and all constraints in it (formulated in LaTeX).
            Then you need to identify the type of this problem, such as Linear Programming, Quadratic Programming,
            Integer Programming, Mixed Integer Programming, or Combinatorial Optimization Problem, etc.
            Here are additional points to consider when giving your answer:
            (1) Your responses should be informative, logical and reasonable;
            (2) When you define the constraints, make sure you consider all possible situations;
            (3) You are supposed to establish the mathematical model as simple as possible;
            (4) You should give thoroughly and comprehensively explanations about why you model the problem this way.
            '''
            messages = [{"role": "system", "content" :prompt},
            {"role": "user", "content" : gpt3_CoT_input}]
            # gpt3_CoT_input = 'Q: ' + oneshot_example['Q'] + '\nA: '  + '\n\nQ: ' + original_question + "\nA: "  + CoT
            gpt3_CoT_output = openai.ChatCompletion.create(model = gpt3_engine,
                                                        messages = messages,
                                                        max_tokens = gpt3_CoT_max_tokens,
                                                        temperature = engine_temperature,
                                                        top_p = engine_topP)
            print('GPT-3 API call time: ' + str(time.time()-start) + '\n')
            if few_shots==1:
                problems[str(i+1)]['One-shot']=gpt3_CoT_output["choices"][0]['message']['content']
            else:
                problems[str(i+1)]['Few-shot']=gpt3_CoT_output["choices"][0]['message']['content']
            # print(gpt3_CoT_output)
    return problems
with open('problemsv4.json', 'r', encoding='utf-8') as fp:
# Load the JSON to a Python dict
    problems = json.load(fp)
problems=Few_shot_GPT(problems,questions_per_course,1)
problems=Few_shot_GPT(problems,questions_per_course,2)
with open('problemsv5.json', 'w', encoding='utf-8') as fp:  # Added encoding='utf-8'
    json.dump(problems, fp, indent=4)