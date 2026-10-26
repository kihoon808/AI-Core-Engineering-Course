"""실습 04 기본필수: 이웃 3개의 투표와 평균을 비교합니다."""
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

# 데이터 설정 kNN 모델에 입력할 학습 데이터와 정답 데이터 (실습의 데이터는 3.2 근접한 4,2,1) 
X = [[1], [2], [4], [7], [9]] #입력 데이터
class_y = [0, 0, 1, 1, 1] #분류 정답
number_y = [10, 20, 40, 70, 90] #회귀 정답

# 3.2에 가까운 입력은 4, 2, 1입니다. 거리: 0.8, 1.2, 2.2
# TODO B04a: 분류에서 이웃 수를 3으로 바꾸세요.
# 힌트: n_neighbors는 참고할 이웃 수입니다.
classifier = KNeighborsClassifier(n_neighbors=3) #k=3으로 설정
classifier.fit(X, class_y) #분류로 학습시키기 위해 model객체에 X와 class_y를 입력한다.
print("분류:", classifier.predict([[3.2]])) #3.2의 분류를 prediction에 넣는다.
print("결과가 0인 이유는 4,2,1 이웃 중 0,0,1 이기 때문에 0이 2개이기 때문이다. (투표로 결정)")

# TODO B04b: 회귀에서도 이웃 수를 3으로 바꾸세요.
# 힌트: 같은 이웃의 숫자 정답 [40, 20, 10]을 평균냅니다.
regressor = KNeighborsRegressor(n_neighbors=3) #k=3으로 설정
regressor.fit(X, number_y) #회귀로 학습시키기 위해 model객체에 X와 number_y를 입력한다.
print("회귀:", regressor.predict([[3.2]]).round(2)) #3.2의 회귀를 prediction에 넣는다.
