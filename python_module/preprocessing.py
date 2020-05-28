from TextAnalysiser import TextAnalysiser
import xlsxwriter

import os
rootdir = './Thesis_Dataset/send/or - without note/'
textAnalysiser = TextAnalysiser()
outputJson = []
# write to excel file
workbook = xlsxwriter.Workbook('text_analysis_ver2.xlsx')
worksheet = workbook.add_worksheet()

row = 1
col = 0
classlist = list(map(int,filter(lambda dir: not dir.startswith('.'),os.listdir(rootdir))))
for classNum in classlist:
    classDir = rootdir + '{}/'.format(classNum)
    amountOfFile = 0
    for root,subdirs,files  in os.walk(classDir):
        amountOfFile += len(files)
        for file in files:
            if( not file.startswith('.')):
                print(root + '/' + file)
                inputFile = open(root + '/' + file,mode='r',encoding='utf-8')
                inputText = inputFile.read()
                inputFile.close()
                output = textAnalysiser.analysis(inputText)
                output['grade_level'] = classNum
                output['name_document'] =  file
                for key,val in output.items():
                    worksheet.write(row,col,val)
                    col+=1
                row+=1
                col=0

workbook.close()

