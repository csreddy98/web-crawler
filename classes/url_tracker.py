# create a tree of urls and their corresponding classes 
# Check if a given url is in the tree
# store the sub-urls as children of the parent url in the tree
# also store if the web page is already crawled or not
# return the tree as an image file or a text file

# Path: classes\url_tracker.py

import os
import sys
from urllib.parse import urlparse
from urllib.request import urlopen
import BeautifulSoup as bs
import re


class UrlTrackerTree:
    def __init__(self, url, parent=None, depth=0):
        self.tree = {}
        self.crawled = False
        self.to_crawl = []
        self.url = url
        self.parent = parent
        self.children = []
        self.depth = depth

    def add_child(self, child):
        self.children.append(child)
    
    def get_children(self):
        return self.children
    
    def get_parent(self):
        return self.parent
    
    def get_url(self):
        return self.url
    
    def type_of_url(self):
        if self.url.endswith(".png") or self.url.endswith(".jpg") or self.url.endswith(".gif") or self.url.endswith(".jpeg") or self.url.endswith(".bmp") or self.url.endswith(".svg") or self.url.endswith(".ico"):
            return "image"
        elif self.url.endswith(".pdf") or self.url.endswith(".doc") or self.url.endswith(".docx") or self.url.endswith(".xls") or self.url.endswith(".xlsx") or self.url.endswith(".ppt") or self.url.endswith(".pptx"):
            return "document"
        return "webpage"

    def is_crawled(self):
        return self.crawled

    def crawledd(self):
        # This function marks the tree as crawled
        self.crawled = True
    
    def find_url_in_tree(self, url):
        # This function finds a url in the tree recursively and returns the node if found
        if self.url == url:
            return self
        for child in self.children:
            if child.find_url_in_tree(url) is not None:
                return child.find_url_in_tree(url)
        return None
    
    def return_tree_as_dict(self):
        # This function returns the tree as a dictionary
        tree = {}
        tree["url"] = self.url
        tree["type"] = self.type_of_url()
        tree["crawled"] = self.crawled
        tree["children"] = []
        for child in self.children:
            tree["children"].append(child.return_tree_as_dict())
        return tree
    
    def store_tree_as_dict(self, filename):
        # This function stores the tree as a dictionary in a file
        tree = self.return_tree_as_dict()
        with open(filename, "w") as f:
            f.write(str(tree))
            
    def get_depth(self):
        # This function returns the depth of the tree
        if len(self.children) == 0:
            return 0
        else:
            return max([child.get_depth() for child in self.children]) + 1
        
    def add_children(self, children):
        # This function adds children to the tree
        for child in children:
            self.add_child(child)