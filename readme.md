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

2.  Store the api in a json (key = ‘google_api_key’) and store it as config.json

3.  Run the cbg rest etl ,  rest attr etl and review scraper etl

 

### Data

-   Restaurant data is acquired on census block groups based on high foot
    traffic data

-   Reviews are scraped from maps and only 80% of reviews are taken where total
    reviews \> 500
