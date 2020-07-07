import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import pickle
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

xlsxFile = pd.ExcelFile('./EachDocumentStatisticalNumber.xlsx')
postag_to_df_map = pd.read_excel(xlsxFile,sheet_name=None)

excelFileName_to_colIndex_map = {'./grade_models_score.xlsx':2,
'./group2grade_models_score.xlsx':3,
'./school_models_score.xlsx':-1}
for excelFileName,colIndex in excelFileName_to_colIndex_map.items():
    writer = pd.ExcelWriter(excelFileName, engine='xlsxwriter')

    for postag,dataFrame in postag_to_df_map.items():
        if len(dataFrame.index)<50:
            continue
        X_data = dataFrame.loc[:,np.concatenate([dataFrame.columns[0:2],dataFrame.columns[4:8]])].values.tolist()
        print(X_data)
        Y_data = dataFrame.loc[:,dataFrame.columns[colIndex]].values.tolist()
        model_score_df = pd.DataFrame()
        for name,estimator in classificatier_estimator_dict.items():
            model_score_df[name] = cross_val_score(estimator,X_data,Y_data,cv=10,scoring='accuracy')
        model_score_df.to_excel(writer, sheet_name=postag, index=True)

    writer.save()
    writer.close() 
xlsxFile.close()
