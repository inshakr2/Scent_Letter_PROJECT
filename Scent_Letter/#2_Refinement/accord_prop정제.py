# -*- coding: utf-8 -*-

import pandas as pd
import pickle

                ##### accord_perf  #####
                
file = open('사용자 지정 경로/main_perf_Z.txt','rb')
my_frame = pickle.load(file)
file.close() 

               
my_frame = my_frame.loc[:,['name','accords']]
my_frame

# Unique accords
tm = []
for i in my_frame.accords:
    if type(i) == list:
        temp = dict(pd.Series(i)).keys()
        for k in temp:
            tm.append(k)
    else :
        for d in i.keys():
            tm.append(d)
            
len(pd.unique(tm))
u_acc = list(pd.Series(tm).unique())
# Unique acc에 name 컬럼을 추가
u_acc.insert(0,'name')
u_acc
# DF 만들기
my_temp = pd.DataFrame(columns=u_acc)
for i in range(0,len(my_frame)):
    n = my_frame.iloc[i,0]
    c = my_frame.iloc[i,1]
    
    for k,v in c.items():
        my_temp.at[i,k] = v
    my_temp.at[i,'name'] = n
    print(i)
    my_temp = my_temp.fillna(0)

my_frame = my_temp[:]
my_frame['total'] = my_frame.iloc[:,1:].sum(axis=1)
sum(my_frame.total.isnull())

for i in range(1,78): #accord 77개 / 0번은 Name
    my_frame.iloc[:,i] = my_frame.iloc[:,i]/my_frame.total

my_frame = my_frame.drop('total',axis=1)

file = open('사용자 지정 경로/acc_perf_z.txt','wb')
pickle.dump(my_frame,file)
file.close()

