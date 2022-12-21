# Rolling_Min_Max
This code contains a trading strategy that uses data from the Binance API to buy and sell cryptocurrency. It utilizes the pandas and numpy libraries to analyze the data and make decisions on when to buy and sell.

The strategy uses the rolling max and min of the high and low prices to calculate a midpoint, and then buys when the close price crosses above the midpoint. It sells when the close price approaches within 0.4% of the rolling max.

The strategy is demonstrated by applying it to ETHUSDT data and plotting the results along with buy and sell points. The resulting profit for each trade is also calculated and the total net profit is printed.

It is worth noting that this is a very simple trading strategy and is not intended to be used as a comprehensive investment strategy. It is provided as an example of how technical analysis can be used to develop a trading strategy, and should not be used to make actual trades without further analysis and consideration.
