# coding: utf-8
# 跟单笔记预处理，
# 1.对于词语数量只有四个的词汇进行不做分词处理 直接找对于的词库或者内容过滤
# 2.对于全部文本的整合全部输出到一个文件种，做词频统计 图形显示
# 3.对文本做了打分处理后，可以做类型相识度处理，检测打分结果

class NotesPretreatment(object):
    def __init__(self):
        print('初始化')

