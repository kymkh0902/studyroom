import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

## 데이터 부르기
def load_data(file_dir):
    mnist = input_data.read_data_sets(file_dir, one_hot=True)
    X_train = mnist.train.images
    X_test = mnist.test.images
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
