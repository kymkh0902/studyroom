import tensorflow as tf

class Model(object):
    def __init__(self, config):
        self.num_unit1 = config.num_unit1
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
        self.X = tf.reshape(self.X, [-1, 28, 28, 1])
        self.Y = tf.placeholder(tf.float32, [None, 10])

    ## 모델을 설계하여 logits 구하기
    def build_neural_net(self):
        filter1 = tf.Variable(tf.random_normal([3, 3, 1, 32], stddev=0.01))
        L1 = tf.nn.conv2d(self.X, filter=filter1, strides=[1, 1, 1, 1],
                          padding='SAME')
        L1 = tf.nn.relu(L1)
        L1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                            padding='SAME')
        L1 = tf.nn.dropout(L1, keep_prob=self.keep_prob_placeholder)

        filter2 = tf.Variable(tf.random_normal([3, 3, 32, 64], stddev=0.01))
        L2 = tf.nn.conv2d(L1, filter=filter2, strides=[1, 1, 1, 1],
                          padding='SAME')
        L2 = tf.nn.relu(L2)
        L2 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                            padding='SAME')
        L2 = tf.nn.dropout(L2, keep_prob=self.keep_prob_placeholder)

        filter3 = tf.Variable(tf.random_normal([3, 3, 64, 128], stddev=0.01))
        L3 = tf.nn.conv2d(L2, filter=filter3, strides=[1, 1, 1, 1],
                          padding='SAME')
        L3 = tf.nn.relu(L3)
        L3 = tf.nn.max_pool(L3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                            padding='SAME')
        L3 = tf.nn.dropout(L3, keep_prob=self.keep_prob_placeholder)
        L3 = tf.reshape(L3, [-1, 128 * 4 * 4])

        fc1 = tf.layers.dense(L3, units=self.num_unit1, activation=tf.nn.relu,
                              bias_initializer=tf.zeros_initializer(),
                              kernel_initializer=tf.contrib.layers.xavier_initializer())
        fc1 = tf.nn.dropout(fc1, keep_prob=self.keep_prob_placeholder)

        self.logits = tf.layers.dense(fc1, units=self.num_classes,
                              bias_initializer=tf.zeros_initializer(),
                              kernel_initializer=tf.contrib.layers.xavier_initializer())
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
