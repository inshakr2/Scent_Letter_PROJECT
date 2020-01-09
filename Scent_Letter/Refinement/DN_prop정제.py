# -*- coding: utf-8 -*-

import pickle
import pandas as pd

                ##### DN_perf  #####
                
# Day/Night 부분만 추출
file = open('사용자 지정 경로/main_perf_Z.txt','rb')
my_frame = pickle.load(file)
file.close() 
                
my_frame = my_frame.loc[:,['name','vote']]
a = 0
for i in range(0,len(my_frame)):
    try:
        a += 1
        my_frame.loc[i,'day'] = my_frame.vote[i].get('day')
        my_frame.loc[i,'night'] = my_frame.vote[i].get('night')
        print(a)
    except:
        if KeyError:
            my_frame.loc[i,'day'] = 0
            my_frame.loc[i,'night'] = 0
        else :
            for j in my_frame.vote[i]:
                my_frame.loc[i,'day'] = list(j.values())[7]
                my_frame.loc[i,'night'] = list(j.values())[8]
            
my_frame = my_frame.dropna()
my_frame = my_frame.drop('vote',axis=1)
# 기본 data set 완료
my_frame
my_frame['total'] = my_frame.sum(axis=1)

for i in range(1,3):
    my_frame.iloc[:,i] = my_frame.iloc[:,i]/my_frame.total

my_frame = my_frame.reset_index()
my_frame = my_frame.drop('index',axis=1)
my_frame = my_frame.drop('total',axis=1)
my_frame

len(my_frame)
my_frame

file = open('사용자 지정 경로/DN_perf_z.txt','wb')
pickle.dump(my_frame,file)
file.close()
