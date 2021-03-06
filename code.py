#Arabic Sentiment Analysis using Twitter Data Set

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

from os import listdir
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import NearestCentroid

path='/kaggle/input/'
neg_path = path + 'twitter/Negative/Negative/'
pos_path = path + 'twitter/Positive/Positive/'
neg_names = listdir(neg_path)
pos_names = listdir(pos_path)
neg_data=[]
for i in range(len(neg_names)):
    with open(neg_path+neg_names[i], 'r', encoding = "ISO-8859-1") as myfile:
        neg_data.append(myfile.read().replace('\n', ''))
pos_data=[]
for i in range(len(pos_names)):
    with open(pos_path+pos_names[i], 'r', encoding = "ISO-8859-1") as myfile:
        pos_data.append(myfile.read().replace('\n', ''))
data=pos_data+neg_data
labels = np.zeros(2000);
labels[0:1000]=0;
labels[1000:2000]=1;

#model setting
kf = StratifiedKFold(n_splits=5)
i_count = 1

avg_f1_DT=0
avg_f1_RF=0
avg_f1_NCC=0
avg_f1_L1SVM=0
avg_f1_L2SVM=0


#5 Models
DT=tree.DecisionTreeClassifier()
RF=RandomForestClassifier(n_estimators=10)
NCC=NearestCentroid()
L1SVC = LinearSVC(loss = 'squared_hinge', penalty = 'l1', dual = False)
L2SVC = LinearSVC(loss = 'squared_hinge', penalty = 'l2', dual = False)

for train_index, test_index in kf.split(data, labels):
    #train data and test data
    X_train = [data[i] for i in train_index]
    X_test = [data[i] for i in test_index]
    y_train, y_test = labels[train_index], labels[test_index]
    vectorizer = TfidfVectorizer(min_df=5, max_df = 0.8, sublinear_tf=True, use_idf=True,stop_words='english')
    train_corpus_tf_idf = vectorizer.fit_transform(X_train)
    test_corpus_tf_idf = vectorizer.transform(X_test)
    
    print('\n=====The No.'+str(i_count)+' round of CV')
    
    #decision tree
    DT.fit(train_corpus_tf_idf, y_train)
    pred = DT.predict(test_corpus_tf_idf)
    score = metrics.f1_score(y_test, pred, average='macro')
    avg_f1_DT = avg_f1_DT + score
    print('decision tree:\nThe confusion matrix:')
    print(confusion_matrix(y_test, pred))
    print('The F-1 Score: '+str(score))
    
    #random forest
    RF.fit(train_corpus_tf_idf, y_train)
    pred = RF.predict(test_corpus_tf_idf)
    score = metrics.f1_score(y_test, pred, average='macro')
    avg_f1_RF = avg_f1_RF + score
    print('random forest:\nThe confusion matrix:')
    print(confusion_matrix(y_test, pred))
    print('The F-1 Score: '+str(score))
    
    #Nearest Centroid Classifier
    NCC.fit(train_corpus_tf_idf, y_train)
    pred = NCC.predict(test_corpus_tf_idf)
    score = metrics.f1_score(y_test, pred, average='macro')
    avg_f1_NCC = avg_f1_NCC + score
    print('Nearest Centroid Classifier:\nThe confusion matrix:')
    print(confusion_matrix(y_test, pred))
    print('The F-1 Score: '+str(score))
    
    #L1SVC
    L1SVC.fit(train_corpus_tf_idf, y_train)
    pred = L1SVC.predict(test_corpus_tf_idf)
    score = metrics.f1_score(y_test, pred, average='macro')
    avg_f1_L1SVM = avg_f1_L1SVM + score
    print('L1SVM:\nThe confusion matrix:')
    print(confusion_matrix(y_test, pred))
    print('The F-1 Score: '+str(score))
    
    #L2SVC
    L2SVC.fit(train_corpus_tf_idf, y_train)
    pred = L2SVC.predict(test_corpus_tf_idf)
    score = metrics.f1_score(y_test, pred, average='macro')
    avg_f1_L2SVM = avg_f1_L2SVM + score
    print('L2SVM:\nThe confusion matrix:')
    print(confusion_matrix(y_test, pred))
    print('The F-1 Score: '+str(score))
    
    
    i_count+=1
print("\n=====The Average F1 Score for DT is: "+str(avg_f1_DT/5)+"========")
print("\n=====The Average F1 Score for RF is: "+str(avg_f1_RF/5)+"========")
print("\n=====The Average F1 Score for NCC is: "+str(avg_f1_NCC/5)+"========")
print("\n=====The Average F1 Score for L1SVC is: "+str(avg_f1_L1SVM/5)+"========")
print("\n=====The Average F1 Score for L2SVC is: "+str(avg_f1_L2SVM/5)+"========")

print("\n=====L2SVC has the best performance=====")

fulldata_corpus_tf_idf = vectorizer.fit_transform(data)
L2SVC.fit(fulldata_corpus_tf_idf, labels)

