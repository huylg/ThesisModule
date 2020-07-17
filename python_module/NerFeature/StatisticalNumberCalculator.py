import pandas as pd
import xlsxwriter

dataFrame = pd.read_excel('EachDocumentStatisticalNumber.xlsx', sheet_name="EachDocument")
outputFile = pd.ExcelWriter('./StatisticalNumber.xlsx', engine='xlsxwriter')


gradeLevelDataFrame = dataFrame.groupby('grade_level').mean().round(decimals=3)
del gradeLevelDataFrame['group_2_grade']
del gradeLevelDataFrame['school']

groupLevelDataFrame = dataFrame.groupby('group_2_grade').mean().round(decimals=3)
del groupLevelDataFrame['school']
del groupLevelDataFrame['grade_level']   

schoolLevelDataFrame = dataFrame.groupby('school').mean().round(decimals=3)
del schoolLevelDataFrame['group_2_grade']
del schoolLevelDataFrame['grade_level']

schoolLevelDataFrame.transpose().to_excel(outputFile,sheet_name="school",index=True)
gradeLevelDataFrame.transpose().to_excel(outputFile,sheet_name='grade',index=True)
groupLevelDataFrame.transpose().to_excel(outputFile,sheet_name="group",index=True)

outputFile.close()