#!/usr/bin/env python3
# coding: utf-8

import os
import re
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

from pandas.io.json import json

from app.src.utils.fileutils import loadLine


def split_sents(content):
    """
    文章分句处理, 切分长句，冒号，分号，感叹号等做切分标识
    :param content:
    :return:
    """
    return [sentence for sentence in re.split(r'[？?！!。，；;：:\n\r]', content) if sentence]


class LtpParser:
    def __init__(self):
        LTP_DIR = "../../res/ltp/ltp_data_v3.4.0"
        LTP_DIR_USER = "../../res/ltp/ltp_data_user"
        self.segmentor = Segmentor()
        self.segmentor.load_with_lexicon(os.path.join(LTP_DIR, "cws.model"), os.path.join(LTP_DIR_USER, "fulluserdict.txt"))
        # self.segmentor.load(os.path.join(LTP_DIR, "cws.model"))

        self.postagger = Postagger()
        self.postagger.load_with_lexicon(os.path.join(LTP_DIR, "pos.model"), os.path.join(LTP_DIR_USER, "fulluserdict.txt"))
        # self.postagger.load(os.path.join(LTP_DIR, "pos.model"))

        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))

        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(LTP_DIR, 'pisrl_win.model'))

    '''语义角色标注'''

    def format_labelrole(self, words, postags):
        arcs = self.parser.parse(words, postags)
        roles = self.labeller.label(words, postags, arcs)
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {arg.name: [arg.name, arg.range.start, arg.range.end] for arg in role.arguments}
        return roles_dict

    def build_parse_child_dict_two(self, words, arcs):
        """
        为句子中的每个词语维护一个保存句法依存儿子节点的字典
        Args:
            words: 分词列表
            postags: 词性列表
            arcs: 句法依存列表
        """
        child_dict_list = []
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                if arcs[arc_index].head == index + 1:
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            # if child_dict.has_key('SBV'):
            #    print words[index],child_dict['SBV']
            child_dict_list.append(child_dict)
        return child_dict_list

    '''句法分析---为句子中的每个词语维护一个保存句法依存儿子节点的字典'''

    def build_parse_child_dict(self, words, postags, arcs):
        # print(words, postags, "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

        child_dict_list = []
        format_parse_list = []
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):

                if arcs[arc_index].head == index + 1:  # arcs的索引从1开始
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            child_dict_list.append(child_dict)
        rely_id = [arc.head for arc in arcs]  # 提取依存父节点id
        relation = [arc.relation for arc in arcs]  # 提取依存关系
        heads = ['Root' if id == 0 else words[id - 1] for id in rely_id]  # 匹配依存父节点词语
        for i in range(len(words)):
            # ['ATT', '李克强', 0, 'nh', '总理', 1, 'n']
            a = [relation[i], words[i], i, postags[i], heads[i], rely_id[i] - 1, postags[rely_id[i] - 1]]
            format_parse_list.append(a)

        return child_dict_list, format_parse_list

    '''parser主函数'''

    def parser_main(self, sentence):
        words = list(self.segmentor.segment(sentence))
        postags = list(self.postagger.postag(words))
        arcs = self.parser.parse(words, postags)
        child_dict_list, format_parse_list = self.build_parse_child_dict(words, postags, arcs)
        parse_child_dict = self.build_parse_child_dict_two(words, arcs)
        roles_dict = self.format_labelrole(words, postags)
        return words, postags, child_dict_list, roles_dict, format_parse_list, parse_child_dict

    '''parser主函数'''

    def parser_main_two(self, sentence):
        words = list(self.segmentor.segment(sentence))
        postags = list(self.postagger.postag(words))
        arcs = self.parser.parse(words, postags)
        # 命名实体识别，主要是hi识别一些人名，地名，机构名等。
        netags = self.recognizer.recognize(words, postags)
        # 格式化数据
        child_dict_list, format_parse_list = self.build_parse_child_dict(words, postags, arcs)
        # 语义角色
        roles_dict = self.format_labelrole(words, postags)
        return words, postags, netags, arcs, child_dict_list, format_parse_list, roles_dict


def save_no_index_tag():
    list_remark = loadLine('../../res/foo.txt')

    fp = open('../../assert/triple-extractor.txt', "w", encoding='utf-8', errors='ignore')

    for item_data in list_remark:
        print('item_data', item_data)
        in_json = json.loads(item_data)  # Encode the data
        remarks = in_json['remarks'] if in_json['remarks'] else " "
        custom_state = in_json['custom_state'] if in_json['custom_state'] else "\t\t"
        if remarks != '':
            sentences = split_sents(remarks)
            temp_content = []
            for sentence in sentences:
                words, postags, child_dict_list, roles_dict, format_parse_list, parse_child_dict = parse.parser_main( sentence)
                for temp_item in format_parse_list:
                    if 'HED' in temp_item[0]:
                        temp_content.append(parse_child_dict[temp_item[2]])
            fp.write(custom_state + '-----' + str(words) +'++++++++'+temp_item[1]+'\t'+str(temp_content[0])+ '\n')
        else:
            fp.write(custom_state + '\t' + '' + '\n\n\n')
    fp.close()


if __name__ == '__main__':
    parse = LtpParser()
    # sentence = '李克强总理今天来我家了,我感到非常荣幸'
    # sentence = '没有需求'
    #
    # words, postags, child_dict_list, roles_dict, format_parse_list = parse.parser_main(sentence)
    save_no_index_tag()
