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
    hemisphere_image_urls=hemisphere(browser)

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
            # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    hmtl=browser.html

        # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    img_href =[]
    hemisphere={"img_url":[], "title":[]}

        # 3. Write code to retrieve the image urls and titles for each hemisphere.
    hemisphere_soup=soup(hmtl, "html.parser")
    for link in hemisphere_soup.find_all("a", class_="itemLink product-item"):
        if link.get("href") not in img_href:
            img_href.append(link.get("href"))
            
    img_href.remove("#")
    for x in img_href:
        browser.visit(f'https://marshemispheres.com/{x}')
        hemisphere_img_title=soup(browser.html,"html.parser").find("h2", class_="title").get_text()
        #hemisphere_image_title.append(hemisphere_img_title)
        for y in soup(browser.html,"html.parser").find_all("a"):
            if y.get_text()=="Sample":
                hemisphere_img_final=y.get("href")
                url_img=f'https://marshemispheres.com/{hemisphere_img_final}'
                #hemisphere_image_urls.append(f'https://marshemispheres.com/{hemisphere_img_final}')
        
        dic={"img_url":url_img,"title":hemisphere_img_title}
        hemisphere["img_url"].append(url_img)
        hemisphere["title"].append(hemisphere_img_title)
        hemisphere_image_urls.append(dic)
    browser.quit()
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




