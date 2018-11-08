import fasttext

# 训练监督文本，train_data.txt，模型会默认保存在当前目录下，名称为"fasttext_test.model.bin"；thread表示以3个线程进行训练，不加默认1个线程
classifier = fasttext.supervised('../../res/foo-60k.txt', 'fasttext_test.model', label_prefix='__label__', thread=3)

# 验证数据集
result = classifier.test('../../assert/normalSentence.json')
# 输出准确率和召回率
print(result.precision, result.recall)

# 预测文本分类, articles是一段文本用字符串表示, k=3表示输入可能性较高的三个分类，不加参数默认只输出一个
result = classifier.predict('../../res/foo.txt', k=3)

# 载入模型
classifier = fasttext.load_model("fasttext_test.model.bin", label_prefix="__label__")
