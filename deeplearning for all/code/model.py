import tensorflow as tf

class Model(object):
    def __init__(self, config):
        self.num_units = config.num_units
        self.num_classes = config.num_classes
        self.learning_rate = config.learning_rate
        self.num_epochs = config.num_epochs
        self.batch_size = config.batch_size
        self.build()

    # 입력 데이터를 지정해준다.
    def add_placeholders(self):
        self.X = tf.placeholder(tf.float32, [None, 784], name='X')
        self.y = tf.placeholder(tf.float32, [None, 10], name='y')

    # 모델을 설계해서 logits를 구하자.
    def build_neural_net(self):
        fc1 = tf.layers.dense(self.X, units=self.num_units, activation=tf.nn.relu)
        self.logits = tf.layers.dense(fc1, units=self.num_classes)
        self.pred = tf.argmax(self.logits, axis=1, name='prediction')

    # loss를 구하자.
    def build_loss(self):
        self.loss = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=self.y, logits=self.logits))

    # train_op를 만들자.
    def build_train_op(self):
        optimizer = tf.train.GradientDescentOptimizer(self.learning_rate)
        self.train_op = optimizer.minimize(self.loss)

    # prediction 값을 구하자.
    def build_accuracy(self):
        correction = tf.equal(tf.argmax(self.y, axis=1), self.pred)
        self.accuracy = tf.reduce_mean(tf.cast(correction, tf.float32))

    # 모델을 build 한다.
    def build(self):
        self.add_placeholders()
        self.build_neural_net()
        self.build_loss()
        self.build_train_op()
        self.build_accuracy()

    # 모델을 train 한다.
    def train(self, sess, X, y):
        input_feed = {}
        input_feed[self.X] = X
        input_feed[self.y] = y

        output_feed = [self.train_op, self.loss]
        _, loss = sess.run(output_feed, feed_dict=input_feed)
        return loss


    # 모델을 eval 한다.
    def eval(self, sess, X, y):
        input_feed = {}
        input_feed[self.X] = X
        input_feed[self.y] = y

        output_feed = [self.loss, self.accuracy]
        loss, accuracy = sess.run(output_feed, feed_dict=input_feed)
        return loss, accuracy


