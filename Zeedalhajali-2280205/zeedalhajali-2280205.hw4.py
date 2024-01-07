file = open('orcl.csv', 'r')

# Read the data
data = [dict(zip(file.readline().strip().split(','), line.strip().split(','))) for line in file]

file.close()

# Print the first 5 rows
for row in data:
    print(row)


#TASK 2
file = open('orcl.csv', 'r')

columns = file.readline().strip().split(',')

# Read the rest of the data
data = []
for lines in file:
    values = lines.strip().split(',')
    row = dict(zip(columns, values))
    data.append(row)

# Close the file
file.close()

# Get the closing prices
prices = [float(row['Close']) for row in data]

# Calculate 5-day SMA
sma_5 = [sum(prices[i:i + 5]) / 5 for i in range(len(prices) - 4)]

# Calculate 14-day RSI
changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
gains = [max(change, 0) for change in changes]
losses = [max(-change, 0) for change in changes]
rsi_14 = [100 - 100 / (1 + sum(gains[i:i + 14]) / sum(losses[i:i + 14])) for i in range(len(gains) - 13)]

# Print the first 5 values of 5-day SMA and 14-day RSI
print("5-day SMA:", sma_5)
print("14-day RSI:", rsi_14)

#TASK 3
import csv

# Function to calculate Simple Moving Average (SMA)
def calculate_sma(data, window):
    return sum(data[-window:]) / window

# Function to calculate Relative Strength Index (RSI)
def calculate_rsi(data, window):
    gains = losses = 0
    # Calculate gains and losses for the last 'window' elements
    for i in range(1, window+1):
        change = data[-i] - data[-i-1]
        if change > 0:
            gains += change
        elif change < 0:
            losses += abs(change)
    rs = gains / losses if losses else 0
    # Calculate RSI
    return 100 - (100 / (1 + rs))

# Open the input CSV file and output CSV files
with open('orcl.csv', 'r') as f, open('orcl-sma.csv', 'w') as f_sma, open('orcl-rsi.csv', 'w') as f_rsi:
    reader = csv.reader(f)
    headers = next(reader)
    closing_prices = [float(row[headers.index('Close')]) for row in data]
    writer_sma = csv.writer(f_sma)
    writer_rsi = csv.writer(f_rsi)
    # Write headers to the output CSV files
    writer_sma.writerow(['Date', 'SMA'])
    writer_rsi.writerow(['Date', 'RSI'])
    # Calculate SMA and RSI for each data point and write to the output CSV files
    for i in range(len(data)):
        if i >= 14:  # We use a 14-day window for SMA and RSI
            sma = calculate_sma(closing_prices[:i+1], 14)
            rsi = calculate_rsi(closing_prices[:i+1], 14)
            writer_sma.writerow([data[i][headers.index('Date')], sma])
            writer_rsi.writerow([data[i][headers.index('Date')], rsi])


