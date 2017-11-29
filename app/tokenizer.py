# -*- coding: utf-8 -*-
import MeCab


def tokenize(text, validTags):
    words = []
    mecab = MeCab.Tagger("")
    tmps = mecab.parse(text).split('\n')
    for tmp in tmps:
        if tmp == 'EOS':
            break
        else:
            infos = tmp.split('\t')
            wordInfoString = infos[1]
            wordInfos = wordInfoString.split(',')
            if validTags is None:
                words.append(wordInfos[6])
            else:
                if wordInfos[0] in validTags:
                    words.append(wordInfos[6])
    return words


if __name__ == '__main__':
    text = "品川駅がきれいです"
    test = tokenize(text, None)
    print test
