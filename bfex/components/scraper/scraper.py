from bs4 import BeautifulSoup
from abc import ABC
import requests
import json
import re
from bfex.components.scraper.scrapp import *

base_url = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"

class Scraper(ABC):
    
    def __init__(self, url, type):
        self.url = url
        self.type = type
        
    def validate_url(self):
        pass

    def get_content(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_scrapps(self):
        return []