import requests
import pygal

def get_stock_data(symbol, function, apikey):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=TKD85DJRC6KNT94C'
    r = requests.get(url)
    data = r.json()
    return data

def plot_data(stock_data, chart_type):
    chart = pygal.Line() if chart_type == "line" else pygal.Bar()
    
    # Extracting data
    dates = []
    closing_prices = []
    for date_str, values in stock_data['Time Series (Daily)'].items():
        dates.append(datetime.strptime(date_str, '%Y-%m-%d'))
        closing_prices.append(float(values['4. close']))
    
    # Adding data to chart
    chart.x_labels = [date.strftime('%Y-%m-%d') for date in dates]
    chart.add('Closing Price', closing_prices)
    
    # Rendering chart
    chart.render_in_browser()


def main():
    apikey = 'TKD85DJRC6KNT94C'

    # Start of user inputs
    print("\x1b[6;30;45m" + "Enter the stock symbol" + "\x1b[0m")

    stock_symbol = input()
    
    print("\x1b[6;30;42m" + "Chart types" + "\x1b[0m")
    print("---------------")
    print("1. Bar")
    print("2. Line")
    print("")
    
    #While loop to ensure user does not input an invalid chart type
    while True:
        print("\x1b[6;30;45m" + "Enter the chart type: " + "\x1b[0m")
        chart_type = input()
        if chart_type == "1" or chart_type == "2":
            break
        else:
            print("Invalid chart type. Please try again.")
    
    chart_type = "bar" if chart_type == "1" else "line"
    
    print("\x1b[6;30;45m" + "Time series functions" + "\x1b[0m")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    
    #While loop to ensure user does not input an invalid time series function
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
    
    # Validate date range
    while True: 
        if begin_date > end_date:
            print("The beginning date cannot be after the end date. Please try again.")
            begin_date = input("Enter the beginning date (YYYY-MM-DD): ")
            end_date = input("Enter the end date (YYYY-MM-DD): ")
        else:
            break
    
    # Fetch data from API
    stock_data = get_stock_data(stock_symbol, time_series_function, apikey)
    
    # Plot the data
    plot_data(stock_data, chart_type)

if __name__ == "__main__":
    main()
