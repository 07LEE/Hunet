import pandas as pd
import numpy as np

class KDT:
 
    def MID(df):  # 중간값 추가하기
        high_prices = df['High'].values
        low_prices = df['Low'].values
        mid_prices = (high_prices + low_prices) / 2
        df['Mid'] = mid_prices


    def SMA(df, num):  # 단순이동평균선 만들기
        i = df['Close'].rolling(window=num).mean()
        df['MA%s' % num] = i


    def SMA_position(df, SMA_S, SMA_L) : # 단순이동평균
        i = df['Close'].rolling(window=SMA_S).mean()
        df['SMA%s' % SMA_S] = i
        i = df['Close'].rolling(window=SMA_L).mean()
        df['SMA%s' % SMA_L] = i
        df["SMA_position"] = np.where(df['SMA%s' %SMA_S] > df['SMA%s' %SMA_L], 1, -1)


    def Bollinger(df, SMA=30, dev=2) :
        df["SMA"] = df["Close"].rolling(SMA).mean()
        df["Lower"] = df["SMA"] - df["Close"].rolling(SMA).std() * dev # 상단 볼린저 밴드
        df["Upper"] = df["SMA"] + df["Close"].rolling(SMA).std() * dev # 하단 볼린저 밴드

        df["distance"] = df.Close - df.SMA 
        df["BB_position"] = np.where(df.Close < df.Lower, 1, np.nan) # 1. oversold -> go long
        df["BB_position"] = np.where(df.Close > df.Upper, -1, df["BB_position"]) # 2. overbought -> go short
        df["BB_position"] = np.where(df.distance * df.distance.shift(1) < 0, 0, df["BB_position"])
        df["BB_position"] = df.BB_position.ffill().fillna(0) # where 1-3 isn´t applicable -> hold previous position



    def RSI(df):  # RSI 구하기      
        periods = 20
        df.Close.diff()
        df["U"] = np.where(df.Close.diff() > 0, df.Close.diff(), 0)
        df["D"] = np.where(df.Close.diff() < 0, -df.Close.diff(), 0)
        df["MA_U"] = df.U.rolling(periods).mean()
        df["MA_D"] = df.D.rolling(periods).mean()
        df["RSI"] = df.MA_U / (df.MA_U + df.MA_D) * 100

        rsi_upper = 70
        rsi_lower = 30

        df["RSI_position"] = np.where(df.RSI > rsi_upper, -1, np.nan) # 1. overbought -> go short
        df["RSI_position"] = np.where(df.RSI < rsi_lower, 1, df.RSI_position) # 2. oversold -> go long
        df.RSI_position = df.RSI_position.fillna(0) # 3. where 1 & 2 isn´t applicable -> neutral


    def train_test_split_print(x_train, x_test, y_train, y_test):
        print('x_train shape : ', x_train.shape)
        print('y_train shape : ', y_train.shape)
        print('x_test shape : ', x_test.shape)
        print('y_test shape : ', y_test.shape)


    def returns(df, num):  # num 기간동안의 수익률
        df['returns%s' % num] =  df['Close'].pct_change(periods=num)


    # %% 무작위 조합 알고리즘
    def SMA(df) :
        from scipy.optimize import brute
        import pandas as pd
        import numpy as np

        def run_strategy(SMA):
            data = df.copy()
            data["returns"] = np.log(data.Close.div(data.Close.shift(1)))
            data["SMA_S"] = data.Close.rolling(int(SMA[0])).mean()
            data["SMA_L"] = data.Close.rolling(int(SMA[1])).mean()
            data.dropna(inplace = True)
            
            data["position"] = np.where(data["SMA_S"] > data["SMA_L"], 1, -1)
            data["strategy"] = data.position.shift(1) * data["returns"]
            data.dropna(inplace = True)
            
            return -data[["returns", "strategy"]].sum().apply(np.exp)[-1] # maximize absolute performance

        SMA_S, SMA_L = brute(run_strategy, ((5, 20, 1), (50, 252, 1)))
        return int(SMA_S), int(SMA_L)

   
    def MACD(df) :
        ema_s = 12 # EMA Short
        ema_l = 26 # EMA Long
        signal_mw = 9 # Moving Window for Signal Line

        df["EMA_S"] = df.Close.ewm(span = ema_s, min_periods = ema_s).mean()
        df["EMA_L"] = df.Close.ewm(span = ema_l, min_periods = ema_l).mean() 
        df["MACD"] = df.EMA_S - df.EMA_L
        df["MACD_Signal"] = df.MACD.ewm(span = signal_mw, min_periods = signal_mw).mean()
        df["MACD_position"] = np.where(df.MACD - df.MACD_Signal > 0, 1, -1)

        df.loc[:, ('Close', 'EMA_S', 'EMA_L')].iplot()
        df.loc[:, ('MACD', 'MACD_Signal')].iplot()

    ### MACD 선이 이 시그널 라인을 넘어가면 롱 포지션으로 매수 시점이고
    ### MACD 선이 시그널 라인 밑으로 향하면 쇼트 포지션으로 매도 시점을 알립니다


    def KD(df) :
        periods = 14
        df["roll_low"] = df.Low.rolling(periods).min()
        df["roll_high"] = df.High.rolling(periods).max()
        df["K"] = (df.Close - df.roll_low) / (df.roll_high - df.roll_low) * 100 # K 지표
        moving_av = 3
        df["D"] = df.K.rolling(moving_av).mean() # D 지표
        df["KD_position"] = np.where(df["K"] > df["D"], 1, -1)

        ### K선이 D선을 위로 가로지를 때마다 매수하라는 신호
        ### K선이 D선을 아래로 가로지를 때마다 매도하라는 신호