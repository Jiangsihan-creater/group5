# -*- coding: utf-8 -*-
# @Project : Spam_Email_Classificaton
# @FileName: spam_calssification_GloVe.py
# @Software: PyCharm
import pandas as pd
import numpy as np
import re
import string
import os

from sklearn.model_selection import train_test_split
from tqdm import tqdm
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer  # 词干提取
from sklearn import metrics
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, SpatialDropout1D, Dropout, GRU, SimpleRNN
# from keras.initializers import Constant
from keras.optimizers import Adam

stemmer = PorterStemmer()
# 加载停用词
STOPWORDS = set(stopwords.words("english"))
PUNCT_TO_REMOVE = string.punctuation


# 数据清洗
def data_processing(text: str):
    text = text.lower()
    text = re.compile(r'https?://\S+|www\.\S+').sub(r'', text)
    text = text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))
    text = " ".join([word for word in str(text).split() if word not in STOPWORDS])
    text = " ".join([stemmer.stem(word) for word in text.split()])
    return text


# 归一化
def label_TO_2D(label: str):
    if label == 'ham':
        return 0
    else:
        return 1


# email = np.array(train['Email']).reshape((1, len(train)))[0].tolist()
# label = np.array(train['Label']).reshape((1, len(train)))[0].tolist()

# 划分数据集，9:1
# train_email, train_label, test_email, test_label = [], [], [], []
# for i in range(len(train)):
#     if i % 10 != 0:
#         train_email.append(email[i])
#         train_label.append(label[i])
#     else:
#         test_email.append(email[i])
#         test_label.append(label[i])

# 评测模型
def metrics_MODLE(true_labels, predicted_labels):
    dic = {}
    """
    :param true_labels: 实际的标签（类别）
    :param predicted_labels: 预测的类别
    :return:
    """
    accuracy_score = np.round(metrics.accuracy_score(true_labels, predicted_labels), 5)
    precision_score = np.round(metrics.precision_score(true_labels, predicted_labels, average='weighted'), 5)
    recall_score = np.round(metrics.recall_score(true_labels, predicted_labels, average='weighted'), 5)
    f1_score = np.round(metrics.f1_score(true_labels, predicted_labels, average='weighted'), 5)
    print('正确率:', accuracy_score)
    print('精度:', precision_score)
    print('召回率:', recall_score)
    print('F1得分:', f1_score)
    dic = {"accuracy_score": accuracy_score, "precision_score": precision_score, "recall_score": recall_score,
           "f1_score": f1_score}
    return dic


def create_corpus_new(df):
    print(
        "——————————————————————————————————————————————加载csv文件数据到corpus列表中————————————————————————————————————————————————————")
    corpus = []
    for tweet in tqdm(df['Email']):
        words = [word.lower() for word in word_tokenize(tweet)]  # w
        corpus.append(words)  #
    return corpus


def _train(proportion, data_path, batch_size=4, epochs=3):
    # 加载训练数据 读取csv格式训练数据集 存贮在一个名为train的pandas数据框中
    traindata = pd.read_csv(data_path, encoding='utf-8')
    print('traindata ---------------------------- \n')
    print(traindata)

    traindata['Email'] = traindata['Email'].apply(data_processing)
    traindata['Label'] = traindata['Label'].apply(label_TO_2D)

    # cleandata = traindata
    # corpus = create_corpus_new(cleandata)
    # 创建语料库
    corpus = create_corpus_new(traindata)

    print(os.getcwd())
    # embedding_dict = {}
    # with open("./glove/glove.6B.100d.txt", 'r', encoding='utf-8') as f:
    #     for line in f:
    #         values = line.split()
    #         word = values[0]
    #         vectors = np.asarray(values[1:], 'float32')
    #         embedding_dict[word] = vectors

    # 配置模型
    MAX_LEN = 50
    tokenizer_obj = Tokenizer()
    tokenizer_obj.fit_on_texts(corpus)
    sequences = tokenizer_obj.texts_to_sequences(corpus)

    # 完成分词和编码后通过padding把所有词向量补成同样长度
    tweet_pad = pad_sequences(sequences, maxlen=MAX_LEN, truncating='post', padding='post')

    word_index = tokenizer_obj.word_index  # index从1开始
    print('Number of unique words:', len(word_index))  # 总共有多少个单独的词

    num_words = len(word_index) + 1  # 添加0行，index从1开始
    # embedding_matrix = np.zeros((num_words, 100))
    #
    # print("————————————————————————————————————生成编码矩阵——————————————————————————————————————")
    # for word, i in tqdm(word_index.items()):
    #     if i < num_words:
    #         emb_vec = embedding_dict.get(word)
    #         if emb_vec is not None:
    #             embedding_matrix[i] = emb_vec
    #
    # print(embedding_matrix)

    # 构建模型
    model = Sequential()
    # 100, embeddings_initializer=Constant(embedding_matrix)
    embedding = Embedding(num_words, 100, embeddings_initializer='glorot_normal', input_length=MAX_LEN, trainable=False)

    model.add(embedding)

    model.add(SpatialDropout1D(0.2))

    # model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model.add(GRU(64, input_shape=(None, 50, 100), return_sequences=True, dropout=0.2, recurrent_dropout=0.2))
    model.add(GRU(32))
    # model.add(GRU(100,dropout=0.2,recurrent_dropout=0.2))

    # model.add(SimpleRNN(100,dropout=0.2,recurrent_dropout=0.2))

    model.add(Dense(1, activation='sigmoid'))

    # 设置训练参数
    optimizer = Adam(lr=5e-4)
    # 编译
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    print("——————————————————————————————————————模型各层的参数状况——————————————————————————————————————————————————")
    model.summary()

    train_data = tweet_pad[:2000]
    test_data = tweet_pad[4000:]

    # test_size=0.2 划分测试集的比例，将3000行数据中划分出20%=600行作为测试集
    X_train, X_test, y_train, y_test = train_test_split(train_data, traindata[:2000]['Label'].values, test_size=0.2)
    print("训练集的形状:", X_train.shape)
    print("交叉验证集形状:", X_test.shape)

    # barch_size =4 训练一次网络用4个样本，epochs=2 全部样本被训练两次后结束模型训练 validation_data 指定验证数据 verbose=2 每个epoch输出一行记录
    glove_model = model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_test, y_test),
                            verbose=2)

    test_pred = model.predict(test_data)  # 获取预测值
    print('预测值----------------------------------------\n\n')
    # print(str(test_pred))

    test_pred_int = test_pred.round().astype('int')
    # print(test_pred_int)

    # 保存模型
    model.save('spam_classifier.h5')

    # evaluate model prediction performance
    return metrics_MODLE(true_labels=traindata[4000:]['Label'].values,
                         predicted_labels=test_pred_int)
