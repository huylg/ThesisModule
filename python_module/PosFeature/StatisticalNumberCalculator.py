import pandas as pd
import xlsxwriter

sheet_to_df_map = pd.read_excel('EachDocumentStatisticalNumber.xlsx', sheet_name=None)
outputFile = pd.ExcelWriter('./Pos_StatisticalNumber_2.xlsx', engine='xlsxwriter')


gradeLevelDataFrame = pd.DataFrame()
groupLevelDataFrame = pd.DataFrame()
schoolLevelDataFrame = pd.DataFrame()

postagSet = set(['A','C','N','R','V','E'])

for postag,dataFrame in sheet_to_df_map.items():
    if postag in postagSet:
        dataFrameGroupByGradeLevel = dataFrame.groupby('grade_level').mean().round(decimals=3)
        del dataFrameGroupByGradeLevel['group_2_grade']
        del dataFrameGroupByGradeLevel['school']
        gradeLevelDataFrame = pd.concat([gradeLevelDataFrame,dataFrameGroupByGradeLevel],axis = 1)

        dataFrameGroupByGroupOf2Grade = dataFrame.groupby('group_2_grade').mean().round(decimals=3)
        del dataFrameGroupByGroupOf2Grade['school']
        del dataFrameGroupByGroupOf2Grade['grade_level']   
        groupLevelDataFrame = pd.concat([groupLevelDataFrame,dataFrameGroupByGroupOf2Grade],axis = 1)

        dataFrameGroupBySchool = dataFrame.groupby('school').mean().round(decimals=3)
        del dataFrameGroupBySchool['group_2_grade']
        del dataFrameGroupBySchool['grade_level']
        schoolLevelDataFrame = pd.concat([schoolLevelDataFrame,dataFrameGroupBySchool],axis = 1)

schoolLevelDataFrame.to_excel(outputFile,sheet_name="school",index=True)
gradeLevelDataFrame.to_excel(outputFile,sheet_name='grade',index=True)
groupLevelDataFrame.to_excel(outputFile,sheet_name="group",index=True)

outputFile.close()
