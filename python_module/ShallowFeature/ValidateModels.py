import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import pickle
from TextAnalysiser import TextAnalysiser
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

xlsxFile = pd.ExcelFile('./selectionFetures.xlsx')
dataFrame = pd.read_excel(xlsxFile,'Sheet1')

# columnNameList = ['number_of_sentence','number_of_character','number_of_distinct_word','psvw','aslw','number_of_distinct_proper_noun']

X_data = dataFrame.loc[:,dataFrame.columns[1:]].values.tolist()


sheetNameList = {}
sheetNameList['EachSchool'] = dataFrame.loc[:,dataFrame.columns[0]].values.tolist()

writer = pd.ExcelWriter('./choose_features_models_score.xlsx', engine='xlsxwriter')

for sheetName,Y_data in sheetNameList.items():
    model_score_df = pd.DataFrame()
    for name,estimator in classificatier_estimator_dict.items():
        model_score_df[name] = cross_val_score(estimator,X_data,Y_data,cv=10,scoring='accuracy')

    model_score_df=model_score_df.append(model_score_df.mean(numeric_only=True, axis=0),ignore_index=True)
    model_score_df.to_excel(writer, sheet_name=sheetName, index=False)

writer.save()
xlsxFile.close()
writer.close() 
