Google Maps Restaurant Review Scraper
=====================================

###  

Description:
------------

This is a scraper to scraper user reviews for restaurants from Google Maps using
the foot traffic data provided by Safegraph on census block group level (cbg).

###  

### Steps

1.  Create a Google Places API using
    https://console.cloud.google.com/home/dashboard

2.  Write the api_key to a json (key = ‘google_api_key’) and store it as
    config.json in the config folder

3.  Download the webdriver for Chrome ensuring the same version as current
    Chrome installation

4.  Run the Review Scraper Notebook

 

### Data

-   Restaurant data is acquired on census block groups based on high foot
    traffic data

-   Output data includes the Census Block Group (restaurants withing radius of
    search), Restaurant Attributes (Restaurant type, Caption, Keywords) and
    Restaurant Reviews (User ID, Name, \# of Reviews)
