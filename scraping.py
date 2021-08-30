#!/usr/bin/env python
# coding: utf-8
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt 

def scrape_all():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    #the **executable_path is just unpacking a suitcase
    # headless=false means that all of the browser's actions will be displayed in a Chrome window so we can see them
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph= mars_news(browser)
    hemisphere_image_urls= hemisphere(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere(browser),
        "last_modified": dt.datetime.now()}
       # Stop webdriver and return data
    browser.quit()
    return data

#we will be using the browser variable define outside of the def
def mars_news(browser):
    #scrape the NASA website
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    #the actual code is <div class="list_text">
    #the wait_time is strategic since some sites have images that take a while to load
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # the 'div.list_text' doesn't work with the find funciton
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = news_soup.find('div', class_='content_title').get_text()
        news_title

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p
    except AttributeError:
        return None, None
    return news_title, news_p

def featured_image(browser): 
    # ###feature images 
    # 
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        #<img class="fancybox-image" src="image/featured/mars3.jpg" alt="">
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    ###Mars vs Earth Facts 
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    #General exception often used to catch multiple types of errors
    except BaseException:
        return None
    #assign columns and index of datafram
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    ## if you need to go from df to html,,,  df.to_html()
    return df.to_html(classes="table table-striped")

    #close down the browser
    #browser.quit()

def hemisphere(browser):
    ### this is my second option for code 
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []

    imgs_links= browser.find_by_css("a.product-item h3")
    for x in range(len(imgs_links)):
        hemisphere={}
        # Find elements going to click link
        #https://splinter.readthedocs.io/en/latest/finding.html
        browser.find_by_css("a.product-item h3")[x].click()
        # Find sample Image link
        #https://splinter.readthedocs.io/en/latest/finding.html
        sample_img= browser.find_link_by_text("Sample").first
        hemisphere['img_url']=sample_img['href']
        # Get hemisphere Title
        # I was getting a builtin method error on the html site, this might be the reason
        #https://www.reddit.com/r/flask/comments/dhteiv/builtin_method_title_of_str_object_at/
        hemisphere['img_title']=browser.find_by_css("h2.title").text
        #Add Objects to hemisphere_img_urls list
        hemisphere_image_urls.append(hemisphere)
        # Go Back
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




