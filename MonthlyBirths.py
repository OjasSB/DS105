def monthly_births(country, year):
    import pandas as pd
    df=pd.read_csv('Births Data UN.csv')
    df=df[df['Country or Area']==country]
    df=df[df['Year']==year]
    births=df['Value']/df.iloc[0]['Value']
    births=births*100
    births=round(births,2)
    births=list(births)[1:13]
    return births

