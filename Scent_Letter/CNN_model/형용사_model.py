# -*- coding: utf-8 -*-


import numpy as np
from PIL import Image
import glob
import pickle
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import load_model

# 이미지 사이즈 동일하게 변환
caltech_dir = '학습이미지데이터/형용사'
categories = ['가벼운', '개성적인', '거친', '고급스러운', '관능적인', '귀여운', '기운찬', '깔끔한', '남성적인',
              '달콤한', '도시적인', '동양적인', '동적인', '따뜻한', '맑은', '매력적인', '무거운', '밝은',
              '부드러운', '사랑스러운', '상쾌한', '서양적인', '성숙한', '소박한', '수수한', '순수한', '시원한', '신선한',
              '어두운', '여성적인', '우아한', '은은한', '인공적인', '자연적인', '전원적인', '전통적인', '젊은', '점잖은',
              '정적인', '중후한', '차가운', '차분한', '편안한', '현대적인', '화려한']
len(categories)

nb_class = len(categories)
image_w = 128
image_h = 128
pixels = image_w * image_h * 3

# X, Y 생성
X = []
Y = []

for idx, cat in enumerate(categories):
    label = [0 for i in range(nb_class)]
    label[idx] = 1
    image_dir = caltech_dir + '/' + cat
    files = glob.glob(image_dir + '/*.jpg')
    print(files)
    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert('RGB')
        img = img.resize((image_w, image_h))
        data = np.asarray(img)
        X.append(data)
        Y.append(label)
        if i % 100 == 0:
            print(i, '\n', data)

X = np.array(X) 
print(X.shape)
Y = np.array(Y) 
print(Y.shape)

# X, Y 저장
file = open('디렉토리/형용사_45_X.txt', 'wb')
pickle.dump(X, file)
file.close()

file = open('디렉토리/형용사_45_Y.txt', 'wb')
pickle.dump(Y, file)
file.close()

    #####################################################################
# X, Y 불러오기
file = open('디렉토리/형용사_45_X.txt','rb')     
X = pickle.load(file)
file.close()

file = open('디렉토리/형용사_45_Y.txt','rb')     
Y = pickle.load(file)
file.close()

# 정규화 작업
X = X.astype('float32') / 255

# CNN
model = Sequential()
model.add(Conv2D(64, (3, 3), padding = 'same', input_shape = (128, 128, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), padding = 'same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(256, (3, 3), padding = 'same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), padding = 'same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding = 'same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(45))   
model.add(Activation('softmax'))
model.summary()

# 트레이닝
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

# 적용
hist = model.fit(X, Y, batch_size = 32, epochs = 1000, verbose = 1, validation_data = (X, Y))

# 저장
model.save('형용사_45_model.h5')

# 불러오기
model = load_model('형용사_45_model.h5')

# 테스트
files = glob.glob('테스트 파일 위치')
X = []
for i, f in enumerate(files):
    img = Image.open(f)
    img = img.convert('RGB')
    img = img.resize((128, 128))
    data = np.asarray(img)
    X.append(data)
X = np.array(X)
X = X.astype('float32')/255

labels = ['가벼운', '개성적인', '거친', '고급스러운', '관능적인', '귀여운', '기운찬', '깔끔한', '남성적인',
              '달콤한', '도시적인', '동양적인', '동적인', '따뜻한', '맑은', '매력적인', '무거운', '밝은',
              '부드러운', '사랑스러운', '상쾌한', '서양적인', '성숙한', '소박한', '수수한', '순수한', '시원한', '신선한',
              '어두운', '여성적인', '우아한', '은은한', '인공적인', '자연적인', '전원적인', '전통적인', '젊은', '점잖은',
              '정적인', '중후한', '차가운', '차분한', '편안한', '현대적인', '화려한']
r = model.predict(X, batch_size = 32)
res = r[0]
for i, acc in enumerate(res):
    print(labels[i], '=', acc * 100)
print('예측결과 : ', labels[res.argmax()])