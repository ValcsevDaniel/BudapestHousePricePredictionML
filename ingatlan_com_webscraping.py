# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 21:01:07 2023

@author: valcs
"""
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import undetected_chromedriver as uc
import re
from seleniumbase import Driver
from datetime import datetime


url = "https://ingatlan.com/33574491"
def number_of_half_rooms(str):
    if(len(str.split(' ')) >= 3):
        return float(str.split(' ')[2])
    else:
        return 0
def get_all_house_details(bs):
    individual_houses =[]
    links = bs.find_all("a")
    for link in links:
        
        try:
            txt = link.get("href")
        except:
            
            txt=""
        if(type(txt) == type("s")):
            house_detail = re.search('^\/\d{8}$', txt)
            if house_detail:
                
                individual_houses.append(house_detail.string)
    return individual_houses
def cookie_accept(dr):
    time.sleep(2)
    dr.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
 
def scrape_specific_house(url, dr,bs):
    
    
    
    time.sleep(3)
    tables = bs.find_all("table" , {"col col-print-6 table table-borderless h-100 w-50 border-end border-1"})
    specs = {}
    for table in tables:
        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.find_all('td')
            specs[tds[0].get_text(separator='|').strip()] = tds[1].get_text(separator='|').strip()
    tables_second_column =  bs.find_all("table" , {"col col-print-6 table table-borderless ms-3 h-100 w-50"})
    for table in tables_second_column:
        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.find_all('td')
            specs[tds[0].get_text(separator='|').strip()] = tds[1].get_text(separator='|').strip()
        
            
    
    return specs
    
    

    
def scrape_single_page(url):
     
    
     
   
    
    
        
    
    dr = Driver(uc=True)
    dr.get(url)
    page_count = 1
    page_count += 1
    bs = BeautifulSoup(dr.page_source,"lxml")
    
    

    prices = bs.find_all("span" , {"class":"fw-bold fs-5 text-onyx me-3 font-family-secondary"})
    adresses = bs.find_all("span" , {"class" : "d-block fw-500 fs-7 text-onyx font-family-secondary"})
    housing = {}
    count = 0
    
    
    
        
    for i in range(len(prices)):
        
        temp = {}
        temp["price"] = float(prices[i].get_text(separator='|').split(' ')[0].replace(',','.'))
        temp["adress"] = adresses[i].get_text(separator='|')
        housing[i + 1] = temp
    
    
    size_rooms_balcony_row = bs.find_all("div" ,{"class" : "d-flex justify-content-start"})
    i = 1
    for value in size_rooms_balcony_row:
        v = value.find_all("span" , {"class" : "fs-7 text-onyx fw-bold"})
        count = 0
      
        for s in v:
            if count == 0:
                housing[i]["size"] = float(s.get_text(separator='|').split(' ')[0].replace(',','.'))
            elif count == 1:
                housing[i]["rooms"] = float(s.get_text(separator='|').split(' ')[0])
                housing[i]["half_rooms"] = number_of_half_rooms(s.get_text(separator='|'))
            elif count == 2:
                housing[i]["balcony"] = float(s.get_text(separator='|').split(' ')[0].replace(',','.'))
            count += 1
            
        
        i += 1
    #cookie_accept()
    
    
    
    dr.quit()
    url_ending_list = get_all_house_details(bs)
    count_specifics = 1
    
    for url_end in url_ending_list:
        
         
        # Setting the driver path and requesting a page 
        dr = Driver(uc=True)
         
        # Changing the property of the navigator value for webdriver to undefined 
        
        url = "https://ingatlan.com{ending}".format(ending=url_end)
        
        dr.get(url)
        time.sleep(3)
        bs = BeautifulSoup(dr.page_source,"lxml")
        temp = scrape_specific_house(url, dr, bs)
        temp_dict = housing[count_specifics]
        merge_dict = {**temp_dict, **temp}
        housing[count_specifics] = merge_dict
        
        dr.quit()
        count_specifics += 1
        
        
    
    df = pd.DataFrame(housing).T
    return df
frames = []
beginning_time = datetime.now()
print(beginning_time)
for i in range(1,100):
    print("Current Page: ", i)
    frame = scrape_single_page(f"https://ingatlan.com/lista/elado+lakas+xi-ker?page={i}")
    frames.append(frame)
result = pd.concat(frames)
result_copy = result
result_copy = result.reset_index().drop('index', axis=1)

result_copy.to_csv('tizenegyedik_ker_elso.csv', index=False)
end = datetime.now()
print("The program took : " , end - beginning_time)





        
    