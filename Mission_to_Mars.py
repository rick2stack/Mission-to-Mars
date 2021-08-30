#!/usr/bin/env python
# coding: utf-8

# In[36]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[37]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[11]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[12]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[13]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[14]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[15]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[16]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[17]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[18]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[19]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[20]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[114]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)
hmtl=browser.html


# In[117]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
img_href =[]


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
    hemisphere_image_urls.append(dic)
    


# In[118]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[119]:


# 5. Quit the browser
browser.quit()


# In[ ]:




