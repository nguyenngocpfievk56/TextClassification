# -*- coding: utf-8 -*-

from tokenizer import tokenize
import glob
import os
import operator
from const import *


THRESHOLD = 0.05
VALID_TAGS = ['形容詞', '名詞', '動詞']
LABEL = "social"


def makeDictionary():
    dict = {}
    os.chdir("./data")
    for path in glob.glob("*"):
        os.chdir("./" + path)
        for f in glob.glob("*.txt"):
            fr = open(f)
            content = fr.read()
            words = tokenize(content, VALID_TAGS)
            for word in words:
                if word in dict:
                    dict[word] += 1
                else:
                    dict[word] = 1

            fr.close()
        os.chdir("../")

    os.chdir("../")
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
    min_thr = len(sorted_dict) * THRESHOLD
    max_thr = len(sorted_dict) * (1-THRESHOLD)
    official_dict = sorted_dict[int(min_thr):int(max_thr)]

    fw = open(DICT_PATH, 'w')
    for term in official_dict:
        fw.write(term[0] + '、')
    fw.close()


def getDictAPI(path):
    fread = open(path)
    content = fread.read()
    fread.close()
    return content


def loadDictionary(path):
    fread = open(path)
    content = fread.read()
    tmp = content.split("、")
    dict = []
    for w in tmp:
        if w != '':
            dict.append(w)

    fread.close()
    return dict


def convertTextToVector(text, dict):
    vector = []
    words = tokenize(text, VALID_TAGS)
    for w in dict:
        if w in words:
            vector.append(float(1))
        else:
            vector.append(float(0))

    return vector


def makeDataFile():
    fdata = open(DATA_PATH, 'w')
    dict = loadDictionary(DICT_PATH)

    os.chdir("./data")
    for path in glob.glob("*"):
        os.chdir("./" + path)
        for f in glob.glob("*.txt"):
            print f
            fread = open(f)
            text = fread.read()
            fread.close()
            vector = convertTextToVector(text, dict)

            for i in vector:
                fdata.write(str(i) + ',')

            if path == LABEL:
                fdata.write(str(1))
            else:
                fdata.write(str(0))

            fdata.write("\n")

        os.chdir("../")

    os.chdir("../")

    fdata.close()
    print "-----DONE-----"
