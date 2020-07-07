import pandas as pd

xlsxFile = pd.ExcelFile('./StatisticalNumber.xlsx')
dataFrame = pd.read_excel(xlsxFile,'EachDocument')


writer = pd.ExcelWriter('./ShallowFeatures_StatisticalNumber.xlsx', engine = 'xlsxwriter')

dataFrameGroupByGradeLevel = dataFrame.groupby('grade_level').mean()
del dataFrameGroupByGradeLevel['group_2_grade']
del dataFrameGroupByGradeLevel['school']
dataFrameGroupByGradeLevel.to_excel(writer,sheet_name = 'EachGrade',index=True)

dataFrameGroupByGroupOf2Grade = dataFrame.groupby('group_2_grade').mean()
del dataFrameGroupByGroupOf2Grade['school']
del dataFrameGroupByGroupOf2Grade['grade_level']
dataFrameGroupByGroupOf2Grade.to_excel(writer,sheet_name = 'GroubOf2Grade',index=True)

dataFrameGroupBySchool = dataFrame.groupby('school').mean()
del dataFrameGroupBySchool['group_2_grade']
del dataFrameGroupBySchool['grade_level']
dataFrameGroupBySchool.to_excel(writer,sheet_name = 'School',index=True)


writer.save()
xlsxFile.close()