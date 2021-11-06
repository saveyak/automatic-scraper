#!/usr/bin/env python
# coding: utf-8

# In[12]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[13]:


url = "https://clarkesworldmagazine.com/"
headers = {'name': 'Sharon Lurye', 
           'email': 'sharonrlurye@gmail.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')


# In[14]:


titles = soup.select("p.story")

rows = []

for d in range(len(titles)):
    row = {}
    row['title'] = titles[d].text
    row['byline'] = soup.select("p.byline")[d].text
    row['link'] = soup.select("p.story a")[d].get("href")
    rows.append(row)

df = pd.DataFrame(rows)
df['issue'] = soup.select_one("h1.issue").text

df


# In[15]:


df[['issue_number','date']] = df.issue.str.split("–", expand=True)
df = df.drop('issue', axis=1)
df


# In[16]:


#Find children of nodes: https://stackoverflow.com/questions/6287529/how-to-find-children-of-nodes-using-beautifulsoup

fiction = soup.select("div.index-table div.index-table")[0]

fiction_titles = fiction.select("p.story")
fiction_titles = [title.text for title in fiction_titles]

fiction_titles


# In[17]:


cover = soup.select("div.index-table div.index-table")[2].select_one("p.story").text

cover


# In[18]:


df['category'] = df['title'].apply(lambda x:"Fiction" if x in fiction_titles else "Cover" if x in cover else "Non-fiction")

df


# In[19]:


#Save df and append to previous CSV

df.to_csv('clarkesworld.csv', mode='a', index=False)


# In[20]:


#Remove duplicates from CSV

df = pd.read_csv('clarkesworld.csv')
df.drop_duplicates(inplace = True)
df = df[df['byline'].str.contains("byline") == False]
df.to_csv('clarkesworld.csv', index=False)

