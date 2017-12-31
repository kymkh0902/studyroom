import tensorflow as tf

class Model(object):
    def __init__(self, config):
        self.seq_length = config.seq_length
        self.learning_rate = config.learning_rate
        self.batch_size = config.batch_size
        self.num_epochs = config.num_epochs
        self.hidden_size = config.hidden_size
        self.num_classes = config.num_classes
        self.data_dim = config.data_dim
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
        cell = tf.contrib.rnn.BasicLSTMCell(self.hidden_size, state_is_tuple=True)
        multi_cells = tf.contrib.rnn.MultiRNNCell([cell for _ in range(2)],
                                                  state_is_tuple=True)

        ##initial_state = multi_cells.zero_state(self.batch_size, tf.float32)
        outputs, _states = tf.nn.dynamic_rnn(
            multi_cells, self.X_one_hot, dtype = tf.float32)

        X_for_fc = tf.reshape(outputs, [-1, self.hidden_size])
        outputs = tf.contrib.layers.fully_connected(X_for_fc, self.num_classes,
                                                    activation_fn=None)
        self.outputs = tf.reshape(outputs, [self.batch_size, self.seq_length, self.num_classes])
        self.weights = tf.ones([self.batch_size, self.seq_length])

        ##X_for_softmax = tf.reshape(outputs, [-1, self.hidden_size])
        ##softmax_w = tf.get_variable("softmax_w", [self.hidden_size, self.num_classes])
        ##softmax_b = tf.get_variable("softmax_b", [self.num_classes])

        ##self.outputs = tf.matmul(X_for_softmax, softmax_w) + softmax_b


    ## Loss 구하기
    def build_loss(self):
        seq_loss = tf.contrib.seq2seq.sequence_loss(logits=self.outputs, targets=self.Y,
                                                weights=self.weights)
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
        input_feed[self.X_one_hot] = X
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
