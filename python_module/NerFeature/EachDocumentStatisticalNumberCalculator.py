from vncorenlp import VnCoreNLP
import numpy as np
import os
import pandas as pd
import xlsxwriter


jarFullPath = os.path.abspath("../VnCoreNLP/VnCoreNLP-1.1.1.jar")
annotator = VnCoreNLP(jarFullPath, annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g')

rootdir = '../Dataset/send/or - without note/'
writer = pd.ExcelWriter('./EachDocumentStatisticalNumber.xlsx', engine='xlsxwriter')
dataFrame = pd.DataFrame()
classlist = list(map(int,filter(lambda dir: not dir.startswith('.'),os.listdir(rootdir))))

for classNum in classlist:
    classDir = rootdir + '{}/'.format(classNum)

    for root,subdirs,files  in os.walk(classDir):
         for file in files:
            if( not file.startswith('.')):
                inputFile = open(root + '/' + file,mode='r',encoding='utf-8')   
                inputText = inputFile.read()
                sentenceList = annotator.ner(inputText)
                nertagCount = {}
                nertagCount['PER'] = []
                nertagCount['LOC'] = []
                nertagCount['ORG'] = []
                nertagCount['MISC'] = []
                for sentence in sentenceList:
                    for(word,nerTag) in sentence:
                        for key in nertagCount.keys():
                            if key != 'O' and key in nerTag:
                                nertagCount[key].append(word)
                                break

                resultDict = {}
                amountOfSentence = len(sentenceList)
                for nertag,wordList in nertagCount.items():
                    amountOfWord = len(wordList)
                    amountOfUniqueWord = len(set(wordList))    
                    resultDict['avg_{}_per_document'.format(nertag)]= amountOfWord
                    resultDict['avg_unique_{}_per_document'.format(nertag)]= amountOfUniqueWord
                    resultDict['avg_{}_per_sentence'.format(nertag)]= amountOfWord/amountOfSentence
                    resultDict['avg_unique_{}_per_sence'.format(nertag)]= amountOfUniqueWord/amountOfSentence
                resultDict['grade_level'] = classNum
                resultDict['group_2_grade'] = classNum//2
                resultDict['school'] = (1 if classNum<=5 else (2 if classNum<=9 else 3))
                dataFrame = dataFrame.append(resultDict,ignore_index=True)

dataFrame.to_excel(writer,index=False,sheet_name="EachDocument")
writer.close()