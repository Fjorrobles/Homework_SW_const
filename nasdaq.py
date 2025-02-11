#2568689
"""
Using urllib and json to get values from the NASDAQ website for 4 different companies 
over the last five years and comparing the closing price data.
"""
import urllib.request
import json 
#using regular expressions to search through data and store it in a variable
import re 
def download_data(ticker: str) -> dict:
    '''dowloading data from the NASDAQ website to view the Min, Max, Avg, Medium, and Ticker'''
    URL = f'https://www.nasdaq.com/market-activity/stocks/{ticker}/historical'

    try:
        #using the library to open the link and read the data
        with urllib.request.urlopen(URL) as response:
            html = response.read().decode()
        
        #data in this website is specific so we need to find all rows of data (asked ChatGPT)
        data = r'\"close\":\"([\d\.]+)\"'
        #turning the data from the website into a html file
        closing_prices = re.findall(data, html)
      
        #need to convert the list of strings into floats
        closing_prices = [float(price) for price in closing_prices]

        if closing_prices:   
            # Calculate min, max, avg, and median
            stock_summary = {
                'min': min(closing_prices),
                'max': max(closing_prices),
                'avg': sum(closing_prices) / len(closing_prices),
                'medium': max(closing_prices) - min(closing_prices),
                'ticker': ticker
            }

            return stock_summary
        else:
            print("Error: No closing prices were found")
            return None
    #output an error message if the attempt to find the information from the url doesn't work
    except IOError as e:
        print(e)
    return{}

#saving the data into a json file (also had ChatGPT help)
def save_json(data: dict):
    '''Putting the stock_summary data into a json file'''
    with open('stocks.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    print("Data saved to stocks.json")

#Using 4 different ticker inputs to find data
ticker = ['AAPL','MSFT','GOOGL','TSLA'] 
data_total = {}

for stock in ticker:
    data = download_data(stock)
    if data:
        data_total[stock] = data

save_json(data_total)
