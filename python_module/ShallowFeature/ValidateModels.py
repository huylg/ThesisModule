import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import pickle
from TextAnalysiser import TextAnalysiser
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC,LinearSVC,NuSVC
from sklearn.naive_bayes import GaussianNB,MultinomialNB,ComplementNB,BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from collections import Counter

import xlsxwriter



classificatier_estimator_dict = {
    'SVC': SVC(random_state=0,kernel='linear'),
    # 'NuSVC': NuSVC(random_state=0),
    'LinearSVC': LinearSVC(random_state=0),
    'GaussianNB': GaussianNB(),
    'MultinomialNB': MultinomialNB(),
    'ComplementNB': ComplementNB(),
    'BernoulliNB': BernoulliNB(),
    'DecisionTreeClassifier': DecisionTreeClassifier(),
}

xlsxFile = pd.ExcelFile('./validation_result/StatisticalNumber.xlsx')
dataFrame = pd.read_excel(xlsxFile,'EachDocument')

X_data = dataFrame.loc[:,dataFrame.columns[0:17]].values.tolist()
sheetNameList = {}
sheetNameList['EachGrade'] = dataFrame.loc[:,dataFrame.columns[-4]].values.tolist()
sheetNameList['EachGroupOf2Grade']= dataFrame.loc[:,dataFrame.columns[-2]].values.tolist()
sheetNameList['EachSchool'] = dataFrame.loc[:,dataFrame.columns[-1]].values.tolist()

writer = pd.ExcelWriter('./models_score.xlsx', engine='xlsxwriter')

for sheetName,Y_data in sheetNameList.items():
    model_score_df = pd.DataFrame()
    for name,estimator in classificatier_estimator_dict.items():
        model_score_df[name] = cross_val_score(estimator,X_data,Y_data,cv=10,scoring='accuracy')
    model_score_df.to_excel(writer, sheet_name=sheetName, index=True)

writer.save()

xlsxFile.close()
writer.close() 
