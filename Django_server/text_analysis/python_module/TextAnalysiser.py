from collections import Counter
import os
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from vncorenlp import VnCoreNLP
import pickle

class TextAnalysiser:
    def __init__(self):
        #open dataset file
        frequencyWordFile = open('./Dataset/FrequencyWord.txt',mode='r',encoding='utf8')
        frequencySyllableFile = open('./Dataset/FrequencySyllable.txt',mode='r',encoding='utf8')
        commonWordFile = open('./Dataset/3000_most_word.txt',mode = 'r', encoding="utf8")
        commonSyllableFile = open('./Dataset/3000_most_syllable.txt', mode = 'r', encoding="utf8")
        sinoVietWordFile = open('./Dataset/sino_vietnamese.txt',mode='r', encoding="utf8")
        dialectWordFile = open('./Dataset/dialect.txt',mode='r', encoding="utf8")
        modulePickleFile = open('./text_analysis/python_module/MultinomialNB_readability.pickle',mode='rb')

        #read data from file and process
        rawCommonWordList = commonWordFile.read()
        rawCommonSyllableList = commonSyllableFile.read()
        rawSinoVietWordSet = sinoVietWordFile.read()
        rawDialectWordSet = dialectWordFile.read()

        self.commonWordSet = set(rawCommonWordList.split('\n'))
        self.commonSyllableSet = set(rawCommonSyllableList.split('\n'))
        self.sinoVietWordSet = set(rawSinoVietWordSet.split('\n'))
        self.dialectWordSet = set(rawDialectWordSet.split('\n'))
        self.module = pickle.load(modulePickleFile)

        rawFrequencyWordList = list(frequencyWordFile.read().split('\n'))
        rawFrequencySyllableList = list(frequencySyllableFile.read().split('\n'))

        # load and resize(from 1- 100) frequency word list
        self.frequencyWordRankingDictionary = {}
        for i in range(0,len(rawFrequencyWordList)-1):
            word = ' '.join(list(rawFrequencyWordList[i].split())[0:-2])
            rank = i // 362 + 1
            self.frequencyWordRankingDictionary[word]=rank

        # load and resize(from 1- 100) frequency word list
        self.frequencySyllableRankingDictionary = {}
        for i in range(0,len(rawFrequencySyllableList)-1):
            syllable = rawFrequencySyllableList[i].split()[0]
            rank = i//80 + 1
            self.frequencySyllableRankingDictionary[syllable] = rank

        #close all file    
        frequencyWordFile.close()
        frequencySyllableFile.close()
        commonWordFile.close()
        commonSyllableFile.close()
        sinoVietWordFile.close()
        dialectWordFile.close()
        modulePickleFile.close()

        # load vncorenlp annator
        jarFullPath = os.path.abspath("VnCoreNLP/VnCoreNLP-1.1.1.jar")
        self.annotator = VnCoreNLP(jarFullPath, annotators="wseg,pos,ner", max_heap_size='-Xmx2g') 
        
    
    def analysis(self,rawInputData):
   
        inputSentenceList = self.annotator.annotate(rawInputData)['sentences']
        inputPosWordList = []
        inputWordList=[]
        inputSyllableList = []
        inputNerWordList = []

        for sentence in inputSentenceList:
            for wordDict in sentence:
                word = wordDict['form']
                postag = wordDict['posTag']
                nerlabel = wordDict['nerLabel']

                if postag != 'CH':
                    word = word.replace('_',' ')
                    inputSyllableList += word.lower().split()

                if nerlabel!='O':
                    first, phrase = nerlabel.split("-")
                    if not inputNerWordList or first == 'B':
                        inputNerWordList.append((word,phrase))
                    else:
                        inputNerWordList[-1] = (inputNerWordList[-1][0] + " {}".format(word),phrase)

                inputPosWordList.append((word,postag))
                inputWordList.append(word)
        inputWordCounter = Counter(inputWordList)
        inputSyllableCounter = Counter(inputSyllableList)
        inputDistinctSyllableSet = set(inputSyllableList)

        inputProperNounWordList = []
        for  wordPosTuple in inputPosWordList:
            word = wordPosTuple[0]
            pos = wordPosTuple[1]
            if pos == 'Np':
                inputProperNounWordList.append(word)
        inputDistinctProperNounWordList = set(inputProperNounWordList)

        inputDialectWordList = list(filter(lambda word: word in self.dialectWordSet,inputWordList))
        inputDistinctDialectWordList = set(inputDialectWordList)

        inputSinoVietWordList = list(filter(lambda word: word in self.sinoVietWordSet,inputWordList))
        inputDistinctSinoViewWordList = set(inputSinoVietWordList)

        #shallow features

        # number of sentence
        numberOfSentence = len(inputSentenceList)

        # number of Word
        numberOfWord = len(inputWordList)

        # number of distinct Word
        numberOfDistinctWord = len(inputWordCounter)

        # number of syllable:
        numberOfSyllable = len(inputSyllableList)

        # number of distinct syllable:
        numberofDistinctSyllable = len(inputDistinctSyllableSet)

        # number of character
        numberOfCharacter = 0
        for syllable in inputSyllableList:
            numberOfCharacter+=len(syllable)

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
        inputDifficultSyllybleList = list(filter(lambda syllable: not syllable.lower() in self.commonSyllableSet,inputSyllableList))
        numberOfDifficultSyllable = len(inputDifficultSyllybleList)
        pds = numberOfDifficultSyllable/numberOfSyllable

        # percertange of difficult word
        inputDifficultWordList = list(filter(lambda word: not word.lower() in self.commonWordSet,inputWordList))
        numberOfDifficultWord = len(inputDifficultWordList)
        pdw = numberOfDifficultWord / numberOfWord

    #Posbased Feature
        #percertange of Sino-vietnamese word
        numberOfSinoVietWord = len(inputSinoVietWordList)
        psvw = numberOfSinoVietWord / numberOfWord

        #percertange of dialect words (pdiaw)
        numberOfDialectWord = len(inputDialectWordList)
        pdiadw = numberOfDialectWord / numberOfWord

        # number of proper nouns
        numberOfProperNouns = len(inputProperNounWordList)

        #number of Distinct proper nouns
        numberOfDistinctProperNouns = len(inputDistinctProperNounWordList)
        
        postagWordListDict = {
            'A': [],
            'N': [],
            'R':[],
            'V':[],
            'C':[],
            'E':[]
        }

        for word,postag in inputPosWordList:
            if postag in postagWordListDict:
                postagWordListDict[postag].append(word)
        
        postagCounter = {}
        postagUniqueCounter = {}
        for postag,wordlist in postagWordListDict.items():
            postagCounter[postag] = len(wordlist)
            postagUniqueCounter[postag] = len(set(wordlist))

        #average number of postag per sentence
        averageNumberOfPostagPerSentence = {}
        for postag, number in postagCounter.items():
            averageNumberOfPostagPerSentence[postag] = number/numberOfSentence

        #average number of unique postag per sentence
        averageNumberOfUniquePostagPerSentence = {}
        for postag, number in postagUniqueCounter.items():
            averageNumberOfUniquePostagPerSentence[postag] = number/numberOfSentence
        
        #percertange of postag per document
        percertangeOfPostagPerDocument = {}
        for postag, number in postagCounter.items():
            percertangeOfPostagPerDocument[postag] = number/numberOfWord
        
        #percertange of unique postag per document
        percertangeOfUniquePostagPerDocument = {}
        for postag, number in postagUniqueCounter.items():
            percertangeOfUniquePostagPerDocument[postag] = number/numberOfWord

        #percertange of unique postag div unique word per document
        percertangeOfUniquePostagDivUniqueWordPerDocument = {}
        for postag, number in postagUniqueCounter.items():
            percertangeOfUniquePostagDivUniqueWordPerDocument[postag] = number/numberOfDistinctWord

    #Entity destiny Features
        # number of entity per documet
        entityList = []
        for word,postag in inputPosWordList:
            if 'N' in postag:
                entityList.append(word)
        numberOfEntityPerDocument = len(entityList)

        # number of unique entity per document
        numberOfUniqueEntityPerDocument = len(set(entityList))

        # number of entity per sentence
        numberOfEntityPerSentence = numberOfEntityPerDocument/numberOfSentence

        # number of unique entity per sentence
        numberOfUniqueEntityPerSentence = numberOfUniqueEntityPerDocument/numberOfSentence

        #number of named entity per document
        numberOfNamedEntityPerDocument = len(inputNerWordList)

        #number of unique named entity per document 
        numberOfUniqueNamedEntityPerDocument = len(set(inputNerWordList))

        #number of named entity per sentence
        numberOfNamedEntityPerSentence = numberOfNamedEntityPerDocument/numberOfSentence

        #number of unique named entity per sentence
        numberOfUniqueNamedEntityPerSentence = numberOfUniqueNamedEntityPerDocument/numberOfSentence

        #ratpercertangeio number named entity div number enity
        percertangeNumberNamedEntityDivNumberEnityPerDocument = numberOfNamedEntityPerDocument / numberOfEntityPerDocument

        #percertange unique number named entity div unique number enity
        percertangeUniqueNumberNamedEntityDivUniqueNumberEnityPerDocument = numberOfUniqueNamedEntityPerDocument / numberOfUniqueEntityPerDocument

        #percertange named entity
        percertangeNamedEntity = numberOfNamedEntityPerDocument/numberOfWord

    #readability formula
        # Luong An Vinh Fomula
        lavFomulaResult = 0.004*aslc + 0.1905*awlc + 2.7147*pdw - 0.7295

        # NH1982 fomula
        nh1982FomulaResult =  2*awlc + 0.2*aslc - 6

        # NH1985 fomula
        wdIndex =  pdw*100
        nh1985FomulaResult = 0.27*wdIndex + 0.13*aslc +1.74

        #readability classification
        X_data = np.array([numberOfSentence,numberOfWord,numberOfDistinctWord,numberOfSyllable,numberofDistinctSyllable,numberOfCharacter,numberOfProperNouns,numberOfDistinctProperNouns,aslw,asls,aslc,awls,awlc,pds,pdw,psvw,pdiadw]).reshape(1, -1)
        readabilityClassfication = self.module.predict(X_data).tolist()[0]

    #-----------------------other info-------------------

        #word Ranking
        wordRanking = {}
        for word in inputWordList:
            if word.lower() in self.frequencyWordRankingDictionary:
                wordRanking[word] = self.frequencyWordRankingDictionary[word.lower()] 
            else:
                wordRanking[word] = 100

        #syllable Ranking
        syllableRanking = {}
        for syllable in inputSyllableList:
            if syllable.lower() in self.frequencySyllableRankingDictionary:
                syllableRanking[syllable] = self.frequencySyllableRankingDictionary[syllable.lower()]
            else:
                syllableRanking[syllable] = 100

        #output
        output = {
            'data':{
                'Shallow':{
                    'number_of_sentence':numberOfSentence,
                    'number_of_word' : numberOfWord,
                    'number_of_distinct_word': numberOfDistinctWord,
                    'number_of_syllable':numberOfSyllable,
                    'number_of_distinct_syllable':numberofDistinctSyllable,
                    'number_of_character':numberOfCharacter,
                    'aslw':aslw,
                    'asls':asls,
                    'aslc':aslc,
                    'awls':awls,
                    'awlc':awlc,
                    'pds':pds,
                    'pdw':pdw
                },
                'Pos':{
                    'number_of_proper_noun':numberOfProperNouns,
                    'number_of_distinct_proper_noun':numberOfDistinctProperNouns,
                    'psvw':psvw,
                    'pdiadw':pdiadw,
                    'averageNumberOfPostagPerSentence': averageNumberOfPostagPerSentence,
                    'averageNumberOfUniquePostagPerSentence': averageNumberOfUniquePostagPerSentence,
                    'percertangeOfPostagPerDocument': percertangeOfPostagPerDocument,
                    'percertangeOfUniquePostagPerDocument': percertangeOfUniquePostagPerDocument,
                    'percertangeOfUniquePostagDivUniqueWordPerDocument':percertangeOfUniquePostagDivUniqueWordPerDocument
                },
                
                'Ner':{
                    'numberOfEntityPerDocument':numberOfEntityPerDocument,
                    'numberOfUniqueEntityPerDocument':numberOfUniqueEntityPerDocument,
                    'numberOfEntityPerSentence':numberOfEntityPerSentence,
                    'numberOfUniqueEntityPerSentence':numberOfUniqueEntityPerSentence,
                    'numberOfNamedEntityPerDocument':numberOfNamedEntityPerDocument,
                    'numberOfUniqueNamedEntityPerDocument':numberOfUniqueNamedEntityPerDocument,
                    'numberOfNamedEntityPerSentence':numberOfNamedEntityPerSentence,
                    'numberOfUniqueNamedEntityPerSentence':numberOfUniqueNamedEntityPerSentence,
                    'percertangeNumberNamedEntityDivNumberEnityPerDocument':percertangeNumberNamedEntityDivNumberEnityPerDocument,
                    'percertangeUniqueNumberNamedEntityDivUniqueNumberEnityPerDocument':percertangeUniqueNumberNamedEntityDivUniqueNumberEnityPerDocument,
                    'percertangeNamedEntity':percertangeNamedEntity
                 
                }
            },
            


            'readabiity': readabilityClassfication,
            
            'formula':{
                'LAVFomula' : lavFomulaResult,
                'NH1982' : nh1982FomulaResult,
                'NH1985': nh1985FomulaResult
            },

            'wordPair':{
                'SyllableRanking': syllableRanking,
                'wordRanking': wordRanking,
                'nertag': inputNerWordList,
                'postag' : inputPosWordList,
                'wordCounter' : inputWordCounter,
                'syllableCounter' : inputSyllableCounter
            }

        }
        return output
