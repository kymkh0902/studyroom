import tensorflow as tf
from config import Config
from data_util import load_data
import numpy as np

config = Config()
graph = tf.get_default_graph()
sess = tf.Session()

## 가장 최신의 checkpoint를 불러온다.
checkpoint_filename = tf.train.latest_checkpoint(config.save_path)
## graph를 불러온다. (우리가 만든 모델 구조)
saver = tf.train.import_meta_graph(checkpoint_filename + '.meta')
## 변수를 불러온다.
saver.restore(sess, checkpoint_filename)

## 기존 name을 참고해서 현재 불러온 graph내의 값들을 불러와서 변수로 지정한다.
pred = graph.get_tensor_by_name('prediction:0')
X = graph.get_tensor_by_name('X:0')
Y = graph.get_tensor_by_name('Y:0')

## 데이터를 불러온다.
_, X_train, X_test, Y_train, Y_test = load_data(config.data_dir)
sample_data, sample_label = X_test[: 20], Y_test[: 20]

## 모델을 제대로 불러와서 실행하는지 확인해보자.
prediction = sess.run(pred, feed_dict={X: sample_data, Y: sample_label})
true_label = np.argmax(sample_label, axis=1)
accuracy = np.sum(np.equal(prediction, true_label))/len(prediction)

print('Accuracy: {:.0%}'.format(accuracy))