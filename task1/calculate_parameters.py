import pandas as pd
import numpy as np

trade_data = pd.read_csv('tradelog.csv', parse_dates = True) 

ticker_column = 'Ticker'
entry_time_column = 'Entry Time'
entry_price_column = 'Entry Price'
exit_time_column = 'Exit Time'
exit_price_column = 'Exit Price'

if len(trade_data) == 0:
    print("No trades found. Exiting.")
    exit()

total_trades = len(trade_data)
profitable_trades = len(trade_data[trade_data[exit_price_column] > trade_data[entry_price_column]])
loss_making_trades = len(trade_data[trade_data[exit_price_column] < trade_data[entry_price_column]])
win_rate = profitable_trades / total_trades
average_profit_per_trade = trade_data[trade_data[exit_price_column] > trade_data[entry_price_column]][exit_price_column].mean() - \
trade_data[trade_data[exit_price_column] > trade_data[entry_price_column]][entry_price_column].mean()

average_loss_per_trade = trade_data[trade_data[exit_price_column] < trade_data[entry_price_column]][entry_price_column].mean() - \
trade_data[trade_data[exit_price_column] < trade_data[entry_price_column]][exit_price_column].mean()

risk_reward_ratio = abs(average_profit_per_trade / average_loss_per_trade)
loss_rate = 1 - win_rate
expectancy = (win_rate * average_profit_per_trade) - (loss_rate * average_loss_per_trade)
risk_free_rate = 0.05  
average_ror_per_trade = (expectancy - risk_free_rate) / trade_data[exit_price_column].std()
sharpe_ratio = (expectancy - risk_free_rate) / trade_data[exit_price_column].std()
cumulative_returns = np.cumsum(trade_data[exit_price_column] - trade_data[entry_price_column])

if len(cumulative_returns) > 0:
    max_drawdown = np.max(np.maximum.accumulate(cumulative_returns) - cumulative_returns)
else:
    max_drawdown = 0
if len(cumulative_returns) > 0:
    max_drawdown_percentage = (max_drawdown / np.maximum.accumulate(cumulative_returns)) * 100
else:
    max_drawdown_percentage = 0
beginning_value = 6500  

if len(cumulative_returns) > 0:
    ending_value = cumulative_returns[1] + beginning_value
else:
    ending_value = beginning_value

num_periods = total_trades 
cagr = (ending_value / beginning_value) ** (1 / num_periods) - 1

if (max_drawdown_percentage != 0).any():
    calmar_ratio = cagr / max_drawdown_percentage
else:
    calmar_ratio = 0

# Write results to a text file
with open('parameters_results.txt', 'w') as file:
    file.write("Total Trades: {}\n".format(total_trades))
    file.write("Profitable Trades: {}\n".format(profitable_trades))
    file.write("Loss-Making Trades: {}\n".format(loss_making_trades))
    file.write("Win Rate: {}\n".format(win_rate))
    file.write("Average Profit per trade: {}\n".format(average_profit_per_trade))
    file.write("Average Loss per trade: {}\n".format(average_loss_per_trade))
    file.write("Risk Reward ratio: {}\n".format(risk_reward_ratio))
    file.write("Expectancy: {}\n".format(expectancy))
    file.write("Average ROR per trade: {}\n".format(average_ror_per_trade))
    file.write("Sharpe Ratio: {}\n".format(sharpe_ratio))
    file.write("Max Drawdown: {}\n".format(max_drawdown))
    file.write("Max Drawdown Percentage: {}\n".format(max_drawdown_percentage))
    file.write("CAGR: {}\n".format(cagr))
    file.write("Calmar Ratio: {}\n".format(calmar_ratio))

print("Results written to 'parameters_results.txt'")

# Create a DataFrame with the results
results_df = pd.DataFrame({
    'Total Trades': [total_trades],
    'Profitable Trades': [profitable_trades],
    'Loss-Making Trades': [loss_making_trades],
    'Win Rate': [win_rate],
    'Average Profit per trade': [average_profit_per_trade],
    'Average Loss per trade': [average_loss_per_trade],
    'Risk Reward ratio': [risk_reward_ratio],
    'Expectancy': [expectancy],
    'Average ROR per trade': [average_ror_per_trade],
    'Sharpe Ratio': [sharpe_ratio],
    'Max Drawdown': [max_drawdown],
    'Max Drawdown Percentage': [max_drawdown_percentage],
    'CAGR': [cagr],
    'Calmar Ratio': [calmar_ratio]
})

# Save results to a CSV file
results_df.to_csv('parameters_results.csv', index=False)
print("Results written to 'parameters_results.txt' and 'parameters_results.csv'")



