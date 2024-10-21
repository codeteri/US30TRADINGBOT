import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetch historical data for Dow Jones
ticker = '^DJI'  # Dow Jones Industrial Average
data = yf.download(ticker, start='2010-01-01', end='2024-10-01')

# Calculate moving averages
short_window = 50
long_window = 200

data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

# Create signals
data['Signal'] = 0
data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)
data['Position'] = data['Signal'].diff()

# Plotting
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='DJIA Price', alpha=0.5)
plt.plot(data['Short_MA'], label='50-Day MA', alpha=0.75)
plt.plot(data['Long_MA'], label='200-Day MA', alpha=0.75)

# Plot buy signals
plt.plot(data[data['Position'] == 1].index, 
          data['Short_MA'][data['Position'] == 1], 
          '^', markersize=10, color='g', lw=0, label='Buy Signal')

# Plot sell signals
plt.plot(data[data['Position'] == -1].index, 
          data['Short_MA'][data['Position'] == -1], 
          'v', markersize=10, color='r', lw=0, label='Sell Signal')

plt.title('Dow Jones Industrial Average with Buy/Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()