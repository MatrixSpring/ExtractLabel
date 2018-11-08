# coding: utf-8
from pandas.io.json import json

class MarkRecord(object):

    def __init__(self):
        print('初始化~')
        # 这个需要设计
        # 负面词设置为-400， 担心类型-200， 感兴趣+200， 推荐产品+200
        self.score_indifferent = -400
        self.score_risk = -200
        self.score_interest = 200
        self.score_recommend_products = 200
        self.total_score = 0

    def mark_record(self, itemdata):
        print('打分')

        print('兴趣指标', itemdata[1], type(itemdata[1]))

        # contact_method = json.loads(itemdata[1])  # Encode the data
        # agency_product = json.loads(itemdata[2])  # Encode the data
        # time_list = json.loads(itemdata[3])  # Encode the data
        # emotion_status = json.loads(itemdata[4])  # Encode the data
        # product_list = json.loads(itemdata[5])  # Encode the data
        # money_manage = json.loads(itemdata[6])  # Encode the data
        # risk_level = json.loads(itemdata[7])  # Encode the data

        contact_method = itemdata[0]  # Encode the data
        agency_product = itemdata[1]  # Encode the data
        time_list = itemdata[2]  # Encode the data
        emotion_status = itemdata[3]  # Encode the data
        product_list = itemdata[4]  # Encode the data
        money_manage = itemdata[5]  # Encode the data
        risk_level = itemdata[6]  # Encode the data

        print('兴趣指标',  emotion_status['indifferent_result'], emotion_status['interest_result'])
        print('理财方式', money_manage['solid_list'], money_manage['stock_list'], money_manage['realty_list'], money_manage['overseas_list'],
              money_manage['future_list'], money_manage['fund_list'], money_manage['insurance_list'], money_manage['insurance_list'],)
        print('risk_level', risk_level['risk_level'])

        self.total_score = len(emotion_status['indifferent_result']) * self.score_indifferent

        self.total_score = self.total_score + len(emotion_status['interest_result']) * self.score_interest

        if len(product_list['product_list']) > 0:
            self.total_score = self.total_score + self.score_recommend_products

        self.total_score = self.total_score + len(risk_level['risk_level']) * self.score_risk

        return self.total_score