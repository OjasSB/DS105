'''This module contains utility functions, variables, and data structures for use in the notebooks.'''

import pandas as pd

#------------------------------------Top and bottom countries of indices------------------------------------

# UN Indices Data:
indices_data=pd.read_csv('../data/UN HDR all indices data.csv')
indices_data=indices_data[['country','hdi_2021','le_2021','eys_2021','mys_2021','gnipc_2021', 'gdi_2021','ihdi_2021','coef_ineq_2021','region']]

high_hdi=indices_data[indices_data['hdi_2021']>0.8]['country'].tolist()
low_hdi=indices_data[indices_data['hdi_2021']<0.7]['country'].tolist()

top_50_mys=indices_data.sort_values(by=['mys_2021'], ascending=False).head(50)['country'].tolist()
bottom_50_mys=indices_data.sort_values(by=['mys_2021'], ascending=True).head(50)['country'].tolist()

#------------------------------------Income groups------------------------------------

# World Bank Data:
wb_data=pd.read_csv('../data/income_data.csv')

low_income=wb_data[wb_data['Income group']=='Low income']['Country'].tolist()
high_income=wb_data[wb_data['Income group']=='High income']['Country'].tolist()