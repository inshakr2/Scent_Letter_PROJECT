# -*- coding: utf-8 -*-

import pickle
import pandas as pd
import numpy as np


file = open('사용자 지정 경로/weather_perf_z.txt','rb')
my_weather_frame = pickle.load(file)
file.close()    

file = open('사용자 지정 경로/DN_perf_z.txt','rb')
my_DN_frame = pickle.load(file)
file.close()    


                ##### weather_one_hot  #####

weather_max = my_weather_frame.max(axis = 1)
weather_one_hot = pd.DataFrame(np.zeros(my_weather_frame.shape).astype('int'), columns = my_weather_frame.columns)
weather_one_hot.iloc[:, 0] = my_weather_frame.iloc[:, 0]
weather_one_hot.loc[:, 'night'] = 0
for i in range(len(my_weather_frame)):
    for j in range(1, len(my_weather_frame.columns)):
        if my_weather_frame.iloc[i, j] >= weather_max[i] * 0.9:
            weather_one_hot.iloc[i, j] = 1
    if my_DN_frame.night[i] >= 0.7:
        weather_one_hot.iloc[i, 5] = 1

weather_one_hot

weather_one_hot = weather_one_hot.reindex(columns = ['name','autumn', 'night', 'spring', 'summer', 'winter'])

file = open('사용자 지정 경로/weather_one_hot.txt','wb')
pickle.dump(weather_one_hot, file)
file.close() 


weather_one_hot.info()
