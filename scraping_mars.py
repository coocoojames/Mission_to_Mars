#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_data():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_summary = mars_news(browser)
    data = {
      "news_title": news_title,
      "news_summary": news_summary,
      "mars_hemispheres": mars_hemispheres(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()}
    browser.quit()
    return data
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_summary = slide_elem.find('div', class_='article_teaser_body').text.strip()
    except AttributeError:
        return None, None
    return news_title, news_summary
def mars_hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []
    html = browser.html
    h_soup = soup(html, 'html.parser')
    href = h_soup.find_all('div', class_='item')

    for items in href:
        hem_dict = {}
        link = items.find('a')['href']
        browser.visit(url+link)
        html = browser.html
        h_soup = soup(html, 'html.parser')
        img_url_rel = h_soup.find('li').find('a')['href']
        img_url = f'https://marshemispheres.com/{img_url_rel}'
        title = h_soup.find('h2', class_='title').get_text()
        hem_dict['img_url'] = img_url
        hem_dict['title'] = title
        browser.back()
        hemisphere_image_urls.append(hem_dict)
    return hemisphere_image_urls
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    # df
    return df.to_html()

if __name__ == "__main__": 
    # If running as script, print scraped data
    print(scrape_data())
# browser.quit()

