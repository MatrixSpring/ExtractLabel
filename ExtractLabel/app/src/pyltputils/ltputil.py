# -*- coding: utf-8 -*-
import pyltp


class LTPUtil:

    def __init__(self, seg_model_path='../../res/ltp/ltp_data_v3.4.0/cws.model',
                 pos_model_path='../../res/ltp/ltp_data_v3.4.0/pos.model',
                 rec_model_path='../../res/ltp/ltp_data_v3.4.0/ner.model',
                 par_model_path='../../res/ltp/ltp_data_v3.4.0/parser.model',
                 seg_lexicon_path='../../res/ltp/ltp_data_user/fulluserdict.txt'):
        self.__segmentor = None
        self.__seg_model_path = seg_model_path
        self.__seg_lexicon_path = seg_lexicon_path
        self.__postagger = None
        self.__pos_model_path = pos_model_path
        self.__recognizer = None
        self.__rec_model_path = rec_model_path
        self.__parser = None
        self.__par_model_path = par_model_path

    # split sentences
    def SentenceSplitter(self, sents):
        sentList = pyltp.SentenceSplitter.split(sents)
        return sentList

    # segment
    def Segmentor(self, sent):
        if self.__segmentor is None:
            self.__segmentor = pyltp.Segmentor()
            if self.__seg_lexicon_path is None:
                self.__segmentor.load(self.__seg_model_path)
            else:
                self.__segmentor.load_with_lexicon(self.__seg_model_path, self.__seg_lexicon_path)

        words = self.__segmentor.segment(sent)
        return words

    # postagger
    def Postagger(self, words=None, sent=None):
        if self.__postagger is None:
            self.__postagger = pyltp.Postagger()
            if self.__seg_lexicon_path is None:
                self.__postagger.load(self.__pos_model_path)
            else:
                self.__postagger.load_with_lexicon(self.__pos_model_path, self.__seg_lexicon_path)

        postags = None
        if sent is not None:
            words = self.Segmentor(sent)
            postags = self.__postagger.postag(words)
        else:
            postags = self.__postagger.postag(words)
        return postags

    # named entity recognizer
    def NamedEntityRecognizer(self, words=None, postags=None, sent=None):
        if self.__recognizer is None:
            self.__recognizer = pyltp.NamedEntityRecognizer()
            self.__recognizer.load(self.__rec_model_path)

        if sent is not None:
            words = self.Segmentor(sent)
            postags = self.Postagger(words)
        netags = self.__recognizer.recognize(words, postags)
        return netags

    # parser
    def Parser(self, words=None, postags=None, sent=None):
        if self.__parser is None:
            self.__parser = pyltp.Parser()
            self.__parser.load(self.__par_model_path)

        if sent is not None:
            words = self.Segmentor(sent)
            postags = self.Postagger(words)
        arcs = self.__parser.parse(words, postags)
        return arcs

    def __del__(self):
        if self.__segmentor is not None:
            self.__segmentor.release()

        if self.__postagger is not None:
            self.__postagger.release()

        if self.__recognizer is not None:
            self.__recognizer.release()

        if self.__parser is not None:
            self.__parser.release()
