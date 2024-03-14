import requests

# Prompt for user inputs
print("\x1b[6;30;45mEnter the stock symbol\x1b[0m")
stock_symbol = input()

print("\x1b[6;30;42mChart types\x1b[0m")
print("---------------")
print("1. Bar")
print("2. Line")
chart_type = input("Enter the chart type (1 for Bar, 2 for Line): ")

# Validate chart type and convert to correct format for API call
if chart_type == "1":
    chart_type = "bar"
elif chart_type == "2":
    chart_type = "line"
else:
    print("Invalid chart type. Exiting program.")
    exit()

# Time series function mapping
print("\x1b[6;30;45mTime series functions\x1b[0m")
print("1. Daily")
print("2. Weekly")
time_series_input = input("Enter the time series function (1 for Daily, 2 for Weekly): ")
time_series_functions = {
    "1": "TIME_SERIES_DAILY",
    "2": "TIME_SERIES_WEEKLY"
}
time_series_function = time_series_functions.get(time_series_input)

if not time_series_function:
    print("Invalid time series function. Exiting program.")
    exit()

# Date inputs
begin_date = input("\x1b[6;30;45mEnter the beginning date (YYYY-MM-DD):\x1b[0m ")
end_date = input("\x1b[6;30;45mEnter the end date (YYYY-MM-DD):\x1b[0m ")

# Validate date order
if begin_date > end_date:
    print("The beginning date cannot be after the end date. Exiting program.")
    exit()

api_key = 'TKD85DJRC6KNT94C'

# API request URL
url = f"https://www.alphavantage.co/query?function={time_series_function}&symbol={stock_symbol}&apikey={api_key}"

# Make the API request
response = requests.get(url)
data = response.json()

# Check for errors in response
if 'Error Message' in data:
    print("Error from API:", data['Error Message'])
else:
    print(data)

# Placeholder for chart generation (not implemented in this script)
# $PLACEHOLDER$

