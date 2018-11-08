# -*- coding: utf-8 -*-
from pandas.io.json import json
from pyparsing import basestring

from app.src.pyltputils.ltptree import tree_builder
from app.src.pyltputils.ltputil import LTPUtil
from app.src.utils.fileutils import FilePersist
from app.src.utils.utils import split_sents


def ltp_util():
    ltpUtil = LTPUtil()

    sentences = "Python才是世界上最好的编程语言。PHP不是。"

    # test sentence spliter
    sentList = ltpUtil.SentenceSplitter(sentences)
    print("========== Test 00 - Spliter =========")
    for item in sentList:
        print(item)
    print("======================================\n\n")

    sentence = "群众非常赞赏政府打击腐败的举措。"

    # test segment
    words = ltpUtil.Segmentor(sentence)
    print("========== Test 01 - Segment =========")
    for item in words:
        print(item)
    print("======================================\n\n")

    # test postage 01
    postags = ltpUtil.Postagger(words)
    print("========== Test 02 - POS words =========")
    pList = list(postags)
    for item in pList:
        print(item)
    print("========================================\n\n")

    # test postage 02
    postags = ltpUtil.Postagger(sent=sentence)
    print("========== Test 03 - POS sents =========")
    pList = list(postags)
    for item in pList:
        print(item)
    print("========================================\n\n")

    # test named entity recognizer 01
    ner = ltpUtil.NamedEntityRecognizer(words, postags)
    print("========== Test 04 - NER words =========")
    nList = list(ner)
    for item in nList:
        print(item)
    print("========================================\n\n")

    # test named entity recognizer 02
    ner = ltpUtil.NamedEntityRecognizer(sent=sentence)
    print("========== Test 05 - NER sents =========")
    nList = list(ner)
    for item in nList:
        print(item)
    print("========================================\n\n")

    # test parser 01
    arcs = ltpUtil.Parser(words, postags)
    print("========== Test 06 - PAR words =========")
    aList = list(arcs)
    for item in aList:
        print(str(item.head) + ": " + item.relation)
    print("========================================\n\n")

    # test parser 02
    arcs = ltpUtil.Parser(sent=sentence)
    print("========== Test 07 - PAR sents =========")
    aList = list(arcs)
    for item in aList:
        print(str(item.head) + ": " + item.relation)
    print("========================================\n\n")


def ltp_tree(sent):
    # sent = "群众非常赞赏政府打击腐败的举措。"
    # sent = "昨天见面了，签署了德骏的协议，沟通了客户的资产情况，下周出去玩，大概22号左右回来"
    tree = tree_builder(sent)
    return tree


def get_three_result(three_level, tree):
    # 如果是第三个内容 首先判断是不是 宾语，在判断定于 在判断状态
    is_find = False
    for itemData in three_level:
        if 'VOB' in itemData.relation or 'POB' in itemData.relation or 'IOB' in itemData.relation or 'FOB' in itemData.relation:
            is_find = tree
            return itemData.context
    if is_find is False:
        for itemData in three_level:
            if 'COO' in itemData.relation:
                is_find = tree
                same_head = get_same_head_node(itemData, tree)
                return itemData.context + get_att_result(same_head, tree)
    else:
        return ''


def get_two_result(rootNode, fist_level, tree):
    # 如果是第二个内容  需要判断动词介词前面是否有 定语状语
    notelist = []
    for i in range(tree.getRIndex()):
        notelist.append(tree.find(i + 1))

    indexlist = []
    for item in fist_level:
        indexlist.append(item.index)

    resultcontent = rootNode.context

    if rootNode.index > 1 and rootNode.index < len(notelist):
        itemone = notelist[rootNode.index - 2]
        itemtwo = notelist[rootNode.index]
        if itemone.root.index in indexlist:
            if 'ADV' in itemone.getRoot().relation or 'DBL' in itemtwo.getRoot().relation:
                resultcontent = itemone.root.context + resultcontent
        if itemtwo.root.index in indexlist:
            if 'CMP' in itemtwo.getRoot().relation:
                resultcontent = resultcontent + itemtwo.root.context

    # print('resultcontent ', resultcontent)
    return resultcontent


def get_first_result(fist_level, tree):
    # 如果是第一个内容 首先判断是不是 主语，在判断定于 在判断状态
    is_find = False
    for itemData in fist_level:
        if 'SBV' in itemData.relation:
            is_find = tree
            return itemData.context
    if is_find is False:
        for itemData in fist_level:
            if 'ATT' in itemData.relation:
                is_find = tree
                same_head = get_same_head_node(itemData, tree)
                return get_att_result(same_head, tree) + itemData.context
    if is_find is False:
        for itemData in fist_level:
            if 'ADV' in itemData.relation:
                is_find = tree
                return itemData.context
    else:
        return ''


def get_att_result(fist_level, tree):
    for itemData in fist_level:
        if 'ATT' in itemData.relation:
            return itemData.context
    else:
        return ''


def get_same_head_node(rootNode, tree):
    same_level = []
    for i in range(tree.getRIndex()):
        node_item = tree.find(i + 1).getRoot()
        if node_item.head == rootNode.index:  # 将不是标签符号的子分支内容补全
            same_level.append(node_item)
    return same_level


# 获取主谓宾
def getSubjectPredicateObject(tree):
    for i in range(tree.getRIndex()):
        print(tree.find(i + 1).toString())

    rootNode = tree.getRoot()
    fist_level = get_same_head_node(rootNode, tree)
    result = []

    # 选第一个内容
    contentOne = get_first_result(fist_level, tree)
    if get_first_result(fist_level, tree) is None:
        contentOne = ""
    result.append(contentOne)

    # 第二个内容
    # print('fist_level ', type(fist_level))
    result.append(get_two_result(rootNode, fist_level, tree))

    # 选第三个内容
    contentThree = get_three_result(fist_level, tree)
    if get_three_result(fist_level, tree) is None:
        contentThree = ""
    result.append(contentThree)
    # print('result', result)
    return result


if __name__ == "__main__":
    # ltp_util()
    # ltp_tree()

    # sentence = "微信告知睿策清算资金近期能到，前段时间停牌股票已复牌"
    # mtree = ltp_tree(sentence)
    # getSubjectPredicateObject(mtree)

    # sentence = "已成交维护 正在开会，下午再联系下"
    # substring = split_sents(sentence)
    #
    # for str in substring:
    #     print('str', str)
    #     mtree = ltp_tree(str)
    #     getSubjectPredicateObject(mtree)

    filePersist = FilePersist()
    list_remark = filePersist.loadLine('../../res/foo.txt')

    fp = open('../../assert/tree-triple-extractor-2.txt', "w", encoding='utf-8', errors='ignore')

    count = 1
    for item_data in list_remark:
        count = count + 1
        in_json = json.loads(item_data)  # Encode the data
        remarks = in_json['remarks'] if in_json['remarks'] else " "
        if remarks != '':
            custom_state = in_json['custom_state'] if in_json['custom_state'] else " "
            substring = split_sents(remarks)
            result = []
            itemresult = ''
            for str in substring:
                if str.strip() is not '':
                    mtree = ltp_tree(str)
                    itemresult = getSubjectPredicateObject(mtree)
                    print('itemresult', itemresult, str)
                    resultstr = '['+', '.join(itemresult)+']'
                    result.append(resultstr)
            print('result_string', remarks, itemresult)

            result_string = ', '.join(result)

            fp.write(custom_state + '\t' + remarks + '\t' + '{' + result_string + '} ' + '\n')
    fp.close()
    print('count', count)
