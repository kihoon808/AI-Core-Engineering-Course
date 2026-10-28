"""실습 01: 실제 실패 6건인 손계산 예제입니다. 아직 모델을 학습하지 않습니다."""
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
# 행은 실제, 열은 예측입니다. 1은 좋은 결과가 아니라 관심 클래스인 '실패'입니다.
y = [0]*14 + [1]*6 #실제값, (0이 성공, 1이 실패)
pred = [0]*10 + [1]*4 + [0]*4 + [1]*2 #pred는 예측값
"""
실제 정상(14건) 중 10건 정상(0), 4건 실패(1)로 예측
실제 실패(6건) 중 4건 정상(0), 2건 실패(1)로 예측
"""

print("혼동행렬(행 실제 / 열 예측, 성공0·실패1)")
print(confusion_matrix(y, pred, labels=[0, 1])) 

"""
accuracy_score는 
"""
acc = accuracy_score(y, pred) 
precision = precision_score(y, pred, zero_division=0)
recall = recall_score(y, pred, zero_division=0)
f1 = f1_score(y, pred, zero_division=0)

print(f"Accuracy={acc:.3f}, Precision={precision:.3f}, Recall={recall:.3f}, F1={f1:.3f}")
print("실제 실패 6건 중 발견: 2건")
