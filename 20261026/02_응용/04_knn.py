"""실습 04 응용: 같은 세 이웃에서 가중치만 바꿉니다."""
from sklearn.neighbors import KNeighborsRegressor

X = [[1], [2], [4], [7], [9]] #입력 데이터
y = [10, 20, 40, 70, 90] #정답 데이터
for weight in ["uniform", "distance"]:
    # TODO A04: weights에 반복 변수 weight를 넣으세요.
    # 힌트: 이웃 수는 3으로 고정합니다.
    model = KNeighborsRegressor(n_neighbors=3, weights=weight) #k=3으로 설정, 가중치를 반복 변수로 설정
    model.fit(X, y) #회귀로 학습시키기 위해 model객체에 X와 y를 입력한다.
    print(weight, "예측:", model.predict([[3.2]]).round(2)) #3.2의 회귀를 prediction에 넣는다.
# uniform은 3개를 똑같이, distance는 가까운 값에 더 큰 비중을 줍니다.
