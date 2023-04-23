'''Reads the Births Data UN.csv file and creates a new dataframe with the total number of births per month and the percentage of births per month.'''
# Results saved in births_df: Both count and percentage

# Read data file and remove unnecessary columns & records
import pandas as pd
births_data=pd.read_csv('../data/Births Data UN.csv')
births_data.drop(['Area', 'Record Type', 'Value Footnotes', 'Source Year'],axis=1,inplace=True)
births_data=births_data.query("Month in ['January','February','March','April','May','June','July','August','September','October','November','December']")

# Groupby month and sum births
births_df=births_data.groupby('Month').sum()[['Value']]
births_df=births_df.reindex(['January','February','March','April','May','June','July','August','September','October','November','December'])
births_df.index=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
births_df['births_percentage']=(births_df['Value']/births_df['Value'].sum()*100).round(2)
births_df.rename(columns={'Value':'births_count'},inplace=True)