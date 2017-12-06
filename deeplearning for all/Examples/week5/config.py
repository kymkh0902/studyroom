## 변수 모음
class Config():
    def __init__(self):
        self.learning_rate = 0.001
        self.num_epochs = 5
        self.batch_size = 100
        self.num_unit1 = 625
        self.num_classes = 10
        self.keep_prob = 0.7
        self.data_dir = '../../MNIST_data'
