import requests

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
#While loop to ensure user does not input an invalid chart type
while True:
    print("\x1b[6;30;45m" + "Enter the chart type: " + "\x1b[0m")
    chart_type = input()
    if chart_type == "1" or chart_type == "2":
        break
    else:
        print("Invalid chart type. Please try again.")

chart_type = "bar" if chart_type == "1" else "line"
print("")
print("\x1b[6;30;45m" + "Time series functions" + "\x1b[0m")
time_series_function = input()
print("")
print("\x1b[6;30;45m" + "Enter the beginning date (YYYY-MM-DD)" + "\x1b[0m")
begin_date = input()
print("")
print("\x1b[6;30;45m" + "Enter the end date (YYYY-MM-DD):" + "\x1b[0m")
end_date = input()
print("")
#While loop to ensure user doesnt input an end date that is before the beginning date DOESNT WORK RN I HAVE A FIX FOR IT
while True: 
    if begin_date > end_date:
        print("The beginning date cannot be after the end date. Please try again.")
        begin_date = input("Enter the beginning date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
    else:
        break

# Using inputs, creates the link w/ the API
url = f"https://www.alphavantage.co/query?function={time_series_function}&symbol={stock_symbol}&interval={chart_type}&apikey=TKD85DJRC6KNT94C"
r = requests.get(url)
data = r.json()

# Generate and open the graph in the user's default browser
# $PLACEHOLDER$
print(data)
