# PROJECT_  Scent Letter

사진과 어울리는 향수를 추천하는 AI 모델입니다.

형용사를 매개로 시각과 후각을 매칭하였으며, 향에 어울리는 형용사는 자체적으로 시행한 설문조사 결과를 반영했습니다.

__By. 유창열, 이광진, 이희주__


## 시스템 흐름

![image](https://user-images.githubusercontent.com/59518805/72042018-84d03980-32f0-11ea-8a35-b3a04491bd36.png)

## 구축환경

Python을 기반으로 구현하였으며, Webdriver로는 Firefox와 Tor Browser를 이용하였습니다.

사용한 핵심 모듈은 아래와 같습니다.

__1. sklearn__
  * KNeighborsClassifier

__2. tensorflow__

__3. keras__
  * ADAM Optimizer
  
__4. numpy__

__5. pandas__

__6. selenium__

__7. BeautifulSoup__

__8. pickle__

## 실행방법 ##


    깃 허브에서 file을 모두 다운로드 받으시고, 

    Data folder를 사용자 지정 directory에 저장합니다. 
    
    
    다음으로 함께 첨부되어 있는 Exe.py 파일을 Python에서 open 하고 지정한 directory를 입력합니다.
    
    마지막으로 함수를 compile 한 뒤에 실행합니다.
    
## 결과 예시 ##


![image](https://user-images.githubusercontent.com/59518805/72044336-e3001b00-32f6-11ea-9829-1262e5c9ebd8.png)




## Version 2. 개선점

1. 각 형용사 별 학습 사진의 수를 500개로 균일화


   

## Reference

[향수 Data](https://www.fragrantica.com/): 모든 향수의 data를 수집한 Site 입니다. 

[iri 색연구소](http://www.iricolor.com/index3.html): 시각에 대한 형용사를 조회하기 위하여 참고한 Site 입니다.
  
[설문조사](https://forms.gle/x3TANSHC86FLNsvz5): 향과 형용사를 매칭시킬 때 사용한 Google form 입니다.

참고 논문 
  > 색채를 매개변수로 활용한 시각과 후각의 상관관계 연구 (예사길, 2012)
  > 
  > 후각 중심의 감성디자인을 위한 색체 공감각 연구 (박민영, 2012)
  >
  > 후각적 감성과 시각적 감성의 연상관계 (이수빈, 2015)
  >

