import pandas as pd

df = pd.read_excel("excel.xlsx", header=2)

print(df.head())  #print first 5 rows

print(df.columns) #print name of all the columns available

print(df.fillna(0,inplace=True))  #fillna finds out all the values automatically and replce with 0 in this case and inplace true is done so that our dataframe gets changed permanently

print(df.isnull().sum())  #prints the total number of null values in each columns

print(df.duplicated())  #checks if the rows are duplicated or not

print(df.columns.duplicated())  #checks if the columns are duplicated or not