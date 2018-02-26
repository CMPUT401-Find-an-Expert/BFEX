from bs4 import BeautifulSoup
from abc import ABC
import requests
import json
import re
from bfex.components.scraper.scrapp import *

base_url = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"

class Scraper(ABC):
    """ Abstract Base Class for a scraper to scrape a website """
    
    def __init__(self, url, type):
        """ From a URL and type we can successfully scrape a website
        
            :param url: url gotten from elastic search or other scrape.
            :param type: what type of webpage this is. This could be:
                - ResearcherID
                - OrcId
                - Profile page from faculty of science
                Each type will have similar web page design
            :return: none
        """
        self.url = url
        self.type = type
        
    def validate_url(self):
        """ This will make sure the URL is reachable
            :return: True if URL is reachable; False otherwise
        """
        pass

    def get_content(self):
        """ This returns the entire html scrape
            :return: A beautiful soup object with all html data
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_scrapps(self):
        """ :param name: formatted name of the faculty memeber.
            :return: none
        """
        return []