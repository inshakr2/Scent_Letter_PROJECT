# -*- coding: utf-8 -*-

import pickle
import pandas as pd
import numpy as np


file = open('사용자 지정 경로/main_perf_Z.txt','rb')     
fin = pickle.load(file)
file.close()

fin

fin['accords']

len(fin['group'].unique())

df = pd.DataFrame()
for i in fin['group'].unique():
    temp = []
    for j in fin[fin['group'] == i]['accords']:        
        if type(j) == dict:
            for k in j.keys():
                temp.append(k)
        elif type(j) == list:
            for k in j:
                for l in k.keys():
                    temp.append(l)
    df = df.append(pd.DataFrame([[i, temp]], columns=['group', 'accord']), ignore_index=True)

df


a = {}
for i in range(32):
    for j in df['accord'][i]:
        if j not in a.keys():
            a[j] = df['group'][i]            
        else:
            a[j] = a[j]+','+(df['group'][i])

len(a)
a

acc_group = pd.DataFrame()
for i, j in a.items():
    acc_group = acc_group.append(pd.DataFrame([[i,j]], columns = ['accord','group'])
                                ,ignore_index=True)

acc_group

column = ['accord']

for i in list(fin['group'].unique()):
    column.append(i)

column

acc_group.info()


pd.Series(acc_group['group'][0].split(',')).value_counts().index

dff = pd.DataFrame(columns = column)

for i in range(len(acc_group['accord'])):
    cn = pd.Series(acc_group['group'][i].split(',')).value_counts()
    temp = pd.DataFrame([cn], columns = cn.index)
    temp['accord'] = acc_group['accord'][i]
    dff = dff.append(temp, ignore_index=True)
    
dff.info()

dff = dff.fillna(0)

aaa = dff.iloc[:,:-1]

aaa = aaa/np.array(aaa).sum(axis=1).reshape(-1,1)
aaa
acc_group_prop = pd.merge(dff.iloc[:,-1],aaa,left_index=True, right_index=True)

file = open('사용자 지정 경로/acc_group_prop.txt','wb')     
pickle.dump(acc_group_prop, file)
file.close()

acc_group_prop
























