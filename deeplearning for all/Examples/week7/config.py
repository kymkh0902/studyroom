## 변수 모음
class Config():
    def __init__(self):
        self.sentence = ("If you want to build a ship, don't drum up people together to "
                         "collect wood and don't assign them tasks and work, but rather "
                         "teach them to long for the endless immensity of the sea.")
        self.char_set = list(set(self.sentence))
        self.char_dic = {w: i for i, w in enumerate(self.char_set)}
        self.sample_idx = [self.char_dic[w] for w in self.sentence]
        self.data_dim = len(self.char_set)
        self.hidden_size = len(self.char_set)
        self.num_classes = self.hidden_size
        self.seq_length = 10
        self.learning_rate = 0.1

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
        self.num_epochs = 500
        self.dropout_rate = 0.3
        self.use_dropout = False
        self.data_dir = '../MNIST_data'
        self.num_checkpoints = 3
        self.checkpoint_every = 1
        self.save_path = '../MNIST_data/week7/'
        self.save_filename = 'mnist_model'