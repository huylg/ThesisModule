# New Section
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import pickle
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

import xlsxwriter

classificatier_estimator_dict = {
    'LogisticRegression': LogisticRegression(random_state=0),
    'KNN': KNeighborsClassifier(),
    'SVC': SVC(random_state=0,kernel='linear'),
    'GaussianNB': GaussianNB(),
    'MultinomialNB': MultinomialNB(),
    'RandomForest': RandomForestClassifier(),
    'DecisionTreeClassifier': DecisionTreeClassifier()
}

xlsxFile = pd.ExcelFile('./Shallow_StatisticalFile.xlsx')
dataFrame = pd.read_excel(xlsxFile,'EachDocument')


print(dataFrame.columns[0])

sheetNameList = {}
sheetNameList['EachGrade'] = dataFrame['grade'].values.tolist()
sheetNameList['EachGroupOf2Grade']= [num//2 for num in sheetNameList['EachGrade']]
sheetNameList['EachSchool'] = [1 if num <= 5 else (2 if num<=9 else 3) for num in sheetNameList['EachGrade']]

del dataFrame['grade']
X_data = dataFrame.loc[:,dataFrame.columns[1:]].values.tolist()

writer = pd.ExcelWriter('./Shallow_models_score.xlsx', engine='xlsxwriter')

for sheetName,Y_data in sheetNameList.items():
    model_score_df = pd.DataFrame()
    for name,estimator in classificatier_estimator_dict.items():
        model_score_df[name] = cross_val_score(estimator,X_data,Y_data,cv=10,scoring='accuracy')

    model_score_df=model_score_df.append(model_score_df.mean(numeric_only=True, axis=0),ignore_index=True)
    model_score_df.to_excel(writer, sheet_name=sheetName, index=False)

writer.save()
xlsxFile.close()
writer.close() 