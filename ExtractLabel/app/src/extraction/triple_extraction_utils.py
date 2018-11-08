# coding: utf-8

import re

from pandas.io.json import json

from app.src.extraction.sentence_parser import LtpParser, split_sents
from app.src.filter.filterclass import FilterCategory


class TripleExtractor:
    def __init__(self):
        self.parser = LtpParser()
        self.filterCategory = FilterCategory()

    def complex_prefix(self, words, postags, child_dict_list, word_index):
        node = child_dict_list[word_index]
        if 'ADV' in node:
            return words[node.get('ADV')[0]]
        return ""

    def complete_e(self, words, postags, child_dict_list, word_index):
        """
        完善识别的部分实体
        """
        child_dict = child_dict_list[word_index]
        prefix = ''
        if 'ATT' in child_dict:
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])

        postfix = ''
        if postags[word_index] == 'v':
            if 'VOB' in child_dict:
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if 'SBV' in child_dict:
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

        return prefix + words[word_index] + postfix

    '''利用语义角色标注,直接获取主谓宾三元组,基于A0,A1,A2'''

    def fact_triple_extract(self, sentence, words, postags, netags, arcs, child_dict_list):

        # child_dict_list = self.build_parse_child_dict(words, arcs)

        itemShow = []
        for item in netags:
            itemShow.append(item)
        print('child_dict_list', child_dict_list, words, arcs, itemShow)
        result = []
        for index in range(len(postags)):
            # 抽取以谓词为中心的事实三元组
            if postags[index] == 'v':
                child_dict = child_dict_list[index]
                # 主谓宾
                if 'SBV' in child_dict:
                    if 'VOB' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        r = words[index]
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                        result.append("主语谓语宾语关系\t(%s, %s, %s)\n" % (e1, r, e2))
                    else:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        r = words[index]
                        e2 = ''
                        result.append("动宾短语\t(%s, %s, %s)\n" % (e1, r, e2))
                # 含有介宾关系的主谓动补关系
                elif 'SBV' in child_dict:
                    if 'CMP' in child_dict:
                        print('微信搜不到 微信搜不到')
                        # e1 = words[child_dict['SBV'][0]]
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        cmp_index = child_dict['CMP'][0]
                        if 'POB' in child_dict_list[cmp_index]:
                            # r 需要补齐
                            cmp_context = self.complete_e(words, postags, child_dict_list, child_dict['CMP'][0])
                            r = words[index] + cmp_context + words[cmp_index]
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
                            result.append("介宾关系主谓动补\t(%s, %s, %s)\n" % (e1, r, e2))
                        else:
                            cmp_context = self.complex_prefix(words, postags, child_dict_list, child_dict['CMP'][0])
                            r = words[index]
                            e2 = cmp_context + words[cmp_index]
                            result.append("介宾关系主谓动补\t(%s, %s, %s)\n" % (e1, r, e2))
                    else:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        r = words[index]
                        e2 = ''
                        result.append("介宾短语\t(%s, %s, %s)\n" % (e1, r, e2))
                # 定语后置，动宾关系
                elif arcs[index].relation == 'ATT':
                    if 'VOB' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, arcs[index].head - 1)
                        r = words[index]
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                        temp_string = r + e2
                        if temp_string == e1[:len(temp_string)]:
                            e1 = e1[len(temp_string):]
                        if temp_string not in e1:
                            result.append("定语后置动宾关系\t(%s, %s, %s)\n" % (e1, r, e2))
                # 并列关系   左附加关系（LAD）右附加关系（RAD）
                elif 'COO' in child_dict:
                    print('附加关系')


            elif postags[index] == 'p':
                child_dict = child_dict_list[index]
                print('主语是介词', sentence, words, child_dict)
                # 主谓宾
                if 'SBV' in child_dict and 'POB' in child_dict:
                    e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                    r = words[index]
                    e2 = self.complete_e(words, postags, child_dict_list, child_dict['POB'][0])
                    result.append("2.1主语介词宾语关系\t(%s, %s, %s)\n" % (e1, r, e2))
                # 介宾短语
                if 'ADV' in child_dict and 'POB' in child_dict:
                    e1 = self.complete_e(words, postags, child_dict_list, child_dict['ADV'][0])
                    r = words[index]
                    e2 = self.complete_e(words, postags, child_dict_list, child_dict['POB'][0])
                    result.append("2.2介宾短语\t(%s, %s, %s)\n" % (e1, r, e2))

        print('result ', sentence, result)
        return result

    '''利用语义角色标注,直接获取主谓宾三元组,基于A0,A1,A2'''

    def fact_triple_extract_two(self, sentence, words, postags, netags, arcs, child_dict_list, format_parse_list,
                                roles_dict):
        print('child_dict_list', child_dict_list, format_parse_list, roles_dict)

        itemShow = []
        for item in netags:
            itemShow.append(item)
        print('child_dict_list', child_dict_list, words, arcs, itemShow)
        result = []
        # for index in range(len(postags)):
        for itemData in format_parse_list:
            if 'HED' in itemData[0]:
                # 抽取以谓词为中心的事实三元组
                if itemData[3] == 'v':
                    child_dict = child_dict_list[itemData[2]]
                    # 主谓宾
                    if 'SBV' in child_dict:
                        if 'VOB' in child_dict:
                            e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                            r = words[itemData[2]]
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                            result.append("主语谓语宾语关系\t(%s, %s, %s)\n" % (e1, r, e2))
                        elif 'CMP' in child_dict:
                            e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                            r = words[itemData[2]]
                            e2 = self.complex_prefix(words, postags, child_dict_list, child_dict['CMP'][0]) + \
                                 self.complete_e(words, postags, child_dict_list, child_dict['CMP'][0])
                            result.append("谓语补足语关系\t(%s, %s, %s)\n" % (e1, r, e2))
                        else:
                            e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                            r = words[itemData[2]]
                            e2 = ""
                            result.append("动宾短语 : ('"'%s'"', '"'%s'"', '"'%s'"')" % (e1, r, e2))
                    # 含有介宾关系的主谓动补关系
                    elif 'SBV' in child_dict:
                        if 'CMP' in child_dict:
                            print('微信搜不到 微信搜不到')
                            # e1 = words[child_dict['SBV'][0]]
                            e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                            cmp_index = child_dict['CMP'][0]
                            if 'POB' in child_dict_list[cmp_index]:
                                # r 需要补齐
                                cmp_context = self.complete_e(words, postags, child_dict_list, child_dict['CMP'][0])
                                r = words[itemData[2]] + cmp_context + words[cmp_index]
                                e2 = self.complete_e(words, postags, child_dict_list,
                                                     child_dict_list[cmp_index]['POB'][0])
                                result.append("介宾关系主谓动补\t(%s, %s, %s)\n" % (e1, r, e2))
                            else:
                                cmp_context = self.complex_prefix(words, postags, child_dict_list, child_dict['CMP'][0])
                                r = words[itemData[2]]
                                e2 = cmp_context + words[cmp_index]
                                result.append("介宾关系主谓动补\t(%s, %s, %s)\n" % (e1, r, e2))
                        else:
                            e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                            r = words[itemData[2]]
                            e2 = ''
                            result.append("介宾短语\t(%s, %s, %s)\n" % (e1, r, e2))
                    # # 定语后置，动宾关系
                    # elif arcs[itemData[0]].relation == 'ATT':
                    #     if 'VOB' in child_dict:
                    #         e1 = self.complete_e(words, postags, child_dict_list, arcs[itemData[2]].head - 1)
                    #         r = words[itemData[2]]
                    #         e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                    #         temp_string = r + e2
                    #         if temp_string == e1[:len(temp_string)]:
                    #             e1 = e1[len(temp_string):]
                    #         if temp_string not in e1:
                    #             result.append("定语后置动宾关系\t(%s, %s, %s)\n" % (e1, r, e2))
                    # 并列关系   左附加关系（LAD）右附加关系（RAD）
                    elif 'COO' in child_dict:
                        print('附加关系')
                    elif 'VOB' in child_dict:
                        print('介宾关系主谓动补')
                        e1 = self.complete_e(words, postags, child_dict_list, arcs[itemData[2]].head - 1)
                        r = words[itemData[2]]
                        # e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                        result.append("定语后置动宾关系\t(%s, %s, %s)\n" % (e1, r, ''))
                elif itemData[3] is 'p':
                    child_dict = child_dict_list[itemData[2]]
                    print('主语是介词', sentence, words, child_dict)
                    # 主谓宾
                    if 'SBV' in child_dict and 'POB' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        r = words[itemData[2]]
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['POB'][0])
                        result.append("2.1主语介词宾语关系\t(%s, %s, %s)\n" % (e1, r, e2))
                    # 介宾短语
                    elif 'ADV' in child_dict and 'POB' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['ADV'][0])
                        r = words[itemData[2]]
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['POB'][0])
                        result.append("2.2介宾短语\t(%s, %s, %s)\n" % (e1, r, e2))
                elif itemData[3] is 'p':
                    child_dict = child_dict_list[itemData[2]]
                    print('主语是介词', sentence, words, child_dict)
                    # 主谓宾
                    if 'SBV' in child_dict and 'POB' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        r = words[itemData[2]]
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['POB'][0])
                        result.append("2.1主语介词宾语关系\t(%s, %s, %s)\n" % (e1, r, e2))
                    # 介宾短语
                    elif 'ADV' in child_dict and 'POB' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['ADV'][0])
                        r = words[itemData[2]]
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['POB'][0])
                        result.append("2.2介宾短语\t(%s, %s, %s)\n" % (e1, r, e2))
        print('result ', sentence, result)
        return result

    def triples_main(self, content):
        '''程序主控函数'''
        sentences = split_sents(content)
        # 主谓宾定状补 三元组
        svos_list = []
        svos = []
        # 联系方式
        contact_method = []
        # 机构名称
        agency_product = []
        # 时间名词
        time_list = []
        # 感兴趣
        interest_result = []
        # 不感兴趣
        indifferent_result = []
        # 产品名称
        product_list = []
        # 固收
        solid_list = []
        # 股票
        stock_list = []
        # 房地产
        realty_list = []
        # 海外投资 海外账户
        overseas_list = []
        # 期货
        future_list = []
        # 基金
        fund_list = []
        # 保险
        insurance_list = []
        # 其他
        other_list = []
        # 风险偏好
        risk_level = []
        for sentence in sentences:
            words, postags, netags, arcs, child_dict_list, format_parse_list, roles_dict = self.parser.parser_main_two(
                sentence)
            # svo = self.fact_triple_extract_two(sentence, words, postags, netags, arcs, child_dict_list, format_parse_list, roles_dict)

            svo = self.fact_triple_extract(sentence, words, postags, netags, arcs, child_dict_list)
            # 过滤联系方式
            for item in self.filterCategory.filter_contact_method(words):
                contact_method.append(item)
            # 过滤机构产品
            proper_names = self.filterCategory.filter_proper_names(netags, words)
            if proper_names.strip() != "":
                agency_product.append(proper_names)
            # 过滤时间名词
            for time_item in self.filterCategory.filter_time_date(words):
                time_list.append(time_item)
            # 过滤兴趣爱好的指标打分
            interest_list, indifferent_list = self.filterCategory.filter_discuss_hobbies(words)
            for interest_item in interest_list:
                interest_result.append(interest_item)
            for indifferent_item in indifferent_list:
                indifferent_result.append(indifferent_item)
            # 过滤产品名称
            products = self.filterCategory.filter_product_name(postags, words)
            for product_item in products:
                product_list.append(product_item)

            # 过滤理财方式
            # 固收，股票，房地产， 海外投资 海外账户，期货，基金，保险，其他
            solid_investment, stock_investment, realty_investment, overseas_investment, future_investment, fund_investment, insurance_investment, other_investment = self.filterCategory.filter_finance_method(words)
            for solid_item in solid_investment:
                solid_list.append(solid_item)
            # 股票
            for stock_item in stock_investment:
                stock_list.append(stock_item)
            # 房地产
            for realty_item in realty_investment:
                realty_list.append(realty_item)
            # 海外投资 海外账户
            for overseas_item in overseas_investment:
                overseas_list.append(overseas_item)
            # 期货
            for future_item in future_investment:
                future_list.append(future_item)
            # 基金
            for fund_item in fund_investment:
                fund_list.append(fund_item)
            # 保险
            for insurance_item in insurance_investment:
                insurance_list.append(insurance_item)
            # 其他
            for other_item in other_investment:
                other_list.append(other_item)

            # 过滤风险担心
            risk_list = self.filterCategory.filter_risk_level(words)
            for risk_item in risk_list:
                risk_level.append(risk_item)
            # 提取内容添加
            for svo_item in svo:
                svos.append(svo_item)

        svos_list.append({"contact_method": contact_method})
        svos_list.append({"agency_product": agency_product})
        svos_list.append({"time_list": time_list})
        svos_list.append({"interest_result": interest_result, "indifferent_result": indifferent_result})
        svos_list.append({"product_list": product_list})
        svos_list.append({"solid_list": solid_list, "stock_list": stock_list, "realty_list": realty_list, "overseas_list": overseas_list,
                     "future_list": future_list, "fund_list": fund_list, "insurance_list": insurance_list, "other_list": other_list})
        svos_list.append({"risk_level": risk_level})
        svos_list.append(svos)
        return svos_list


''' 提取（产品）名词 提取沟通方式 提取三元组内容'''
if __name__ == "__main__":
    extractor = TripleExtractor()

    # content6 = '一听就说不在这边买了，现在有点忙 挂断'
    content6 = '爱人任延涛做主'
    svos = extractor.triples_main(content6)
    print('svos', svos)

    # filePersist = FilePersist()
    # list_remark = filePersist.loadLine('../../res/foo.txt')
    #
    # fp = open('../../assert/tree-triple-extractor-4.txt', "w", encoding='utf-8', errors='ignore')
    # for item_data in list_remark:
    #     in_json = json.loads(item_data)  # Encode the data
    #     remarks = in_json['remarks'] if in_json['remarks'] else " "
    #     if remarks != '':
    #         custom_state = in_json['custom_state'] if in_json['custom_state'] else " "
    #         # out_json = {}
    #         # out_json["custom_state"] = custom_state
    #         # out_json["remarks"] = remarks
    #
    #         svos = extractor.triples_main(remarks)
    #         # print('svos', remarks, str(svos))
    #         # if len(svos):
    #         #     content = ", ".join(svos)
    #         # else:
    #         #     content = svos
    #         fp.write(custom_state + '\t' + remarks + '\t' + str(svos) + '\n')
    # fp.close()
