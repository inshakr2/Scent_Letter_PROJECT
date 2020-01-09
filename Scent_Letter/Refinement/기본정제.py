# -*- coding: utf-8 -*-

import pandas as pd
import pickle

file = open('사용자 지정 경로/main_perf_fin.txt','rb')
data = pickle.load(file)
file.close()

                    ##### 1차 정제 #####
                    # nan 제거, 사용할 컬럼만 선택, 투표수 10 이상인 향수만 선택
data.info()

frame = pd.DataFrame(data)
frame = frame.dropna()  # 45175
my_frame = frame.loc[:,['name','brand','group','accords','vote','n_vote']]  # 45175
my_frame = my_frame.loc[my_frame.n_vote >= 10,:]    # 22459
my_frame = my_frame.reset_index()   # 인덱스 번호 새로 매김
my_frame = my_frame.drop('index',axis=1)
my_frame.info()

                    ##### 2차 정제 #####

# accords 이중 리스트 제거         
a = 0
for i in my_frame.accords:
    if type(i) == list:
        temp = dict(pd.Series(i))
        my_frame.accords.iat[a] = temp[0]
        print(a) 
    else :
        pass
    a += 1

for i in my_frame.accords:
    if type(i) == list:
        print(i)

# vote 이중 리스트 제거
a = 0
for i in my_frame.vote:
    if type(i) == list:
        temp = dict(pd.Series(i))
        my_frame.vote.iat[a] = temp[0]
        print(a)
    else :
        pass
    a += 1    

for i in my_frame.vote:
    if type(i) == list:
        print(i)

my_frame.vote
my_frame.accords

# 기본적인 정제 완료
file = open('사용자 지정 경로/main_perf_Z.txt','wb')
pickle.dump(my_frame, file)
file.close()

