# coding: utf-8
import os

from gensim import corpora, models, similarities
from pandas.io.json import json

from app.src.extraction.sentence_parser import LtpParser
from app.src.utils.fileutils import load_file, loadLine, save_class_notes


class ClassifyGensim(object):

    def __init__(self):
        self.parser = LtpParser()
        self.raw_documents = []
        self.corpora_documents = []
        self.dictionary = None
        self.corpus = None
        # tfidf
        self.tfidf_model = None
        self.corpus_tfidf = None
        self.similarity = None
        # lsi
        self.lsi = None
        self.corpus_lsi = None
        self.similarity_lsi = None

    def init_classify(self, category_path):

        if not os.path.isdir(category_path):
            print("【{0}】不是目录".format(category_path))
            exit(-1)

        # 先将某一类的内容添加到列表
        for filename in os.listdir(category_path):
            result = load_file(category_path + filename)
            self.raw_documents.append(result)

        # 将列表中的句子分词后添加到分词的存储列表
        for item_text in self.raw_documents:
            # 分词结果
            # 过滤停用词？
            item_seg = list(self.parser.segmentor.segment(item_text))
            self.corpora_documents.append(item_seg)

        # 生成字典和向量语料
        self.dictionary = corpora.Dictionary(self.corpora_documents)

        # 生成bow向量 通过下面一句将得到语料中每一个种类对应的稀疏向量
        # 向量的每一个元素代表一个word在这篇文档中出现的次数
        self.corpus = [self.dictionary.doc2bow(text) for text in self.corpora_documents]

        # corpus 是一个返回bow向量的迭代器. 下面代码将完成对corpus中出现的每一个特征的IDF值的统计工作
        self.tfidf_model = models.TfidfModel(self.corpus)
        self.corpus_tfidf = self.tfidf_model[self.corpus]
        # 将语料库生成similarity工具
        self.similarity = similarities.Similarity('Similarity-tfidf-index', self.corpus_tfidf, num_features=20000)

        # lsi
        self.lsi = models.LsiModel(self.corpus_tfidf)
        self.corpus_lsi = self.lsi[self.corpus_tfidf]
        self.similarity_lsi = similarities.Similarity('Similarity-LSI-index', self.corpus_lsi, num_features=20000)

        self.similarity_lsi.num_best = 2

    # tfidf 分类
    def notes_classify_tfidf(self, notes_path):
        note_list = loadLine(notes_path)
        self.similarity.num_best = 5
        print('note_item', note_list[0], len(note_list))
        result_list = []
        for note_item in note_list:
            in_json = json.loads(str(note_item))  # Encode the data
            # print('note_item', in_json['remarks'])
            remark = in_json['remarks']
            note_corpus = self.parser.segmentor.segment(remark)
            # 生成note的词袋
            note_doc2bow = self.dictionary.doc2bow(note_corpus)
            # 根据之前训练生成的model，生成query的IFIDF值，然后进行相似度计算
            note_tfidf = self.tfidf_model[note_doc2bow]
            # 获取相似度结果
            note_similarity = self.similarity[note_tfidf]

            if note_similarity:
                # 返回最相似的样本材料,(index_of_document, similarity) tuples
                print('111111 type inside ', type(note_similarity[0]), note_similarity)
                result_list.append({'remarks': remark, 'position': note_similarity[0]})
        return result_list

    # 使用LSI模型进行相似度计算
    def notes_classify_lsi(self, notes_path):
        note_list = loadLine(notes_path)
        print('note_item', note_list[0], len(note_list))
        result_list = []
        for note_item in note_list:
            in_json = json.loads(str(note_item))  # Encode the data
            # print('note_item', in_json['remarks'])
            remark = in_json['remarks']
            # 1.分词
            note_corpus = self.parser.segmentor.segment(remark)
            # 2.转换成bow向量
            note_doc2bow = self.dictionary.doc2bow(note_corpus)
            # 3.计算tfidf值
            note_tfidf = self.tfidf_model[note_doc2bow]
            # 更新LSI的值
            # self.lsi.add_documents(note_tfidf)
            # 4.计算lsi值
            note_lsi = self.lsi[note_tfidf]
            if note_lsi:
                # 返回最相似的样本材料,(index_of_document, similarity) tuples
                print('111111 type inside ', type(note_lsi[0]), note_lsi)
                result_list.append({'remarks': remark, 'position': note_lsi[0]})
        return result_list


if __name__ == '__main__':
    classifyTFIDF = ClassifyGensim()
    category_path = '../../res/status-category/status-category-1/'
    content_list = '../../res/foo-60k.txt'
    class_save_path = '../../assert/class_notes_2/'
    classifyTFIDF.init_classify(category_path)
    result_list = classifyTFIDF.notes_classify_tfidf(content_list)

    print('result_list', len(result_list))
    save_class_notes(category_path, result_list, class_save_path)
