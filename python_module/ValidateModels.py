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
from sklearn.model_selection import train_test_split
from collections import Counter

import xlsxwriter

estimator_dict = {
    'SVC': SVC(random_state=0),
    # 'NuSVC': NuSVC(random_state=0),
    'LinearSVC': LinearSVC(random_state=0),
    'GaussianNB': GaussianNB(),
    'MultinomialNB': MultinomialNB(),
    'ComplementNB': ComplementNB(),
    'BernoulliNB': BernoulliNB(),
    'DecisionTreeClassifier': DecisionTreeClassifier()
}

xlsxFile = pd.ExcelFile('./text_analysis_ver2.xlsx')
dataFrame = pd.read_excel(xlsxFile,'text_analysis')

Y_data = dataFrame.loc[:,dataFrame.columns[-1]].values.tolist()
X_data = dataFrame.loc[:,dataFrame.columns[0:17]].values.tolist()

writer = pd.ExcelWriter('./models_score_grade_6.xlsx', engine='xlsxwriter')

for name,estimator in estimator_dict.items():
    model_score_df = pd.DataFrame()
    for step in range(0,10):
        X_train,X_test,Y_train,Y_test = train_test_split(X_data,Y_data,test_size = 0.3)

        est = estimator

        est.fit(X_train,Y_train)

        Y_Predict = est.predict(X_test)
        #save model score to excel
        model_score_dict = {'accurary':accuracy_score(Y_test,Y_Predict).item()}
        model_score_df=model_score_df.append(model_score_dict,ignore_index=True)
    
        #save estimator as a pickle file
        # outfile = open("trainned_models/{}_{}.pickle".format(name,step), 'wb')
        # fastPickler = pickle.Pickler(outfile, pickle.HIGHEST_PROTOCOL)
        # fastPickler.fast = 1
        # fastPickler.dump(est)
        # outfile.close()

    model_score_df.to_excel(writer, sheet_name=name, index=True)

writer.save()

xlsxFile.close()
writer.close()