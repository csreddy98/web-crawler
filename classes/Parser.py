# This parser class handles the parsing of the html files 
# The HTML files contain the links to the other pages, heading, paragraphs, image urls, and document urls.
# The HTML also contains the information about people, places, organizations, etc.

import BeautifulSoup as bs
import requests
import re
import os
import json

class Parser:
    """This parser class handles the parsing of the html files 
    The HTML files contain the links to the other pages, heading, paragraphs, image urls, and document urls.
    The HTML also contains the information about people, places, organizations, etc."""

    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).text
        self.soup = bs.BeautifulSoup(self.html, "html.parser")
        self.links = []
        self.heading = ""
        self.paragraphs = []
        self.image_urls = []
        self.document_urls = []
        self.people = []
        self.places = []
        self.organizations = []
        self.extractions = []
        
    def get_links(self):
        """This function returns the links from a webpage"""
        for link in self.soup.find_all('a'):
            self.links.append(link.get('href'))
        return self.links
    
    def get_heading(self):
        """This function returns the heading from a webpage"""
        self.heading = self.soup.find('h1').text
        return self.heading

    def get_paragraphs(self):
        """This function returns the paragraphs from a webpage"""
        for paragraph in self.soup.find_all('p'):
            self.paragraphs.append(paragraph.text)
        return self.paragraphs
    
    def get_image_urls(self):
        """This function returns a list of dictoinaries that contain image urls and alt text"""
        for image in self.soup.find_all('img'):
            self.image_urls.append({"url": image.get('src'), "alt": image.get('alt')})
        return self.image_urls

    def get_document_urls(self):
        """This function returns a list of dictionaries that contain document urls and alt text"""
        for document in self.soup.find_all('a'):
            if document.get('href').endswith(".pdf") or document.get('href').endswith(".docx") or document.get('href').endswith(".doc") or document.get('href').endswith(".txt") or document.get('href').endswith(".xlsx") or document.get('href').endswith(".xls") or document.get('href').endswith(".pptx") or document.get('href').endswith(".ppt") or document.get('href').endswith(".csv") or document.get('href').endswith(".xml"):
                self.document_urls.append({"url": document.get('href'), "alt": document.text})
        return self.document_urls
    