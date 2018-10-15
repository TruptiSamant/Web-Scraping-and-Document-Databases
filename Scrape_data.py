
# ## Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks.
# The following outlines what you need to scrape.
####################################################################################
#imports
# from bs4 import BeautifulSoup
from splinter import Browser, exceptions
import pandas as pd
import re
from bs4 import BeautifulSoup



class MissionMars:
    def __init__(self, browser):
        # open a browser
        self.browser = Browser(browser, headless=True)
        # Width, Height
        self.browser.driver.set_window_size(640, 480)

    # #quit the browsser
    def __del__(self):
        self.browser.quit()


    ############################ Functions ################################
    def get_headline(self, url): #https://mars.nasa.gov/news
        """Get the headline and para from https://mars.nasa.gov/news.
        Returns tuple
        -------
        String
            Title.
        """
        self.browser.visit(url)
        #get the Xpath for headline
        # index 0 to select from the list
        soup = BeautifulSoup(self.browser.html, 'lxml')
        news_title=soup.find('div', {'class':'content_title'})
        news_p=soup.find('div', {'class':'article_teaser_body'})
        return news_title.text, news_p.text


    def get_featured_image_url(self, url): #https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
        """Get the featured image
        Returns
        -------
        type
            Description of returned object.
        """
        try:
            self.browser.visit(url)
            image_href = self.browser.find_by_xpath('//*[@id="page"]/section[3]/div/ul/li[1]/a')["data-fancybox-href"]
            browser_url = self.browser.url.split('/')
            image_url = browser_url[0] + '//' + browser_url[1] + '/' + browser_url[2] + image_href
            return image_url
        except:
            print (f"Error getting: {url}")

    def get_mars_weather(self, url): #https://twitter.com/marswxreport?lang=en
        """Get the Mars weather.
        Parameters
        ----------
        url : https://twitter.com/marswxreport?lang
        Returns
        -------
        type
            Description of returned object.
        """
        try:
            self.browser.visit(url)
            soup = BeautifulSoup(self.browser.html, 'lxml')
            # mars_weather=soup.find(string=re.compile("Sol"))
            return soup.find(string=re.compile("Sol"))
        except:
            print (f"Error getting: {url}")



    def get_mars_facts(self, url): #https://space-facts.com/mars/
        """Short summary.
        Returns
        -------
        type
            Description of returned object.
        """
        try:
            self.browser.visit(url)

            info_table = self.browser.find_by_xpath('//*[@id="tablepress-mars"]/tbody/tr')
            # mars_facts_list = []
            mars_facts_list = [(row.find_by_tag("td")[0].text, row.find_by_tag("td")[1].text) for row in info_table]
            # mars_facts_list.append((row.find_by_tag("td")[0].text, row.find_by_tag("td")[1].text))
            mars_facts_df = pd.DataFrame(data=mars_facts_list, columns=[ "Description","Value"])
            mars_facts_df.set_index('Description', inplace=True)
            return mars_facts_df
        except:
            print (f"Error getting: {url}")

    def get_mars_hemispheres(self, url): # https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
        """Short summary.
        Parameters
        ----------
        url) : # https://astrogeology.usgs.gov/search/results?q
            Description of parameter `url)`.
        Returns
        -------
        type
            Description of returned object.
        """
        self.browser.visit(url)

        try:
            image_urls = self.browser.find_by_xpath('//*[@id="product-section"]/div[2]')
            titles = [i.html for i in image_urls.find_by_tag('h3')]
        except exceptions.ElementDoesNotExist:
            print(f"ElementDoesNotExist: Please check the commention {browser.url}")

        #get the URLs and loop through
        hemisphere_image_urls = []
        for title in titles:
            try:
                self.browser.click_link_by_partial_text(title)
                image_url = self.browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[2]')
                image = image_url.find_by_tag('a')['href']
                hemisphere_image_urls.append(dict({'title': title, 'image_url': image }))
                self.browser.back()
            except exceptions.ElementDoesNotExist:
                print(f"ElementDoesNotExist: Please check the commention {self.browser.url}")
        return hemisphere_image_urls
