import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

xlsxFile = pd.ExcelFile('./text_analysis_transpose.xlsx')
dataFrame = pd.read_excel(xlsxFile,'Sheet1')

gradeLevelList = dataFrame.loc[:,dataFrame.columns[-1]].to_numpy()
staticalIndexList = dataFrame.loc[:,dataFrame.columns[0:17]].to_numpy()

model = LinearRegression().fit(staticalIndexList,gradeLevelList)
print(model)