# 预测
import pandas as pd
import numpy as np
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from nltk import word_tokenize


# 定义预测函数
def predict_spam(email_text, tokenizer, model):
    # 预处理邮件文本
    words = [word.lower() for word in word_tokenize(email_text)]
    tokenizer.fit_on_texts(words)
    # 将文本转换成序列
    sequences = tokenizer.texts_to_sequences([words])
    padded_sequence = pad_sequences(sequences, maxlen=50, padding='post', truncating='post')
    # 使用模型进行预测
    pred = model.predict(padded_sequence)[0][0]
    print(str(pred))
    label = 'spam' if pred >= 0.5 else 'ham'
    return label


# 定义预测邮件类别的方法
def predict_email_category(file_path):
    # 读取csv文件
    df = pd.read_csv(file_path)
    # # 加载训练好的模型
    model = load_model('spam_classifier.h5')
    tokenizer = Tokenizer()

    predict_result = []
    # 预测每个邮件的类别
    for index, row in df.iterrows():
        email_text = row['Email']
        label = predict_spam(email_text, tokenizer, model)
        print('Email text:', email_text)
        print('Label:', label)
        predict_result.append(label)
    return predict_result
