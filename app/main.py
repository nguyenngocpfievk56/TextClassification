import numpy as np
from chainer.datasets import tuple_dataset
import chainer
import chainer.functions as F
import chainer.links as L
from chainer.dataset import concat_examples
from chainer import iterators
from chainer import optimizers
from const import *


def loadData(path):
    fdata = open(path)
    train_data = []
    train_label = []
    for line in fdata:
        tmp = line.split(",")
        train = np.array([np.float32(float(x)) for x in tmp[0:len(tmp) - 1]])
        label = np.int32(line.split(",")[len(tmp) - 1])
        train_data.append(train)
        train_label.append(label)

    fdata.close()
    # threshold = np.int32(len(train_data) / 10 * 9)
    # train = tuple_dataset.TupleDataset(train_data[0:threshold], train_label[0:threshold])
    # test = tuple_dataset.TupleDataset(train_data[threshold:], train_label[threshold:])
    data = tuple_dataset.TupleDataset(train_data, train_label)
    return data


class Network(chainer.Chain):
    def __init__(self, n_out=2):
        super(Network, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(None, n_out)

    def __call__(self, x):
        return F.sigmoid(self.l1(x))


def train(max_epoch):
    train = loadData(DATA_PATH)
    batchsize = 128
    train_iter = iterators.SerialIterator(train, batchsize)
    model = Network()
    optimizer = optimizers.MomentumSGD(lr=0.01, momentum=0.9)
    optimizer.setup(model)

    while train_iter.epoch < max_epoch:
        train_batch = train_iter.next()
        doc_train, target_train = concat_examples(train_batch)
        prediction_train = model(doc_train)
        loss = F.softmax_cross_entropy(prediction_train, target_train)
        print("Loss: ", loss)
        model.cleargrads()
        loss.backward()
        optimizer.update()

    chainer.serializers.save_npz('classification.model', model)
