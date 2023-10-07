import matplotlib.pyplot as plt
import json
import numpy as np
import logging
import math
legend_font = {"family": "Times New Roman"}
plt.rcParams["font.sans-serif"]=["Times New Roman"] #设置字体
font_size = 18

continuous_sub_categories = ['UOP', 'LPP', 'QPP']
integer_sub_categories = ['IPP', 'TSP', 'KP', 'VRP']

Category = continuous_sub_categories + integer_sub_categories
type_shot = ['zero-shot', 'one-shot', 'few-shot']

# ---------- GPT-3.5 data setting --------
GPT_3_5 = {}
data_gpt_zero = [3, 4, 0, 5, 0, 4, 0]
data_gpt_one = [1, 1, 2, 0, 0, 1, 0]
data_gpt_few = [1, 1, 2, 0, 0, 0, 0]
data_list1 = [data_gpt_zero, data_gpt_one, data_gpt_few]

# ---------- Vicuna_13B data setting --------
Vicuna_13B = {}
data_vicuna_zero = [1, 1, 0, 3, 0, 3, 0]
data_vicuna_one = [3, 0, 1, 0, 1, 0, 0]
data_vicuna_few = [2, 0, 0, 0, 0, 0, 0]
data_list2 = [data_vicuna_zero, data_vicuna_one, data_vicuna_few]


def init_data():
    for index1, t in enumerate(type_shot):
        GPT_3_5[t] = {}
        Vicuna_13B[t] = {}
        for index2, data in enumerate(Category):
            GPT_3_5[t][data] = data_list1[index1][index2]
            print(f"GPT-3.5: {GPT_3_5[t][data]}")
        for index2, data in enumerate(Category):
            Vicuna_13B[t][data] = data_list2[index1][index2]
            print(f"Vicuna-13B: {Vicuna_13B[t][data]}")

def plot_few_shot():
    x = np.arange(len(Category))  # the label locations
    width = 0.31  # the width of the bars
    gap = 0.5*width + 0.04 # the gap in between
    gap1 = 0.5*width + 0.1
    fig, ax = plt.subplots(figsize=(15, 8))
    models = ["GPT-3.5","Vicuna-13B"]
    type_shot = ['zero-shot', 'one-shot', 'few-shot']
    classes = ["Decsion variables","Constraints"]
    colorbar = {"zero-shot":'#6eb5ff',"one-shot":'#f6a6ff',"few-shot":'#f8cecc'}
    for index, t in enumerate(models):
        data_list = eval("data_list" + str(index+1))
        pre = [0, 0, 0, 0, 0, 0, 0]
        if index == 0:
            for idx, v in enumerate(data_list):
                ax.bar(x - gap, v, width, label=type_shot[idx], color=colorbar[type_shot[idx]], bottom=pre)
                pre = np.sum([pre, v], axis=0).tolist()
                if idx == len(data_list)-1:
                    for z, y in zip(range(len(pre)), pre):
                        plt.text(z-gap, y + 0.05, "GPT-3.5", ha='center', fontsize=font_size-1,color='black')
        else:
            for idx, v in enumerate(data_list):
                ax.bar(x + gap, v, width, color=colorbar[type_shot[idx]], bottom=pre)
                pre = np.sum([pre, v], axis=0).tolist()
                if idx == len(data_list)-1:
                    for z, y in zip(range(len(pre)), pre):
                        plt.text(z+gap, y + 0.05 , "Vicuna", ha='center', fontsize=font_size-1,color='black')

    ax.set_ylabel('Count',font={'size': font_size, 'family': 'Times New Roman'})
    ax.set_xlabel('Problem Type',font={'size': font_size, 'family': 'Times New Roman'})
    ax.set_title('Improvement on One-shot / Few-shot Learning',fontdict={'size': font_size+1})
    ax.set_xticks(x)
    ax.set_xticklabels(Category,rotation=0)
    plt.tick_params(labelsize=font_size)
    ax.legend(frameon=False, loc='upper right',prop={'size': font_size, 'family': 'Times New Roman'})
    plt.tight_layout()
    plt.show()
    fig.savefig("./improvement.png",dpi=600)
    fig.savefig("./improvement.pdf",dpi=600)
    fig.savefig("./improvement.eps",dpi=600)



if __name__ == '__main__':
    init_data()
    plot_few_shot()
