import pandas as pd
import numpy as np
from TextAnalysiser import TextAnalysiser

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

xlsxFile = pd.ExcelFile('./text_analysis_ver2.xlsx')
dataFrame = pd.read_excel(xlsxFile,'text_analysis')

gradeLevelList = dataFrame.loc[:,dataFrame.columns[-3]].to_numpy()
staticalIndexList = dataFrame.loc[:,dataFrame.columns[0:17]].to_numpy()
# lavFomulaResultList = dataFrame.loc[:,dataFrame.columns[-6]].to_numpy()

model = LinearRegression().fit(staticalIndexList,gradeLevelList)

# print(model.predict(staticalIndexList[67].reshape(1,-1)))
# print(gradeLevelList[67])

# rows = len(staticalIndexList)
# result = 0
# for i in range(rows):
#     result += pow(model.predict(staticalIndexList[i].reshape(1,-1))-gradeLevelList[i],2)/rows
#     print(model.predict(staticalIndexList[i].reshape(1,-1)),gradeLevelList[i],lavFomulaResultList[i])
# print(result)
# print(rows)


outputs = model.predict(staticalIndexList)
rsquare=r2_score(gradeLevelList,outputs)
print(rsquare)