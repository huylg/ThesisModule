from collections import Counter
import underthesea

class TextAnalysiser:
    def __init__(self):
        commonWordFile = open('./Thesis_Dataset/3000_most_word.txt',mode = 'r', encoding="utf8")
        commonSyllableFile = open('./Thesis_Dataset/3000_most_syllable.txt', mode = 'r', encoding="utf8")
        sinoVietWordFile = open('./Thesis_Dataset/sino_vietnamese.txt',mode='r', encoding="utf8")
        dialectWordFile = open('./Thesis_Dataset/dialect.txt',mode='r', encoding="utf8")

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
    
    def analysis(self,rawInputData):
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

        inputDialectWordList = list(filter(lambda word: word in self.dialectWordSet,inputWordList))
        inputDistinctDialectWordList = set(inputDialectWordList)

        inputSinoVietWordList = list(filter(lambda word: word in self.sinoVietWordSet,inputWordList))
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
        inputDifficultSyllybleList = list(filter(lambda syllable: not syllable in self.commonSyllableSet,inputSyllableList))
        numberOfDifficultSyllable = len(inputDifficultSyllybleList)
        pds = numberOfDifficultSyllable/numberOfSyllable

        # percertange of difficult word
        inputDifficultWordList = list(filter(lambda word: not word in self.commonWordSet,inputWordList))
        numberOfDifficultWord = len(inputDifficultWordList)
        pdw = numberOfDifficultWord / numberOfWord

        #percertange of Sino-vietnamese word
        numberOfSinoVietWord = len(inputSinoVietWordList)
        psvw = numberOfSinoVietWord / numberOfWord

        #percertange of dialect words (pdiaw)
        numberOfDialectWord = len(inputDialectWordList)
        pdiadw = numberOfDialectWord / numberOfWord

        # Luong An Vinh Fomula
        lavFomulaResult = 0.004*aslc + 0.1905*awlc + 2.7147*pdw - 0.7295

        # NH1982 fomula
        nh1982FomulaResult =  2*awlc + 0.2*aslc - 6

        # NH1985 fomula
        wdIndex =  pdw*100
        nh1985FomulaResult = 0.27*wdIndex + 0.13*aslc +1.74

        #output
        output = {
            'posTag' : inputPosWordList,
            'wordCounter' : inputWordCounter,
            'number_of_sentence':numberOfSentence,
            'number_of_word' : numberOfWord,
            'number_of_distinct_word': numberOfDistinctWord,
            'number_of_syllable':numberOfSyllable,
            'number_of_distinct_syllable':numberofDistinctSyllable,
            'number_of_character':numberOfCharacter,
            'number_of_proper_noun':numberOfProperNouns,
            'number_of_distinct_proper_noun':numberOfProperNouns,
            'aslw':aslw,
            'asls':asls,
            'aslc':aslc,
            'awls':awls,
            'awlc':awlc,
            'pds':pds,
            'pdw':pdw,
            'psvw':psvw,
            'pdiadw':pdiadw,
            'LAVFomula' : lavFomulaResult,
            'NH1982' : nh1982FomulaResult,
            'NH1985': nh1985FomulaResult
        }
        return output
      