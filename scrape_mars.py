
#Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA Mars News 
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Latest News 
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    #JPL Mars Space Images - Featured Image

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Featured Image 
    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = url + relative_image_path

    #Mars Facts Table 
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = df.iloc[0]
    comparison = df[1:]
    comparison.set_index('Mars - Earth Comparison')
    html_table = comparison.to_html()
    html_table.replace('\n', '')

    #Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    names = soup.find_all('div', class_='item')

    hemisphere = []

    for x in names: 
        itemtitle = x.find('div', class_='description').find('a').find('h3').text
        baseurl = x.find('a')['href']
        usgs_url = 'https://marshemispheres.com/'
        image_url = usgs_url + baseurl
        browser.visit(image_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find('div', class_='downloads').find('ul').find('li').find('a')['href']
        final_image = usgs_url + image
        hemisphere.append({'title':itemtitle, 'img_url':final_image})
        
    browser.quit()
    
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_facts': html_table,
        'hemisphere_images': hemisphere,
    }
    return mars_data
