import re


def split_sents(content):
    return [sentence for sentence in re.split(r'[？?！!，。；;：:\n\r]', content) if sentence]