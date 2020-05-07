from collections import Counter
import underthesea

class TextAnalysiser:

    def __init__(self,rawInputData):
        rawInputData = rawInputData.lower()
        self.rawIntput = rawInputData
        self.__loadDataFromFile()
        self.sentenceMarkList = set([',','.','!','?',':',';','-'])
        self.sentenceList = underthesea.sent_tokenize(rawInputData)
        self.wordList = list(filter(lambda x: not  x in self.sentenceMarkList ,underthesea.word_tokenize(rawInputData)))
        
        self.syllableList = []
        for word in self.wordList:
            self.syllableList += word.split()

        self.charList = []
        for syllable in self.syllableList:
            self.charList += list(syllable)

        self.wordCounter = Counter(self.wordList)
        self.posWordList = underthesea.pos_tag(rawInputData)

    def __loadDataFromFile(self):
        commonWordFile = open('../Thesis_Dataset/3000_most_word.txt',mode = 'r', encoding="utf8")
        commonSyllableFile = open('../Thesis_Dataset/3000_most_syllable.txt', mode = 'r', encoding="utf8")
        sinoVietWordFile = open('../Thesis_Dataset/sino_vietnamese.txt',mode='r', encoding="utf8")
        dialectWordFile = open('../Thesis_Dataset/dialect.txt',mode='r', encoding="utf8")

        rawCommonWordList = commonWordFile.read()
        rawCommonSyllableList = commonSyllableFile.read()
        rawSinoVietWordSet = sinoVietWordFile.read()
        rawDialectWordSet = dialectWordFile.read()

        self.commonWordSet = set(rawCommonWordList.split('\n'))
        self.commonSyllableSet = set(rawCommonSyllableList.split('\n'))
        self.sinoVietWordSet = set(rawSinoVietWordSet.split('\n'))
        self.dialectWordSet = set(rawDialectWordSet.split('\n'))

        commonWordFile.close()
        commonSyllableFile.close()
        sinoVietWordFile.close()
        dialectWordFile.close() 
    
    # average sentence length in word
    @staticmethod
    def calculateASLW(sentenceList,wordList):
        return len(wordList)/len(sentenceList)

    # average sentence length in syllable 
    @staticmethod
    def calculateASLS(sentenceList,syllableList):
        return len(syllableList)/len(sentenceList) 

    # average senetence length in character
    @staticmethod
    def calculateASLC(sentenceList,charList): 
        return len(charList)/len(sentenceList) 

    # average word length in character
    @staticmethod
    def calculateAWLC(wordList,charList):
        return len(charList)/len(wordList) 

    # averagew word length in syllable
    @staticmethod
    def calculateAWLS(wordList,syllableList):
        return len(syllableList)/len(wordList)

    # percertange of difficult syllables
    @staticmethod
    def calculatePDS(syllableList,commonSyllableSet):
        totalSyllable = len(syllableList)
        totalDifficultSyllable = len(list(filter(lambda syllable: not syllable in commonSyllableSet,syllableList)))
        return totalDifficultSyllable/totalSyllable

    # percertange of difficult word
    @staticmethod
    def calculatePDW(wordList,commonWordSet):
        totalWord = len(wordList)
        totalDifficultWord = len(list(filter(lambda word: not word in commonWordSet,wordList)))
        return totalDifficultWord/totalWord

    #percertange of Sino-vietnamese word
    @staticmethod
    def calculatePSVW(wordList,sinoVietWordSet):
        totalWord = len(wordList)
        totalSinoVietWord = len(list(filter(lambda word: word in sinoVietWordSet,wordList)))
        return totalSinoVietWord/totalWord

    #percertange of dialect words (pdiaw)
    @staticmethod
    def calculatePDiaW(wordList,dialectWordSet):
        totalWord = len(wordList)
        totalDialectWord = len(list(filter(lambda word: word in dialectWordSet,wordList)))
        return totalDialectWord/totalWord

    #calculate score
    @staticmethod
    def calculateLAVFomula(aslcIndex, awlcIndex, pdwIndex ):
        return 0.004*aslcIndex + 0.1905*awlcIndex + 2.7147*pdwIndex - 0.7295
 
    @staticmethod
    def calculateNH1982(aslcIndex,awlcIndex):
        return 2*awlcIndex + 0.2*aslcIndex - 6
    
    @staticmethod
    def calculateNH1985(aslcIndex, pswIndex):
        wdIndex =  pswIndex*100
        return 0.27*wdIndex + 0.13*aslcIndex +1.74
