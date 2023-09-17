#!/usr/bin/env python
# coding: utf-8

# In[7]:


import scrapetube
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
import datetime
import warnings
import collections
warnings.filterwarnings("ignore")
import os
s=HTMLSession()
url="https://www.youtube.com/@tseries/videos"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
data = s.get(url, headers=headers)
soup=bs(data.content,'html')
channel_id=soup.find('link',title='RSS').get('href').split('=')[1]
url="https://www.youtube.com/watch?v="
df=pd.DataFrame(columns=['URL','Upload_date'])
vids=[]
letter_counts = collections.defaultdict(int)
videos=scrapetube.get_channel(channel_id,sort_by="newest")
for video in videos:
    url1=url+str(video['videoId'])
    datas = s.get(url1, headers=headers)
    soup1=bs(datas.content,'html')
    datasb=soup1.find('div',class_='watch-main-col')
    dates=str(datasb.find('meta',itemprop='uploadDate')).split('"')[1]
    date = datetime.datetime.strptime(dates, "%Y-%m-%d").date()
    start = datetime.datetime.strptime("2023-05-22", "%Y-%m-%d").date()
    end = datetime.datetime.strptime("2023-08-08", "%Y-%m-%d").date()
    if start <= date <= end:
        vids.append(str(video['videoId']))
        df=df.append({'URL':url1,'Upload_date':date.strftime('%B %d, %Y')},ignore_index=True)
    elif date < start:
        break
for vid in vids:
    for letter in vid:
            letter_counts[letter] += 1
rep_char = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)
print("The count of all charactes in videoId:",rep_char)
print("The most repeated char is:",rep_char[0])
df.to_excel('link&date.xlsx',encoding='ISO-8859-1',index=False)
print("The link&date.xlsx file has the list of video's URL and respective Uploaddates that are uploaded between August 8, 2023 and May 22, 2023.")



# In[ ]:




