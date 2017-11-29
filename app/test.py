# -*- coding: utf-8 -*-
from test_model import classify
from preprocess import loadDictionary
from const import *
import sys


dict = loadDictionary(DICT_PATH)

content = sys.argv[1]
cls = classify(content, dict)
print cls