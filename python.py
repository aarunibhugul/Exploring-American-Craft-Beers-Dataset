import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_beer = pd.read_csv("beers.csv")
df_brew = pd.read_csv("breweries.csv")

#--------Getting columns names-------#

beer_column_list = []
for col in df_beer.columns:
    beer_column_list.append(col)

breweries_column_list = []
for col in df_brew.columns:
    breweries_column_list.append(col)

#------renaming the unnamed column-----#
df_beer = df_beer.rename(columns={"Unnamed: 0":"row_count"})
df_brew = df_brew.rename(columns={"Unnamed: 0":"row_count"})

#--------setting index-----#

df_brew['brewery_id'] = df_brew.index


#---------merging two dataframes-----#
df = pd.merge(df_beer, df_brew, on = "brewery_id")
df.to_csv("merged.csv")

#################---------Cleaning the data------##################
df = df.rename(columns = {"name_x":"beer_name","name_y":"brewery_name"})

#--------dropping the unwanted columns-------#
df = df.drop(["row_count_x","row_count_y"], axis = 1)



#---------Checking for empty columns--------#
empty_column_list = []
for col in df.columns:
    if (df[col].isna().any()) == True:
        empty_column_list.append(col)

empty_numeric_column_list = []
empty_categorical_column_list = []
for col in empty_column_list:
    if (df[col].dtype == 'float64' or df[col].dtype == 'int64'):
        empty_numeric_column_list.append(col)
    else:
        empty_categorical_column_list.append(col)

#-----------filling the null columns----------#

#-----Numerical Columns---#
for i in empty_numeric_column_list:
    df[i] = df.fillna(df[i].mean())

#-----Categorical Columns-------#
mode_list = []
for i in empty_categorical_column_list:
    mode_list.append(df[i].mode())
for i in empty_categorical_column_list:
    df[i] = df[i].fillna("American IPA")

#-------------Exploratory Analysis---------##


#numer of breweries in top 10 cities
citywise_brewries = df.groupby('city')["brewery_name"].count().nlargest(10)
citywise_brewries.plot(kind='bar', title='Top 10 Cities with the Most Breweries')
plt.ylabel("Number of Breweries")
plt.savefig('Top 10 Cities with the Most Breweries')

# number of breweries per state
state_wise_brewries = df.groupby("state")["brewery_name"].count().nlargest(len(df['state']))
state_wise_brewries.plot(kind = 'bar', title = "State wise Brewery Count")
plt.ylabel("Number of Breweries")
plt.savefig('State wise Brewery Count')

#number of each style
style_frequency = df['style'].value_counts().nlargest(10)
style_frequency.plot(kind = 'bar', title = 'Count of each Beer styles')
plt.ylabel("Frequency")
plt.savefig('Count of each Beer styles')
# plt.show()

#Average alcohol brewed in each citywise_brewries
average_abv_city = df.groupby('city')['abv'].mean().nlargest(10)
