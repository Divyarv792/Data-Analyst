#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
import pandas as pd
import csv
import time
s=HTMLSession()
url="https://www.amazon.in/s?k=bags&page=5&crid=2M096C61O4MLT&qid=1693204039&sprefix=ba%2Caps%2C283&ref=sr_pg_4"

def all_datas(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    data = s.get(url, headers=headers)
    #print(data)getting response 503 after 2url
    soup=bs(data.content,'lxml')
    datas(soup)
    return soup
   
def datas(soup):
    header=['Product Name','Price','Rating','No of Reviews','ASIN','Manufacturer','URL']
    with open(r'C:\Users\Naveen\Desktop\data science\data scrapping\Amazon data scraping project\CSV folder\page5.csv','w', newline='',encoding='UTF8')as f:
        writer=csv.writer(f)
        writer.writerow(header)

    products=soup.find_all('div', class_=['sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16', 'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16'])
    for product in products: 
        product_name=product.find('span',class_ = 'a-size-medium a-color-base a-text-normal').text
        product_price=product.find('span', class_= 'a-price-whole').text
        if product.find('span',class_='a-size-base s-underline-text'):
            No_of_reviews=product.find('span',class_='a-size-base s-underline-text').text.strip('()')
        else: 
            No_of_reviews='No reviews'
        if product.find('span',class_='a-icon-alt'):
            product_rating=product.find('span',class_='a-icon-alt').text
        else:
            product_rating='No rating'
        product_URL=product.h2.a['href']
        new_URL=product_URL.replace(product_URL,'https://www.amazon.in/'+product_URL)
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
        c=HTMLSession()
        newdata = c.get(new_URL, headers=header)
        sp=bs(newdata.content,'lxml')
        if sp.find('ul',class_='a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list'):
            reqdata=sp.find('ul',class_='a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list')
            req=reqdata.find_all('span')
            for r in req:
                x='ASIN'
                if x in r.get_text():
                    ASIN=r.get_text().split(':')[1].replace(' ','').strip().replace('\n','')  
                    break
            for r in req:
                y='Manufacturer'
                if y in r.get_text():
                    Manufacturer=r.get_text().split(':')[1].replace(' ','').strip().replace('\n','')
                    break
        elif sp.find('table',{'id':'productDetails_detailBullets_sections1'}):
            reqdata=sp.find('table',{'id':'productDetails_detailBullets_sections1'})
            req=reqdata.find_all('tr')
            for r in req:
                x='ASIN'
                if x in r.text:
                    ASIN=r.td.text.strip()
                    break
            for r in req:
                x='Manufacturer'
                if x in r.text:
                    Manufacturer=r.td.text.strip()
                    break
   
        data=(product_name,product_price,product_rating,No_of_reviews,ASIN,Manufacturer,new_URL)
        with open(r'C:\Users\Naveen\Desktop\data science\data scrapping\Amazon data scraping project\CSV folder\page5.csv','a+', newline='',encoding='UTF8')as f:
            writer=csv.writer(f)
            writer.writerow(data)
while(True):
    soup=all_datas(url)
    datas(soup)
    time.sleep(3600)
   

    



# In[ ]:




