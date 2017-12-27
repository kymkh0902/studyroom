import numpy as np
import os

## 데이터 부르기
def load_data(path, seq_length):
    sentence = os.path.join(path)
    with open(sentence, "r", encoding='utf-8', errors='ignore') as f:
        sentence = f.read()

    char_set = list(set(sentence))
    char_dic = {w: i for i, w in enumerate(char_set)}

    dataX = []
    dataY = []

    for i in range(0, len(sentence) - seq_length):
        x_str = sentence[i:i + seq_length]
        y_str = sentence[i + 1: i + seq_length + 1]

        x = [char_dic[c] for c in x_str]
        y = [char_dic[c] for c in y_str]

        dataX.append(x)
        dataY.append(y)

    dataX = np.array(dataX)
    dataY = np.array(dataY)

    X_train = dataX[:round(dataX.shape[0] * 0.8)]
    X_test = dataX[round(dataX.shape[0] * 0.8):]
    Y_train = dataX[:round(dataY.shape[0] * 0.8)]
    Y_test = dataX[round(dataY.shape[0] * 0.8):]
    return char_set, X_train, X_test, Y_train, Y_test


## Generator 생성 함수
def generator(data, labels, batch_size):
    size = data.shape[0]
    shuffled_indices = np.random.choice(size, size, replace=False)
    data = data[shuffled_indices]
    labels = labels[shuffled_indices]
    for i in range(size // batch_size):
        yield data[i*batch_size: (i+1)*batch_size], labels[i*batch_size: (i+1)*batch_size]
