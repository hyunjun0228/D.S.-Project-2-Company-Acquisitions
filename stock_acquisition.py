import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import clean_data_acq as cd

stock_info = pd.read_csv('stock.csv', index_col=0)
acquisitions = pd.read_csv('acquisitions.csv')
acquisitions_values = acquisitions[['AcquisitionID','Value (USD)']]
acquisitions_values = cd.extract_clean_values(acquisitions_values)

# Cleaned Data Set
acquisitions= cd.clean_data(acquisitions)

class Company_stock:
  # Take in string for the company_name and beginning year 
  def __init__(self, company_name, years):
    self.company_name = company_name
    self.company_df = stock_info[stock_info.company == company_name].copy()
    self.company_df['date'] = self.company_df['date'].apply(pd.to_datetime)
    date_begin = pd.to_datetime(str(years) + "-" + "01" + '-' + "01")
    self.company_df = self.company_df[self.company_df.date >= date_begin]
  
  def plot_stocks(self):
    ax = sns.lineplot(data=self.company_df, x='date', y='price', color='lightpink')
    ax.set_xlabel('Years')
    ax.set_ylabel("Stock Price ($)")
    ax.set_title(f"Change in Stock Prices of {str(self.company_name).capitalize()}")  
    return ax
    
  def plot_volume(self):
    sns.lineplot(data=self.company_df, x='date', y='volume', color='blue')
  
  def get_stock_years(self):
    return range(np.min(self.company_df['date'].dt.year), np.max(self.company_df['date'].dt.year) + 1)
  
  def get_stock_data(self):
    stock_data = self.company_df.groupby(self.company_df['date'].dt.year).price.mean().reset_index()
    return stock_data['price']


class Company_acq:
  def __init__(self, company_name):
    self.name = company_name
    self.acq = acquisitions[acquisitions.parentCompany == company_name]
  
  def get_companyName(self):
    return str(self.name)
  
  def get_year_count(self):
    range_of_years = range(self.acq['date'].dt.year.min(), self.acq['date'].dt.year.max() + 1)
    groupby_year = self.acq.groupby(self.acq['date'].dt.year).id.count().reset_index()
    for i in range_of_years:
      groupby_year = groupby_year.append({"date": i, "id": 0}, ignore_index = True)
    groupby_year = groupby_year.drop_duplicates(subset=['date'], keep='first')
    groupby_year = groupby_year.sort_values(by=['date']).reset_index(drop=True)
    return groupby_year['id']
  def plot_acquisitions(self, tickIntervals = None):
    range_of_years = range(self.acq['date'].dt.year.min(), self.acq['date'].dt.year.max() + 1)
    groupby_year = self.acq.groupby(self.acq['date'].dt.year).id.count().reset_index()
    for i in range_of_years:
      groupby_year = groupby_year.append({"date": i, "id": 0}, ignore_index = True)
    groupby_year = groupby_year.drop_duplicates(subset=['date'], keep='first')
    groupby_year = groupby_year.sort_values(by=['date']).reset_index(drop=True)

    ax = sns.barplot(data=groupby_year, x='date', y='id', color='lightblue', linewidth=1)
    ax.set_xlabel("Years")
    ax.set_ylabel("Number of Acquisitions")
    
    if tickIntervals is not None:
      ax.set_xticks(np.arange(min(ax.get_xticks()), max(ax.get_xticks()) + 1, tickIntervals))
    ax.set_title(f"Number of Acquisitions of {str(self.name)}")
    return ax

  def get_min_year(self):
    return np.min(self.acq['year'])
  
  def get_stock_name(self):
    return self.name.lower()

  def get_year_range(self):
    return np.arange(min(self.acq['year']), max(self.acq['year']) + 1, 1)






  





