# -*- coding: utf-8 -*-

import pickle
import pandas as pd
import numpy as np

      ##### CNN data section #####
                # Man
                
file = open('사용자 지정 경로/main_perf_m.txt','rb')
my_frame = pickle.load(file)
file.close() 

group = pd.read_csv('사용자 지정 경로/형용사향수_p.csv',encoding='cp949')
group.columns = group.columns[1:].insert(0,'group')
group = group.drop('기타',axis=1)

    ##### 향수 > (계열) > 형용사 #####
x = my_frame.loc[:,['name','group']]
x.group = [i.lower() for i in x.group]
y = group[:]
data_1 = pd.merge(x,y,on='group',how='inner')    
data_1 = np.round(data_1,3)
data_1.info()

    ##### 향수 > (accord) > (계열) > 형용사 #####

file = open('사용자 지정 경로/acc_perf_m.txt','rb')
my_acc_frame_m = pickle.load(file)
file.close()  

file = open('사용자 지정 경로/acc_group_prop.txt','rb')
acc_group_prop = pickle.load(file)
file.close()

x = my_acc_frame_m.drop('name',axis=1)
y = acc_group_prop.drop('accord',axis=1)
z = group.iloc[:,1:]
z = z.sort_index(axis=1)
    
step_1 = np.array(x).dot(np.array(y))
step_2 = step_1.dot(np.array(z))
step_2 = np.round(step_2,3)
data_2 = pd.DataFrame(step_2,columns=z.columns)
data_2

                ##### 1, 2 data 병합 (가중치 = 5:5) #####
    
#x = (data_1.iloc[:,2:] + data_2) / 2            ### 가중치 수정 부분
x = data_1.iloc[:,2:].add(data_2, fill_value=0)/2
y = data_1.name

file = open('사용자 지정 경로/CNN_data_m.txt','wb')
pickle.dump(x,file)
file.close()

file = open('사용자 지정 경로/CNN_label_m.txt','wb')
pickle.dump(y,file)
file.close()



                # Woman
                
file = open('사용자 지정 경로/main_perf_w.txt','rb')
my_frame = pickle.load(file)
file.close() 

group = pd.read_csv('사용자 지정 경로/형용사향수_p.csv',encoding='cp949')
group.columns = group.columns[1:].insert(0,'group')
group = group.drop('기타',axis=1)

    ##### 향수 > (계열) > 형용사 #####
x = my_frame.loc[:,['name','group']]
x.group = [i.lower() for i in x.group]
y = group[:]
data_1 = pd.merge(x,y,on='group',how='inner')    
data_1 = np.round(data_1,3)
data_1.info()

    ##### 향수 > (accord) > (계열) > 형용사 #####

file = open('사용자 지정 경로/acc_perf_w.txt','rb')
my_acc_frame_w = pickle.load(file)
file.close()  

file = open('사용자 지정 경로/acc_group_prop.txt','rb')
acc_group_prop = pickle.load(file)
file.close()

x = my_acc_frame_w.drop('name',axis=1)
y = acc_group_prop.drop('accord',axis=1)
z = group.iloc[:,1:]
z = z.sort_index(axis=1)
    
step_1 = np.array(x).dot(np.array(y))
step_2 = step_1.dot(np.array(z))
step_2 = np.round(step_2,3)
data_2 = pd.DataFrame(step_2,columns=z.columns)
data_2

                ##### 1, 2 data 병합 (가중치 = 5:5) #####
    
#x = (data_1.iloc[:,2:] + data_2) / 2            ### 가중치 수정 부분
x = data_1.iloc[:,2:].add(data_2, fill_value=0)/2
y = data_1.name

file = open('사용자 지정 경로/CNN_data_w.txt','wb')
pickle.dump(x,file)
file.close()

file = open('사용자 지정 경로/CNN_label_w.txt','wb')
pickle.dump(y,file)
file.close()


