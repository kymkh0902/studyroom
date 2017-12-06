import tensorflow as tf

class Model(object):
    def __init__(self, config):
        self.num_unit1 = config.num_unit1
        self.num_unit2 = config.num_unit2
        self.num_unit3 = config.num_unit3
        self.num_unit4 = config.num_unit4
        self.num_classes = config.num_classes
        self.learning_rate = config.learning_rate
        self.num_epochs = config.num_epochs
        self.batch_size = config.batch_size
        self.keep_prob = config.keep_prob
        self.keep_prob_placeholder = tf.placeholder(tf.float32)
        self.build()

    ## 입력 데이터 저장
    def add_placeholders(self):
        self.X = tf.placeholder(tf.float32, [None, 784])
        self.Y = tf.placeholder(tf.float32, [None, 10])

    ## 모델을 설계하여 logits 구하기
    def build_neural_net(self):
        fc1 = tf.layers.dense(self.X, units=self.num_unit1, activation=tf.nn.relu,
                              bias_initializer=tf.zeros_initializer(),
                              kernel_initializer=tf.contrib.layers.xavier_initializer())
        fc1 = tf.nn.dropout(fc1, keep_prob=self.keep_prob_placeholder)
        fc2 = tf.layers.dense(fc1, units=self.num_unit2, activation=tf.nn.relu,
                              bias_initializer=tf.zeros_initializer(),
                              kernel_initializer=tf.contrib.layers.xavier_initializer())
        fc2 = tf.nn.dropout(fc1, keep_prob=self.keep_prob_placeholder)
        fc3 = tf.layers.dense(fc2, units=self.num_unit3, activation=tf.nn.relu,
                              bias_initializer=tf.zeros_initializer(),
                              kernel_initializer=tf.contrib.layers.xavier_initializer())
        fc3 = tf.nn.dropout(fc1, keep_prob=self.keep_prob_placeholder)
        fc4 = tf.layers.dense(fc3, units=self.num_unit4, activation=tf.nn.relu,
                              bias_initializer=tf.zeros_initializer(),
                              kernel_initializer=tf.contrib.layers.xavier_initializer())
        fc4 = tf.nn.dropout(fc1, keep_prob=self.keep_prob_placeholder)
        self.logits = tf.layers.dense(fc4, units=self.num_classes)
        self.pred = tf.identity(self.logits, 'prediction')

    ## Loss 구하기
    def build_loss(self):
        self.loss = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=self.Y, logits=self.logits))

        ## train_op 만들기
    def build_train_op(self):
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        self.train_op = optimizer.minimize(self.loss)

    ## prediction 구하기
    def build_accuracy(self):
        correction = tf.equal(tf.argmax(self.Y, axis=1), tf.argmax(self.pred, axis=1))
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
        input_feed[self.keep_prob_placeholder] = self.keep_prob

        output_feed = [self.train_op, self.loss]
        _, loss = sess.run(output_feed, feed_dict=input_feed)
        return loss

    ## 모델을 eval 하기
    def eval(self, sess, X, Y):
        input_feed = {}
        input_feed[self.X] = X
        input_feed[self.Y] = Y
        input_feed[self.keep_prob_placeholder] = 1

        output_feed = [self.loss, self.accuracy]
        loss, accuracy = sess.run(output_feed, feed_dict=input_feed)
        return loss, accuracy
