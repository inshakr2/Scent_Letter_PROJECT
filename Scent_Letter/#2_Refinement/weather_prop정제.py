# -*- coding: utf-8 -*-

import pandas as pd
import pickle

                    ##### weather_z #####

# 계절만 추출, 계절별 가중치 부여
file = open('사용자 지정 경로/main_perf_Z.txt','rb')
my_frame = pickle.load(file)
file.close()                 
                    
my_frame = my_frame.loc[:,['name','vote']]
a = 0
for i in range(0,len(my_frame)):
    try:
        a += 1
        my_frame.loc[i,'spring'] = my_frame.vote[i].get('spring')
        my_frame.loc[i,'summer'] = my_frame.vote[i].get('summer')
        my_frame.loc[i,'autumn'] = my_frame.vote[i].get('autumn')
        my_frame.loc[i,'winter'] = my_frame.vote[i].get('winter')
        print(a)
    except:
        if KeyError:
            my_frame.loc[i,'spring'] = 0
            my_frame.loc[i,'summer'] = 0
            my_frame.loc[i,'autumn'] = 0
            my_frame.loc[i,'winter'] = 0
        else :
            for j in my_frame.vote[i]:
                my_frame.loc[i,'spring'] = list(j.values())[4]
                my_frame.loc[i,'summer'] = list(j.values())[5]
                my_frame.loc[i,'autumn'] = list(j.values())[6]
                my_frame.loc[i,'winter'] = list(j.values())[3]

my_frame
my_frame = my_frame.dropna()
my_frame = my_frame.drop('vote',axis=1)

# 기본 data set 완료, 
my_frame
my_frame['total'] = my_frame.sum(axis=1)

for i in range(1,5):
    my_frame.iloc[:,i] = my_frame.iloc[:,i] / my_frame.total

my_frame = my_frame.reset_index()
my_frame = my_frame.drop('index',axis=1)
my_frame = my_frame.drop('total',axis=1)
my_frame
len(my_frame)

file = open('사용자 지정 경로/weather_perf_z.txt','wb')
pickle.dump(my_frame,file)
file.close()