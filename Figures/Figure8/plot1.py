import matplotlib.pyplot as plt
import json
import numpy as np
import logging
import math
import matplotlib as mpl
legend_font = {"family" : "Times New Roman"}
font_size = 17
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
labels1 = continuous_sub_categories1 + integer_sub_categories1
model_list = ["GPT3.5","GPT4"]
mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams['text.usetex'] = False
plt.rcParams['font.sans-serif'] = ['Times New Roman']
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
                res[k]["num_dec_var"] = res[k]["num_dec_var"]/int(number)
                res[k]["num_constraint"] = res[k]["num_constraint"]/int(number)
                # res[k]["num_dec_var"] = math.log(res[k]["num_dec_var"]/int(number),2)
                # res[k]["num_constraint"] = math.log(res[k]["num_constraint"]/int(number),2)
        logging.info("We have finished counting")
        return res

    with open('problems.json', 'r', encoding='utf-8') as fp:
    # Load the JSON to a Python dict
        data = json.load(fp)
    count = preprocess(data)
    x = np.arange(len(labels))  # the label locations
    width = 0.25  # the width of the bars
    gap = 0.5*width + 0.05
    fig, ax = plt.subplots(figsize=(15, 8))
    classes = ["Decsion variables","Constraints"]
    colorbar = {"Decsion variables":'#6eb5ff',"Constraints":'#f6a6ff'}
    for idx, t in enumerate(classes):
        data_list  = []
        for  i in labels:
            data_list.append(list(count[i].values())[idx])
        if idx == 0:
            ax.bar(x - gap, data_list, width, label=t,color=colorbar[t])
        else:
            ax.bar(x + gap, data_list, width, label=t,color=colorbar[t])
        print(t)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel(' $Log_2{Count}$',font={'size': font_size, 'family': 'Times New Roman'})
    ax.set_ylabel('Count',font={'size': font_size, 'family': 'Times New Roman'})
    plt.yscale("log",base=2)
    ax.set_xlabel('Problem Type',font={'size': font_size, 'family': 'Times New Roman'})
    ax.set_title(' Scales for Each Type of Problem',fontdict={'size': font_size+1})
    ax.set_xticks(x)
    plt.tick_params(labelsize=font_size)
    # ax.set_xt
    ax.set_xticklabels(labels1,rotation=0)
    ax.legend(frameon=False, loc='upper left',prop={'size': font_size, 'family': 'Times New Roman'})
    plt.tight_layout()
    plt.show()
    fig.savefig("./scale_of_problem.png",dpi=600)
    fig.savefig("./scale_of_problem.pdf",dpi=600)
    fig.savefig("./scale_of_problem.eps",dpi=600)
    return

if __name__ == "__main__":
    plot_volume_img()