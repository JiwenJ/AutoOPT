import matplotlib.pyplot as plt
import json
import numpy as np
import logging
import math
import matplotlib as mpl
legend_font = {"family" : "Times New Roman"}
plt.rcParams["font.sans-serif"]=["Times New Roman"] #设置字体
font_size = 14

questions_per_subcategory = 5
continuous_sub_categories1 = ['UOP', 'LPP',
                             'QPP']
continuous_sub_categories = ['Unconstrained optimization problem', 'Linear programming',
                             'Quadratic programming']
integer_sub_categories1 = ['IPP',
                          'TSP', 'KP', 'VRP']
integer_sub_categories = ['Integer linear programming',
                          'TSP problem', 'Knapsack problem', 'VRP problem']
labels = continuous_sub_categories + integer_sub_categories
model_list = ["GPT3.5","GPT4"]
# mpl.rcParams.update(mpl.rcParamsDefault)
# mpl.rcParams['text.usetex'] = False
# plt.rc('text', usetex=True)
def preprocess(raw_data, errors):
    res = {}
    for k in labels:
        res[k] = {e:{"GPT3.5":0,"GPT4":0} for e in errors}
    logging.info("We have finished initiation")
    for v in raw_data.values():
        for k,data in v.items():
            for element in data.values():
                if element['GPT3.5_MError'] != []:
                    for err_type in element['GPT3.5_MError']:
                        res[k][err_type]["GPT3.5"] += 1
                if element['GPT4_MError'] != []:
                    for err_type in element['GPT4_MError']:
                        res[k][err_type]["GPT4"] += 1
    logging.info("We have finished counting")
    return res

def plot_error_img():

    # plot the bar map to show the modeling error type of GPT4 and GPT3.5
    # according to error message in problems.json.
    # We temporarily conclude there are types of error during modeling:
    # 1. Objective function setting error
    # 2. Objective function simplifying error
    # 3. Constraint setting error
    # 4. Constraint missing error
    # 5. Constraint redundant error
    # 6. Decision variable setting error
    labels = continuous_sub_categories + integer_sub_categories
    labels1 = continuous_sub_categories1 + integer_sub_categories1
    # error_list = ["Objective function setting error","Constraint setting error"]
    error_list = ["Objective function setting error","Objective function simplifying error","Constraint setting error",
                  "Constraint missing error","Constraint redundant error","Decision variable setting error"]
    # color_bar = {"Objective function setting error": "#FF7F0E", "Objective function simplifying error": "royalblue",
    #              "Constraint setting error": "#D62728", "Constraint missing error": "c",
    #              "Constraint redundant error": "mediumseagreen", "Decision variable setting error": "gold", }
    color_bar = {"Objective function setting error": "#F6A6FF", "Objective function simplifying error": "#ace8bc",
                "Constraint setting error": "#F8CECC", "Constraint missing error": "#d1c5f2",
                "Constraint redundant error": "#6eb5ff", "Decision variable setting error": "#fff2cc", }
    with open('problems.json', 'r', encoding='utf-8') as fp:
    # Load the JSON to a Python dict
        data = json.load(fp)
    error_count = preprocess(data,error_list)
    x = np.arange(len(labels1))  # the label locations
    width = 0.32  # the width of the bars
    gap = width*0.6
    fig, ax = plt.subplots(figsize=(18, 8))
    pre = [0, 0, 0, 0, 0, 0, 0]
    pre1 = [0, 0, 0, 0, 0, 0, 0]
    for id, model in enumerate(model_list):
        for idx,i in enumerate(error_list):
            data_list = []
            temp = 0
            for label in labels:
                temp += error_count[label][i][model]
                data_list.append(temp)
            num = len(error_list) # num = 8

            if id == 0:
                print(i)
                print(pre)
                # pass
                ax.bar(x - gap, data_list, width, label=i,color=color_bar[i],bottom=pre)
                pre = np.sum([pre, data_list], axis=0).tolist()
                if idx == len(error_list)-1:
                    print("Here")
                    for z, y in zip(range(len(pre)), pre):
                        plt.text(z-gap, y + 0.2, "GPT-3.5", ha='center', fontsize=font_size,color='black')


            else:
                # pass
                ax.bar(x + gap, data_list, width,color=color_bar[i],bottom=pre1)
                pre1 = np.sum([pre1, data_list], axis=0).tolist()
                if idx == len(error_list) - 1:
                    print("Here")
                    for z, y in zip(range(len(pre1)), pre1):
                        if y != 0:
                            plt.text(z + gap, y + 0.2, "GPT-4", ha='center', fontsize=font_size, color='black')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Count',font={'size':font_size})
    ax.set_xlabel('Problem Type',font={'size':font_size})
    plt.tick_params(labelsize=font_size)
    ax.set_title('Error for Each Type of Optimization Problem',font={'size':font_size+1})
    ax.set_xticks(x)
    ax.set_xticklabels(labels1,rotation=0,fontsize=font_size)
    ax.legend(frameon=False,prop={'size': font_size})
    plt.show()
    fig.savefig("./error.eps",dpi=600 ,bbox_inches='tight')
    fig.savefig("./error.png",dpi=600, bbox_inches='tight')
    return

def plot_volume_img():
    # plot map to show the size of each type of problem inlcluding numbers of optimized variables
    # and constraints
    def preprocess(data):
        print("Here")
        res = {}
        for k in labels:
            res[k] = {"num_dec_var":0,"num_constraint":0}
        logging.info("We have finished initiation")
        for v in data.values():
            for k,data in v.items():
                number = 0
                for num, element in data.items():
                        res[k]["num_dec_var"] += element["num_dec_var"]
                        res[k]["num_constraint"] += element["num_constraint"]
                        number = num
                res[k]["num_dec_var"] = math.log(res[k]["num_dec_var"]/int(number),2)
                res[k]["num_constraint"] = math.log(res[k]["num_constraint"]/int(number),2)
        logging.info("We have finished counting")
        return res

    with open('problems.json', 'r', encoding='utf-8') as fp:
    # Load the JSON to a Python dict
        data = json.load(fp)
    count = preprocess(data)
    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars
    fig, ax = plt.subplots(figsize=(15, 6))
    classes = ["Decsion variables","Constraints"]
    colorbar = {"Decsion variables":'r',"Constraints":'b'}
    for idx, t in enumerate(classes):
        data_list  = []
        for  i in labels:
            data_list.append(list(count[i].values())[idx])
        if idx == 0:
            ax.bar(x - width, data_list, width, label=t,color=colorbar[t])
        else:
            ax.bar(x + width, data_list, width, label=t,color=colorbar[t])
        print(t)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(' $Log_2{Count}$')
    ax.set_xlabel('Problem Type')
    ax.set_title(' Scale Of Each Problem')
    ax.set_xticks(x)
    # ax.set_xt
    ax.set_xticklabels(labels,rotation=0,fontsize=8)
    ax.legend()

    plt.show()
    fig.savefig("./3.pdf",dpi=600)
    return


def calculate_acc(sub_categories, category):

    GPT4_lib = {i: {} for i in sub_categories}
    GPT3_5_lib = {i: {} for i in sub_categories}
    with open('problems.json', 'r', encoding='utf-8') as fp:
        # Load the JSON to a Python dict
        data = json.load(fp)
    for i, sub_cat in enumerate(sub_categories):
        for j in range(questions_per_subcategory):
            idx = i*5+j
            tmp1 = data[category][sub_cat][str(j+1)]['GPT4_lib']
            if tmp1:
                GPT4_lib[sub_cat][tmp1] = GPT4_lib[sub_cat].get(tmp1, 0)+1
            tmp2 = data[category][sub_cat][str(j+1)]['GPT3.5_lib']
            if tmp2:
                GPT3_5_lib[sub_cat][tmp2] = GPT3_5_lib[sub_cat].get(tmp2, 0)+1
    return GPT4_lib, GPT3_5_lib

if __name__ == "__main__":
    # plot_volume_img()
    plot_error_img()