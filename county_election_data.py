# -*- coding: utf-8 -*-
"""
Creates a dataframe that contains 2016 election results, and data for counties in New York State
@author: JWackerow
"""

import pandas as pd
import requests

# create a dictionary in order to store URLs for different types of New York county data
county_data_urls = { "College": "http://www.indexmundi.com/facts/united-states/quick-facts/new-york/percent-of-people-25-years-and-over-with-bachelors-degree-or-higher#table", 
                     "Pop_Density": "https://www.indexmundi.com/facts/united-states/quick-facts/new-york/population-density#table",
                     "Income" : "https://www.indexmundi.com/facts/united-states/quick-facts/new-york/income-per-capita#table",
                     "White %" : "https://www.indexmundi.com/facts/united-states/quick-facts/new-york/white-not-hispanic-population-percentage#table"}

# website address used to pull election results for New York counties
url = "https://www.nytimes.com/elections/2016/results/new-york"

# create dataframe for of election results for counties in New York
def election_dataframe(url):
    html = requests.get(url).content
    df_election = pd.read_html(html)[1]
    df_election.rename(columns={"Vote by county":"County"}, inplace=True)
    # Add a column to show the county's election result
    df_election["Label"] = df_election.apply(label_result, axis=1)
    # once the election result column (label) has been created we can drop the Clinton / Trump columns
    df_election.drop(['Clinton', 'Trump'], axis=1, inplace=True)
    # Change names of counties that were labeled incorrectly on the website so they match the names in our other dataframes. 
    df_election["County"].replace({"Brooklyn":"Kings", "Manhattan":"New York", "Staten Island":"Richmond", "Saint Lawrence": "St. Lawrence"}, inplace=True)    
    return df_election
                  
# Creates a dataframe with a specific data field for NY counties.
def get_county_data(field):
    html = requests.get(county_data_urls[field]).content
    df = pd.read_html(html)[0]
    df.set_index("County", inplace=True)
    # rename the column header to the field name
    df = df.rename(columns={"Value": field})
    return df

def create_county_data_dataframe():
    # Create a list of dataframes by looping through data URLs in the county_data_path dictionary. I use pandas concat to return a single dataframe.
    county_dataframes = []
    for key in county_data_urls.keys():
        county_dataframes.append(get_county_data(key))
    return pd.concat(county_dataframes, axis=1)

# Labels the county's election result as 0 for Trump or 1 for Clinton
def label_result(row):
    if row["Clinton"] < row["Trump"]:
        return 0
    else:
        return 1

# Merge the election results with the county data
df_ny_data = pd.merge(election_dataframe(url), create_county_data_dataframe(), right_index=True, left_on="County")
# print to review your data
print(df_ny_data)