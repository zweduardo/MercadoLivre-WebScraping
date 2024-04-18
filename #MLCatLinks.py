#From the Links of the subcategories, we can obtain the links of the best sellers of each subcategory
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


Lin = "https://www.mercadolivre.com.br/tablet-samsung-galaxy-tab-a9-5g-64gb-4gb-ram-grafite/p/MLB28532152?pdp_filters=deal:MLB779362-6&hide_psmb=true#promotion_type=DEAL_OF_THE_DAY&searchVariation=MLB28532152&deal_print_id=9f495a13-690e-4e5e-9b61-463638f5aeba&position=2&search_layout=grid&type=product&tracking_id=db17e120-c42a-4887-b07a-8603eb892b10&deal_print_id=b24e1f7c-d901-49ce-baab-3733138c263f&promotion_type=DEAL_OF_THE_DAY"
driver = webdriver.Firefox()
sqlite_db = r"C:\Users\eduar\Documents\Selenium\Descontassso\Descontasso\mercadolivre.db"
conn = sqlite3.connect(sqlite_db)
cur = conn.cursor()
Links2 = cur.execute("SELECT LINK_URL, LINK_NAME FROM MLLinks").fetchall()
now = datetime.date.today()
Year = now.strftime("%Y")
Month = now.strftime("%m")
Day = now.strftime("%d")
anomesdia = ""+Year+Month+Day+""

for Link in Links2:
    driver.get(Link[0])
    Products = driver.find_elements(By.CLASS_NAME,'ui-recommendations-card__content')
    for Product in Products:
        Url = Product.find_element(By.CLASS_NAME, 'ui-recommendations-card__link').get_attribute('href')
        Description = Product.find_element(By.CLASS_NAME, 'ui-recommendations-card__title').text
        pricebeforevirg = Product.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
        price = pricebeforevirg.replace('.','')
        Data = [anomesdia, Url, Description, price, Link[1]]
        df_nova_linha = pd.DataFrame([Data], columns=['Date','Link','Description','Price','Category'])
        df_nova_linha.to_sql('MLBestSellers', conn, if_exists='append',index=False)
        conn.commit()
conn.close()
driver.close()
print(".")