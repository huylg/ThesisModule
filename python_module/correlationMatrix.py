import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

features = ['Shallow','Ner','Pos']

for feature in features:

    data = pd.read_excel("{}_StatisticalFile.xlsx".format(feature))

    corrmat = data.corr()
    top_corr_features = corrmat.index
    plt.figure(figsize=(20,20))
    #plot heat map
    g=sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")
    plt.savefig("{}_correlation.png".format(feature))
