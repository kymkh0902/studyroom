import tensorflow as tf

class Model(object):
    def __init__(self, config):
        self.learning_rate = config.learning_rate
        self.num_epochs = config.num_epochs
        self.batch_size = config.batch_size
        self.use_dropout = config.use_dropout
        self.dropout_rate = 0.0
        # use_dropout 사용 여부에 대한 로직 추가
        if self.use_dropout:
            self.dropout_rate = config.dropout_rate
        self.build()

### tf.layers.dropout은 keep_prob을 변수로 받는게 아니라 dropout rate을 변수로 받음.
### 그러므로 0.7이 아니라 0.3을 입력해줘야 하고 실제 돌렸을 때 안 되었던 것은 1.0이 eval에 들어가서 node가 없는 상태로 평가를 해서
### accuracy가 낮게 나온 것임. keep_prob -> dropout_rate로 바꿔주고 나머지 코드는 그대로


    ## 입력 데이터 저장
    def add_placeholders(self):
        self.X = tf.placeholder(tf.float32, [None, 784])
        self.X = tf.reshape(self.X, [-1, 28, 28, 1])
        self.Y = tf.placeholder(tf.float32, [None, 10])
        self.dropout_placeholder = tf.placeholder(tf.float32, [])

    ## 모델을 설계하여 logits 구하기
    def build_neural_net(self):
        conv1 = tf.layers.conv2d(inputs=self.X, filters=32, kernel_size=[3, 3],
                                 padding='SAME', activation=tf.nn.relu)
        pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2],
                                        padding='SAME', strides=2)
        dropout1 = tf.layers.dropout(inputs=pool1, rate=self.dropout_rate,
                                     training=True)

        conv2 = tf.layers.conv2d(inputs=dropout1, filters=64, kernel_size=[3, 3],
                                 padding='SAME', activation=tf.nn.relu)
        pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2],
                                        padding='SAME', strides=2)
        dropout2 = tf.layers.dropout(inputs=pool2, rate=self.dropout_rate,
                                     training=True)

        conv3 = tf.layers.conv2d(inputs=dropout2, filters=128, kernel_size=[3, 3],
                                 padding='SAME', activation=tf.nn.relu)
        pool3 = tf.layers.max_pooling2d(inputs=conv3, pool_size=[2, 2],
                                        padding='SAME', strides=2)
        dropout3 = tf.layers.dropout(inputs=pool3, rate=self.dropout_rate,
                                     training=True)
        flat = tf.reshape(dropout3, [-1, 128 * 4 * 4])

        fc1 = tf.layers.dense(inputs=flat, units=625, activation=tf.nn.relu,
                              bias_initializer=tf.zeros_initializer(),
                              kernel_initializer=tf.contrib.layers.xavier_initializer())
        fc1_dropout = tf.layers.dropout(inputs=fc1, rate=self.dropout_rate)

        self.logits = tf.layers.dense(inputs=fc1_dropout, units=10,
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
        input_feed[self.dropout_placeholder] = self.dropout_rate

        output_feed = [self.train_op, self.loss]
        _, loss = sess.run(output_feed, feed_dict=input_feed)
        return loss

    ## 모델을 eval 하기
    def eval(self, sess, X, Y):
        input_feed = {}
        input_feed[self.X] = X
        input_feed[self.Y] = Y
        input_feed[self.dropout_placeholder] = 0.0

        output_feed = [self.loss, self.accuracy]
        loss, accuracy = sess.run(output_feed, feed_dict=input_feed)
        return loss, accuracy
