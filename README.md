# BudapestHousingPricePrediction

This projects purpose is to take publicly available data from ingatlan.com and build a machine learning model using the data to predict house prices

## Data collection 

The data is collected using the `ingatlan_com_webscraping.py` script, due to the bot detection on *ingatlan.com* it takes a lot of time to scrape data. The script is using selenium with 
[undetected chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver). With this method it takes around 6 hours to collect 100 pages of data, which means it takes around 
6 hours to collect data from around 2000 houses. The script saves the data to CSV files, and then it can be later processed. All of the data that I have collected so far are in the *datasets* folder.

## Data processing 

I have reduced the number of features, the script collects 31 features for each house including things like insulation, AC unit, Utility pricing etc. however a significant number of houses
on *ingatlan.com* have missing features, therefore I decided to reduce the number of features to the most important ones, and the ones that are more available. 

In some cases, I worked on the assumption that a person who is listing their house for sale would display all of the beneficial information in the advertisement, therefore if they did not specify
whether or not for example the building has an elevator I assume that it is beacuse it does not have one. 

## ML algorithm 

Due to the fact that this is a regression problem and I have structured data I experimented with some ensemble methods. Using RandomForestRegressor, I have achieved **82%** accuarcy *(on r2 score)* and **70%** accuracy on my cross validation mean score.


