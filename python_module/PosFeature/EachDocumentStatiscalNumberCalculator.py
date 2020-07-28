from vncorenlp import VnCoreNLP
import numpy as np
import os
import pandas as pd
import xlsxwriter

jarFullPath = os.path.abspath("../VnCoreNLP/VnCoreNLP-1.1.1.jar")
annotator = VnCoreNLP(jarFullPath, annotators="wseg,pos", max_heap_size='-Xmx2g') 

rootdir = '../Dataset/send/or - without note/'
writer = pd.ExcelWriter('./combine_EachDocumentStatisticalNumber.xlsx', engine='xlsxwriter')

classlist = list(map(int,filter(lambda dir: not dir.startswith('.'),os.listdir(rootdir))))

dataFrame = pd.DataFrame()
postagSet = set(['A','C','N','R','V','E'])

for classNum in classlist:
    classDir = rootdir + '{}/'.format(classNum)

    for root,subdirs,files  in os.walk(classDir):
         for file in files:
            if( not file.startswith('.')):
                print(root + '/' + file)
                documentPostagWordList = {}
                wordlistInDocument = []
                inputFile = open(root + '/' + file,mode='r',encoding='utf-8')   
                inputText = inputFile.read()
                sentenceList = annotator.pos_tag(inputText)
                noOfSentenceInDocument = 0
                for sentence in sentenceList:
                    for (word,postag) in sentence:
                        documentPostagWordList[postag] = documentPostagWordList[postag] + [word] if postag in documentPostagWordList  else []
                        wordlistInDocument.append(word)
                    noOfSentenceInDocument+=1
                        
                for postag in documentPostagWordList.keys():
                    if 'N' in postag and postag != 'N':
                        documentPostagWordList['N']+=documentPostagWordList[postag]
                    if 'V' in postag and postag != 'V':
                        documentPostagWordList['V']+=documentPostagWordList[postag]
                        
                noOfWordInDocument = len(wordlistInDocument)
                noOfUniqueWordInDocument = len(set(wordlistInDocument))
                resultDict = {}

                for postag,wordList in documentPostagWordList.items():
                    if not postag in postagSet:
                        continue
                    noOfWordWithPostag = len(wordList)
                    noOfUniqueWordWithPostag = len(set(wordList))
                    resultDict['no_{}'.format(postag)] = noOfWordWithPostag
                    resultDict['per_of_{}'.format(postag)] = noOfWordWithPostag/noOfWordInDocument * 100
                    resultDict['per_of_unique_{}_per_document'.format(postag)] = noOfUniqueWordWithPostag/noOfWordInDocument * 100
                    resultDict['ratio_unique_{}_pet_totel_unique_word'.format(postag)] = noOfUniqueWordWithPostag/noOfUniqueWordInDocument
                    resultDict['avg_{}_in_sentence'.format(postag)] = noOfWordWithPostag/noOfSentenceInDocument
                    resultDict['avg_unique_{}_in_sentence'.format(postag)] = noOfUniqueWordWithPostag/noOfSentenceInDocument
                    resultDict['grade_level'] = classNum
                    resultDict['group_2_grade'] = classNum//2
                    resultDict['school'] = (1 if classNum<=5 else (2 if classNum<=9 else 3))
                dataFrame = dataFrame.append(resultDict,ignore_index=True)
dataFrame.fillna(0, inplace=True)
dataFrame.to_excel(writer,sheet_name='EachDocument',index=False)
writer.close()


