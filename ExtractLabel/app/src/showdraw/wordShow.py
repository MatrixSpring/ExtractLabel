# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt

import os
from wordcloud import WordCloud
from scipy.misc import imread


# 生成词云图
def show_word_cloud(word_content):
    print("wordContent : ", word_content)
    mask_img = imread('../assert/image/stormtrooper_mask.png')
    # 生成词云
    font = os.path.join(os.path.dirname(__file__), '../../res/ttf/DroidSansFallbackFull.ttf')
    word_show = WordCloud(
        max_font_size=40,
        font_path=font,
        mask=mask_img).generate(word_content)
    image_produce = word_show.to_image()
    image_produce.show()


# 生成饼状图
def show_pie_graph(word_content):
    # print("showPieGraph : " + wordContent)
    # make a square figure
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
    plt.figure(1, figsize=(6, 9))
    # print("showPieGraph : " + wordContent)

    labels = [u'大型', u'中型', u'小型', u'微型']
    sizes = [46, 253, 321, 66]  # 每块值

    list_labels = []  ## 空列表
    list_sizes = []  ## 空列表
    for item in word_content:
        list_labels.append(item['word'])  ## 使用 append() 添加元素
        size = float(item['count']) * 1000
        list_sizes.append(size)  ## 使用 append() 添加元素

    colors = ['red', 'yellowgreen', 'lightskyblue', 'yellow', 'green', 'blue']  # 每块颜色定义
    explode = (0, 0, 0, 0)  # 将某一块分割出来，值越大分割出的间隙越大
    patches, text1, text2 = plt.pie(list_sizes,
                                    # explode=explode,
                                    labels=list_labels,
                                    colors=colors,
                                    autopct='%3.2f%%',  # 数值保留固定小数位
                                    shadow=False,  # 无阴影设置
                                    startangle=90,  # 逆时针起始角度设置
                                    pctdistance=0.6)  # 数值距圆心半径倍数距离
    # patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部的文本
    # x，y轴刻度设置一致，保证饼图为圆形
    plt.axis('equal')
    plt.show()


# 生成饼状图
def show_pie_graph_two(word_content):
    # print("showPieGraph : " + wordContent)
    # make a square figure
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码
    plt.figure(1, figsize=(6, 9))
    # print("showPieGraph : " + wordContent)

    labels = [u'大型', u'中型', u'小型', u'微型']
    sizes = [46, 253, 321, 66]  # 每块值

    list_labels = []  ## 空列表
    list_sizes = []  ## 空列表
    for item in word_content:
        list_labels.append(item['class_type'])  ## 使用 append() 添加元素
        size = float(item['number'])
        list_sizes.append(size)  ## 使用 append() 添加元素

    colors = ['red', 'yellowgreen', 'lightskyblue', 'yellow', 'green', 'blue']  # 每块颜色定义
    explode = (0, 0, 0, 0)  # 将某一块分割出来，值越大分割出的间隙越大
    patches, text1, text2 = plt.pie(list_sizes,
                                    # explode=explode,
                                    labels=list_labels,
                                    colors=colors,
                                    autopct='%3.2f%%',  # 数值保留固定小数位
                                    shadow=False,  # 无阴影设置
                                    startangle=90,  # 逆时针起始角度设置
                                    pctdistance=0.6)  # 数值距圆心半径倍数距离
    # patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部的文本
    # x，y轴刻度设置一致，保证饼图为圆形
    plt.axis('equal')
    plt.show()


# 生成柱状图
def show_bar_graph(data_list):
    name_list = []  # 空列表标签
    num_list = []  # 空列表标签的数据
    for item in data_list:
        name_list.append(item['class_type'])    # 使用 append() 添加元素
        size = float(item['number'])
        num_list.append(size)                   # 使用 append() 添加元素
    plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list)
    plt.show()


# 生成雷达图
def show_radar_graph(data_list):
    # 数据个数
    data_lenth = 0
    name_list = []  # 空列表标签
    num_list = []  # 空列表标签的数据
    data_lenth = len(data_list)
    for item in data_list:
        name_list.append(item['class_type'])    # 使用 append() 添加元素
        size = float(item['number'])
        num_list.append(size)                   # 使用 append() 添加元素

    # ========自己设置结束============
    angles = np.linspace(0, 2 * np.pi, data_lenth, endpoint=False)
    num_list = np.concatenate((num_list, [num_list[0]]))  # 闭合
    angles = np.concatenate((angles, [angles[0]]))  # 闭合

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)  # polar参数！！
    ax.plot(angles, num_list, 'bo-', linewidth=2)  # 画线
    ax.fill(angles, num_list, facecolor='r', alpha=0.25)  # 填充
    ax.set_thetagrids(angles * 180 / np.pi, name_list, fontproperties="SimHei")
    ax.set_title("matplotlib雷达图", va='bottom', fontproperties="SimHei")
    ax.set_rlim(0, 10)
    ax.grid(True)
    plt.show()
