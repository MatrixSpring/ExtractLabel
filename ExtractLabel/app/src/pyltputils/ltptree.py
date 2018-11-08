# -*- coding: utf-8 -*-
from app.src.pyltputils.ltputil import LTPUtil

ltpUtil = LTPUtil()


class Node:
    def __init__(self, index, relation, head, postag, context, polarity, lchild=None, rchild=None):
        self.index = index
        self.head = head
        self.relation = relation
        self.postag = postag
        self.context = context
        self.polarity = polarity
        self.lindex = index
        self.rindex = index
        self.lchild = lchild
        self.rchild = rchild


class LTPTree:
    def __init__(self, index, relation, head, postag, context, polarity=0.0):
        self.root = Node(index, relation, head, postag, context, polarity)

    def addChild(self, child_tree):
        if child_tree.root.index < self.root.index:
            if self.root.lindex > child_tree.root.lindex:
                self.root.lindex = child_tree.root.lindex
            if self.root.lchild is None:
                self.root.lchild = list()
                self.root.lchild.append(child_tree)
            else:
                added_flag = False
                for iter in range(len(self.root.lchild))[::-1]:
                    if self.root.lchild[iter].root.head == child_tree.root.index:
                        sub_tree = self.root.lchild[iter]
                        child_tree.addChild(self.root.lchild[iter])
                        self.root.lchild.remove(sub_tree)
                if child_tree.root.lchild is not None:
                    # child_tree.root.lchild.sort(lambda x, y: cmp(x.root.index, y.root.index))
                    child_tree.root.lchild.sort(key=lambda x: {x.root.index})

                for iter in range(len(self.root.lchild)):
                    if child_tree.root.head == self.root.lchild[iter].root.index:
                        added_flag = True
                        self.root.lchild[iter].addChild(child_tree)
                    elif self.root.lchild[iter].inrange(child_tree.root.head):
                        added_flag = True
                        self.root.lchild[iter].addChild(child_tree)
                if added_flag is False:
                    self.root.lchild.append(child_tree)
                # self.root.lchild.sort(lambda x, y: cmp(x.root.index, y.root.index))
                self.root.lchild.sort(key=lambda x: {x.root.index})

        else:
            if self.root.rindex < child_tree.root.rindex:
                self.root.rindex = child_tree.root.rindex
            if self.root.rchild is None:
                self.root.rchild = list()
                self.root.rchild.append(child_tree)
            else:
                added_flag = False
                for iter in range(len(self.root.rchild))[::-1]:
                    if self.root.rchild[iter].root.head == child_tree.root.index:
                        sub_tree = self.root.rchild[iter]
                        child_tree.addChild(self.root.rchild[iter])
                        self.root.rchild.remove(sub_tree)
                # 如果出现顺序错误，可能要修改这里。
                if child_tree.root.rchild is not None:
                    # child_tree.root.rchild.sort(lambda x, y: cmp(x.root.index, y.root.index))
                    child_tree.root.rchild.sort(key=lambda x: {x.root.index})
                for iter in range(len(self.root.rchild)):
                    if self.root.rchild[iter].root.index == child_tree.root.head:
                        added_flag = True
                        self.root.rchild[iter].addChild(child_tree)
                    elif self.root.rchild[iter].inrange(child_tree.root.head):
                        added_flag = True
                        self.root.rchild[iter].addChild(child_tree)
                if added_flag is False:
                    self.root.rchild.append(child_tree)
                # self.root.rchild.sort(lambda x, y: cmp(x.root.index, y.root.index))
                self.root.rchild.sort(key=lambda x: {x.root.index})

    def getLIndex(self):
        return self.root.lindex

    def getRIndex(self):
        return self.root.rindex

    def toString(self):
        return "head: " + str(self.root.head) + "\t" + \
               "index: " + str(self.root.index) + "\t" + \
               "relation: " + self.root.relation + "\t" + \
               "postage: " + self.root.postag + "\t" + \
               "context: " + self.root.context + "\t" + \
               "polarity: " + str(self.root.polarity) + "\t" + \
               "lindex: " + str(self.root.lindex) + "\t" + \
               "rindex: " + str(self.root.rindex) + "\t"

    def toJson(self):
        return "{" + "head: " + "\"" + str(self.root.head) + "\"" + \
               "index: " + "\"" + str(self.root.index) + "\"" + \
               "relation: " + "\"" + self.root.relation + "\"" + \
               "postage: " + "\"" + self.root.postag + "\"" + \
               "context: " + "\"" + self.root.context + "\"" + \
               "polarity: " + "\"" + str(self.root.polarity) + "\"" + \
               "lindex: " + "\"" + str(self.root.lindex) + "\"" + \
               "rindex: " + "\"" + str(self.root.rindex) + "\"" + "}"


    def find(self, index):
        if index < self.root.lindex or index > self.root.rindex:
            print("Error! Out of range!")
        if index == self.root.index:
            return self
        elif index < self.root.index:
            for tree in self.root.lchild:
                if tree.inrange(index):
                    return tree.find(index)
        else:
            for tree in self.root.rchild:
                if tree.inrange(index):
                    return tree.find(index)


    def inrange(self, index):
        return (self.root.lindex <= index and self.root.rindex >= index)


    def getRoot(self):
        return self.root


def tree_parse(tree):
    # print('tree', tree)
    tree.find(0)


def tree_builder(sentence):
    words = ltpUtil.Segmentor(sentence)
    postags = ltpUtil.Postagger(words)
    arcs = ltpUtil.Parser(words, postags)

    head_index = -1
    for i in range(len(arcs)):
        if arcs[i].head == 0: head_index = i + 1

    # 属性polarity默认使用0.0,按需修改
    index = 0
    if head_index == -1:
        index = 0
    else:
        index = head_index - 1
    # print('index', index, postags, words)
    if postags and words:
        tree = LTPTree(head_index, 'HED', 0, postags[index], words[index])
    else:
        tree = LTPTree(head_index, 'HED', 0, postags, words)

    # 将子节点添加到树
    for i in range(len(arcs)):
        if i + 1 != head_index:
            p_tree = LTPTree(i + 1, arcs[i].relation, arcs[i].head, postags[i], words[i])
            tree.addChild(p_tree)
    return tree
