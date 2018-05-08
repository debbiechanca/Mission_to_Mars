# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
from selenium import webdriver

def scrape():
    mars_data = {}

    # find button and click it to start data scaping
    # button = browser.find_by_name("button")
    # button.click()
    # time.sleep(2)

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. Assign the text to variables 
    # that you can reference later.

    # URL of NASA Mars News Site
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    html = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html.text, 'html.parser')

    # Save 'content_title' section in an iterable list
    result = soup.find('div', class_='content_title')
    news_title = result.a.text.strip()
    
    news_link = result.find('a').get('href')    
    url = 'https://mars.nasa.gov' + news_link
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    result = soup.find('div', class_='wysiwyg_content') 
    news_p = result.find('p').text.strip()  

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

 # JPL Mars Space Images - Featured Image
    # Visit the url for JPL's Featured Space Image here.
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Make sure to find the image url to the full size .jpg image.
    # Make sure to save a complete url string for this image.

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    string = soup.article.get('style')
    string
    image_url = string.split("url('/")[1].split("');")[0]
    featured_image_url = "https://www.jpl.nasa.gov/" + image_url

    mars_data["featured_image_url"] = featured_image_url

    # Mars Weather
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called mars_weather.
    url = 'https://twitter.com/marswxreport?lang=en'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    result = soup.find('div', class_='js-tweet-text-container')
    mars_weather = result.find_next('p').text.strip()

    mars_data["weather"] = mars_weather

    # Mars Facts 
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.
    url = 'https://space-facts.com/mars/'
    df = pd.read_html(url)[0]
    df = df.set_index(0).rename(columns={1:"value"})
    del df.index.name
    html_table = df.to_html()

    # Strip unwanted newlines to clean up the table.
    html_table.replace('\n', '')    
    mars_data["facts"] = html_table

# Mars Hemispheres
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere 
# name. Use a Python dictionary to store the data using the keys img_url and title.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for
# each hemisphere.
    hemisphere_image_urls = []

    url_list = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']

    for url in url_list:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
    
        result = soup.find('div', class_='content')
        title = result.find('h2').text
    
        result = soup.find('div', class_='downloads')
        image_url = result.li.find('a').get('href')

        hemisphere_image_url = {"title": title, "img_url": image_url}
        hemisphere_image_urls.append(hemisphere_image_url)

    # return mars data dictionary
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data