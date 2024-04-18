#Obtain the links of the subcategories of the Mercado Livre website
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import datetime 
import re
import openpyxl
from operator import length_hint
import time
import pandas as pd
import sqlite3


Lin = "https://www.mercadolivre.com.br/categorias#menu=categories"
driver = webdriver.Firefox()
sqlite_db = r"C:\Users\eduar\Documents\Selenium\mercadolivre.db"
conn = sqlite3.connect(sqlite_db)
cur = conn.cursor()
driver.get(Lin)
time.sleep(5)
Linksstr = []
Links = driver.find_elements(By.CLASS_NAME, 'categories__subtitle')
Links2 = driver.find_elements(By.CLASS_NAME, 'categories__subtitle-title')
i=0
while i<len(Links):
    Link_name = Links2[i].text
    Link_url = Links[i].get_attribute('href')
    print(Link_name)
    print(Link_url)
    Data = [ Link_name, Link_url]
    df_nova_linha = pd.DataFrame([Data], columns=['LINK_NAME','LINK_URL'])
    df_nova_linha.to_sql('MLLinks', conn, if_exists='append',index=False)
    i = i + 1
conn.commit()
conn.close()

driver.close()
print("THE END")