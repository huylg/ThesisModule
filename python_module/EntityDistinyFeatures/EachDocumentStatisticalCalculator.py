from vncorenlp import VnCoreNLP
import numpy as np
import os
import pandas as pd
import xlsxwriter
jarFullPath = os.path.abspath("../VnCoreNLP/VnCoreNLP-1.1.1.jar")
annotator = VnCoreNLP(jarFullPath, annotators="wseg,pos,ner", max_heap_size='-Xmx2g') 

rootdir = '../Dataset/send/or - without note/'
writer = pd.ExcelWriter('./EachDocumentStatisticalNumber.xlsx', engine='xlsxwriter')


classlist = list(map(int,filter(lambda dir: not dir.startswith('.'),os.listdir(rootdir))))
dataFrame = pd.DataFrame()

for classNum in classlist:
    classDir = rootdir + '{}/'.format(classNum)

    for root,subdirs,files  in os.walk(classDir):
         for file in files:
            if( not file.startswith('.')):
                print(root + '/' + file)
                inputFile = open(root + '/' + file,mode='r',encoding='utf-8')   
                inputText = inputFile.read()
                annotateResult = annotator.annotate(inputText)
                entityList = []
                namedEntityList = []
                sentenceList = annotateResult['sentences']
                wordList = []
                for senetnce in sentenceList:
                    for word in senetnce:
                        wordList.append(word['form'])
                        #check noun pharse
                        if 'N' in word['posTag']:
                            entityList.append(word['form'])
                            if word['nerLabel'] != 'O':
                                namedEntityList.append(word['form'])
                resultDict = {}

                amountEntity = len(entityList)
                amountUniqueEntity = len(set(entityList))
                amountNamedEntity = len(namedEntityList)
                amountUniqueNamedEntity = len(set(namedEntityList))
                amountSentence = len(sentenceList)
                amountWord = len(word)

                resultDict['avg_amount_entity_per_sen'] = amountEntity/amountSentence
                resultDict['avg_amount_entity_per_doc'] = amountEntity
                resultDict['avg_amount_unique_entity_per_sen'] = amountUniqueEntity/amountSentence
                resultDict['avg_amount_unique_entity_per_doc'] = amountUniqueEntity
                resultDict['avg_amount_named_entity_per_sen'] = amountNamedEntity/amountSentence
                resultDict['avg_amount_named_entity_per_doc'] = amountNamedEntity
                resultDict['avg_amount_unique_named_entity_per_sen'] = amountUniqueNamedEntity/amountSentence
                resultDict['avg_amount_unique_named_entity_per_doc'] = amountUniqueNamedEntity
                resultDict['avg_amount_entity_per_sen'] = amountEntity/amountSentence
                resultDict['avg_amount_entity_per_doc'] = amountEntity
                resultDict['per_NameEntity_word'] = amountNamedEntity/amountWord
                resultDict['per_uniqueNameEntity_word'] = (amountNamedEntity/amountWord)/amountSentence
                resultDict['per_NameEntity_entity'] = amountNamedEntity/amountEntity
                resultDict['per_uniqueNameEntity_entity'] = amountUniqueNamedEntity/amountUniqueEntity
                resultDict['grade_level'] = classNum
                resultDict['group_2_grade'] = classNum//2
                resultDict['school'] = (1 if classNum<=5 else (2 if classNum<=9 else 3))
                dataFrame = dataFrame.append(resultDict,ignore_index=True)

dataFrame.to_excel(writer,sheet_name='EachDocument',index=False)
writer.close()

