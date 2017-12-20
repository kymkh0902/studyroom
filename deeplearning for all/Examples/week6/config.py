## 변수 모음
class Config():
    def __init__(self):
        self.learning_rate = 0.001
        self.num_epochs = 5
        self.batch_size = 100
        self.dropout_rate = 0.3
        self.use_dropout = True
        self.data_dir = '../MNIST_data'
        self.num_checkpoints = 3
        self.checkpoint_every = 1
        self.save_path = '../MNIST_data/week6/'
        self.save_filename = 'mnist_model'