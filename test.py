import csv
import numpy as np

csvfile_test=file('test_label.csv','rb')
reader_test=csv.reader(csvfile_test)
csvfile_log=file('user_log.csv','rb')
reader_log=csv.reader(csvfile_log)

i=0
test_label=[]
test_user_label=[]
test_merchant_label=[]

user_log_id=[]
merchant_id=[]
item_id=[]
cat_id=[]
brand_id=[]
time_stamp=[]
action_type=[]

for line in reader_test:
    if i==0:
        i+=1
    else:
        test_label.append(line[0])
for i in range(len(test_label)):
    test_user_label.append(test_label[i].split('#')[0])
    test_merchant_label.append(test_label[i].split('#')[1])
test_label=np.array(test_label)
test_user_label=np.array(test_user_label)
test_merchant_label=np.array(test_merchant_label)
same_cat=np.zeros(test_label.shape[0])
same_cat=same_cat.astype(str)
times_cat=np.zeros(test_label.shape[0])
buy_before=np.zeros(test_label.shape[0])
buy_before=buy_before.astype(str)
times=np.zeros(test_label.shape[0])
merchant_s_item=np.zeros(test_label.shape[0])
merchant_s_item=merchant_s_item.astype(str)
test_data=np.column_stack((test_user_label,test_merchant_label))
test_add=np.zeros([test_label.shape[0],4])
test_add=test_add.astype(str)
test_info=np.zeros([test_label.shape[0],2])
test_info=test_info.astype(str)

i=0
for line in reader_log:
    if i==0:
        i+=1
    else:
        if(line[6]!='0'):
           user_log_id.append(line[0])
           item_id.append(line[1])
           cat_id.append(line[2])
           merchant_id.append(line[3])
           brand_id.append(line[4])
           time_stamp.append(line[5])
           action_type.append(line[6])
user_log_id=np.array(user_log_id)
item_id=np.array(item_id)
cat_id=np.array(cat_id)
merchant_id=np.array(merchant_id)
brand_id=np.array(brand_id)
time_stamp=np.array(time_stamp)
action_type=np.array(action_type)

user_id=np.loadtxt("user_info.csv",delimiter=",",skiprows=1,dtype="string",usecols=(0,))
age_range=np.loadtxt("user_info.csv",delimiter=",",skiprows=1,dtype="string",usecols=(1,))
gender=np.loadtxt("user_info.csv",delimiter=",",skiprows=1,dtype="string",usecols=(2,))

data_=np.column_stack((user_log_id,merchant_id,item_id,cat_id,brand_id,time_stamp,action_type))
temp1_array=np.arange(user_log_id.shape[0])
temp2_array=np.arange(user_id.shape[0])
temp3_array=np.arange(merchant_id.shape[0])
flag=0

for i in range(len(test_label)):
    flag_t=True
    flag_c=True
    flag_s=True
    c=temp1_array[user_log_id==test_user_label[i]]
    for k in range(len(c)):
        if(merchant_id[c[k]]==test_merchant_label[i]):
            test_add[i][0]=item_id[c[k]]
            test_add[i][1]=cat_id[c[k]]
            test_add[i][2]=brand_id[c[k]]
            test_add[i][3]=action_type[c[k]]
            flag=k
            break
    for k in range(len(c)):
        if(item_id[c[k]]==test_add[i][0] and k!=flag):
            buy_before[i]='1'
            if(action_type[c[k]]=='1'):
                times[i]+=0.5
            elif(action_type[c[k]]=='2'):
                times[i]+=1
            else:
                times[i]+=1.5
            flag_t=False
    for k in range(len(c)):
        if(cat_id[c[k]]==test_add[i][1] and k!=flag):
            same_cat[i]='1'
            if(action_type[c[k]]=='1'):
                times_cat[i]+=0.5
            elif(action_type[c[k]]=='2'):
                times_cat[i]+=1
            else:
                times_cat[i]+=1.5
            flag_c=False
    c=temp3_array[merchant_id==test_merchant_label[i]]
    for k in range(len(c)):
        if(item_id[c[k]]==test_add[i][0] and k!=flag):
            merchant_s_item[i]='1'
            flag_s=False
            break
    if(flag_s):
        merchant_s_item[i]='0'
    if(flag_t):
        buy_before[i]='0'
    if(flag_t):
        buy_before[i]='0'

for i in range(len(test_label)):
    c=temp2_array[user_id==test_data[i][1]]
    test_info[i][0]=age_range[c[0]]
    test_info[i][1]=gender[c[0]]

times=times.astype(str)
times_cat=times_cat.astype(str)
test_data=np.column_stack((test_data,test_add,test_info,buy_before,times,same_cat,times_cat,merchant_s_item))
test_data=test_data.astype(float)
np.savetxt("newtest.csv",test_data,delimiter=",")

csvfile_test.close()
csvfile_log.close()
