# %%
from sklearn.metrics import plot_confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, GRU, SimpleRNN, Dense, GlobalMaxPool1D
import tensorflow as tf
from KDT import KDT
import FinanceDataReader as fdr
import cufflinks as cf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brute

# %% 종목 검색
symbol = '041510'  # 원하는 종목 코드
start = "2010-01-01"  # 검색 시작일
end = "2022-12-31"  # 검색 종료일

df = fdr.DataReader(symbol, start, end)
df.info()
df.loc[:, ('Close')].iplot()

# %% SMA 관련 지표 추가하기
SMA_S, SMA_L = KDT.SMA(df)
KDT.SMA_position(df, SMA_S, SMA_L)
df.loc[:, ('Close', 'SMA%s' % SMA_S, 'SMA%s' % SMA_L)].iplot()

# %%
KDT.MACD(df)  # %% MACD 지표 추가하기
KDT.RSI(df)  # %% RSI 지표 추가하기
df.RSI_position.value_counts()

# %%  SO 전략 K 지표, D 지표
KDT.KD(df)
df.loc[:, ('Close', 'roll_low', 'roll_high')].iplot()
df.loc[:, ('K', 'D')].iplot()

# %% 볼린저 벤드 지표
KDT.Bollinger(df)
df.loc[:, ('Close', 'Upper', 'Lower')].iplot()

# %% 조합한 지표
df["comb_position"] = 0
df["comb_position"] = np.where(df.MACD_position == 1, 1, 0)
df["comb_position"] = np.where(df.RSI_position == 1, df.comb_position + 1 , df.comb_position) 
df["comb_position"] = np.where(df.KD_position == 1, df.comb_position + 1 , df.comb_position) 
df["comb_position"] = np.where(df.BB_position == 1, df.comb_position + 1 , df.comb_position) 
df.comb_position.value_counts()

# %% 
KDT.returns(df, 5)

#%% 가격 자체를 예측
series = df['Close'].values.reshape(-1, 1)
scaler = StandardScaler()
scaler.fit(series[:len(series) // 2])
series = scaler.transform(series).flatten()

T = 10
D = 1
X = []
Y = []
for t in range(len(series) - T):
  x = series[t:t+T]
  X.append(x)
  y = series[t+T]
  Y.append(y)

X = np.array(X).reshape(-1, T, 1)  # 이제 데이터는 N x T x D 크기가 될 것이다.
Y = np.array(Y)
N = len(X)
print("X.shape", X.shape, "Y.shape", Y.shape)

# %% 모델 설계
i = Input(shape=(T, 1))
x = LSTM(5)(i)
x = Dense(1)(x)
model = Model(i, x)

#모델 컴파일
model.compile(loss='mse', optimizer=Adam(lr=0.1),)

# 모델 훈련
r = model.fit(X[:-N//2], Y[:-N//2], epochs=100,
              validation_data=(X[-N//2:], Y[-N//2:]),)

# %% 손실을 시각화 해 본다
plt.plot(r.history['loss'], label='loss')
plt.plot(r.history['val_loss'], label='val_loss')
plt.legend()

# %%
outputs = model.predict(X)
print(outputs.shape)
predictions = outputs[:, 0]

plt.plot(Y, label='targets')
plt.plot(predictions, label='predictions')
plt.legend()
plt.show()

# %%################################################

#%% LogisticRegression
sf = df[['SMA_position', 'RSI_position',
         'KD_position', 'BB_position', 'comb_position', 'RSI']]
sf['Change_position'] = np.where(df["Change"] > 0, 1, 0)

# %%
sf["target"] = np.where(df.returns5 > 0.02, 1, np.nan)
sf["target"] = np.where(df.returns5 < 0.01, 0, sf.target) 
sf.target = sf.target.fillna(0)
sf["target"] = sf["target"].shift(-1)
sf = sf.dropna()

sf.target.value_counts()
# %% 
X = sf.iloc[:, 0:7]
y = sf.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False)
KDT.train_test_split_print(X_train, X_test, y_train, y_test)

# 기본값으로 로짓 모형을 설정하고 학습한다
logreg = LogisticRegression().fit(X_train, y_train)

#분석결과를 출력한다
print("prediction:", logreg.predict(X_test))
print("Train Data score : ", round(logreg.score(X_train, y_train), 3))
print("Test Data score : ", round(logreg.score(X_test, y_test), 3))

# %% 오차행렬 시각화
# Plot non-normalized confusion matrix
titles_options = [("Confusion matrix, without normalization", None)]

for title, normalize in titles_options:
    disp = plot_confusion_matrix(
        logreg, X_test, y_test, cmap=plt.cm.Blues, normalize=normalize)
    disp.ax_.set_title(title)
    print(title)
    print(disp.confusion_matrix)

plt.show()

# %%##############################################################

# %%
df["target"] = sf["target"]
df = df.dropna()
# %% 
X = df.iloc[:, 0:29]
y = df.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y)
KDT.train_test_split_print(X_train, X_test, y_train, y_test)

# 기본값으로 로짓 모형을 설정하고 학습한다
logreg = LogisticRegression().fit(X_train, y_train)

#분석결과를 출력한다
print("prediction:", logreg.predict(X_test))
print("Train Data score : ", round(logreg.score(X_train, y_train), 3))
print("Test Data score: ", round(logreg.score(X_test, y_test), 3))

# %% 오차행렬 시각화
# Plot non-normalized confusion matrix
titles_options = [("Confusion matrix, without normalization", None)]

for title, normalize in titles_options:
    disp = plot_confusion_matrix(
        logreg, X_test, y_test, cmap=plt.cm.Blues, normalize=normalize)
    disp.ax_.set_title(title)
    print(title)
    print(disp.confusion_matrix)
 
plt.show()

# %%
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

prediction = logreg.predict(X_test)
precision = precision_score(y_test, prediction, average="macro")
print("precision:", precision)
recalI = recall_score(y_test, prediction, average="macro")
print("recall:", recalI)
f1_score = f1_score(y_test, prediction, average="macro")
print("f1 score:", f1_score)

# %%
