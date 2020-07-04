from TextAnalysiser import TextAnalysiser
import xlsxwriter

import os
rootdir = './Dataset/send/or - without note/'
textAnalysiser = TextAnalysiser()
outputJson = []
# write to excel file
workbook = xlsxwriter.Workbook('StatisticalNumber.xlsx')
worksheet = workbook.add_worksheet('EachDocument')

columnNameList = ["number_of_sentence",	"number_of_word",	"number_of_distinct_word",
	"number_of_syllable","number_of_distinct_syllable",	"number_of_character",
    	"number_of_proper_noun","number_of_distinct_proper_noun","aslw","asls",	"aslc",	"awls",
        	"awlc",	"pds",	"pdw",	"psvw",	"pdiadw",	"LAVFomula",
            "NH1982"	,"NH1985"	,"grade_level",	"document_name", "group_2_grade","school"]

for i in range(len(columnNameList)):
    worksheet.write(0,i,columnNameList[i])

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
                output['group_2_grade'] = classNum//2
                output['school'] = (1 if classNum<=5 else (2 if classNum<=9 else 3))
                for key,val in output.items():
                    worksheet.write(row,col,val)
                    col+=1
                row+=1
                col=0

workbook.close()

