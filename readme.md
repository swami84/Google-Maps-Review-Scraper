Google Maps Restaurant Review Scraper
=====================================

###  

Description:
------------

This is a scraper to scrape restaurant reviews from Google Maps for restaurants
in high foot traffic census block groups

###  

### Steps

1.  Create a Google Places API using
    https://console.cloud.google.com/home/dashboard

2.  Write the api_key to a json (key = ‘google_api_key’) and store it as
    config.json in the config folder

3.  Download the webdriver for Chrome ensuring the same version as current
    Chrome installation

4.  Run the Review [Scraper
    Notebook](https://nbviewer.org/github/swami84/Google-Maps-Review-Scraper/blob/main/notebooks/Review%20Scraper.ipynb)

 

### Data

-   Restaurant data is acquired based on census block group foot traffic

-   Google Places API request requires location data (lat, lng) and radius of
    search. I have assumed that cbgs are circular and calculated radius from the
    area of cbg (available)

-   Output data includes the Census Block Group (restaurants withing radius of
    search), Restaurant Attributes (Restaurant type, Caption, Keywords) and
    Restaurant Reviews (User ID, Name, \# of Reviews)
