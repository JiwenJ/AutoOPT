import matplotlib.pyplot as plt
import json
import numpy as np
import logging
import math
legend_font = {"family": "Times New Roman"}
plt.rcParams["font.sans-serif"] = ["Times New Roman"]  # 设置字体
font_size = 17
continuous_sub_categories = ['UOP', 'LPP', 'QPP']
integer_sub_categories = ['IPP', 'TSP', 'KP', 'VRP']
Category = continuous_sub_categories + integer_sub_categories

# --------- data setting --------
data_llama2_zero = [1, 1, 2, 0, 0, 1, 0]
data_vicuna_zero = [1, 1, 0, 3, 0, 3, 0]
data_wizardlm_zero = [0, 2, 2, 2, 1, 0, 1]
data_wizardmath_zero = [2, 3, 2, 2, 0, 1, 0]
data_gpt3_5_zero = [3, 4, 0, 5, 0, 4, 0]
data_gpt4_zero = [5, 4, 5, 5, 4, 5, 2]


models = ["llama2", "vicuna", "wizardlm", "wizardmath", "gpt3_5", "gpt4" ]


def plot_few_shot():
    x = np.arange(len(Category))  # the label locations
    width = 0.08  # the width of the bars
    gap = 0.5  # the gap in between
    gap1 = 0.5*width
    fig, ax = plt.subplots(figsize=(15, 8))
    type_shot = [ 'LLaMA2-13B', "Vicuna-13B", 'WizardLM-13B', 'WizardMath-13B', 'GPT-3.5', 'GPT-4']
    colorbar = {"gpt4": '#6eb5ff', "gpt3_5": '#f6a6ff',
    "llama2": '#F8CECC',"vicuna":'#ace8bc',
    "wizardlm":'#d1c5f2',"wizardmath":'#fff2cc' }
    for index, t in enumerate(models):
        data_name = f"data_{t}_zero"
        data_list = eval(data_name)
        ax.bar(x+width*(index-3), data_list, width, label=type_shot[index],color=colorbar[t])
    plt.ylim((0, 7))

    ax.set_ylabel('Count', font={'size': font_size,
                  'family': 'Times New Roman'})
    ax.set_xlabel('Problem Type', font={
                  'size': font_size, 'family': 'Times New Roman'})
    ax.set_title('Zero Shot Performance of Different Common LLMs',
                 fontdict={'size': font_size+1})
    ax.set_xticks(x)
    ax.set_xticklabels(Category, rotation=0)
    plt.tick_params(labelsize=font_size)
    ax.legend(frameon=False, loc='upper right', prop={
              'size': font_size, 'family': 'Times New Roman'})
    plt.tight_layout()
    plt.show()
    fig.savefig("./ZeroShot.png", dpi=600)
    fig.savefig("./ZeroShot.pdf", dpi=600)
    fig.savefig("./ZeroShot.eps", dpi=600)


if __name__ == '__main__':
    plot_few_shot()
