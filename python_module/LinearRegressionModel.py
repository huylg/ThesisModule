import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

xlsxFile = pd.ExcelFile('./text_analysis_document.xlsx')
dataFrame = pd.read_excel(xlsxFile,'Sheet0')

gradeLevelList = dataFrame.loc[:,dataFrame.columns[-2]].to_numpy()
print(dataFrame.columns[-2])
staticalIndexList = dataFrame.loc[:,dataFrame.columns[0:17]].to_numpy()

model = LinearRegression().fit(staticalIndexList,gradeLevelList)
print(model.coef_)