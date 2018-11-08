# coding=utf-8
from app.src.structure.Trie import Trie

word_stop_path = '../../res/lexicon/word-stop.txt'
word_time_path = '../../res/lexicon/nt-time.txt'

# 源文件


# 获取固定格式(每一行一个数据的内容)
def item_words_list(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


class FilterCategory(object):

    def __init__(self):
        self.stopwords = item_words_list(word_stop_path)
        self.timewords = item_words_list(word_time_path)
        self.interest_word = item_words_list(word_positive_path)
        self.indifferent_word = item_words_list(word_negative_path)
        self.trie = Trie()
        self.word_product = item_words_list(word_product_path)
        for item_data in self.word_product:
            self.trie.add(item_data)

    # 对停用词过滤
    def filter_stop_word(self, words):
        """
        对停用词过滤
        :param words: list
        :return:
        """
        outstr = ''
        for word in words:
            if word not in self.stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        return outstr

    # 联系方式：电话 短信 微信 见面 约见 预约 邮寄
    def filter_contact_method(self, words):
        cmode = ["电话", "短信", "微信", "见面", "约见", "预约", "邮寄", "寄", '寄送' "约", '约好了' '邀约', '推荐', '推', '推下',
                 '沟通', '询问', '告诉', '跟进', '邮箱', '语音信箱', '邀请', '拜访', '座机', '回访', '跟跟', '邀请函']
        intersection = [item for item in cmode if item in words]
        return intersection

    # 过滤投资方式
    def filter_finance_method(self, words):
        # 固定收入 银行理财
        solid_investment = ['固收', '短期固收', '保守', '银行理财', '银行']
        # 股票
        stock_investment = ['股市', '股票', '套着', '炒股', '股市套起', '股市底', '炒股票', '炒炒股']
        # 房地产
        realty_investment = ['房子', '房产', '买房了', '买了房', '买房子了', '买房产了', '住宅', '房地产']
        # 海外投资 海外账户
        overseas_investment = ['海外保险', '美金', '美元', '美元基金', '美元项目', '海外账户', '美元股权', '美金保险',
                               '美元产品', '海外', '港币', '']
        # 期货
        future_investment = ['期货', '炒原油', '大宗', '大宗商品']
        # 基金
        fund_investment = ['基金', '建仓', '持仓', '加仓', '补仓', '满仓', '半仓', '重仓', '轻仓', '空仓', '平仓',
                           '做多', '做空', '踏空', '逼空', '套期保值']
        # 保险
        insurance_investment = ['保险', '平安', '人寿', '大都会', '泰康养老保险', '重疾险', '分红险', '重疾']
        # 其他
        other_investment = ['比特币', 'P2P', '放低快贷', '房抵快贷', '房地快贷', '黄金', '贵金属', '私募', '股权', '币圈', '区块链']

        solid_investment_list = [item for item in solid_investment if item in words]
        stock_investment_list = [item for item in stock_investment if item in words]
        realty_investment_list = [item for item in realty_investment if item in words]
        overseas_investment_list = [item for item in overseas_investment if item in words]
        future_investment_list = [item for item in future_investment if item in words]
        fund_investment_list = [item for item in fund_investment if item in words]
        insurance_investment_list = [item for item in insurance_investment if item in words]
        other_investment_list = [item for item in other_investment if item in words]

        return solid_investment_list, stock_investment_list, realty_investment_list, overseas_investment_list, \
               future_investment_list, fund_investment_list, insurance_investment_list, other_investment_list

    # 过滤客户的风险等级
    def filter_risk_level(self, words):
        # 谨慎 不热观的
        # 可以先过滤词汇的词性 加快效率
        prudent_investment = ['观望', '雷太多', '稳健型', '暴雷', '亏损了', '亏损', '跑路', '保守', '亏了', '都赔了',
                              '没钱投', '没钱了', '不太敢投', '无风险', '市场太乱', '踩雷', '谨慎', '低风险', '悲观',
                              '不热观', '风险', '风控不足', '风控', '不足', '爆仓', '没经验', '没有经验', '太差', '下行',
                              '犹豫', '受伤', '被骗', '安全', '冷淡', '担忧', '安全性', '行情不好', '不好', '不安全',
                              '没钱', '贸易战', '清盘', '都赔了', '不投了', '风险太大', '负面消息', '不放心', '担心',
                              '不太敢', '不敢', '再考虑', '担忧', '保守', '赎回', '无存续', '不打算', '很担心']
        return [item for item in prudent_investment if item in words]

    # 过滤专有名词 地名 机构
    def filter_proper_names(self, netags, words):
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
    def filter_time_date(self, words):
        """
        过滤时间词汇
        :param words:
        :return:
        """
        return [item for item in self.timewords if item in words]

    # 过滤兴趣爱好的指标打分
    def filter_discuss_hobbies(self, words):
        """
        过滤是否有兴趣的词 分为两类一类表现出感兴趣
        :param words:
        :return:
        """
        # 感兴趣
        interest_list = [item for item in self.interest_word if item in words]
        # 不敢兴趣
        indifferent_list = [item for item in self.indifferent_word if item in words]
        return interest_list, indifferent_list

    # 过滤产品名称
    def filter_product_name(self, netags, words):
        """
        使用trie 树存储产品名称信息,传进来句子分词列表
        :param words:
        :return:
        """
        print('filter_product_name', netags, words)
        # 必须是名词查询才有意义
        type_list = ['m', 'i', 'n', 'nd', 'nh', 'ni', 'nl', 'ns', 'nt', 'nz']
        filter_netags = [item for item in type_list if item in netags]
        word_list = []
        if filter_netags:
            for word in filter_netags:
                result_list = self.trie.wordsWithPrefix(words[netags.index(word)])
                if result_list:
                    word_list.append(result_list)
        return word_list
