### 어느정도 해결책을 찾고 있는거 같아서 수정 좀 많이 해서 올리긴 했는데,
### 지금 문제가 입력 데이터하고 출력데이터를 정확히 지정하지 않는 것인 거 같음
### 또한, 원핫하는 코딩이 있는데, 이게 정확히 어느 부분에 쓰이는지 모르겠음
### Train.py에 X_data, Y_data에 대해서 추가적으로 넣어봤음
### 또한, Train.py에서는 출력을 어떻게 해야하는지 감이 안 잡힘
### 출력을 저렇게 하라고 되어 있는데, 도저히 매칭이 안됨요
### 지금 문제점을 정확히 파악을 못하여, 정확히 못쓰는 점 양해 바람 ㄳㄳ


import tensorflow as tf

class Model(object):
    def __init__(self, config):
        self.sentence = config.sentence
        self.char_set = config.char_set
        self.char_dic = config.char_dic
        self.sample_idx = config.sample_idx
        self.data_dim = config.data_dim
        self.hidden_size = config.hidden_size
        self.num_classes = config.num_classes
        self.seq_length = config.seq_length
        self.learning_rate = config.learning_rate
        self.num_epochs = config.num_epochs
        self.use_dropout = config.use_dropout
        self.dropout_rate = 0.0
        # use_dropout 사용 여부에 대한 로직 추가
        if self.use_dropout:
            self.dropout_rate = config.dropout_rate
        self.build()


    ## 입력 데이터 저장
    def add_placeholders(self):
        self.X = tf.placeholder(tf.float32, [None, self.seq_length])
        self.Y = tf.placeholder(tf.float32, [None, self.seq_length])
        self.X_one_hot = tf.one_hot(self.X, self.num_classes)
        self.dropout_placeholder = tf.placeholder(tf.float32, [])

    ## 모델을 설계하여 logits 구하기
    def build_neural_net(self):
        self.dataX = []
        self.dataY = []

        for i in range(0, len(self.sentence) - self.seq_length):
            x_str = self.sentence[i:i + self.seq_length]
            y_str = self.sentence[i + 1: i + self.seq_length + 1]

            x = [self.char_dic[c] for c in x_str]
            y = [self.char_dic[c] for c in y_str]

            self.dataX.append(x)
            self.dataY.append(y)

        self.batch_size = len(self.dataX)

        cell = tf.contrib.rnn.BasicLSTMCell(self.hidden_size, state_is_tuple=True)
        cell = tf.contrib.rnn.MultiRNNCell([cell] * 2, state_is_tuple=True)
        initial_state = cell.zero_state(self.batch_size, tf.float32)
        outputs, _states = tf.nn.dynamic_rnn(
            cell, self.X_one_hot, initial_state = initial_state, dtype = tf.float32)

        X_for_softmax = tf.reshape(outputs, [-1, self.hidden_size])
        softmax_w = tf.get_variable("softmax_w", [self.hidden_size, self.num_classes])
        softmax_b = tf.get_variable("softmax_b", [self.num_classes])
        outputs = tf.matmul(X_for_softmax, softmax_w) + softmax_b
        self.outputs = tf.reshape(outputs,
                                  [self.batch_size, self.seq_length, self.num_classes])

        self.weights = tf.ones([self.batch_size, self.seq_length])


    ## Loss 구하기
    def build_loss(self):
        seq_loss = tf.contrib.seq2seq.sequence_loss(logits=self.outputs,
                                                         targets=self.Y, weights=self.weights)
        self.loss = tf.reduce_mean(seq_loss)

    ## train_op 만들기
    def build_train_op(self):
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        self.train_op = optimizer.minimize(self.loss)

    ## prediction 구하기
    def build_accuracy(self):
        correction = tf.equal(tf.argmax(self.Y, axis=2), tf.argmax(self.outputs, axis=2))
        self.accuracy = tf.reduce_mean(tf.cast(correction, tf.float32))

    ## 모델을 build 하기
    def build(self):
        self.add_placeholders()
        self.build_neural_net()
        self.build_loss()
        self.build_train_op()
        self.build_accuracy()

    ## 모델을 train 하기
    def eval(self, sess, X, Y):
        input_feed = {}
        input_feed[self.X_one_hot] = X
        input_feed[self.Y] = Y
        input_feed[self.dropout_placeholder] = self.dropout_rate

        output_feed = [self.loss, self.accuracy, self.outputs]
        loss, accuracy, results = sess.run(output_feed, feed_dict=input_feed)
        return loss, results
