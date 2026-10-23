"""06 기본필수: 숫자 1열과 문자 1열을 함께 변환합니다."""
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

train = pd.DataFrame({"input_chars": [100, 200, 300],
                      "task_type": ["qa", "summary", "qa"]})
valid = pd.DataFrame({"input_chars": [400, 500],
                      "task_type": ["summary", "qa"]})
                      
#ColumnTransformer은 여러 컬럼을 한꺼번에 처리해줌. pipeline 안에 들어감. 튜플 안에 "num", StandardScaler(), ["input_chars"] 넣고, 
#튜플 안에 ("cat", OneHotEncoder(sparse_output=False), ["task_type"]) 넣으면 됨. 순서대로 처리됨. 숫자는 표준화, 문자는 원-핫 변환.
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["input_chars"]),
    ("cat", OneHotEncoder(sparse_output=False), ["task_type"]),
])
preprocessor.fit(train)
# TODO B06-1: preprocessor의 transform으로 valid를 변환하세요.
# valid_ready = valid
valid_ready = preprocessor.transform(valid)
# valid_ready = [[-1.342, 0.0, 1.0], [-0.447, 1.0, 0.0]]

print("변환 전:", valid.shape)
print("변환 후:", valid_ready.shape)
print(valid_ready.round(3))
