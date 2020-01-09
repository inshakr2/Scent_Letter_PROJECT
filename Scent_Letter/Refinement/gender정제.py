# -*- coding: utf-8 -*-

import pickle
import pandas as pd
import re

file = open('사용자 지정 경로/main_perf_Z.txt','rb')
my_frame = pickle.load(file)
file.close() 
my_frame.info()

temp = []
for i in my_frame['name']:
    if re.match('.+for men$', i):
        temp.append([i,1,0])
    elif re.match('.+for women$', i):
        temp.append([i,0,1])
    elif re.match('.+[for women \+ men]$', i):
        temp.append([i,1,1])
    else:
        temp.append([i,0,0])

gender = pd.DataFrame(temp, columns=['name','men','women'])
gender

file = open('사용자 지정 경로/gender_perf.txt','wb')
pickle.dump(gender, file)
file.close()
