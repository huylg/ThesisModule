from TextAnalysiser import TextAnalysiser
import pandas as pd
import numpy as np
import xlsxwriter

import os
rootdir = './Dataset/send/or - without note/'
textAnalysiser = TextAnalysiser()

featuresExcelFileDict = {
    'Shallow' : pd.ExcelWriter('Shallow_StatisticalFile.xlsx', engine = 'xlsxwriter'),
    'Pos' : pd.ExcelWriter('Pos_StatisticalFile.xlsx', engine = 'xlsxwriter'),
    'Ner' : pd.ExcelWriter('Ner_StatisticalFile.xlsx', engine = 'xlsxwriter')   
}
featureDataFrameDict = {
    'Shallow' : pd.DataFrame(),
    'Pos' : pd.DataFrame(),
    'Ner' : pd.DataFrame()
}
classlist = list(map(int,filter(lambda dir: not dir.startswith('.'),os.listdir(rootdir))))
for classNum in classlist:
    classDir = rootdir + '{}/'.format(classNum)
    for root,subdirs,files  in os.walk(classDir):
        for file in files:
            if( not file.startswith('.')):
                print(root + '/' + file)
                inputFile = open(root + '/' + file,mode='r',encoding='utf-8')   
                inputText = inputFile.read()
                inputFile.close()
                analysisResult = textAnalysiser.analysis(inputText)

                for feature, data in analysisResult.items():
                    data['grade'] = classNum
                    featureDataFrameDict[feature] = featureDataFrameDict[feature].append(data,ignore_index=True)

for feature, dataFrame in featureDataFrameDict.items():
    dataFrame.to_excel(featuresExcelFileDict[feature],sheet_name='EachDocument',index=False)
    featuresExcelFileDict[feature].close()
                

               



