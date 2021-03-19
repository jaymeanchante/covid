from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pandas as pd

## covid cases and deaths
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

## mobility index
# reads from google
url = "https://www.gstatic.com/covid19/mobility/Region_Mobility_Report_CSVs.zip"
resp = urlopen(url)
zipfile = ZipFile(BytesIO(resp.read()))
f = "2020_BR_Region_Mobility_Report.csv"
df = pd.read_csv(zipfile.open(f))
# subset and format the data
df = df.loc[df["iso_3166_2_code"] == "BR-RS",].iloc[:, -7:].copy()
df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)
df = df.rename(columns={i: i.replace("_percent_change_from_baseline", "") for i in df.columns}).copy()
# save to disk
df.to_csv("./data/mobility_index.csv", index=False)