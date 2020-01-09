# -*- coding: utf-8 -*-

def scent_letter():
    
                        ##### library section #####
    import pickle
    import numpy as np
    from sklearn.neighbors import KNeighborsClassifier
    from keras.models import load_model
    import glob
    from PIL import Image


                        ##### file load section #####
    G = None
    while bool(G) == False:
        G = input('향수를 사용할 분의 성별을 입력해주세요. (M/W) :')
        if G.upper() == 'M':
            file = open('사용자 지정 경로/main_perf_m.txt','rb')
            my_main_frame = pickle.load(file)
            file.close()  

            file = open('사용자 지정 경로/weather_one_hot_m.txt','rb')
            my_weather_one_hot = pickle.load(file)
            file.close()

            file = open('사용자 지정 경로/CNN_data_m.txt','rb')
            x = pickle.load(file)
            file.close()
            
            file = open('사용자 지정 경로/CNN_label_m.txt','rb')
            y = pickle.load(file)
            file.close()
            
        elif G.upper() == 'W':
            file = open('사용자 지정 경로/main_perf_w.txt','rb')
            my_main_frame = pickle.load(file)
            file.close()  

            file = open('사용자 지정 경로/weather_one_hot_w.txt','rb')
            my_weather_one_hot = pickle.load(file)
            file.close()

            file = open('사용자 지정 경로/CNN_data_w.txt','rb')
            x = pickle.load(file)
            file.close()
            
            file = open('사용자 지정 경로/CNN_label_w.txt','rb')
            y = pickle.load(file)
            file.close()
            
        else :
            print('M(남성) 또는 W(여성)으로 입력해주세요.')
            G = None
    
    test = []
    while bool(test) == False:
        test = []
        test_dir = input('테스트할 사진의 정확한 directory를 입력해주세요. :')
        
        
                       ###### 형용사 CNN model section #####     
        files = glob.glob(test_dir)
        CNN_model = load_model('사용자 지정 경로/형용사_45_model.h5')
#        CNN_model = load_model('사용자 지정 경로/형용사_45_model_ver_2.h5')
        labels = ['가벼운', '개성적인', '거친', '고급스러운', '관능적인', '귀여운', '기운찬', '깔끔한', '남성적인',
                  '달콤한', '도시적인', '동양적인', '동적인', '따뜻한', '맑은', '매력적인', '무거운', '밝은',
                  '부드러운', '사랑스러운', '상쾌한', '서양적인', '성숙한', '소박한', '수수한', '순수한', '시원한', '신선한',
                  '어두운', '여성적인', '우아한', '은은한', '인공적인', '자연적인', '전원적인', '전통적인', '젊은', '점잖은',
                  '정적인', '중후한', '차가운', '차분한', '편안한', '현대적인', '화려한']
        for i, f in enumerate(files):
            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((128,128))
            data = np.asarray(img)
            test.append(data)
    test = np.array(test)
    test = test.astype('float32')/255
    
    r = CNN_model.predict(test, batch_size = 32)
    res = r[0]
    for i, acc in enumerate(res):                   
        print(labels[i], '=', np.round(acc * 100, 3))  
    print('예측결과 : ', labels[res.argmax()])      
    print('')                                       
    res = res.reshape((1, -1))
    
                   ###### KNN model section #####                    
    x_train = np.array(x)
    KNN_model = KNeighborsClassifier(n_neighbors=101)
    KNN_model.fit(x_train,y)
    idx = KNN_model.kneighbors(res, return_distance=False)
        
                ###### 계절 CNN model section #####     
    files = glob.glob(test_dir)
    CNN_model_w = load_model('사용자 지정 경로/계절_5_model.h5')
    labels_w = ['autumn', 'night', 'spring', 'summer', 'winter']
    test_w = []
    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert('RGB')
        img = img.resize((128,128))
        data = np.asarray(img)
        test_w.append(data)
    test_w = np.array(test_w)
    test_w = test_w.astype('float32')/255
    
    r_w = CNN_model_w.predict(test_w, batch_size = 32)
    res_w = r_w[0]
    for i, acc in enumerate(res_w):
        print(labels_w[i], '=', np.round(acc * 100, 3))
    print('예측결과 : ', labels_w[res_w.argmax()])
    print('')
    res_w = res_w.reshape((1, -1))
    
    w = []
    if res_w[0][1] == res_w[0].max():
        w.append(2)
        if res_w[0][1] < 0.7:
            for i in [0,2,3,4]:
                if res_w[0][i] >= res_w[0][[0,2,3,4]].max() * 0.8:
                    w.append(i+1)
    else:
        for i in [0,2,3,4]:
            if res_w[0][i] >= res_w[0][[0,2,3,4]].max() * 0.8:
                w.append(i+1)
    
    a = []
    for i in w:
        for j in list(idx[0]):
            if my_weather_one_hot.iloc[j, i] == 1:
                a.append(j)
    
                ##### 대중성 정렬 #####
    if len(a) == 0:
        for i in range(0,3):
            print(my_main_frame.iloc[idx[0]].sort_values(by = 'n_vote', axis = 0, ascending = False).iloc[i, 0])
    elif len(a) == 1:
        print(my_main_frame.iloc[a])
        for i in range(0,2):
            print(my_main_frame.iloc[idx[0]].sort_values(by = 'n_vote', axis = 0, ascending = False).iloc[i, 0])
    elif len(a) == 2:
        for i in range(0,2):
            print(my_main_frame.iloc[a].sort_values(by = 'n_vote', axis = 0, ascending = False).iloc[i, 0])
        print(my_main_frame.iloc[idx[0]].sort_values(by = 'n_vote', axis = 0, ascending = False).iloc[0, 0])    
    else:
        for i in range(0, 3):
            print(my_main_frame.iloc[a].sort_values(by = 'n_vote', axis = 0, ascending = False).iloc[i, 0])
        
scent_letter()


