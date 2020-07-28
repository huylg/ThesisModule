import underthesea
import numpy as np
import os
import pandas as pd
import xlsxwriter

rootdir = '../Dataset/send/or - without note/'
writer = pd.ExcelWriter('./EachDocumentStatisticalNumber.xlsx', engine='xlsxwriter')

classlist = list(map(int,filter(lambda dir: not dir.startswith('.'),os.listdir(rootdir))))

dataFrameDict = {}

for classNum in classlist:
    classDir = rootdir + '{}/'.format(classNum)

    for root,subdirs,files  in os.walk(classDir):
         for file in files:
            if( not file.startswith('.')):
                print(root+'/'+file)
                inputFile = open(root + '/' + file,mode='r',encoding='utf-8')   
                inputText = inputFile.read()
                inputFile.close()

                chunkWord = underthesea.chunk(inputText)
                for word,posTag,chunkTag in chunkWord:
                    print(chunkTag)

