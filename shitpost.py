#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:15:24 2016

@author: namu

This old project has been repurposed as a twitter bot.
"""

from os import listdir
from os.path import isfile, join
from random import random
from getopt import getopt,GetoptError
import sys

_DIRECTOR_FOLDER_NAME = "Words"
_dictionaries = []
_dictionaryNames = []

class Core:
    def __init__(self):
        self._createDictionaries()
    def _createDictionaries(self):
        global _DIRECTOR_FOLDER_NAME
        clear()
        files = self._getFiles(_DIRECTOR_FOLDER_NAME)
        for f in files:
            Dictionary(self._scanFile(f),f.replace(".txt",""))
    def _getFiles(self,folder):
        try:
            files = [f for f in listdir(folder) if isfile(join(folder,f))]
            return files
        except:
            print "Path does not exist maybe"
            sys.exit(0)
    def _scanFile(self,f):
        global _DIRECTOR_FOLDER_NAME
        fi = open(join(_DIRECTOR_FOLDER_NAME,f),"r")
        text = fi.read()
        words = text.replace("\r","").split("\n")
        if words[-1]=="":
            del words[-1]
        fi.close()
        return words
    def generate(self):
        subject = None
        limit = size()
        sentence = pickFrom("base")
        loop = True
        while loop:
            loop = False
            for x in range(limit):
                subject = getNameOfDictionary(x)
                while "%"+subject+"%" in sentence:
                    loop = True
                    sentence = sentence.replace("%"+subject+"%",pickFrom(x),1)
        sentence_words = sentence.split("||")
        for i in range(len(sentence_words)):
            if sentence_words[i][0] == "#":
                sentence_words[i] = sentence_words[i].replace(" ","").replace("-","")
        sentence = "||".join(sentence_words)
        return sentence.replace("%nul%","").replace("||"," ").replace("|","")

    def _debug_generate(self, log_file_name):
        log_file = open(log_file_name, "a")
        log_file.write("Starting creating a sentence.\n")
        
        subject = None
        limit = size()
        sentence = pickFrom("base")
        
        
        loop = True
        while loop:
            
            loop = False
            
            for x in range(limit):
                subject = getNameOfDictionary(x)
                while "%"+subject+"%" in sentence:
                    loop = True
                    log_file.write("Progression: " + sentence + "\n")
                    sentence = sentence.replace("%"+subject+"%",pickFrom(x),1)

        log_file.write("Ending sentence: " + sentence + "\n")
        
        sentence_words = sentence.split("||")

        for i in range(len(sentence_words)):
            if sentence_words[i][0] == "#":
                sentence_words[i] = sentence_words[i].replace(" ","").replace("-","")
        sentence = "||".join(sentence_words)

        log_file.write("Progression: " + sentence + "\n")
        log_file.write("Returning generated sentence: " + sentence.replace("%nul%","").replace("||"," ").replace("|","") + "\n\n")
        log_file.close()
        return sentence.replace("%nul%","").replace("||"," ").replace("|","")

class Dictionary:
    _words = None
    def __init__(self,strings,name):
        global _dictionaries
        global _dictionaryNames
        self._words=[]
        self._addAll(strings)
        _dictionaries.append(self)
        _dictionaryNames.append(name)
    def _addAll(self,strings):
        for x in strings:
            self._words.append(x)
    def _length(self):
        return len(self._words)
    def _get(self,index):
        return self._words[index]
        
def clear():
    _dictionaryNames=[]
    _dictionaries=[]
def size():
    return len(_dictionaryNames)
def pickFrom(x):
    if type(x)==str:
        x=_dictionaryNames.index(x)
    subject=_dictionaries[x]
    limit=subject._length()
    returning=subject._get(int(random()*limit))
    return returning
def getNameOfDictionary(x):
    return _dictionaryNames[x]



def getShitpost(num=1,director_folder="Words"):
    _DIRECTOR_FOLDER_NAME = director_folder
    obj = Core()
    returning=[]
    if num==1:
        return obj.generate()
    for x in range(num):
        returning.append(str(x+1)+") "+obj.generate())
    return "\n".join(returning)


def _debug_getShitpost(num=1,director_folder="Words"):
    _DIRECTOR_FOLDER_NAME = director_folder
    obj = Core()
    returning=[]
    if num==1:
        return obj._debug_generate("generation.log")
    for x in range(num):
        returning.append(str(x+1)+") "+obj._debug_generate("generation.log"))
    return "\n".join(returning)




def usage():
    print "make a shitpost all by yourself"
    print
    print "usage: shitpost [option]..."
    print "-h, --help        := display help"
    print "-c, --count x     := display x number of posts"
    print "-d, --directory x := use x for directory of words"
    print
    print "example:"
    print "shitpost -h"
    print "shitpost -c 20 -d words"
    sys.exit(0)


#defaults
count_arg = 1
director_folder_arg = "Words"

def main():    
    global count_arg
    global _DIRECTOR_FOLDER_NAME
    try:
        opts,args=getopt(sys.argv[1:],"hc:d:",
        ["help","count","directory"])
    except GetoptError as err:
        print str(err)
        usage()
    for o,a in opts:
        if o in ["-h","--help"]:
            usage()
        elif o in ["-c","--count"]:
            count_arg = int(a)
        elif o in ["-d","--directory"]:
            _DIRECTOR_FOLDER_NAME = a
        else:
            assert False,"Unhandled Option"
    getShitpost(count_arg,_DIRECTOR_FOLDER_NAME)

main()
