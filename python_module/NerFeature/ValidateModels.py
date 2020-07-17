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

classificatier_estimator_dict = {
    'LogisticRegression': LogisticRegression(random_state=0),
    'KNN': KNeighborsClassifier(),
    'SVC': SVC(random_state=0,kernel='linear'),
    'GaussianNB': GaussianNB(),
    'MultinomialNB': MultinomialNB(),
    'RandomForest': RandomForestClassifier(),
    'DecisionTreeClassifier': DecisionTreeClassifier()
}

xlsxFile = pd.ExcelFile('./EachDocumentStatisticalNumber.xlsx')
dataFrame = pd.read_excel(xlsxFile,sheet_name="EachDocument")
writer = pd.ExcelWriter("model_score.xlsx", engine='xlsxwriter')

excelFileName_to_colIndex_map = {'grade':-3,
'group':-2,
'school':-1}
X_data = dataFrame.loc[:,dataFrame.columns[0:-3]].values.tolist()
print(dataFrame.columns[0:-3])
for sheetName,colIndex in excelFileName_to_colIndex_map.items():
    model_score_df = pd.DataFrame()
    Y_data = dataFrame.loc[:,dataFrame.columns[colIndex]].values.tolist()
    for name,classificater in classificatier_estimator_dict.items():
        model_score_df[name] = cross_val_score(classificater,X_data,Y_data,cv=10,scoring='accuracy')
    model_score_df=model_score_df.append(model_score_df.mean(numeric_only=True, axis=0),ignore_index=True)
    model_score_df.to_excel(writer, sheet_name=sheetName)

xlsxFile.close()
writer.close()