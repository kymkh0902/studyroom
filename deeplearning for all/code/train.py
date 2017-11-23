from model import Model
from data_util import load_data, generator
from config import Config
import tensorflow as tf

# 변수로 할당된 값을 불러온다. (hyperparameter, data dir, ...)
config = Config()
# data를 불러온다.
X_train, X_test, y_train, y_test = load_data(config.data_dir)
# 모델을 불러온다.
model = Model(config)
# session을 불러온다.
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# for loop를 통한 train 과정
for epoch_i in range(config.num_epochs):
    data_generator = generator(X_train, y_train, config.batch_size)
    for batch_i, (X_batch, y_batch) in enumerate(data_generator):
        model.train(sess, X_batch, y_batch)
        if (batch_i + 1) % 100 == 0:
            test_loss, test_accuracy = model.eval(sess, X_test, y_test)
            train_loss, train_accuracy = model.eval(sess, X_train, y_train)
            print('Epoch: {0}, Batch: {1}/{2}, train_accuracy: {3:.3f}, test_accuracy: {4:.3f}'\
                  .format(epoch_i, batch_i + 1, len(X_train)//config.batch_size,
                          train_accuracy, test_accuracy))


