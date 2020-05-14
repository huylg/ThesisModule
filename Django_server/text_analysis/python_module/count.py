from collections import Counter
import underthesea

commonWordFile = open('../Thesis_Dataset/3000_most_Word.txt',mode = 'r')
commonSyllableFile = open('../Thesis_Dataset/3000_most_syllable.txt', mode = 'r')
sinoVietWordFile = open('../Thesis_Dataset/sino_vietnamese.txt',mode='r')
dialectWordFile = open('../Thesis_Dataset/dialect.txt',mode='r')
inputFile = open(input(),mode='r') 

rawCommonWordList = commonWordFile.read()
rawCommonSyllableList = commonSyllableFile.read()
rawSinoVietWordSet = sinoVietWordFile.read()
rawDialectWordSet = dialectWordFile.read()
rawInputData = inputFile.read()

commonWordFile.close()
commonSyllableFile.close()
sinoVietWordFile.close()
dialectWordFile.close()
inputFile.close()

commonWordSet = set(rawCommonWordList.split('\n'))
commonSyllableSet = set(rawCommonSyllableList.split('\n'))
sinoVietWordSet = set(rawSinoVietWordSet.split('\n'))
dialectWordSet = set(rawDialectWordSet.split('\n'))

inputSentenceList = underthesea.sent_tokenize(rawInputData)
inputPosWordList = underthesea.pos_tag(rawInputData)
inputWordList = underthesea.word_tokenize(rawInputData)
inputWordCounter = Counter(inputWordList)

inputSyllableList = []
for word,pos in inputPosWordList:
    if pos != 'CH':
        inputSyllableList += word.lower().split()
inputDistinctSyllableSet = set(inputSyllableList)

inputProperNounWordList = []
for Word,pos in inputPosWordList:
    if pos == 'Np':
        inputProperNounWordList.append(Word)
inputDistinctProperNounWordList = set(inputProperNounWordList)

inputDialectWordList = list(filter(lambda word: word in dialectWordSet,inputWordList))
inputDistinctDialectWordList = set(inputDialectWordList)

inputSinoVietWordList = list(filter(lambda word: word in sinoVietWordSet,inputWordList))
inputDistinctSinoViewWordList = set(inputSinoVietWordList)


# number of sentence
numberOfSentence = len(inputSentenceList)

# number of Word
numberOfWord = len(inputWordList)

# number of distinct Word
numberOfDistinctWord = len(inputWordCounter)

# number of syllable:
numberOfSyllable = len(inputSyllableList)

# number of distinct syllable:
numberofDistinctSyllable = len(inputSyllableList)

# number of character
numberOfCharacter = 0
for syllable in inputSyllableList:
    numberOfCharacter+=len(syllable)

# number of proper nouns
numberOfProperNouns = len(inputProperNounWordList)

#number of Distinct proper nouns
numberOfDistinctProperNouns = len(inputDistinctProperNounWordList)

# average sentence length in Word
aslw = numberOfWord/numberOfSentence

# average sentence length in syllable 
asls = numberOfSyllable/numberOfSentence

# average sentence length in char 
aslc = numberOfCharacter/numberOfSentence

# average Word length in syllable
awls = numberOfSyllable/numberOfWord

# average Word length in character
awlc = numberOfCharacter/numberOfWord

# percertange of difficult syllables
inputDifficultSyllybleList = list(filter(lambda syllable: not syllable in commonSyllableSet,inputSyllableList))
numberOfDifficultSyllable = len(inputDifficultSyllybleList)
pds = numberOfDifficultSyllable/numberOfSyllable

# percertange of difficult word
inputDifficultWordList = list(filter(lambda word: not word in commonWordSet,inputWordList))
numberOfDifficultWord = len(inputDifficultWordList)
pdw = numberOfDifficultWord / numberOfWord

#percertange of Sino-vietnamese word
numberOfSinoVietWord = len(inputSinoVietWordList)
psvw = numberOfSinoVietWord / numberOfWord

#percertange of dialect words (pdiaw)
numberOfDialectWord = len(inputDialectWordList)
pdiadw = numberOfDialectWord / numberOfWord


#output
print('number of sentence',numberOfSentence)
print('number of word', numberOfWord)
print('number of distinct word', numberOfDistinctWord)
print('number of syllable',numberOfSyllable)
print('number of distinct syllable',numberofDistinctSyllable)
print('number of character',numberOfCharacter)
print('number of proper noun',numberOfProperNouns)
print('number of distinct proper noun',numberOfProperNouns)
print('aslw',aslw)
print('asls',asls)
print('aslc',aslc)
print('awls',awls)
print('awlc',awlc)
print('pds',pds)
print('pdw',pdw)
print('psvw',psvw)
print('pdiadw',pdiadw)