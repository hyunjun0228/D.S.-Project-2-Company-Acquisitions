# This is a project outline:
# Key point: Acquisition of start-ups by huge enterprises shows us the direction in which these enterprises hope to marketize, and could display the current trend in the shift of the economic focus across different industries (ex. shift to environment-friendly industry, meta-verse, AR-VR industries, electric cars, etc.)

# Project Goal: I intend to analyze the acquisition of companies in recent years, how those companies have been doing, and the greatest factor in determining the success of the acquisitions. I will be using two datasets and combining them to utilize the data, in order to widen my perspective on the growth and acquisitions of companies. Some of the key points to look into are as follows:
#				How has certain huge acquisitions made an impact on the company's stock (and how has it changed over time)?
#				How does the acquisition of new companies correspond to the business strategies employed by those companies?
#				How does the revenue and sales relates to the acquisition?
#				What are some key factors that demonstrate the success of the acquisition (success rate of each company's acquisition)?

# Some strategies: When necessary (especially for graphing), I will group the 7 companies according to their specialized industry, Social Media Platform (Facebook, Twitter), Hardware Platform (Apple, IBM, Microsoft), and Search Engine (Google, Yahoo). Granted, these companies have grown so much that they exert power in multitude of different industries, but these are arguably the most fundamental industries each company was founded upon, and thrive the most in.
import pandas as pd
import clean_data_acq as cd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import stock_acquisition as stock_acq




pd.set_option('display.max_column', None)
acquisitions = pd.read_csv('acquisitions.csv')
# Separating the 'Value (USD)' column with the index column as 'AcquisitionID', since the 'Value (USD)' column has a lot of NaN values and we will thus examine this column separately
acquisitions_values = acquisitions[['AcquisitionID','Value (USD)']]
# acquisitions_values has 'id' and 'value' as its column from this point on
acquisitions_values = cd.extract_clean_values(acquisitions_values)

# Cleaned Data Set
acquisitions= cd.clean_data(acquisitions)
print(acquisitions.head())


# google_stock = stock.company_stock('google')
# microsoft_stock = stock.company_stock('microsoft')
# ibm_stock = stock.company_stock('ibm')
# facebook_stock = stock.company_stock('facebook')
# yahoo_stock = stock.company_stock('yahoo')
# twitter_stock = stock.company_stock('twitter')
def make_stock_object(acq_object):
  return stock_acq.Company_stock(acq_object.get_stock_name(), acq_object.get_min_year())

apple_acq = stock_acq.Company_acq('Apple')
apple_stock = make_stock_object(apple_acq)
google_acq = stock_acq.Company_acq('Google')
google_stock = make_stock_object(google_acq)
microsoft_acq = stock_acq.Company_acq('Microsoft')
microsoft_stock = make_stock_object(microsoft_acq)


def plot_stock_acq(acq_object, stock_object, x_intervals=None, y_intervals=None):
  sns.set_context('poster', font_scale=.6, rc={'grid.linewidth': 0.4})
  sns.set_style('darkgrid')

  fig, ax1 = plt.subplots(figsize=(10,8))
  ax1.bar(x=acq_object.get_year_range(), height=acq_object.get_year_count(), color = 'lightblue', linewidth=.5, label='Acquisitions')
  ax1.set_ylabel('Number of Acquisitions', fontsize=16, color='lightblue')
  ax1.set_xlabel('Years', fontsize=16, color='grey')
  ax1.tick_params(axis='y', colors='lightblue')
  ax1.tick_params(axis='x', colors='grey')
  if y_intervals != None:
    ax1.set_yticks([int(i) for i in range(acq_object.get_year_count().min(), acq_object.get_year_count().max() + y_intervals, y_intervals)])
  plt.legend(loc="upper left")  

  ax2 = ax1.twinx()
  color='lightpink'
  ax2.plot(stock_object.get_stock_years(), stock_object.get_stock_data(), color= color, linewidth=2, alpha=.8,label='Stock Price')
  ax2.set_ylabel('Stock Price ($)', color=color, fontsize=16)
  ax2.tick_params(axis='y', colors=color)
  ax2.tick_params(axis='x', colors='grey')
  if x_intervals != None:
    ax2.set_xticks(range(stock_object.get_stock_years()[0], stock_object.get_stock_years()[-1], x_intervals))
  plt.legend(loc="upper right")

  plt.title(f"Changes in Stock Price and Number of Acquisitions for {acq_object.get_companyName()}", fontsize=20)
  sns.despine()
  plt.tight_layout()
  plt.show()
  plt.clf()

