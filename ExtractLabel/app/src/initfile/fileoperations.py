import os

from pandas.io.json import json

from app.src.pyltputils.ltptree import tree_builder
from app.src.utils.fileutils import get_file_child_name
from app.src.utils.wordutils import wordcount


def load_line(path):
    with open(path, 'r', encoding='utf-8') as open_file:
        return open_file.readlines()


def analysis_programme(type, content):
    # print('type', type)
    if type == '未成交':
        tree = tree_builder(content)
        print('tree', tree)
    elif type == '成交中':
        tree = tree_builder(content)
        print('type 成交中', tree)
    elif type == '已成交维护':
        print('type 已成交维护', '')
    elif type == '复购沟通':
        print('type 复购沟通', '')


def init_product_name(content_list):
    save_path = '../../res/ltp/ltp_data_user/fulluserdict.txt'
    fp = open(save_path, "a", encoding='utf-8', errors='ignore')
    fp.write('\n')
    for item in content_list:
        sline = item.replace('\n', "").replace(" ", "") + '\tnz' + '\n'
        fp.write(sline)
    fp.close()


def remove_duplicates(infile, outfile):
    infopen = open(infile, 'r', encoding='utf-8')
    outopen = open(outfile, 'w', encoding='utf-8')
    lines = infopen.read()
    list_out = []
    words = lines.split('\t')
    print('remove_duplicates ', words, len(words))
    count = 0
    for line in words:
        if line not in list_out:
            count = count + 1
            print('line', line)
            list_out.append(line)
            if count == 15:
                count = 0
                outopen.write(line + '\n')
            else:
                outopen.write(line + '\t')
    infopen.close()
    outopen.close()


def file_deal_with(root_path, out_path):
    if not os.path.isdir(root_path):
        print("【{0}】不是目录".format(root_path))
        exit(-1)
    for filename in os.listdir(root_path):
        in_file = root_path + filename
        out_file = out_path + filename
        print('rootPath + "/" + filename ' + root_path + filename)
        remove_duplicates(in_file, out_file)


def get_simple_company(infile, outfile):
    outopen = open(outfile, 'w', encoding='utf-8')
    lines = load_line(infile)
    # 过滤停用词
    stop_word = ['（', '）']
    # 过滤地名
    placename = load_line('../../res/lexicon/ns-place.txt')
    # 过滤公司的修饰字符
    decoratelist = load_line('../../res/lexicon/n-decorate-company.txt')
    for line in lines:
        temp = line
        print('line', line)
        # 过滤公司的修饰词
        for decorate_item in decoratelist:
            decorate_temp = decorate_item.replace('\n', '')
            if decorate_temp in line:
                line = line.replace(decorate_temp, '')
        # 过滤特殊字符
        for stop_item in stop_word:
            stop_temp = stop_item.replace('\n', '')
            if stop_temp in line:
                line = line.replace(stop_temp, '')
        # 过滤地名
        for place_item in placename:
            place_temp = place_item.replace('\n', '')
            if place_temp in line:
                line = line.replace(place_temp, '')

        outopen.write(temp.strip() + '\n')
        outopen.write(line.strip() + '\n')
    outopen.close()


def get_simple_product(infile, outfile):
    outopen = open(outfile, 'w', encoding='utf-8')
    lines = load_line(infile)
    # lines = ['华澳·臻智17号证券投资集合资金信托计划']
    # 过滤公司的修饰字符
    decoratelist = load_line('../../res/lexicon/n-decorate-product.txt')

    for line in lines:
        temp = line
        print('line', line)
        # 过滤公司的修饰词
        for decorate_item in decoratelist:
            item_temp = decorate_item.replace('\n', '')
            if item_temp in line:
                line = line.replace(item_temp, '')

        outopen.write(temp.strip() + '\n')
        outopen.write(line.strip() + '\n')
    outopen.close()


def word_frequency_count(file_path):
    sentence_list = load_line(file_path)
    word_list = []
    result_list = {}
    for sentence_item in sentence_list:
        list_temp = sentence_item.split(",")
        for item_word in list_temp:
            word_list.append(item_word)
    result_list = wordcount(word_list)

    print('result_list', result_list)

if __name__ == '__main__':
    # source_path = '../../res/foo.txt'
    # source_path = '../../res/product_name.txt'
    # save_path = '../../assert/foo-json-empty.txt'

    # in_path = '../../assert/word/class_lexicon_storage_jieba_stop/'
    # out_path = '../../assert/word/word_class_uniq_1/'
    # file_list = load_line(source_path)
    #
    # init_product_name(file_list)

    # file_deal_with(in_path, out_path)

    # in_file = '../../assert/regardless_word.txt'
    # out_file = '../../res/manual-lexicon/word-idiom-n.txt'
    # remove_duplicates(in_file, out_file)

    # ****************************************************************
    # type_path = '../../assert/class_notes_b/'
    # save_path = '../../assert/class_word_1/'
    # files_name = get_file_child_name('../../assert/class_notes_b')
    # for name_item in files_name:
    #     type_name = type_path+name_item
    #     save_name = save_path+name_item
    #     print('type_item  save_type ', type_name, save_name)
    #     remove_duplicates(type_name, save_name)
    # ----------------------------------------------------------------

    # fp = open(save_path, "w", encoding='utf-8', errors='ignore')
    #
    # for file_item in file_list:
    #     in_json = json.loads(file_item)  # Encode the data
    #     custom_state = in_json['custom_state'] if in_json['custom_state'] else " "
    #     remarks = in_json['remarks'] if in_json['remarks'] else " "
    #     # out_json = {}
    #     # out_json["custom_state"] = custom_state
    #     # out_json["remarks"] = remarks
    #     if in_json['remarks'] == '':
    #         fp.write(custom_state+'\t'+remarks + '\n')
    # fp.close()
    # ****************************************************************
    # input_path = '../../assert/company.txt'
    # output_path = '../../assert/company_brief.txt'
    # get_simple_company(input_path, output_path)

    # --------------------------------------------------------------------
    # input_path = '../../res/product_name.txt'
    # output_path = '../../assert/product_brief.txt'
    # get_simple_product(input_path, output_path)

    # --------------------------------------------------------------------
    input_path = '../../assert/word_segmentation.txt'
    word_frequency_count(input_path)
