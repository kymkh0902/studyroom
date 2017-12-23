## 전체적으로 코드가 문제가 많아서 다 고쳐주는 거 보다는 문제가 어디어디 있는지 알려줄테니 다시 짜보셈

## 1. X, Y에 들어가는 데이터는 int 유형임. float 말고 int로 사용해야 함 (아무 것도 안 고치고 돌렸을 때 나오는 에러.)
## 2. X_one_hot은 5개 class인 데이터 중에 0번 째면 [1, 0, 0, 0, 0] 으로 데이터를 변환해주는 코드임 (one-hot encoding)
##    우리는 [batch_size, time_steps, features]로 데이터를 나타낼 건데 one_hot이 features를 만들어주게 됨.
## 3. dataX, dataY 코드가 model에 있는데, 이 코드는 사용할 데이터를 만드는 코드이므로 data_util로 보낸 뒤에 train에서 읽는게 맞음.
## 4. correction 구할 때 Y가 만약 [batch_size, seq_length]로 데이터가 들어오면 argmax를 씌울 필요가 없음. argmax는
##    output 데이터가 [batch_size, time_steps, features]의 형식일 때 [batch_size, time_steps, 1]로 바꿔주기 위함임.
## 5. train 함수가 없음. (기존 코드 참조.)
## 6. eval에 X_one_hot을 feed_dict의 input으로 받는데 모델 내부적으로 X_one_hot은 처리하는 것이므로 X를 받아야 함.
## 7. config에 데이터 관련 값들은 data_util로 가져간 뒤 train할 때 읽는게 나아보임.
## 8. config에 중복된 변수나 이전 과제 변수들은 지울 필요가 있음.


##2차 피드백
##중요. pycharm에 회색 변수 or 빨간 밑줄은 문법적인 오류나 사용하지 않은 변수이므로 바로바로 고치는게 좋음.!

##위에 코드 조금만 다듬으면 돌아갈듯요

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
        self.dataX = config.dataX
        self.dataY = config.dataY
        self.batch_size = config.batch_size
        self.num_epochs = config.num_epochs
        self.use_dropout = config.use_dropout
        self.dropout_rate = 0.0
        # use_dropout 사용 여부에 대한 로직 추가
        if self.use_dropout:
            self.dropout_rate = config.dropout_rate
        self.build()


    ## 입력 데이터 저장
    def add_placeholders(self):
        self.X = tf.placeholder(tf.int32, [None, self.seq_length])
        self.Y = tf.placeholder(tf.int32, [None, self.seq_length])
        self.X_one_hot = tf.one_hot(self.X, self.num_classes)
        self.dropout_placeholder = tf.placeholder(tf.float32, [])

    ## 모델을 설계하여 logits 구하기
    def build_neural_net(self):

        cell = tf.contrib.rnn.BasicLSTMCell(num_units=self.hidden_size, state_is_tuple=True)
        cell = tf.contrib.rnn.MultiRNNCell([cell] * 2, state_is_tuple=True)

        initial_state = cell.zero_state(self.batch_size, tf.float32)
        outputs, _states = tf.nn.dynamic_rnn(
            cell, self.X_one_hot, initial_state = initial_state, dtype = tf.float32)

        outputs = tf.reshape(outputs, [self.batch_size, self.seq_length, self.num_classes])
        X_for_softmax = tf.reshape(outputs, [-1, self.hidden_size])
        softmax_w = tf.get_variable("softmax_w", [self.hidden_size, self.num_classes])
        softmax_b = tf.get_variable("softmax_b", [self.num_classes])

        outputs = tf.matmul(X_for_softmax, softmax_w) + softmax_b
        self.outputs = tf.reshape(outputs, [self.batch_size, self.seq_length, self.num_classes])

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
        correction = tf.equal(tf.argmax(self.Y, axis=1), tf.argmax(self.outputs, axis=1))
        self.accuracy = tf.reduce_mean(tf.cast(correction, tf.float32))

    ## 모델을 build 하기
    def build(self):
        self.add_placeholders()
        self.build_neural_net()
        self.build_loss()
        self.build_train_op()
        self.build_accuracy()

    ## 모델을 train 하기
    def train(self, sess, X, Y):
        input_feed = {}
        input_feed[self.X] = X
        input_feed[self.Y] = Y
        input_feed[self.dropout_placeholder] = self.dropout_rate

        output_feed = [self.train_op, self.loss]
        _, loss = sess.run(output_feed, feed_dict=input_feed)
        return loss

    ## 모델을 eval 하기
    def eval(self, sess, X, Y):
        input_feed = {}
        input_feed[self.X_one_hot] = X
        input_feed[self.Y] = Y
        input_feed[self.dropout_placeholder] = self.dropout_rate

        output_feed = [self.loss, self.accuracy, self.outputs]
        loss, accuracy, results = sess.run(output_feed, feed_dict=input_feed)
        return loss, accuracy, results
