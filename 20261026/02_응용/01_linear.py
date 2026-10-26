"""실습 01 응용: PPT E02의 계수와 수식을 확인합니다."""
from sklearn.linear_model import LinearRegression

#열 순서: [글자 수, 허용 도구 수]
X = [[200, 1], [400, 1], [200, 3], [600, 2]] 

#실행시간(ms)
y = [700, 800, 900, 1000] 

#선형 회귀 방정식: y = 절편 + (가중치1 * 글자 수) + (가중치2 * 도구 수)
model = LinearRegression()

model.fit(X, y) #선형회귀로 학습시키기 위해 model객체에 X와 y를 입력한다.

print("계수:", model.coef_.round(1)) #계수 출력
print("절편:", round(model.intercept_, 1)) #절편 출력
print("[400, 2] 예측(ms):", model.predict([[400, 2]]).round(1)) #400,2의 예측 출력
print("손계산(ms):", 500 + 0.5 * 400 + 100 * 2) #손계산 출력