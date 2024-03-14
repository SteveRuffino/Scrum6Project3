import requests
import plotly.graph_objs as go
import plotly.offline as pyo
import webbrowser
import os

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=TKD85DJRC6KNT94C'
r = requests.get(url)
data = r.json()

# Start of user inputs
print("\x1b[6;30;45m" + "Enter the stock symbol" + "\x1b[0m")
stock_symbol = input()
print("\x1b[6;30;42m" + "Chart types" + "\x1b[0m")
print("---------------")
print("1. Bar")
print("2. Line")
print("")
# While loop to ensure user does not input an invalid chart type
while True:
    print("\x1b[6;30;45m" + "Enter the chart type: " + "\x1b[0m")
    chart_type = input()
    if chart_type in ["1", "2"]:
        break
    else:
        print("Invalid chart type. Please try again.")

chart_type = "bar" if chart_type == "1" else "line"

print("\x1b[6;30;45m" + "Time series functions" + "\x1b[0m")
print("1. Intraday")
print("2. Daily")
print("3. Weekly")
print("4. Monthly")
while True:
    print("\x1b[6;30;45m" + "Enter the time series function: " + "\x1b[0m")
    time_series_function = input()
    if time_series_function in ["1", "2", "3", "4"]:
        break
    else:
        print("Invalid time series function. Please try again.")

if time_series_function == "1":
    time_series_function = "TIME_SERIES_INTRADAY"
elif time_series_function == "2":
    time_series_function = "TIME_SERIES_DAILY"
elif time_series_function == "3":
    time_series_function = "TIME_SERIES_WEEKLY"
else:
    time_series_function = "TIME_SERIES_MONTHLY"

print("\x1b[6;30;45m" + "Enter the beginning date (YYYY-MM-DD)" + "\x1b[0m")
begin_date = input()
print("\x1b[6;30;45m" + "Enter the end date (YYYY-MM-DD):" + "\x1b[0m")
end_date = input()

while True: 
    if begin_date > end_date:
        print("The beginning date cannot be after the end date. Please try again.")
        begin_date = input("Enter the beginning date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
    else:
        break

# Using inputs, creates the link w/ the API
url = f"https://www.alphavantage.co/query?function={time_series_function}&symbol={stock_symbol}&interval=5min&apikey=TKD85DJRC6KNT94C"
r = requests.get(url)
data = r.json()

# Generate and open the graph in the user's default browser
# Extracting the data for the graph
timeseries_key = list(data.keys())[1]
timeseries = data[timeseries_key]

dates = []
values = []
for date, value in timeseries.items():
    dates.append(date)
    values.append(float(value['4. close']))  # You might need to adjust this based on the actual data structure

if chart_type == 'line':
    trace = go.Scatter(x=dates, y=values, mode='lines')
else:
    trace = go.Bar(x=dates, y=values)

data = [trace]
layout = go.Layout(title=f'Stock Prices for {stock_symbol}')
fig = go.Figure(data=data, layout=layout)

# Save the chart as an HTML file and open it
file_name = 'stock_chart.html'
file_path = os.path.join(os.getcwd(), file_name)  # Get the full path of the file
pyo.plot(fig, filename=file_path, auto_open=False)

if not webbrowser.open('file://' + file_path):  # Use the full file path
    try:
        webbrowser.open_new('file://' + file_path)
    except:
        try:
            webbrowser.open_new_tab('file://' + file_path)
        except Exception as e:
            print(f"Failed to open the browser: {e}")
