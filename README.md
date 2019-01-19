# ny_election_data

Create A Single Dataframe Using Data From Multiple Websites

Shows how to use pandas to pull data from different web sources into a single dataframe. The data can then be used to predict a county's election outcome. 

First, we create a dataframe by pulling New York county election results from the NY Times website. Some of the county names were changed in order to match the names used by the other site. We add a label column in order to show the county's election outcome.

Next, we create a dictionary with field names as keys, and the URLs as the values. We then loop through the dictionary to create a dataframe with county data. 

Finally, we merge the two dataframes and add a label to each county. The dataframe can now be used for data analysis. We could create a list of state names to loop through (and insert the state name in the URL) in order to create a larger dataset.
