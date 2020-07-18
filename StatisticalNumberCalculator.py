import pandas as pd
import xlsxwriter

dataFrame = pd.read_excel('EachDocumentStatisticalNumber.xlsx', sheet_name='EachDocument')

writer = pd.ExcelWriter('./StatisticalNumber.xlsx', engine='xlsxwriter')

dataFrameGroupByGradeLevel = dataFrame.groupby('grade_level').mean()
del dataFrameGroupByGradeLevel['group_2_grade']
del dataFrameGroupByGradeLevel['school']
dataFrameGroupByGradeLevel.tranpose().to_excel(writer,sheet_name = "grade",index=True)

dataFrameGroupByGroupOf2Grade = dataFrame.groupby('group_2_grade').mean()
del dataFrameGroupByGroupOf2Grade['school']
del dataFrameGroupByGroupOf2Grade['grade_level']   
dataFrameGroupByGroupOf2Grade.tranpose().to_excel(writer,sheet_name = "group",index=True)

dataFrameGroupBySchool = dataFrame.groupby('school').mean()
del dataFrameGroupBySchool['group_2_grade']
del dataFrameGroupBySchool['grade_level']
dataFrameGroupBySchool.tranpose().to_excel(writer,sheet_name = "school",index=True)

writer.close()