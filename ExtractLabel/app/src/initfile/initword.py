# coding=utf-8

# 时间词库
from pandas.io.json import json

from app.src.extraction.sentence_parser import LtpParser
from app.src.utils.fileutils import loadLine, loadFile, get_file_child_name

# 源文件目录路劲
word_time_path = '../../res/lexicon/'
#  输出词库
word_out_path = '../../res/ltp/ltp_data_user/fulluserdict.txt'


# 将时间词 将产品词 将负面词 正面词 将少于五个字的客服的短语作为常用语词库

# 获取固定格式(每一行一个数据的内容)
def item_words_list(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 去除重复文件
def remove_duplicates(infile, inname, outfile):
    outopen = open(outfile, 'a', encoding='utf-8')
    infile_list = loadLine(infile)
    names = inname.split('/')[-1].split("-")
    print('names', names)
    list_out = []
    for line in infile_list:
        if line not in list_out:
            list_out.append(line)
            outopen.write(line.strip() + '\t' + names[0] + '\n')
    outopen.close()


class InitWord(object):

    def __init__(self):
        self.parser = LtpParser()
        # 地址列表
        self.file_list = get_file_child_name(word_time_path)

    # 合并词汇
    def combination_words(self):
        """
        合并词汇
        :param words: list
        :return:
        """
        for file_item in self.file_list:
            print('combination_words', word_time_path + file_item, file_item, word_out_path)
            remove_duplicates(word_time_path + file_item, file_item, word_out_path)
        return ''

    def word_property(self, file_path, save_path_property):
        result_list = loadLine(file_path)

        for content_item in result_list:
            in_json = json.loads(str(content_item))  # Encode the data
            # print('note_item', in_json['remarks'])
            remark = in_json['remarks']
            # 获取分词
            words = self.parser.segmentor.segment(remark)
            # print('words', words)
            # 词性标注
            postags = self.parser.postagger.postag(words)
            # print('note_item', postags)
            # print('postags', postags)
            result_list = []

            for i in range(len(postags)):
                save_path_temp = save_path_property + postags[i]
                fp = open(save_path_temp, "a", encoding='utf-8', errors='ignore')
                fp.write(words[i] + '\t')
                fp.close()

    def word_segmentation(self, input_path, out_path):
        sentence_list = loadLine(input_path)
        outOpen = open(out_path, 'w', encoding='utf-8')

        for sentence_item in sentence_list:
            in_json = json.loads(sentence_item)  # Encode the data
            remark = in_json['remarks']
            # remark = sentence_item
            print('sentence_item', remark)
            result_list = self.parser.segmentor.segment(remark)
            outOpen.write(', '.join(result_list) + '\n')
        outOpen.close()


if __name__ == '__main__':
    file_path = '../../res/foo-60k.txt'
    save_path_property = '../../assert/class_notes_b/'

    initWord = InitWord()
    # initWord.combination_words()

    initWord.word_segmentation('../../res/foo-60k.txt', '../../assert/word_segmentation.txt')
    # initWord.word_segmentation('../../assert/company.txt', '../../assert/company_brief.txt')

    # initWord.word_property(file_path, save_path_property)
