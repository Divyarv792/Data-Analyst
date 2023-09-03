#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
import os


# In[20]:


files=[file for file in os.listdir(r'CSV folder')]
allpages_data=pd.DataFrame()
for file in files:
    df=pd.read_csv(r'CSV folder\\'+file)
    allpages_data=pd.concat([allpages_data,df])
    allpages_data.to_csv("all_pages.csv", index=False)


# In[23]:


df=pd.read_csv(r'all_pages.csv')


# In[25]:


df.head(100)


# In[ ]:




