import re
commonWordFile = open('../Thesis_Dataset/3000_most_word.txt',mode = 'r', encoding = 'utf-8')
commonSyllableFile = open('../Thesis_Dataset/3000_most_syllable.txt', mode = 'r', encoding = 'utf-8')

inputFilePath = input()
inputFile = open(inputFilePath,mode='r',encoding = 'utf-8')

rawCommonWordList = commonWordFile.read()
rawCommonSyllableList = commonSyllableFile.read()
rawInputData = inputFile.read()

commonWordSet = set(rawCommonWordList.split('\n'))
commonSyllableSet = set(rawCommonSyllableList.split('\n'))
 
sentenceMarkList = set([',','.','!','?',':',';','-'])

#preprocesing
sentenceList = rawInputData.split('\n')

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


#calculate score


#classification


commonWordFile.close()
commonSyllableFile.close()