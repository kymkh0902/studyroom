from model import Model
from data_util import load_data, generator
from config import Config
import tensorflow as tf

## 변수로 할당된 값 불러오기 (hyperparameter, data dir, ...)
config = Config()
## data 불러오기
X_train, X_test, Y_train, Y_test = load_data(config.data_dir)
## 모델을 불러오기
model = Model(config)
## session 불러오기
sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

### saver를 넣어주어야 모델 정보가 생성됨. (code 폴더에 있는 코드 참조)
### 코드 입력 ###

## for loop을 통해 train 과정하기
for epoch_i in range(config.num_epochs):
    data_generator = generator(X_train, Y_train, config.batch_size)
    data_generator2 = generator(X_test, Y_test, config.batch_size)
    for batch_i, (X_batch_train, Y_batch_train) in enumerate(data_generator):
            model.train(sess, X_batch_train, Y_batch_train)
            if (batch_i + 1) % 100 == 0:
                # data_generator2로부터 데이터 가져오기)
                X_batch_test, Y_batch_test = next(data_generator2)
                test_loss, test_accuracy = model.eval(sess, X_batch_test, Y_batch_test)
                train_loss, train_accuracy = model.eval(sess, X_batch_train, Y_batch_train)
                print('Epoch: {0}, Batch: {1}/{2}, train_accuracy: {3:.3f}, test_accuracy: {4:.3f}'\
                    .format(epoch_i, batch_i + 1, len(X_train)//config.batch_size,
                            train_accuracy, test_accuracy))

### zip(A, B)는 A, B 중에 적은 데이터를 가지는 변수를 기준으로 돌아서 위에서 보면
### data_generator2가 중간에 끊겨서 멈추는 것으로 보임.
### test 데이터의 경우에는 train할 때마다 가져올 필요는 없어보이니까 그냥 아래로 빼는 것으로 변경