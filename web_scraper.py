import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
import json
import csv
from io import StringIO
import numpy as np

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
url_stocks = "https://query1.finance.yahoo.com/v7/finance/download/{}"
url_stats = "https://finance.yahoo.com/quote/{}/key-statistics?p={}"
url_profile = "https://finance.yahoo.com/quote/{}/profile?p={}"
url_financials = "https://finance.yahoo.com/quote/{}/financials?p={}"

# Takes in a company's stock market symbols and range in a string format, and creates a csv file that contains information about the historical stock data with an interval of a week, and returns a DataFrame containing the information
def make_stocks_file(symbol, range='10y'):
  params = {
    'range' : range,
    'interval': '1wk',
    'events': 'history'
  }
  response = requests.get(url_stocks.format(symbol), params=params, headers=headers)
  file = StringIO(response.text)
  reader = csv.reader(file)
  data = list(reader)
  data = np.array(data)
  stock_df = pd.DataFrame({'date':[], 'price':[], 'volume':[]})
  stock_df['date'] = data[1:, 0]
  stock_df['price'] = data[1:, 3]
  stock_df['volume'] = data[1:, 6]
  stock_df.to_csv(f'{symbol}_{range}.csv')
  return

# Takes in the company symbol, and returns some key statistics of the company as a DataFrame
def get_company_statistics(symbol):
  response = requests.get(url_stats.format(symbol, symbol), headers=headers)
  soup = bs(response.text, "html.parser")
  pattern = re.compile(r'\s--\sData\s--\s')
  script_data = soup.find('script', text=pattern).contents[0]
  start = script_data.find("context")-2
  json_data = json.loads(script_data[start:-12])
  important_data = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']
  return pd.DataFrame(important_data)

# Takes in the company symbol, and returns the company officers' information, such as pay, stauts, etc.
def get_company_officers(symbol):
  response = requests.get(url_profile.format(symbol, symbol), headers=headers)
  soup = bs(response.text, "html.parser")
  pattern = re.compile(r'\s--\sData\s--\s')
  script_data = soup.find('script', text=pattern).contents[0]
  start = script_data.find("context")-2
  json_data = json.loads(script_data[start:-12])
  important_data = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['companyOfficers']
  return pd.DataFrame(important_data)
 
 # Takes in the company symbol, and returns the company SEC Filings and a link to a webpage that shows the information in more detail
def get_company_secFilings(symbol):
  response = requests.get(url_profile.format(symbol, symbol), headers=headers)
  soup = bs(response.text, "html.parser")
  pattern = re.compile(r'\s--\sData\s--\s')
  script_data = soup.find('script', text=pattern).contents[0]
  start = script_data.find("context")-2
  json_data = json.loads(script_data[start:-12])
  important_data = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['secFilings']['filings']
  return pd.DataFrame(important_data)

# Takes in the company symbol, and returns the annual income staemenet, cash flow, and balansheet of the company and returns each of those three as a dataframe
def get_is_cf_bs_annual(symbol):
  response = requests.get(url_financials.format(symbol, symbol), headers=headers)
  soup = bs(response.text, "html.parser")
  pattern = re.compile(r'\s--\sData\s--\s')
  # Grabbing the first item in the list
  script_data = soup.find('script', text=pattern).contents[0]
  # Front end we use the word "context"
  start = script_data.find("context") - 2
  json_data = json.loads(script_data[start:-12])
  annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
  annual_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
  annual_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
  annual_is_stmts = []
  annual_cf_stmts = []
  annual_bs_stmts = []  
  for s in annual_is:
    statement = {}
    for key, val in s.items():
        try:
          statement[key] = val['raw']
        except TypeError:
           continue
        except KeyError:
          continue
    annual_is_stmts.append(statement)
  for s in annual_cf:
    statement = {}
    for key, val in s.items():
        try:
          statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    annual_cf_stmts.append(statement)
  for s in annual_bs:
    statement = {}
    for key, val in s.items():
      try:
        statement[key] = val['raw']
      except TypeError:
          continue
      except KeyError:
          continue
    annual_bs_stmts.append(statement)
  return pd.DataFrame(annual_is_stmts), pd.DataFrame(annual_cf_stmts), pd.DataFrame(annual_bs_stmts)





