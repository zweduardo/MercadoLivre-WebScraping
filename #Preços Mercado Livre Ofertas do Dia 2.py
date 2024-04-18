#AmazonMAisVendidosSubDep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import datetime 
import re
import openpyxl
import sqlite3
import pandas as pd



#ws.append(stringname)
#wb.save(xlsxname)

sqlite_db = r"C:\Users\eduar\Documents\Selenium\Amazon.db"
conn = sqlite3.connect(sqlite_db)
driver = webdriver.Firefox()
driver.get("https://www.amazon.com.br/gp/bestsellers/?ref_=nav_cs_bestsellers")
#csvname = 'mercadolivre.csv'
#xlsxname = r"C:\Users\eduar\Documents\Selenium\Planilhas\mercadolivre.xlsx"
#wb = openpyxl.load_workbook(xlsxname)
#ws = wb.worksheets[0]
#assert "Python" in driver.title
#Diames = date.today()
#data = date(Diames.year,Diames.month, Diames.day).strftime("%Y-%m-%d")
now = datetime.date.today()
data = now.strftime("%Y%m%d")
Year = now.strftime("%Y")
Month = now.strftime("%m")
Day = now.strftime("%d")
#len = 16*3 #len(driver.find_elements(By.CLASS_NAME, 'promotion-item avg'))
#i = 0
#j = 0
#pag = 0
#pagtot = 20
#wb = openpyxl.load_workbook(xlsxname)
#ws = wb.worksheets[0]
Departamentos = driver.find_element(By.CLASS_NAME, '_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz')
Departamento = Departamentos.find_elements(By.TAG_NAME, 'a')
DepLink = []
DepText = []
for Dep in Departamento:
    DepLink.append(Dep.get_attribute('href'))
    DepText.append(Dep.text)
SubDepLink = []
SubDepText = []
for Link in DepLink:
    driver.get(Link)
    SubDepartamentos = driver.find_element(By.CLASS_NAME, '_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz')
    SubDepartamento = SubDepartamentos.find_elements(By.TAG_NAME, 'a')
    for SubDep in SubDepartamento:
        SubDepLink.append(SubDep.get_attribute('href'))
        SubDepText.append(SubDep.text)

for SDLink, SDText in zip(SubDepLink, SubDepText):
    driver.get(SDLink)
    Products = driver.find_elements(By.ID, 'gridItemRoot')
    for Product in Products:
        try:
            Description = Product.find_element(By.CLASS_NAME, '_cDEzb_p13n-sc-css-line-clamp-3_g3dy1').text
        except:
            try:   
                Description = Product.find_element(By.CLASS_NAME, '_cDEzb_p13n-sc-css-line-clamp-4_2q2cc').text
            except:
                Description = ""
        try:
            afterpricebeforevirg = Product.find_element(By.CLASS_NAME, '_cDEzb_p13n-sc-price_3mJ9Z').text
        except:
            try:
                afterpricebeforevirg = Product.find_element(By.CLASS_NAME, 'p13n-sc-price').text
            except:
                afterpricebeforevirg = ""
        price = afterpricebeforevirg.replace('R$ ','') 
        link = Product.find_element(By.CLASS_NAME, 'a-link-normal').get_attribute('href')
        img_url = Product.find_element(By.TAG_NAME, 'img').get_attribute('src')
        try:
            Starsrow = Product.find_element(By.CLASS_NAME, 'a-icon-row')
            Stars = Starsrow.find_element(By.CLASS_NAME, 'a-link-normal').get_attribute('title')
        except:
            Starsrow = ""
            Stars = ""
        SoldSubDepRank = Product.find_element(By.CLASS_NAME, 'zg-bdg-text').text
        RankSubDep = SoldSubDepRank.replace('#','')
        Amzndata = [data, link , Description, price, img_url, Stars, RankSubDep, SDText]
        df_nova_linha = pd.DataFrame([Amzndata], columns=['Data', 'Link','Description','Price', 'img_url', 'Stars', 'RankSubDep','SubDep'])
        df_nova_linha.to_sql('AmazonBestSellers', conn, if_exists='append', index=False)
        #add_xlsx(MLdata,xlsxname)
        #ws.append(MLdata)
    conn.commit()
#wb.save(xlsxname)
driver.close()
conn.close()