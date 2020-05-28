import json
import os
import numpy as np
from sklearn.model_selection import train_test_split

rootdir = './Thesis_Dataset/send/or - without note/'
classlist = list(map(int,filter(lambda dir: not dir.startswith('.'),os.listdir(rootdir))))

y = []
x = [] 

for classNum in classlist:
    classDir = rootdir + '{}/'.format(classNum)
    for root,subdirs,files  in os.walk(classDir):
        for file in files:
            if( not file.startswith('.')):
                print(root + '/' + file)
                inputFile = open(root + '/' + file,mode='r',encoding='utf-8')
                inputText = inputFile.read()
                inputFile.close()     
                y.append(classNum)
                x.append(inputText)


#split dataset

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)

testFile = open('readability_test.json','w')
trainFile = open('readability_train.json','w')


train_dict = [{'grade_level': i, 'content': j} for i, j in zip(y_train, x_train)]

test_dict = [{'grade_level': i, 'content': j} for i, j in zip(y_test, x_test)]

json.dump(train_dict,trainFile)
json.dump(test_dict,testFile)

testFile.close()
trainFile.close()


