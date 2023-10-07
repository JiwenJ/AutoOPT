import openai
import pandas as pd
import time

import os
import pandas as pd


os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv('OPENAI_API_KEY')
few_shots=2
import json

gpt3_time_delay = 1
CoT = "Let's think step by step."
gpt3_engine = "gpt-3.5-turbo"
gpt3_CoT_max_tokens =2000
engine_temperature = 0
engine_topP = 0
questions_per_course=35

def Few_shot_GPT(problems,questions_per_course,few_shots):
    for i in range(24,26):
        if problems[str(i+1)]['Modeling'] != '':
            print("Already have anwser, Q number:{}".format(i+1))
            continue
        oneshot_question=problems[str(i+1)]['Problem description']
        #oneshot
        oneshot_example={'Q':[problems[str(problems[str(i+1)]['similar questions'][i])]['Problem description'] for i in range(few_shots)],
                            'A':[problems[str(problems[str(i+1)]['similar questions'][i])]['Modeling'] for i in range(few_shots)]}
        if few_shots == 1:
            print("Running GPT-3 one-shot on "  + ' question ' + str(i+1) + '...')
        elif few_shots == 2:
            print("Running GPT-3  few-shot on "  + ' question ' + str(i+1) + '...')
        elif few_shots == 0:
                print("Running GPT-3 Zero-shot on "  + 'question ' + str(i+1) + '...')
        start = time.time()
        time.sleep(gpt3_time_delay) #to avoid an openai.error.RateLimitError
        gpt3_CoT_input=''
        for j in range(few_shots):
            gpt3_CoT_input+='Q: ' + oneshot_example['Q'][j] + '\nA: '+oneshot_example['A'][j]  + '\n'
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
        # print(gpt3_CoT_input)
        # gpt3_CoT_input = 'Q: ' + oneshot_example['Q'] + '\nA: '  + '\n\nQ: ' + original_question + "\nA: "  + CoT
        gpt3_CoT_output = openai.ChatCompletion.create(model = gpt3_engine,
                                                    messages = messages,
                                                    max_tokens = gpt3_CoT_max_tokens,
                                                    temperature = engine_temperature,
                                                    top_p = engine_topP)
        print('GPT-3 API call time: ' + str(time.time()-start) + '\n')
        print("Total tokens: {}".format(gpt3_CoT_output["usage"]["total_tokens"]))
        print("Prompt token: {}".format(gpt3_CoT_output['usage']['prompt_tokens']))
        print("Completion token: {}\n\n".format(gpt3_CoT_output['usage']['completion_tokens']))
        # print(gpt3_CoT_output["choices"][0]['message']['content'])
        if few_shots == 1:
            problems[str(i+1)]['One-shot']=gpt3_CoT_output["choices"][0]['message']['content']
        elif few_shots == 0:
            problems[str(i+1)]['Modeling']=gpt3_CoT_output["choices"][0]['message']['content']
        elif few_shots == 2:
            problems[str(i+1)]['Few-shot']=gpt3_CoT_output["choices"][0]['message']['content']
        # print(gpt3_CoT_output)
    return problems
with open('problemsv6.json', 'r', encoding='utf-8') as fp:
# Load the JSON to a Python dict
    problems = json.load(fp)
try:
    # problems=Few_shot_GPT(problems,questions_per_course,1)
    problems=Few_shot_GPT(problems,questions_per_course,0)
    problems=Few_shot_GPT(problems,questions_per_course,1)
    problems=Few_shot_GPT(problems,questions_per_course,2)
    with open('problemsv6-1.json', 'w', encoding='utf-8') as fp:  # Added encoding='utf-8'
        json.dump(problems, fp, indent=4)
    # problems=Few_shot_GPT(problems,questions_per_course,2)
except:
    print('------error--------')
    with open('problemsv6-1.json', 'w', encoding='utf-8') as fp:  # Added encoding='utf-8'
        json.dump(problems, fp, indent=4)

