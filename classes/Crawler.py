# This file contains a crawler class that is used to crawl the web
# The crawler class is used to crawl the web and store the data in a database

from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re
import datetime
import random
from url_tracker import UrlTrackerTree
from Parser import Parser
import requests

class Crawler:
    """This crawler class uses the UrlTrackerTree to store the urls as a tree and traverse"""
    def __init__(self, base_url, max_urls=1000, max_depth=5):
        self.base_url = base_url
        self.max_urls = max_urls
        self.max_depth = max_depth
        self.url_tracker = UrlTrackerTree(base_url, parent=None)
        self.url_tracker.to_crawl = [base_url]
        self.crawled_urls = 0
        self.crawled_images = 0
        self.crawled_documents = 0
        self.crawled_webpages = 0
        self.crawled_urls_list = []
        self.crawled_images_list = []
        self.crawled_documents_list = []
        self.crawled_webpages_list = []
        self.crawled_urls_dict = {}
        self.crawled_images_dict = {}
        self.crawled_documents_dict = {}
        self.crawled_webpages_dict = {}
        self.crawled_urls_dict["url"] = base_url
        self.crawled_urls_dict["type"] = "webpage"
        self.crawled_urls_dict["crawled"] = True
        self.crawled_urls_dict["children"] = []
        self.crawled_urls_dict["parent"] = None
        self.crawled_urls_dict["depth"] = 0
        self.crawled_urls_list.append(self.crawled_urls_dict)
        self.crawled_webpages_dict["url"] = base_url
        self.crawled_webpages_dict["type"] = "webpage"
        self.crawled_webpages_dict["crawled"] = True
        self.crawled_webpages_dict["children"] = []
        self.crawled_webpages_dict["parent"] = None
        self.crawled_webpages_dict["depth"] = 0
        self.crawled_webpages_list.append(self.crawled_webpages_dict)
        self.crawled_urls_dict = {}
        self.crawled_webpages_dict = {}
        self.crawled_documents_dict = {}
        self.crawled_images_dict = {}
        self.crawled_urls_dict["url"] = base_url
        self.crawled_urls_dict["type"] = "webpage"
        self.crawled_urls_dict["crawled"] = True
        self.crawled_urls_dict["children"] = []
        self.crawled_urls_dict["parent"] = None
        self.crawled_urls_dict["depth"] = 0
        
        
    def get_links(self, url):
        """This function returns the links from a webpage"""
        links = []
        try:
            response = requests.get(url)
        except:
            return links
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all('a'):
            links.append(link.get('href'))
        return links
    
    def get_crawled_urls(self):
        """This function returns the crawled urls"""
        return self.crawled_urls_list

    def get_crawled_webpages(self):
        """This function returns the crawled webpages"""
        return self.crawled_webpages_list
    
    def get_crawled_images(self):
        """This function returns the crawled images"""
        return self.crawled_images_list
    
    def get_crawled_documents(self):
        """This function returns the crawled documents"""
        return self.crawled_documents_list
    
    def get_crawled_urls_count(self):
        """This function returns the number of crawled urls"""
        return self.crawled_urls

    def get_crawled_webpages_count(self):
        """This function returns the number of crawled webpages"""
        return self.crawled_webpages

    def get_depth(self):
        """This function returns the depth of the crawler"""
        return self.depth
    
    def get_crawled_images_count(self):
        """This function returns the number of crawled images"""
        return self.crawled_images
    
    def get_crawled_documents_count(self):
        """This function returns the number of crawled documents"""
        return self.crawled_documents