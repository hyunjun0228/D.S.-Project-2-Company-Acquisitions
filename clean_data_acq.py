import pandas as pd

def month_to_num(month_name):
	month = {'jan': 1, 'feb':2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
	return month[month_name.strip()[:3].lower()]

# Cleans the dataset: Renames the columns, drops unnecessary columns, and fills in the missing values where appropriate
def clean_data(dataSet):
	dataSet = dataSet.rename(columns={'AcquisitionID': 'id', 'AcquisitionYear': 'year', 'Company':'comany_acquired', 'Business':'business', 'Country':'country', 'Derived products': 'products_derived', 'ParentCompany':'parentCompany'})
	dataSet['AcquisitionMonth'] = dataSet['AcquisitionMonth'].apply(lambda x: 'January' if x != x else x)
	dataSet['AcquisitionMonthDate'] = dataSet['AcquisitionMonthDate'].apply(lambda x: 1 if x !=x else x)
	dataSet['AcquisitionMonth'] = dataSet['AcquisitionMonth'].apply(month_to_num)
	dataSet['date'] = dataSet.apply(lambda x: str(x.year) + '-' + str(x.AcquisitionMonth) + '-' + str(int(x.AcquisitionMonthDate)), axis=1)
	dataSet['date'] = dataSet['date'].apply(pd.to_datetime)
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
	df['Date']= df.Date.str.replace('/','-')
	str_split = df['Date'].str.split('-', expand=True)
	str_split[2] = str_split[2].apply(lambda x: "19" + x if x== "99" else "20" + x)
	df['Date'] = str_split[2] + '-' + str_split[0] + '-' + str_split[1]
	df = df[['Date', 'Close', 'Volume']]
	df.columns = map(str.lower, df.columns)
	df = df.rename(columns={'close': 'price'})
	df = df.reindex(index=df.index[::-1]).reset_index(drop=True)
	# Accounting for the stock splits
	df.loc[2:, 'price'] = df['price'] * 2
	df.loc[256:, 'price'] = df['price'] * 2
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
	yh = yh[::31]

	comp_ls = [apple, fb, google, ibm, ms, tw, yh]
	comp_name = ['apple', 'facebook', 'google', 'ibm', 'microsoft', 'twitter', 'yahoo']
	for company, name in zip(comp_ls, comp_name):
		company['company'] = name
	all_combined = pd.concat(comp_ls).reset_index()
	all_combined= all_combined[['company', 'price','volume', 'date']]
	all_combined['date'] = all_combined['date'].apply(pd.to_datetime)
	all_combined.to_csv('stock.csv')
	return all_combined

