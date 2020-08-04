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
xlsxFile = pd.ExcelFile('./combine_EachDocumentStatisticalNumber.xlsx')
dataFrame = pd.read_excel(xlsxFile,sheet_name="EachDocument")
outputFile = pd.ExcelWriter('./validate_result_combine.xlsx', engine='xlsxwriter')


classificatier_estimator_dict = {
    'LogisticRegression': LogisticRegression(random_state=0),
    'KNN': KNeighborsClassifier(),
    'SVC': SVC(random_state=0,kernel='linear'),
    'GaussianNB': GaussianNB(),
    'MultinomialNB': MultinomialNB(),
    'RandomForest': RandomForestClassifier(),
    'DecisionTreeClassifier': DecisionTreeClassifier()
}


labelList = ['school','group_2_grade','grade_level']

for label in labelList:
    x_dataFrame = dataFrame.copy(deep=False)

    for label_2 in labelList:
        del x_dataFrame[label_2]
    x_data = x_dataFrame.values.tolist()
    y_data = dataFrame[label].values.tolist()
    model_score_df = pd.DataFrame()

    for name,classificater in classificatier_estimator_dict.items():
        model_score_df[name] = cross_val_score(classificater,x_data,y_data,cv=10,scoring='accuracy')
    model_score_df=model_score_df.append(model_score_df.mean(numeric_only=True, axis=0),ignore_index=True)
    model_score_df.to_excel(outputFile, sheet_name=label)


outputFile.close()
