import matplotlib.pyplot as plt
import json
import numpy as np

legend_font = {"family" : "Times New Roman"}
plt.rcParams["font.sans-serif"]=["Times New Roman"] #设置字体
questions_per_subcategory = 5
continuous_sub_categories1 = ['UOP', 'LPP',
                              'QPP']
continuous_sub_categories = ['Unconstrained optimization problem', 'Linear programming',
                             'Quadratic programming']
integer_sub_categories1 = ['IPP',
                           'TSP', 'KP', 'VRP']
integer_sub_categories = ['Integer linear programming',
                          'TSP problem', 'Knapsack problem', 'VRP problem']
categories = continuous_sub_categories + integer_sub_categories
categories1 = continuous_sub_categories1 + integer_sub_categories1


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


GPT4_lib1, GPT3_5_lib1 = calculate_acc(continuous_sub_categories, 'Continuous')
GPT4_lib2, GPT3_5_lib2 = calculate_acc(integer_sub_categories, 'Integer')

GPT4_lib = dict(GPT4_lib1, **GPT4_lib2)
GPT3_5_lib = dict(GPT3_5_lib1, **GPT3_5_lib2)


data2 = GPT3_5_lib

data1 = GPT4_lib

print(data1)
print(data2)

# Categories
categories = list(data1.keys())

fig, ax = plt.subplots(figsize=(15, 8))

# Position of each category
ind = np.arange(len(categories))
font_size = 17
bar_width = 0.32


gap = 0.07


color_dict = {'scipy.optimize': '#8FAADC', 'pulp': '#F6A6FF',
              'cvxpy': '#ACE8BC', 'ortools': '#F8CECC'}

# List of labels already used
labels_used = []

for idx, category in enumerate(categories):
    # Get the subcategories for this category in both dictionaries
    subcategories = sorted(
        set(list(data1[category].keys()) + list(data2[category].keys())))

    for i, subcategory in enumerate(subcategories):

        value1 = data1[category].get(subcategory, 0)
        value2 = data2[category].get(subcategory, 0)

        # Labels for legend
        label = subcategory if subcategory not in labels_used else ""

        if i == 0:
            ax.bar(ind[idx] + bar_width + gap, value2, bar_width,
                   label=label, color=color_dict[subcategory])
            ax.bar(ind[idx], value1, bar_width, color=color_dict[subcategory])

        else:

            bottom1 = sum(data1[category].get(sub, 0)
                          for sub in subcategories[:i])
            bottom2 = sum(data2[category].get(sub, 0)
                          for sub in subcategories[:i])
            ax.bar(ind[idx] + bar_width + gap, value2, bar_width,
                   bottom=bottom2, color=color_dict[subcategory])
            ax.bar(ind[idx], value1, bar_width, bottom=bottom1,
                   color=color_dict[subcategory])

        if subcategory not in labels_used:
            labels_used.append(subcategory)
    total_height1 = sum(data1[category].get(sub, 0)
                        for sub in subcategories[:i+1])
    total_height2 = sum(data2[category].get(sub, 0)
                        for sub in subcategories[:i+1])
    ax.text(ind[idx], total_height1, 'GPT-4', ha='center', va='bottom',
            color='black', fontdict={'size': font_size, 'family': 'Times New Roman'})
    ax.text(ind[idx] + bar_width + gap, total_height2, 'GPT-3.5', ha='center', va='bottom',
            color='black', fontdict={'size': font_size, 'family': 'Times New Roman'})

    if subcategory not in labels_used:
        labels_used.append(subcategory)

ax.set_xlabel('Problem Type', font={
              'size': font_size, 'family': 'Times New Roman'})
ax.set_ylabel('Count', font={'size': font_size, 'family': 'Times New Roman'})
ax.set_ylim(0, 7)
ax.set_xticks(ind + bar_width / 2)
ax.set_xticklabels(categories1, fontdict={
                   'size': font_size, 'family': 'Times New Roman'})
ax.legend(frameon=False, loc='upper left', prop={
          'size': font_size, 'family': 'Times New Roman'})
plt.tick_params(labelsize=font_size)
ax.set_title('The Python Libraries Used by GPT-4 and GPT-3.5',
             fontdict={'size': font_size+1, 'family': 'Times New Roman'})
plt.tight_layout()
plt.show()
# fig.savefig("./Python_libraries.png")
fig.savefig("./Python_libraries.eps", dpi=600)
fig.savefig("./Python_libraries.png", dpi=600)
