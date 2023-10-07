import openai
import umap
import json
import matplotlib.pyplot as plt
import numpy as np
from numpy import arange
from sentence_transformers import util
import os

legend_font = {"family" : "Times New Roman"}
font_size = 14
plt.rcParams["font.sans-serif"]=["Times New Roman"] #设置字体
# plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
# openai.api_key = os.getenv('OpenAI_API_Key')
openai.api_key = "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"
image_labels = {'Unconstrained optimization problem':'r.', 'Linear programming':'g.', 'TSP problem':'bx', 'VRP problem':'mx', 'Knapsack problem':'k+', 'Integer linear programming':'cx', 'Quadratic programming':'y+'}
image_labels22 = {'Unconstrained optimization problem':'r.', 'Linear programming':'g.', 'TSP problem':'bx', 'VRP problem':'mx', 'Knapsack problem':'k+', 'Integer linear programming':'cx', 'Quadratic programming':'y+'}
courses_embeddings_location = 'course_embeddings.json'
#-------------------------------------------
embedding_engine = 'text-similarity-davinci-001'
# embedding_engine = 'text-similarity-babbage-001'
# embedding_engine = 'text-similarity-curie-001'
# embedding_engine = 'text-similarity-ada-001'
#-------------------------------------------
questions_per_course = 35
questions_per_topic = 5
number_of_topic = 5
topics = ['Unconstrained optimization problem','Linear programming','Quadratic programming','Integer linear programming',
          'TSP problem','Knapsack problem','VRP problem']
topics1 = ['UOP','LPP','QPP','IPP',
          'TSP','KP','VRP']
#-----------------------------------------
json_location = './problems.json'
#-----------------------------------------
def make_embeddings(embedding_engine, embeddings_location):
    """
    Takes json files of questions using our json file formatting,
        embeds them using OpenAI's embedding_engine,
        and saves a new json, embeddings.json, of the embeddings.
    """
    list_of_embeddings = []
    data_dict = {}

    with open(json_location, 'r',encoding='utf-8') as f:
        data = json.load(f)
    for datum in data.values():
        for k,v in datum.items():
            data_dict[k] = v
    for topic in topics:
        temp = data_dict[topic]
        for value in temp.values():
            raw_question = value['Problem description']
            embedding = openai.Embedding.create(input=raw_question,engine=embedding_engine)['data'][0]['embedding']
            list_of_embeddings.append(embedding)
    embeddings = {'list_of_embeddings':list_of_embeddings}
    with open(embeddings_location, 'w') as f:
        f.write(json.dumps(embeddings))

def get_embeddings(embeddings_file):
    """
    Retrieves embeddings from embeddings_file. Embeddings are assumed to be (n x d).
    """
    with open(embeddings_file, 'r') as f:
        points = json.load(f)['list_of_embeddings']
    return np.array(points)


def reduce_via_umap(embeddings, i,j, num_dims=2):
    """
    Reduces the dimensionality of the provided embeddings(which are vectors) to num_dims via UMAP.
    If embeddings was an (n x d) numpy array, it will be reduced to a (n x num_dims) numpy array.
    """
    # reducer = umap.UMAP(n_components=num_dims,n_neighbors=15, min_dist=0.1, metric='euclidean')

    reducer = umap.UMAP(random_state=42,n_components=num_dims,n_neighbors=i,min_dist=j)
    reduced = reducer.fit_transform(embeddings)
    return reduced

def plot_clusters(points, image_loc,image_loc1, questions_per_course=25, show=False, question_labels=False,
                  label_font='xx-small', dpi=200, width=9.5, height=6.5, legend_loc=(1, 1.01), right_shift=0.72):
    """
    Plots clusters of points. points is assumed to be a n by 2 numpy array.
    Set question_labels to True if you want to see each point labeled with its question number.
    Set show to True if you want the created plot to pop up.
    The other parameters are defaulted to values that we have found to work well for the visual itself.
    """
    x = [x for x,y in points]
    y = [y for x,y in points]

    plt.subplots_adjust(right=right_shift)
    figure = plt.gcf()


    plt.figure(figsize=(7.5, 7.5))
    figure.set_size_inches(w=width,h=height)

    for i, topic in enumerate(topics):
        plt.scatter(x[i*questions_per_topic:(i+1)*questions_per_topic],
                    y[i*questions_per_topic:(i+1)*questions_per_topic],
                    c=image_labels[topic][0],
                    label=topics1[i],
                    marker=image_labels[topic][1])
        # if question_labels:
        #     for j in range(questions_per_course):
        #         plt.annotate(j+1, (x[questions_per_course*i+j], y[questions_per_course*i+j]), fontsize=label_font)

    # plt.legend(bbox_to_anchor=legend_loc)
    # plt.tick_params(labelsize=font_size)

    plt.legend(frameon=False,prop = {'size':font_size},loc='upper left')
    ax = plt.gca()
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    # plt.xticks([])
    # ax.set_xticks([])
    plt.savefig(image_loc1,dpi=600, bbox_inches='tight')
    plt.savefig(image_loc,dpi=600, bbox_inches='tight')
    plt.close()
    if show:
        plt.show()

if __name__ == "__main__":

    if not os.path.exists(courses_embeddings_location):
        make_embeddings(embedding_engine, courses_embeddings_location)
    embeddings = get_embeddings(courses_embeddings_location)
    for i in range(7,8):
        for j in arange(0.7,0.8,0.1):
            i = round(i,1)
            j = round(j,1)
            image_location = "./img/text-similarity-davinci-001-"+str(i)+"-"+str(j)+".png"
            image_location1 = "./img/text-similarity-davinci-001-"+str(i)+"-"+str(j)+".eps"
            reduced_points = reduce_via_umap(embeddings,i,j)
            plot_clusters(reduced_points, image_location,image_location1, questions_per_course=questions_per_course, question_labels=True)

