# -*- coding: utf-8 -*-

import pickle
import pandas as pd

                    ##### main과 gender를 병합 #####
file = open('사용자 지정 경로/main_perf_Z.txt','rb')
my_frame = pickle.load(file)
file.close() 
 
file = open('사용자 지정 경로/gender_perf.txt','rb')
gender = pickle.load(file)
file.close()  

my_frame['man'] = list(gender.men)
my_frame['woman'] = list(gender.women)

file = open('사용자 지정 경로/main_perf_Z.txt','wb')
pickle.dump(my_frame,file)
file.close()

        # main_perf_Z 최종 정제 완료

file = open('사용자 지정 경로/main_perf_Z.txt','rb')
my_frame = pickle.load(file)
file.close() 

                    ##### 남 / 녀 데이터 저장 - main_perf #####
m_data = my_frame.loc[my_frame.man == 1,].iloc[:, :-2]
w_data = my_frame.loc[my_frame.woman == 1,].iloc[:, :-2]

file = open('사용자 지정 경로/main_perf_m.txt','wb')
pickle.dump(m_data,file)
file.close()

file = open('사용자 지정 경로/main_perf_w.txt','wb')
pickle.dump(w_data,file)
file.close()

                    # 남 / 여 인덱스 뽑기
m = my_frame.loc[my_frame.man == 1,].index
w = my_frame.loc[my_frame.woman == 1,].index


                    ##### 남 / 녀 데이터 저장 - weather_one_hot #####
file = open('사용자 지정 경로/weather_one_hot.txt','rb')
my_weather_one_hot = pickle.load(file)
file.close()

m_data = my_weather_one_hot.iloc[m,]
w_data = my_weather_one_hot.iloc[w,]

file = open('사용자 지정 경로/weather_one_hot_m.txt','wb')
pickle.dump(m_data,file)
file.close()

file = open('사용자 지정 경로/weather_one_hot_w.txt','wb')
pickle.dump(w_data,file)
file.close()

                    ##### 남 / 녀 데이터 저장 - weather_one_hot #####
file = open('사용자 지정 경로/acc_perf_z.txt','rb')
my_acc_frame = pickle.load(file)
file.close()  

m_data = my_acc_frame.iloc[m,]
w_data = my_acc_frame.iloc[w,]

file = open('사용자 지정 경로/acc_perf_m.txt','wb')
pickle.dump(m_data,file)
file.close()

file = open('사용자 지정 경로/acc_perf_w.txt','wb')
pickle.dump(w_data,file)
file.close()