import pandas as pd


# Cleans the dataset: Renames the columns, drops unnecessary columns, and fills in the missing values where appropriate
def clean_data(dataSet):
	dataSet = dataSet.rename(columns={'AcquisitionID': 'id', 'AcquisitionYear': 'year', 'Company':'comany_acquired', 'Business':'business', 'Country':'country', 'Derived products': 'products_derived', 'ParentCompany':'parentCompany'})
	dataSet = dataSet.drop(columns=['AcquisitionMonthDate', 'AcquisitionMonth', 'Value (USD)'])
	dataSet = dataSet.fillna(value={'products_derived': "None", "country": "None"})
	return dataSet

# Drops all rows where value column has NaN value
def extract_clean_values(dataSet):
	dataSet = dataSet.dropna()
	dataSet = dataSet.rename(columns={'Value (USD)': 'value', 'AcquisitionID': 'id'})
	return dataSet

# Cleaning 'YAHOO_original' file
def clean_yahoo_dataset():
  pd.set_option('display.max_column', None)
  df = pd.read_csv('yahoo_original.csv')
  df = df.drop_duplicates()
  df['Date'] = df.Date.str.replace('/','-')
  df = df[['Date', 'Close', 'Volume']]
  df.columns = map(str.lower, df.columns)
  df.to_csv('yahoo_18y.csv')

# Combine all the datasets and return a dataframe
def stock_data():
	apple = pd.read_csv('AAPL_33y.csv',index_col=0)
	fb = pd.read_csv('FB_9y.csv',index_col=0)
	google = pd.read_csv('GOOGL_15y.csv',index_col=0)
	ibm = pd.read_csv('IBM_21y.csv',index_col=0)
	ms = pd.read_csv('MSFT_35y.csv',index_col=0)
	tw = pd.read_csv('TWTR_8y.csv',index_col=0)
	yh = pd.read_csv('YAHOO_18y.csv',index_col=0)
	yh = yh[::7]

	comp_ls = [apple, fb, google, ibm, ms, tw, yh]
	comp_name = ['apple', 'facebook', 'google', 'ibm', 'microsoft', 'twitter', 'yahoo']
	for company, name in zip(comp_ls, comp_name):
		company['company'] = name
	all_combined = pd.concat(comp_ls).reset_index()
	all_combined= all_combined[['company', 'price','volume', 'date']]
	return all_combined

