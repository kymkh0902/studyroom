## 변수 모음
class Config():
    def __init__(self):
        self.seq_length = 10
        self.learning_rate = 0.1
        self.batch_size = 170
        self.num_epochs = 500
        self.hidden_size = 27
        self.num_classes = 27
        self.data_dim = 27
        self.dropout_rate = 0.3
        self.use_dropout = True
        self.data_dir = '../../../class/datasets/week7_long_sentence.txt'
        self.num_checkpoints = 3
        self.checkpoint_every = 1
        self.save_path = '../MNIST_data/week7/'
        self.save_filename = 'mnist_model'