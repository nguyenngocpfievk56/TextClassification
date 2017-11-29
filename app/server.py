# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from test_model import classify
from main import train
from preprocess import loadDictionary, makeDictionary, getDictAPI, makeDataFile
from const import *
import time

app = Flask(__name__)
dict = loadDictionary(DICT_PATH)


@app.route('/classification/<string:callback>/<string:content>', methods=['GET'])
def classification(callback,content):
    callback = str(callback)
    content = str(content.encode('utf-8'))
    cls = classify(content, dict)
    response = "%s(%s)" % (callback, str(cls))
    return response


@app.route('/dict/make/<string:callback>')
def makedict(callback):
    makeDictionary()
    response = "%s('%s')" % (callback, "MAKE DICTIONARY DONE")
    return response


@app.route('/dict/get/<string:callback>')
def getdict(callback):
    dictionary = getDictAPI(DICT_PATH)
    dictionary = dictionary.decode('utf8')
    response = "%s('%s')" % (callback, dictionary)
    return response


@app.route('/dict/save/<string:callback>/<string:content>')
def savedict(callback, content):
    fdict = open(DICT_PATH, 'w')
    content = str(content.encode('utf-8'))
    fdict.write(content)
    fdict.close()
    response = "%s('%s')" % (callback, "SAVED")
    return response


@app.route('/data/make/<string:callback>')
def makedatafile(callback):
    makeDataFile()
    response = "%s('%s')" % (callback, "MAKE DATA FILE DONE")
    return response


@app.route('/data/add/<string:callback>/<string:content>/<string:type>')
def addData(callback, content, type):
    content = str(content.encode('utf-8'))
    now = str(int(round(time.time() * 1000)))
    fnew = open("./data/" + type + "/" + now + ".txt", 'w')
    fnew.write(content)
    fnew.close()
    response = "%s('%s')" % (callback, "ADD DATA DONE")
    return response


@app.route('/training/<string:callback>')
def trainingModel(callback):
    max_epoch = 300
    train(max_epoch)
    response = "%s('%s')" % (callback, "TRAINING DONE")
    return response


if __name__ == '__main__':
    app.run(debug=True, port=1234)
