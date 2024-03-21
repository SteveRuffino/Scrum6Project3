import requests
import webbrowser
import os
from lxml import etree
import pygal

def get_user_input():
    print("\x1b[6;30;45m" + "Enter the stock symbol" + "\x1b[0m")
    stock_symbol = input()

    print("\x1b[6;30;42m" + "Chart types" + "\x1b[0m")
    print("---------------")
    print("1. Bar")
    print("2. Line")
    print("")
    chart_type = input_chart_type()

    print("\x1b[6;30;45m" + "Time series functions" + "\x1b[0m")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    time_series_function = input_time_series_function()

    print("\x1b[6;30;45m" + "Enter the beginning date (YYYY-MM-DD)" + "\x1b[0m")
    begin_date = input_date()

    print("\x1b[6;30;45m" + "Enter the end date (YYYY-MM-DD):" + "\x1b[0m")
    end_date = input_date()

    while begin_date > end_date:
        print("The beginning date cannot be after the end date. Please try again.")
        begin_date = input_date("Enter the beginning date (YYYY-MM-DD): ")
        end_date = input_date("Enter the end date (YYYY-MM-DD): ")

    return stock_symbol, chart_type, time_series_function, begin_date, end_date

def input_chart_type():
    while True:
        print("\x1b[6;30;45m" + "Enter the chart type: " + "\x1b[0m")
        chart_type = input()
        if chart_type in ["1", "2"]:
            return "bar" if chart_type == "1" else "line"
        else:
            print("Invalid chart type. Please try again.")

def input_time_series_function():
    while True:
        print("\x1b[6;30;45m" + "Enter the time series function: " + "\x1b[0m")
        time_series_function = input()
        if time_series_function in ["1", "2", "3", "4"]:
            if time_series_function == "1":
                return "TIME_SERIES_INTRADAY"
            elif time_series_function == "2":
                return "TIME_SERIES_DAILY"
            elif time_series_function == "3":
                return "TIME_SERIES_WEEKLY"
            else:
                return "TIME_SERIES_MONTHLY"
        else:
            print("Invalid time series function. Please try again.")

def input_date(prompt=""):
    while True:
        date = input(prompt)
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print("Incorrect date format, should be YYYY-MM-DD")

def fetch_stock_data(stock_symbol, time_series_function):
    url = f"https://www.alphavantage.co/query?function={time_series_function}&symbol={stock_symbol}&interval=5min&apikey=TKD85DJRC6KNT94C"
    r = requests.get(url)
    return r.content

def filter_data_by_date(xml_content, begin_date, end_date):
    root = etree.fromstring(xml_content)
    timeseries = root.find('.//TIME_SERIES_INTRADAY')
    filtered_dates = []
    filtered_values = []
    for child in timeseries:
        date = child.attrib['datetime']
        if begin_date <= date <= end_date:
            filtered_dates.append(date)
            filtered_values.append(float(child.find('.//close').text))
    return filtered_dates, filtered_values

def generate_and_show_chart(stock_symbol, chart_type, filtered_dates, filtered_values, begin_date, end_date):
    chart_title = f'Stock Prices for {stock_symbol} from {begin_date} to {end_date}'
    if chart_type == 'line':
        chart = pygal.Line(title=chart_title, x_label_rotation=45)
    else:
        chart = pygal.Bar(title=chart_title, x_label_rotation=45)

    chart.x_labels = filtered_dates
    chart.add('Close Price', filtered_values)
    chart.render_to_file('stock_chart.svg')
    webbrowser.open('file://' + os.path.abspath('stock_chart.svg'))

def main():
    stock_symbol, chart_type, time_series_function, begin_date, end_date = get_user_input()
    xml_content = fetch_stock_data(stock_symbol, time_series_function)
    filtered_dates, filtered_values = filter_data_by_date(xml_content, begin_date, end_date)
    generate_and_show_chart(stock_symbol, chart_type, filtered_dates, filtered_values, begin_date, end_date)

if __name__ == "__main__":
    main()
