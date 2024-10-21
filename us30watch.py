import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fetch_data(ticker, start_date, end_date):
    """
    Fetch historical data for a given ticker from start_date to end_date.
    """
    return yf.download(ticker, start=start_date, end=end_date)

def calculate_moving_averages(data, short_window, long_window):
    """
    Calculate short and long moving averages.
    """
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    return data

def generate_signals(data, short_window):
    """
    Generate buy/sell signals based on moving averages.
    """
    data['Signal'] = 0
    data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)
    data['Position'] = data['Signal'].diff()
    return data

def plot_data(data):
    """
    Plot the closing price, moving averages, and buy/sell signals.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='DJIA Price', alpha=0.5)
    plt.plot(data['Short_MA'], label='50-Day MA', alpha=0.75)
    plt.plot(data['Long_MA'], label='200-Day MA', alpha=0.75)
    plt.plot(data[data['Position'] == 1].index, data['Short_MA'][data['Position'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(data[data['Position'] == -1].index, data['Short_MA'][data['Position'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    plt.title('Dow Jones Industrial Average with Buy/Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    ticker = '^DJI'
    start_date = '2023-01-01'
    end_date = '2024-10-01'
    short_window = 50
    long_window = 200

    data = fetch_data(ticker, start_date, end_date)
    data = calculate_moving_averages(data, short_window, long_window)
    data = generate_signals(data, short_window)
    plot_data(data)