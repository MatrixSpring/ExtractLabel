# coding: utf-8

# 可能根本都不能用KNN算法 说不定在那句话里面没有对应的词

# step1： 文本向量化表示，计算特征词的TF-IDF值
# step2： 新文本到达后，根据特征词确定文本的向量
# step3 : 在训练文本集中选出与新文本向量最相近的k个文本向量，相似度度量采用“余弦相似度”，根据实验测试的结果调整k值，此次选择20
# step4： 在新文本的k个邻居中，依次计算每类的权重，
# step5： 比较类的权重，将新文本放到权重最大的那个类中

class ClassifyGensim(object):

    def __init__(self):
        print('初始化')

    def computeIDF(self):
        # <word, set(docM,...,docN)>
        wordDocMap = {}
        # <word, IDF值>
        IDFPerWordMap = {}
        countDoc = 0.0


if __name__ == "__main__":
    print('运行')
