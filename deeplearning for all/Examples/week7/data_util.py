import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from config import Config

## 데이터 부르기
def load_data(file_dir):
    mnist = input_data.read_data_sets(file_dir, one_hot=True)
    X_train = mnist.train.images.reshape(-1, 28, 28, 1)
    X_test = mnist.test.images.reshape(-1, 28, 28, 1)
    Y_train = mnist.train.labels
    Y_test = mnist.test.labels
    return X_train, X_test, Y_train, Y_test


## Generator 생성 함수
def generator(data, labels, batch_size):
    size = data.shape[0]
    shuffled_indices = np.random.choice(size, size, replace=False)
    data = data[shuffled_indices]
    labels = labels[shuffled_indices]
    for i in range(size // batch_size):
        yield data[i*batch_size: (i+1)*batch_size], labels[i*batch_size: (i+1)*batch_size]


## RNN 새로운 변수 설정 관련
def load_RNN_data(sentence):
    dataX = []
    dataY = []

    for i in range(0, len(sentence) - config.seq_length):
        x_str = sentence[i:i + config.seq_length]
        y_str = sentence[i + 1: i + config.seq_length + 1]

        x = [config.char_dic[c] for c in x_str]
        y = [config.char_dic[c] for c in y_str]

        dataX.append(x)
        dataY.append(y)

        batch_size = len(dataX)

    return dataX, dataY, batch_size