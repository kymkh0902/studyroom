from model import Model
import numpy as np
from data_util import load_data, generator
from config import Config
import tensorflow as tf
import os

## 변수로 할당된 값 불러오기 (hyperparameter, data dir, ...)
config = Config()
## 모델을 불러오기
model = Model(config)
## session 불러오기
sess = tf.Session()
sess.run(tf.global_variables_initializer())


## saver 생성
saver = tf.train.Saver(max_to_keep=config.num_checkpoints)
save_path = os.path.join(config.save_path, config.save_filename)
step = 0


## for loop을 통해 train 과정하기
for epoch_i in range(config.num_epochs):

    for batch_j in range(config.batch_size):

        model.train(sess, config.dataX, config.dataY)

        step += 1

        if batch_j is 0:
            print(''.join([config.char_set[t] for t in step]), end='')
        else:
            print(config.char_set, end='')

    if  epoch_i % config.checkpoint_every== 0:
        saver.save(sess, save_path, global_step=step)