from collections import Counter
import os
import numpy as np
from vncorenlp import VnCoreNLP

class TextAnalysiser:
    def __init__(self):
        #open dataset file
        frequencyWordFile = open('./Dataset/FrequencyWord.txt',mode='r',encoding='utf8')
        frequencySyllableFile = open('./Dataset/FrequencySyllable.txt',mode='r',encoding='utf8')
        commonWordFile = open('./Dataset/3000_most_word.txt',mode = 'r', encoding="utf8")
        commonSyllableFile = open('./Dataset/3000_most_syllable.txt', mode = 'r', encoding="utf8")
        sinoVietWordFile = open('./Dataset/sino_vietnamese.txt',mode='r', encoding="utf8")
        dialectWordFile = open('./Dataset/dialect.txt',mode='r', encoding="utf8")

        #read data from file and process
        rawCommonWordList = commonWordFile.read()
        rawCommonSyllableList = commonSyllableFile.read()
        rawSinoVietWordSet = sinoVietWordFile.read()
        rawDialectWordSet = dialectWordFile.read()

        self.commonWordSet = set(rawCommonWordList.split('\n'))
        self.commonSyllableSet = set(rawCommonSyllableList.split('\n'))
        self.sinoVietWordSet = set(rawSinoVietWordSet.split('\n'))
        self.dialectWordSet = set(rawDialectWordSet.split('\n'))

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

        # load vncorenlp annator
        jarFullPath = os.path.abspath("./VnCoreNLP/VnCoreNLP-1.1.1.jar")
        self.annotator = VnCoreNLP(jarFullPath, annotators="wseg,pos,ner", max_heap_size='-Xmx2g') 
    
    def analysis(self,rawInputData):
   
        inputSentenceList = self.annotator.annotate(rawInputData)['sentences']
        inputPosWordList = []
        inputWordList=[]
        inputSyllableList = []
        inputNerWordList = []

        for sentence in inputSentenceList
            for wordDict in sentence:
                word = wordDict['form']
                postag = wordDict['posTag']
                # pharsetag = result[2]
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
                

                # if pharsetag != 'O':
                #     first,phrase = pharsetag.split("-")
                #     if not inputPhraseList or first == 'B':
                #         inputPhraseList.append(([word],phrase))
                #     else:
                #         inputPhraseList[-1][0].append(word)
                # else:
                #     inputPhraseList.append(([word],'O'))

                inputPosWordList.append((word,postag))
                inputWordList.append(word)
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
        numberOfDistinctWord = len(set(inputWordList))

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


        shallowOutput = {
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
            }

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
            averageNumberOfPostagPerSentence['averageNumberOf{}PerSentence'.format(postag)] = number/numberOfSentence

        #average number of unique postag per sentence
        averageNumberOfUniquePostagPerSentence = {}
        for postag, number in postagUniqueCounter.items():
            averageNumberOfUniquePostagPerSentence['averageNumberOfUnique{}PerSentence'.format(postag)] = number/numberOfSentence
        
        #percertange of postag per document
        percertangeOfPostagPerDocument = {}
        for postag, number in postagCounter.items():
            percertangeOfPostagPerDocument['percertangeOf{}PerDocument'.format(postag)] = number/numberOfWord
        
        #percertange of unique postag per document
        percertangeOfUniquePostagPerDocument = {}
        for postag, number in postagUniqueCounter.items():
            percertangeOfUniquePostagPerDocument['percertangeOfUnique{}PerDocument'.format(postag)] = number/numberOfWord

        #percertange of unique postag div unique word per document
        percertangeOfUniquePostagDivUniqueWordPerDocument = {}
        for postag, number in postagUniqueCounter.items():
            percertangeOfUniquePostagDivUniqueWordPerDocument['percertangeOfUnique{}DivUniqueWordPerDocument'.format(postag)] = number/numberOfDistinctWord

        posOutput =  {
                'number_of_proper_noun':numberOfProperNouns,
                'number_of_distinct_proper_noun':numberOfDistinctProperNouns,
                'psvw':psvw,
                'pdiadw':pdiadw
        }

        posOutput.update(averageNumberOfPostagPerSentence)
        posOutput.update(averageNumberOfUniquePostagPerSentence)
        posOutput.update(percertangeOfPostagPerDocument)
        posOutput.update(percertangeOfUniquePostagPerDocument)
        posOutput.update(percertangeOfUniquePostagDivUniqueWordPerDocument)


    #Parsed synatic Features
        #number of word phrase per document

        # pharsetagWordListDict = {
        #     'AP':[],
        #     'IP':[],
        #     'NP':[],
        #     'PP':[],
        #     'OP':[],
        #     'RP':[],
        #     'VP':[]
        # }

        # for wordList,phrase in inputPhraseList:
        #     if phrase in pharsetagWordListDict:
        #         pharsetagWordListDict[phrase].append(wordList)


        # numberOfWordPhrasePerDocument = {}
        # for phraseTag, wordList in pharsetagWordListDict.items():
        #     numberOfWordPhrasePerDocument['numberOf{}PerDocument'.format(phraseTag)] = len(wordList)

        # numberOfWordPhrasePerSentence = {}
        # for phraseTag, wordList in pharsetagWordListDict.items():
        #     numberOfWordPhrasePerSentence['numberOf{}PerSentence'.format(phraseTag)] = len(wordList)/len(inputSentenceList)

        # averageLengthOfWordPhraseByWord = {}
        # for phraseTag, wordList in pharsetagWordListDict.items():
        #     averageLengthOfWordPhraseByWord['averageLengthOf{}ByWord'.format(phraseTag)]=0
        #     for wordPhrase in wordList:
        #         averageLengthOfWordPhraseByWord['averageLengthOf{}ByWord'.format(phraseTag)] += len(wordPhrase)
        
        # averageLengthOfWordPhraseByCharacter = {}
        # for phraseTag,wordList in pharsetagWordListDict.items():
        #     averageLengthOfWordPhraseByCharacter['averageLengthOf{}ByCharacter'.format(phraseTag)]=0
        #     for wordPhrase in wordList:
        #         for word in wordPhrase:
        #             averageLengthOfWordPhraseByCharacter['averageLengthOf{}ByCharacter'.format(phraseTag)]+=len(word)
        
        # parseOutput = {}
        # parseOutput.update(numberOfWordPhrasePerDocument)
        # parseOutput.update(numberOfWordPhrasePerSentence)
        # parseOutput.update(averageLengthOfWordPhraseByWord)
        # parseOutput.update(averageLengthOfWordPhraseByCharacter)

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
        nerOutput = {
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
        #output
        output = {
            'Shallow': shallowOutput, 
            'Pos': posOutput,
            'Ner': nerOutput
        }
        return output
