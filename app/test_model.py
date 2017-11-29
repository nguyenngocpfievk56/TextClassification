# coding: utf8
from __future__ import print_function
from chainer import serializers
from main import Network
from preprocess import convertTextToVector, loadDictionary
import numpy as np


def classify(content, dict):
    model = Network()
    serializers.load_npz('classification.model', model)
    x = convertTextToVector(content, dict)
    x = np.array([np.float32(float(i)) for i in x])
    print(len(x))
    x = x[None, ...]
    y = model(x)
    y = y.data
    pred_label = y.argmax(axis=1)
    print('predicted label:', pred_label[0])
    return pred_label[0]


if __name__ == '__main__':
    content = "日本に在留する外国人の数は、ことし６月末の時点で２４７万人余りと過去最高を更新する一方"
    dict = loadDictionary('./dict.txt')
    classify(content, dict)

