 #-*- coding: utf-8 -*-
from collections import Counter
import underthesea
commonWordFile = open('../Thesis_Dataset/3000_most_word.txt',mode = 'r')
commonSyllableFile = open('../Thesis_Dataset/3000_most_syllable.txt', mode = 'r')
sinoVietWordFile = open('../Thesis_Dataset/sino_vietnamese.txt',mode='r')
dialectWordFile = open('../Thesis_Dataset/dialect.txt',mode='r')



rawCommonWordList = commonWordFile.read()
rawCommonSyllableList = commonSyllableFile.read()
rawSinoVietWordSet = sinoVietWordFile.read()
rawDialectWordSet = dialectWordFile.read()
rawInputData = input()

commonWordSet = set(rawCommonWordList.split('\n'))
commonSyllableSet = set(rawCommonSyllableList.split('\n'))
sinoVietWordSet = set(rawSinoVietWordSet.split('\n'))
dialectWordSet = set(rawDialectWordSet.split('\n'))
sentenceMarkList = set([',','.','!','?',':',';','-'])

#preprocesing
rawInputData = rawInputData.lower()

sentenceList = underthesea.sent_tokenize(rawInputData)
wordList = list(filter(lambda x: not  x in sentenceMarkList ,underthesea.word_tokenize(rawInputData)))
print(wordList)
syllableList = []
for word in wordList:
    syllableList += word.split()

charList = []
for syllable in syllableList:
    charList += list(syllable)

wordCounter = Counter(wordList)
posWordList = underthesea.pos_tag(rawInputData)
#count index

# average sentence length in word
def calculateASLW(sentenceList,wordList):
    return len(wordList)/len(sentenceList) 
aslwIndex = calculateASLW(sentenceList,wordList)
print('aslw', aslwIndex)

# average sentence length in syllable 
def calculateASLS(sentenceList,syllableList):
    return len(syllableList)/len(sentenceList) 

aslsIndex = calculateASLS(sentenceList,syllableList)
print('asls', aslsIndex)


# average senetence length in character

def calculateASLC(sentenceList,charList): 
    return len(charList)/len(sentenceList) 

aslcIndex = calculateASLC(sentenceList,charList)
print('aslc', aslcIndex)

# average word length in character

def calculateAWLC(wordList,charList):
    return len(charList)/len(wordList) 

awlcIndex = calculateAWLC(wordList,charList)
print('awlc', awlcIndex)


# averagew word length in syllable

def calculateAWLS(wordList,syllableList):
    return len(syllableList)/len(wordList) 

awlsIndex = calculateAWLS(wordList,syllableList)
print('awls', awlsIndex)

# percertange of difficult syllables

def calculatePDS(syllableList,commonSyllableSet):
    totalSyllable = len(syllableList)
    totalDifficultSyllable = len(list(filter(lambda syllable: not syllable in commonSyllableSet,syllableList)))
    return totalDifficultSyllable/totalSyllable

pdsIndex = calculatePDS(syllableList,commonSyllableSet)
print('pds',pdsIndex)

# percertange of difficult word

def calculatePDW(wordList,commonWordSet):
    totalWord = len(wordList)
    totalDifficultWord = len(list(filter(lambda word: not word in commonWordSet,wordList)))
    return totalDifficultWord/totalWord

pdwIndex = calculatePDW(wordList,commonWordSet)
print('pdw',pdwIndex)

#percertange of Sino-vietnamese word

def calculatePSVW(wordList,sinoVietWordSet):
    totalWord = len(wordList)
    totalSinoVietWord = len(list(filter(lambda word: word in sinoVietWordSet,wordList)))
    return totalSinoVietWord/totalWord

psvwIndex = calculatePSVW(wordList,sinoVietWordSet)
print('psvw',psvwIndex)

#percertange of dialect words (pdiaw)
def calculatePDiaW(wordList,dialectWordSet):
    totalWord = len(wordList)
    totalDialectWord = len(list(filter(lambda word: word in dialectWordSet,wordList)))
    return totalDialectWord/totalWord

pdiawIndex = calculatePDiaW(wordList,dialectWordSet)
print('pdiaw',pdiawIndex)


#calculate score

def calculateLAVFomula(aslcIndex, awlcIndex, pdwIndex ):
    return 0.004*aslcIndex + 0.1905*awlcIndex + 2.7147*pdwIndex - 0.7295
 
def calculateNH1982(aslcIndex,awlcIndex):
    return 2*awlcIndex + 0.2*aslcIndex - 6

def calculateNH1985(aslcIndex, pswIndex):
    #Vocabulary difficulty (WD)
    wdIndex =  pswIndex*100
    return 0.27*wdIndex + 0.13*aslcIndex +1.74

#classification

RL_LavFomula = calculateLAVFomula(aslcIndex,awlcIndex,pdwIndex)
print("LAV",RL_LavFomula)


commonWordFile.close()
commonSyllableFile.close()
sinoVietWordFile.close()
dialectWordFile.close()