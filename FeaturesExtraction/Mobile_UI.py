  
import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
import pandas as pd


def Mobile_UI_Existence(url):
    r = requests.get(url) # get the url from the user
    soup = BeautifulSoup(r.text, 'html.parser') # get acsess
    phrases = soup.find_all('meta') # get all lines that start with meta
    for i in range(len(phrases)):
       try:
               m=phrases[i]
               # search for these terms in in the content or the name of the line
               term1 ='width=device-width,initial-scale=1'
               term2='apple-mobile-web'
               term3='inmobi-site-verification'
               if term1 in m['content']:
                   return 1
               elif term2 in m['name']:
                   return 1
               elif term3 in m['name']:
                   return 1
                
       except:
            pass
            
       
        


def mobile(URL):
    result=Mobile_UI_Existence(URL)
    # if there is no one of the ters in the line this the website is not mobile-UI
    if result !=1:
        return 0
    return result

#url='https://www.lightinthebox.com/?prm=1'
#print(mobile(url))
