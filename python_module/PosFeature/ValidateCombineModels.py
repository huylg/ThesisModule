import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import cross_val_score
from collections import Counter

import xlsxwriter

sheet_to_df_map = pd.read_excel('EachDocumentStatisticalNumber.xlsx', sheet_name=None)
outputFile = pd.ExcelWriter('./validate_result_combine.xlsx', engine='xlsxwriter')


gradeLevelDataFrame = pd.DataFrame()
groupLevelDataFrame = pd.DataFrame()
schoolLevelDataFrame = pd.DataFrame()

postagSet = set(['A','C','N','R','V','E'])

classificatier_estimator_dict = {
    'LogisticRegression': LogisticRegression(random_state=0),
    'KNN': KNeighborsClassifier(),
    'SVC': SVC(random_state=0,kernel='linear'),
    'GaussianNB': GaussianNB(),
    'MultinomialNB': MultinomialNB(),
    'RandomForest': RandomForestClassifier(),
    'DecisionTreeClassifier': DecisionTreeClassifier()
}

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

for name,estimator in classificatier_estimator_dict.items():
    

# schoolLevelDataFrame.transpose().to_excel(outputFile,sheet_name="school",index=True)
# gradeLevelDataFrame.transpose().to_excel(outputFile,sheet_name='grade',index=True)
# groupLevelDataFrame.transpose().to_excel(outputFile,sheet_name="group",index=True)

outputFile.close()
