# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 21:01:07 2023

@author: valcs
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

dr = webdriver.Chrome()
dr.get("https://ingatlan.com/lista/elado+lakas+xiv-ker")
bs = BeautifulSoup(dr.page_source,"lxml")
prices = bs.find_all("span" , {"class":"fw-bold fs-5 text-onyx me-3 font-family-secondary"})
adresses = bs.find_all("span" , {"class" : "d-block fw-500 fs-7 text-onyx font-family-secondary"})
sizes_and_rooms = bs.find_all("span" , {"class" : "fs-7 text-onyx fw-bold"})
rooms = bs.find_all("span" , {"class" : "fs-7 text-onyx fw-bold"})
housing = {}
count = 0
print(len(sizes_and_rooms))
for size in sizes_and_rooms:
    print(size.get_text(separator='|'))
for i in range(len(prices)):
    temp = {}
    print(prices[i].get_text(separator='|'))
    temp["price"] = [prices[i].get_text(separator='|')]
    temp["adress"] = [adresses[i].get_text(separator='|')]
    temp["size"] = [sizes_and_rooms[i*2].get_text(separator='|')]
    temp["room"] = [rooms[i*2 - 1].get_text(separator='|')]
    df = pd.DataFrame(temp)
    housing[str(i)] = df
    