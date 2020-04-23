import re
from underthesea import sent_tokenize
commonWordFile = open('../Thesis_Dataset/3000_most_word.txt',mode = 'r', encoding = 'utf-8')
commonSyllableFile = open('../Thesis_Dataset/3000_most_syllable.txt', mode = 'r', encoding = 'utf-8')
sinoVietWordFile = open('../Thesis_Dataset/sino_vietnamese.txt',mode='r',encoding='utf-8')
dialectWordFile = open('../Thesis_Dataset/dialect.txt',mode='r',encoding='utf-8')

#inputFilePath = input()
#inputFile = open(inputFilePath,mode='r',encoding = 'utf-8')

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

sentenceList = sent_tokenize(text)

#count index

# average sentence length in word
def calculateASLW(sentenceList):
    global sentenceMarkList
    result = 0
    amountOfSentence = len(sentenceList)
    for sentence in sentenceList:
        wordList = list(filter(lambda x: not  x in sentenceMarkList ,sentence.split()))
        result += len(wordList)
    return result / (amountOfSentence if amountOfSentence>0 else 1)

aslwIndex = calculateASLW(sentenceList)
print('aslw', aslwIndex)

# average sentence length in syllable 
def calculateASLS(sentenceList):
    global sentenceMarkList
    result = 0
    amountOfSentence = len(sentenceList)

    for sentence in sentenceList:
        syllableList = list(filter(lambda x: x and not  (x in sentenceMarkList) ,re.split(' |_',sentence)))
        result += len(syllableList)
    return result / (amountOfSentence if amountOfSentence>0 else 1)

aslsIndex = calculateASLS(sentenceList)
print('asls', aslsIndex)


# average senetence length in character

def calculateASLC(sentenceList): 
    global sentenceMarkList
    result = 0
    amountOfSentence = len(sentenceList)
    for sentence in sentenceList:
        charList = list(filter(lambda x: not (x in sentenceMarkList or x == ' '),list(sentence)))
        result += len(charList)
    return result / (amountOfSentence if amountOfSentence>0 else 1)

aslcIndex = calculateASLC(sentenceList)
print('aslc', aslcIndex)

# average word length in character

def calculateAWLC(sentenceList):
    global sentenceMarkList
    totalChar = 0
    totalWord = 0
    for sentence in sentenceList:
        wordList = list(filter(lambda x: not  x in sentenceMarkList ,sentence.split()))
        for word in wordList:
            totalChar += len(word)
        totalWord += len(wordList)
    return totalChar/totalWord

awlcIndex = calculateAWLC(sentenceList)
print('awlc', awlcIndex)


# averagew word length in syllable

def calculateAWLS(SentenceList):
    global sentenceMarkList
    totalSyllable = 0
    totalWord = 0
    for sentence in SentenceList:
        syllableList = list(filter(lambda x: x and not  (x in sentenceMarkList) ,re.split(' |_',sentence)))

        wordList = list(filter(lambda x: not  x in sentenceMarkList ,sentence.split()))
        totalSyllable += len(syllableList)
        totalWord += len(wordList)
    
    return totalSyllable/totalWord

awlsIndex = calculateAWLS(sentenceList)
print('awls', awlsIndex)

# percertange of difficult syllables

def calculatePDS(sentenceList,commonSyllableList):
    global sentenceMarkList
    totalSyllable = 0
    totalDifficultSyllable = 0

    for sentence in sentenceList:
        syllableList = list(filter(lambda x: x and not  (x in sentenceMarkList) ,re.split(' |_',sentence)))
        difficultSyllableList = list(filter(lambda  x: x and not x in commonSyllableList,syllableList))
        totalSyllable += len(syllableList)
        totalDifficultSyllable += len(difficultSyllableList)
    return totalDifficultSyllable/totalSyllable

pdsIndex = calculatePDS(sentenceList,commonSyllableSet)
print('pds',pdsIndex)

# percertange of difficult word

def calculatePDW(sentenceList,commonWordList):
    global sentenceMarkList
    totalWord = 0
    totalDifficultWord = 0
    for sentence in sentenceList:
        wordList = list(filter(lambda x: not  x in sentenceMarkList ,sentence.split()))
        difficultWordList = list(filter(lambda  x : not x.replace('_',' ') in commonWordList,wordList))
        totalWord += len(wordList)
        totalDifficultWord += len(difficultWordList)
    return totalDifficultWord/totalWord

pdwIndex = calculatePDW(sentenceList,commonWordSet)
print('pdw',pdwIndex)

#percertange of Sino-vietnamese word

def calculatePSVW(sentenceList,sinoVietWordSet):
    global sentenceMarkList
    totalSinoVietWord = 0
    totalWord = 0
    for sentence in sentenceList:
        wordList = list(filter(lambda  x: not x in sentenceMarkList, sentence.split()))
        sinoVietWordList = list(filter(lambda x: x.replace('_',' ') in sinoVietWordSet,wordList))
        totalSinoVietWord+=len(sinoVietWordList)
        totalWord+=len(wordList)
    return totalSinoVietWord/totalWord

psvwIndex = calculatePSVW(sentenceList,sinoVietWordSet)
print('psvw',psvwIndex)

#percertange of dialect words (pdiaw)

def calculatePDiaW(sentenceList,dialectWordSet):
    global sentenceMarkList
    totalDialectWord = 0
    totalWord = 0
    for sentence in sentenceList:
        wordList = list(filter(lambda  x: not x in sentenceMarkList, sentence.split()))
        dialectWordList = list(filter(lambda x: x.replace('_',' ') in dialectWordSet,wordList))
        totalWord+=len(wordList)
        totalDialectWord+=len(dialectWordList)
    return totalDialectWord/totalWord

pdiawIndex = calculatePDiaW(sentenceList,dialectWordSet)
print('pdiaw',pdiawIndex)


#calculate score

def calculateLAVFomula(aslcIndex, awlcIndex, pdwIndex ):
    return 0.004*aslsIndex + 0.1905*awlcIndex + 2.7147*pdwIndex - 0.7295
 
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