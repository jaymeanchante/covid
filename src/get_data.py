import pandas as pd

# reads from wikipedia
url = "https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_Brazil"
list_df = pd.read_html(url)
# select df
df = list_df[3].copy()
# subset columns and rows
df = df[[("Date", "Date"), ("Date", "Date.1"), ("South", "RS")]].copy()
df = df.iloc[:-4].copy()
# remove multiindex
df.columns = df.columns.droplevel(0)
df = df.rename(columns={"Date.1": "Type", "RS": "Number"}).copy()
# reshape data
df = pd.pivot(df, index="Date", columns="Type", values="Number").reset_index()
# fill na
df = df.fillna(0).copy()
# save to disk
df.to_csv("./data/covid_cases_deaths.csv", index=False)