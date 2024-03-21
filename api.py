import requests
import pygal
from pygal.style import LightStyle
from lxml import etree
from datetime import datetime

# Check date format
def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Get the data from Alpha Vantage
def fetch_stock_data(symbol, function, interval):
    api_key = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=TKD85DJRC6KNT94C'
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

# Generates the actual chart
def generate_chart(data, chart_type, function):
    if function == "1":
        function = "TIME_SERIES_INTRADAY"
        time_series_key = 'Time Series (5min)'
    elif function == "2":
        function = "TIME_SERIES_DAILY"
        time_series_key = 'Time Series (5min)'
    elif function == "3":
        function = "TIME_SERIES_WEEKLY"
        time_series_key = 'Time Series (5min)'
    else:
        function = "TIME_SERIES_MONTHLY"
        time_series_key = 'Time Series (5min)'
    # Extracting dates and closing prices from the data
    #if function == 'TIME_SERIES_INTRADAY':
    #    time_series_key = 'Time Series (5min)'
    #else:
    #    time_series_key = 'Time Series (Daily)'

    dates = list(data[time_series_key].keys())
    closing_prices = [float(data[time_series_key][date]['4. close']) for date in dates]

    # Pygal chart based on the user's input
    if chart_type == 'bar':
        chart = pygal.Bar(style=LightStyle)
    else:
        chart = pygal.Line(style=LightStyle)

    chart.title = 'Stock Prices Over Time'
    chart.x_labels = dates
    chart.add('Closing Price', closing_prices)
    
    return chart

# Render the chart in the browser
def render_chart(chart):
    svg_data = chart.render()
    svg_str = svg_data.decode('utf-8')  # Decode bytes to string
    html_data = '<html><head></head><body>' + svg_str + '</body></html>'

    # Creates an HTML file for the chart
    with open('stock_chart.html', 'w') as f:
        f.write(html_data)

    print("Chart has been saved as stock_chart.html, open in a browser to view it.")

# User inputs
print("\x1b[6;30;45m" + "Enter the stock symbol" + "\x1b[0m")
stock_symbol = input()

print("\x1b[6;30;42m" + "Chart types" + "\x1b[0m")
print("---------------")
print("1. Bar")
print("2. Line")
print("")

#While loop for input error checking
while True:
    print("\x1b[6;30;45m" + "Enter the chart type: " + "\x1b[0m")
    chart_type = input()
    if chart_type == "1" or chart_type == "2":
        break
    else:
        print("Invalid chart type.")

chart_type = "bar" if chart_type == "1" else "line"

print("\x1b[6;30;45m" + "Time series functions" + "\x1b[0m")
print("1. Intraday")
print("2. Daily")
print("3. Weekly")
print("4. Monthly")
time_series_function = input()

print("\x1b[6;30;45m" + "Enter the beginning date (YYYY-MM-DD)" + "\x1b[0m")
while True:
    begin_date = input()
    if validate_date(begin_date):
        break
    else:
        print("Invalid date format. Please enter in YYYY-MM-DD format.")

print("\x1b[6;30;45m" + "Enter the end date (YYYY-MM-DD):" + "\x1b[0m")
while True:
    end_date = input()
    if validate_date(end_date):
        if datetime.strptime(begin_date, '%Y-%m-%d') <= datetime.strptime(end_date, '%Y-%m-%d'):
            break
        else:
            print("The beginning date cannot be after the end date. Please try again.")
    else:
        print("Invalid date format. Please enter in YYYY-MM-DD format.")

# Fetching the data from Alpha Vantage
data = fetch_stock_data(stock_symbol, time_series_function, chart_type)

# Generate the chart
chart = generate_chart(data, chart_type, time_series_function)  # Passing time_series_function here

# Rendering the chart
render_chart(chart)
