
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
            //*[@id="page"]/section[3]/div/ul/li[8]/a/div/div[2]/img
            //*[@id="page"]/section[3]/div/ul/li[8]/a
        """
        try:
            self.browser.visit(url)
            soup = BeautifulSoup(self.browser.html, 'lxml')
            a=soup.find('ul', {'class':'articles'})
            # print(a)
            image_href = a.find('div', {'class':'img'}).find('img')['src']
            print(f'image_href: {image_href}')
            # image_href = self.browser.find_by_xpath('//*[@id="page"]/section[3]/div/ul/li[1]/a')["data-fancybox-href"]
            # browser_url = self.browser.url.split('/')
            image_url = 'https://www.jpl.nasa.gov' + image_href
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
            soup = BeautifulSoup(self.browser.html, 'lxml')
            image_urls = soup.find_all('div', {'class':'collapsible results'})
            titles= [x.text for x in image_urls[0].find_all('h3')]
        except exceptions.ElementDoesNotExist:
            print(f"ElementDoesNotExist: Please check the commention {browser.url}")

        #get the URLs and loop through
        hemisphere_image_urls = []
        for title in titles:
            try:
                self.browser.click_link_by_partial_text(title.split(' ')[0])
                soup = BeautifulSoup(self.browser.html, 'lxml')
                image_url = soup.find('div', {'class':'downloads'}).find('li').find('a')['href']
                hemisphere_image_urls.append(dict({'title': title, 'image_url': image_url }))
                self.browser.back()
            except exceptions.ElementDoesNotExist:
                print(f"ElementDoesNotExist: Please check the commention {self.browser.url}")
        return hemisphere_image_urls

# m = MissionMars('chrome')
# print(m.get_mars_hemispheres('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'))
