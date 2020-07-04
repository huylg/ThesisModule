import pandas as pd
import xlsxwriter

sheet_to_df_map = pd.read_excel('EachDocumentStatisticalNumber.xlsx', sheet_name=None)
gradeLevelExcelwriter = pd.ExcelWriter('./Grade_StatisticalNumber.xlsx', engine='xlsxwriter')
groupLevelExcelwriter = pd.ExcelWriter('./Group2Grade_StatisticalNumber.xlsx', engine='xlsxwriter')
schoolLevelExcelwriter = pd.ExcelWriter('./School_StatisticalNumber.xlsx', engine='xlsxwriter')


for postag,dataFrame in sheet_to_df_map.items():
    dataFrameGroupByGradeLevel = dataFrame.groupby('grade_level').mean()
    del dataFrameGroupByGradeLevel['group_2_grade']
    del dataFrameGroupByGradeLevel['school']
    dataFrameGroupByGradeLevel.to_excel(gradeLevelExcelwriter,sheet_name = postag)

    dataFrameGroupByGroupOf2Grade = dataFrame.groupby('group_2_grade').mean()
    del dataFrameGroupByGroupOf2Grade['school']
    del dataFrameGroupByGroupOf2Grade['grade_level']   
    dataFrameGroupByGroupOf2Grade.to_excel(groupLevelExcelwriter,sheet_name = postag,index=True)


    dataFrameGroupBySchool = dataFrame.groupby('school').mean()
    del dataFrameGroupBySchool['group_2_grade']
    del dataFrameGroupBySchool['grade_level']
    dataFrameGroupBySchool.to_excel(schoolLevelExcelwriter,sheet_name = postag,index=True)


gradeLevelExcelwriter.close()
groupLevelExcelwriter.close()
schoolLevelExcelwriter.close()
