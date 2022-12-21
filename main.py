import pandas as  pd 
import numpy as np
from binance import Client
import matplotlib.pyplot as plt

# Initialize the Binance client
client = Client()

def getdata(symbol, interval='1h', lookback='400'):
    # Get historical data for the given symbol and time interval
    frame = pd.DataFrame(client.get_historical_klines(symbol,
                                                     interval,
                                                    lookback+' hours UTC'))
    # Select the relevant columns and set the 'Time' column as the index
    frame = frame.iloc[:,0:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame.set_index('Time', inplace=True)
    # Convert the index to datetime and cast the data to float
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame

# Get data for ETHUSDT
df = getdata('ETHUSDT')

# Calculate the rolling max and min of the high and low prices
df['rollhigh'] = df.High.rolling(15).max()
df['rolllow'] = df.Low.rolling(15).max()
# Calculate the midpoint
df['mid'] = (df.rollhigh + df.rolllow)/2
# Create a column indicating whether the close price is within 0.4% of the rolling max
df['highapproach'] = np.where(df.Close > df.rollhigh * 0.996, 1, 0)
# Create a column indicating whether the close price is above the midpoint
df['close_a_mid'] = np.where(df.Close > df.mid, 1, 0)
# Create a column indicating whether the close price has crossed above the midpoint
df['midcross'] = df.close_a_mid.diff() == 1 

# Initialize the in_position flag and lists to store buy and sell dates
in_position = False
buydates,selldates = [], []

# Loop through each row in the DataFrame
for i in range(len(df)):
    # If we are not in a position, check if we should buy
    if not in_position:
        if df.iloc[i].midcross:
            buydates.append(df.iloc[i+1].name)
            in_position = True

    # If we are in a position, check if we should sell
    if in_position:
        if df.iloc[i].highapproach:
            selldates.append(df.iloc[i+1].name)
            in_position = False

# Plot the results
plt.figure(figsize=(20,10))
plt.plot(df[['Close', 'rollhigh', 'rolllow', 'mid']])
plt.scatter(buydates, df.loc[buydates].Open, marker='8', color='g', s=200)
plt.scatter(selldates, df.loc[selldates].Open, marker='8', color='r', s=200)

# Create a DataFrame to store the buy and sell dates and prices
tradesdf = pd.DataFrame( [buydates,selldates,df.loc[buydates].Open, df.loc[selldates].Open]).T
# Set column names for the DataFrame
tradesdf.columns = ['buydates', 'selldates', 'buyprices', 'sellprices']
# Drop rows with missing values (NaN)
tradesdf.dropna(inplace=True)
# Calculate relative profit for each trade
tradesdf['profit_rel'] = (tradesdf.sellprices - tradesdf.buyprices)/tradesdf.buyprices
# Calculate total net profit by summing the values in the 'net_profit' column
tradesdf['net_profit'] = tradesdf.sellprices - tradesdf.buyprices
total_net_profit = tradesdf['net_profit'].sum()
# Print the results
tradesdf