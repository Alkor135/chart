import finplot as fplt
import yfinance

df = yfinance.download('AAPL')
print(df)
fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
fplt.show()
