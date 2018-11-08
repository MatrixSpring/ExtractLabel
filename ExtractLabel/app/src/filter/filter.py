# coding=utf-8
from app.src.structure.Trie import Trie
from app.src.utils.fileutils import FilePersist

word_stop_path = './test/word-stop.txt'
word_time_path = './test/nt-time.txt'
word_product_path = './test/nz-product.txt'
word_negative_path = './test/word-negative-a.txt'
word_positive_path = './test/word-positive-a.txt'


# 获取固定格式(每一行一个数据的内容)
def stop_words_list(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 对停用词过滤
def filter_stop_word(words):
    """
    对停用词过滤
    :param words: list
    :return:
    """
    stopwords = []
    if stopwords:
        stopwords = stop_words_list(word_stop_path)  # 这里加载停用词的路径
    outstr = ''
    for word in words:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


def filter_contact_method(words):
    # 联系方式：电话 短信 微信 见面 约见 预约 邮寄
    cmode = ["电话", "短信", "微信", "见面", "约见", "预约", "邮寄", "寄", "约"]
    intersection = [item for item in cmode if item in words]
    return intersection


# 过滤专有名词 地名 机构
def filter_proper_names(netags, words):
    # 专有名词 NS
    if 'S-Ns' in list(netags):
        return words[list(netags).index('S-Ns')]
    elif 'B-Ns' in list(netags):
        return words[list(netags).index('B-Ns')]
    elif 'S-Nh' in list(netags):
        return words[list(netags).index('S-Nh')]
    else:
        return ''


# 过滤时间名词
def filter_time_date(words):
    """
    过滤时间词汇
    :param words:
    :return:
    """
    timewords = []
    if timewords:
        timewords = stop_words_list(word_time_path)  # 这里加载时间词词的路径
    intersection = [item for item in timewords if item in words]
    return intersection


# 过滤兴趣爱好的指标打分
def filter_discuss_hobbies(words):
    """
    过滤是否有兴趣的词 分为两类一类表现出感兴趣
    :param words:
    :return:
    """
    # 感兴趣
    interest_word = []
    if interest_word:
        interest_word = stop_words_list(word_positive_path)  # 这里加载时间词词的路径
    interest_list = [item for item in interest_word if item in words]
    # 不敢兴趣
    indifferent_word = []
    if indifferent_word:
        indifferent_word = stop_words_list(word_positive_path)  # 这里加载时间词词的路径
    indifferent_list = [item for item in indifferent_word if item in words]
    return {'interest': interest_list, '': indifferent_list}


# 过滤产品名称
def filter_product_name(words):
    """
    使用trie 树存储产品名称信息,传进来句子分词列表
    :param words:
    :return:
    """
    trie = Trie()
    filePersist = FilePersist()
    list_remark = filePersist.loadLine('../../res/product_name.txt')
    for item_data in list_remark:
        trie.add(item_data)

    result_list = []
    for word in words:
        word_list = trie.wordsWithPrefix(word)
        if word_list:
            result_list.append(word_list)

    return result_list
