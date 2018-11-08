# coding=utf-8
from app.src.filter.filterclass import item_words_list


def wordcount(str_list):
    """
    传进来是大量的笔记合并成一个文本后，再对这个文本分词的list结果
    需要去停用词
    :param strl_ist:
    :return:
    """
    count_dict = {}
    # 如果字典里有该单词则加1，否则添加入字典
    stop_word_path = '../../res/word-stop.txt'
    stop_word_list = item_words_list(stop_word_path)
    print('stop_word_list', len(stop_word_list))
    # 过滤停用词
    for str in str_list:
        print('str', str)
        temp_str = str.strip()
        if temp_str not in stop_word_list:
            if temp_str in list(count_dict.keys()):
                count_dict[temp_str] = count_dict[temp_str] + 1
            else:
                count_dict[temp_str] = 1
    # 按照词频从高到低排列
    count_list = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    return count_list
