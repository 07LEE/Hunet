import pandas as pd


def MID(df): # 중간값 추가하기
    high_prices = df['High'].values
    low_prices = df['Low'].values
    mid_prices = (high_prices + low_prices) / 2
    df['Mid'] = mid_prices


def GC_DC(df, short_ma, long_ma): # 골드크로스 데드크로스

    i = df['Close'].rolling(window=short_ma).mean() # 단기 기간 만들기
    df['MA%s' % short_ma] = i

    i = df['Close'].rolling(window=long_ma).mean() # 장기 기간 만들기 
    df['MA%s' % long_ma] = i

    gc_point = [] # 골드 크로스
    dc_point = [] # 데드 크로스

    for i in range(len(df['MA%s' % short_ma])):
        gc_point.append(0)
        dc_point.append(0)

    for i in range(len(df['MA%s' % long_ma])-1):
        if df['MA%s' % short_ma][i] <= df['MA%s' % long_ma][i] and df['MA%s' % short_ma][i+1] > df['MA%s' % long_ma][i+1]:
            gc_point[i] = 1
        elif df['MA%s' % short_ma][i] >= df['MA%s' % long_ma][i] and df['MA%s' % short_ma][i+1] < df['MA%s' % long_ma][i+1]:
            dc_point[i] = 1


def Bollinger(df): # 볼린저 밴드
    df['stddev'] = df['Close'].rolling(window=20).std()  # 20일 표준편차
    df['upper'] = df['MA20'] + (df['stddev'] * 2)  # 상단 볼린저 밴드
    df['lower'] = df['MA20'] - (df['stddev'] * 2)  # 하단 볼린저 밴드


def RSI(df): # RSI 구하기
    closedata = df["Close"]
    delta = closedata.diff()
    U, D = delta.copy(), delta.copy()
    U[U < 0] = 0
    D[D > 0] = 0
    period = 14
    AU = U.ewm(com=period-1, min_periods=period).mean()
    AD = D.abs().ewm(com=period-1, min_periods=period).mean()
    RS = AU/AD
    df['RSI'] = pd.Series(100 - (100/(1+RS)))


def train_test_split_print(x_train, x_test, y_train, y_test) :
    print('x_train shape : ', x_train.shape)
    print('y_train shape : ', y_train.shape)
    print('x_test shape : ', x_test.shape)
    print('y_test shape : ', y_test.shape)


