from pylatex import Document, Section, Subsection, Command, Package, UnsafeCommand
from pylatex.utils import italic, NoEscape
import json


def add_mybox(doc):
    doc.packages.add(Package('tcolorbox'))
    doc.packages.add(Package('amsmath'))
    doc.preamble.append(Command(NoEscape('tcbuselibrary{most}')))

    mybox = UnsafeCommand('newtcolorbox'  # 必填项
                          # 这里添加使用该条命令依赖的包，
                          '{mybox}', 'breakable, colback=white, colframe=black!50, fonttitle=\\bfseries, title=#1', r'1', packages=[]
                          )
    doc.append(mybox)


def JSON_preprocess():
    with open('problemsv6.json', 'r', encoding='utf-8') as fp:
        problems = json.load(fp)
    return problems


def mybox(doc, num, Q, A, A1, A2, A3):
    # doc.append(NoEscape(r"\begin{mybox}{Vicuna-13B}"))
    doc.append(NoEscape(r"\noindent\textbf{Question "+num+r"}: "+Q+r"\\\\"))
    doc.append(NoEscape(r"\textbf{GPT-4"+r"}: "+A+r"\\\\"))
    doc.append(NoEscape(r"\textbf{Vicuna zero-shot"+r"}: " + A1+r"\\\\"))
    doc.append(NoEscape(r"\textbf{Vicuna one-shot"+r"}: " + A2+r"\\\\"))
    doc.append(NoEscape(r"\textbf{Vicuna few-shot"+r"}: " + A3+r"\\\\"))
    # doc.append(NoEscape(r"\end{mybox}"))


if __name__ == '__main__':
    data = JSON_preprocess()
    for i in range(23,36):
        doc = Document('Vicuna-Test-'+str(i))
        add_mybox(doc)
        for k, v in data.items():
            if int(k) == int(i):
                mybox(doc, k, v["Problem description"],
                    v["Modeling"],
                    v["vicuna-zero-shot"],
                    v["vicuna-one-shot"],
                    v["vicuna-few-shot"])
        doc.generate_tex()
