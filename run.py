import csv
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
import random
from sklearn.ensemble import RandomForestClassifier

train_data=np.loadtxt("newtrain.csv",delimiter=",",dtype="string",usecols=(2,3,4,5,6,7,8,9,10,11,12))
train_label=np.loadtxt("newtrain.csv",delimiter=",",dtype="float",usecols=(13,))
test_data=np.loadtxt("newtest.csv",delimiter=",",dtype="string",usecols=(2,3,4,5,6,7,8,9,10,11,12))

num=4
selector=SelectKBest(f_classif,k=num).fit(train_data,train_label)
feature_select=selector.get_support(indices=True)
train_new=selector.transform(train_data)

test_new=test_data[:,feature_select[0]]
for i in range(num-1):
    temp=test_data[:,feature_select[i+1]]
    test_new=np.column_stack((test_new,temp))

sample=train_data.shape[0]/3
arange=np.arange(train_data.shape[0]);
train_sample=random.sample(arange,sample)
train_tr_data=np.delete(train_new,train_sample,0)
train_tr_label=np.delete(train_label,train_sample)
train_ts_data=train_new[train_sample]
train_ts_label=train_label[train_sample]
clf=RandomForestClassifier()
clf.fit(train_tr_data,train_tr_label)
train_result=clf.predict_proba(train_ts_data)
score=clf.score(train_ts_data,train_ts_label)
print score
clf.fit(train_new,train_label)
result=clf.predict_proba(test_new)
test_label=result[:,1]

csvfile_test=file('test_label.csv','rb')
reader_test=csv.reader(csvfile_test)

i=0
test_pairs=[]
for line in reader_test:
    if i==0:
        i+=1
    else:
        test_pairs.append(line[0])

test_pairs=np.array(test_pairs)
csvfile = file('submission.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['user_id#merchant_id','prob'])
data=np.column_stack((test_pairs,test_label))
data=np.ndarray.tolist(data)
writer.writerows(data)
csvfile_test.close()
csvfile.close()




