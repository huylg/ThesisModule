from TextAnalysiser import TextAnalysiser
import xlsxwriter

import os
rootdir = './Thesis_Dataset/send/or - without note/'
textAnalysiser = TextAnalysiser()
classlist = list(map(int,filter(lambda dir: not dir.startswith('.'),os.listdir(rootdir))))
outputClass = {}
for classNum in classlist:
    classDir = rootdir + '{}/'.format(classNum)
    outputJson = []
    amountOfFile = 0
    for root,subdirs,files  in os.walk(classDir):
        amountOfFile += len(files)
        for file in files:
            if( not file.startswith('.')):
                print(root + '/' + file)
                inputFile = open(root + '/' + file,mode='r',encoding='utf-8')
                inputText = inputFile.read()
                inputFile.close()
                outputJson.append(textAnalysiser.analysis(inputText))
    
    output = {
        'number_of_sentence':0,
        'number_of_word' : 0,
        'number_of_distinct_word': 0,
        'number_of_syllable':0,
        'number_of_distinct_syllable':0,
        'number_of_character':0,
        'number_of_proper_noun':0,
        'number_of_distinct_proper_noun':0,
        'aslw':0,
        'asls':0,
        'aslc':0,
        'awls':0,
        'awlc':0,
        'pds':0,
        'pdw':0,
        'psvw':0,
        'pdiadw':0,
        'LAVFomula' : 0,
        'NH1982' : 0,
        'NH1985': 0
    }

    jsonCount = len(outputJson)
    for json in outputJson:
        for key in output.keys():
            output[key] += json[key]/jsonCount
    output['numberOfDocument'] = amountOfFile

    outputClass[classNum] = output

# write to excel file
workbook = xlsxwriter.Workbook('text_analysis.xlsx')
worksheet = workbook.add_worksheet()
row = 0 
col = 0
for jsonKey,jsonValue in outputClass.items():
    worksheet.write(row, col, jsonKey)
    row+=1
    for key,val in jsonValue.items():
        worksheet.write(row,col,key)
        worksheet.write(row,col+1,val)
        row+=1
    row+=1

workbook.close()

print(outputClass)