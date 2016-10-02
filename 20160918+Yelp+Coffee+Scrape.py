
# coding: utf-8

# In[1]:

import os
import numpy as np
import pandas as pd
from csv import DictWriter, DictReader
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
get_ipython().magic('matplotlib inline')
from pylab import rcParams
import requests
from bs4 import BeautifulSoup
rcParams['figure.figsize']=20,5


# # Page One Web Scrape

# In[2]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco%2C+CA&ns=1"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[3]:

name=[]
neighborhood=[]
address=[]
city=[]
phone=[]
price=[]


# In[5]:

result1 = soup.find_all("div",{"class","media-story"})


# In[7]:

result2=soup.find_all("div",{"class","biz-listing-large"})


# In[17]:

for x in result1:
    try:
        name.append(x.contents[1].find_all("span")[1].text)
    except:
        pass


# In[8]:

for x in result2:
    try:
      address.append(x.contents[3].find_all("address")[0].text)
    except:
        pass


# In[9]:

for x in result2:
    try:
      phone.append(x.contents[3].find_all("span",{"class","biz-phone"})[0].text)
    except:
        pass


# In[10]:

for x in result2:
    try:
      neighborhood.append(x.contents[3].find_all("span",{"class","neighborhood-str-list"})[0].text)
    except:
        pass


# In[20]:

nameHolder=list(name)
addressHolder=list(address)
phoneHolder=list(phone)
neighborhoodHolder=list(neighborhood)


# In[26]:

for x in nameHolder:
    if x =="coffee":
        nameHolder.remove(x)
    if x =="Coffee":
        nameHolder.remove(x)


# In[41]:

for i,s in enumerate(neighborhoodHolder):
    neighborhoodHolder[i] = s.strip()


# In[43]:

for i,s in enumerate(phoneHolder):
    phoneHolder[i] = s.strip()


# In[45]:

for i,s in enumerate(addressHolder):
    addressHolder[i] = s.strip()


# In[122]:

priceCat = soup.find_all("div",{"class","price-category"})


# In[133]:

for x in priceCat:
    price.append(x.contents[1].text)


# In[135]:

priceHolder=list(price)


# In[136]:

for i,s in enumerate(priceHolder):
    priceHolder[i] = s.strip()


# In[148]:

nameHolder=DataFrame(nameHolder,columns=["Name"])
addressHolder=DataFrame(addressHolder,columns=["Address"])
neighborhoodHolder=DataFrame(neighborhoodHolder,columns=["Neighborhood"])
phoneHolder=DataFrame(phoneHolder,columns=["Phone Number"])


# In[173]:

priceHolder=DataFrame(priceHolder,columns=["Price Level"])


# In[178]:

pageOne=nameHolder.merge(addressHolder,left_index=True,right_index=True).merge(neighborhoodHolder,left_index=True,right_index=True).merge(phoneHolder,left_index=True,right_index=True).merge(priceHolder,left_index=True,right_index=True)


# In[186]:

priceNumber=[]
for x in pageOne["Price Level"]:
    priceNumber.append(len(x))
    


# In[188]:

priceNumber=DataFrame(priceNumber,columns=["Price Number"])


# In[192]:

pageOne=pageOne.merge(priceNumber,left_index=True,right_index=True)


# In[194]:

pageOne


# # Page Two Scrape

# In[195]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco,+CA&start=10"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[196]:

name2=[]
neighborhood2=[]
address2=[]
city2=[]
phone2=[]
price2=[]


# In[197]:

result1_page2 = soup.find_all("div",{"class","media-story"})
result2_page2=soup.find_all("div",{"class","biz-listing-large"})
priceCat_page2 = soup.find_all("div",{"class","price-category"})


# In[201]:

for x in result1_page2:
    try:
        name2.append(x.contents[1].find_all("span")[1].text)
    except:
        pass


# In[203]:

for x in result2_page2:
    try:
      address2.append(x.contents[3].find_all("address")[0].text)
    except:
        address2.append("N/A")


# In[227]:

for x in result2_page2:
    try:
      phone2.append(x.contents[3].find_all("span",{"class","biz-phone"})[0].text)
    except:
        phone2.append("N/A")


# In[223]:

for x in result2_page2:
    try:
      neighborhood2.append(x.contents[3].find_all("span",{"class","neighborhood-str-list"})[0].text)
    except:
        neighborhood2.append("N/A")


# In[230]:

for x in priceCat_page2:
    try:
        price2.append(x.contents[1].text)
    except:
        price2.append("N/A")


# In[232]:

price2.pop(0)
neighborhood2.pop(0)
phone2.pop(0)
address2.pop(0)


# In[243]:

nameHolder2=list(name2)
addressHolder2=list(address2)
phoneHolder2=list(phone2)
neighborhoodHolder2=list(neighborhood2)
priceHolder2=list(price2)


# In[257]:

for x in nameHolder2:
    if x =="coffee":
        nameHolder2.remove(x)
    if x =="Coffee":
        nameHolder2.remove(x)
    if x =="coffeehouse":
        nameHolder2.remove(x)


# In[247]:

for i,s in enumerate(neighborhoodHolder2):
    neighborhoodHolder2[i] = s.strip()


# In[248]:

for i,s in enumerate(phoneHolder2):
    phoneHolder2[i] = s.strip()


# In[249]:

for i,s in enumerate(addressHolder2):
    addressHolder2[i] = s.strip()


# In[250]:

for i,s in enumerate(priceHolder2):
    priceHolder2[i] = s.strip()


# In[272]:

nameHolder2=DataFrame(nameHolder2,columns=["Name"])
addressHolder2=DataFrame(addressHolder2,columns=["Address"])
neighborhoodHolder2=DataFrame(neighborhoodHolder2,columns=["Neighborhood"])
phoneHolder2=DataFrame(phoneHolder2,columns=["Phone Number"])
priceHolder2=DataFrame(priceHolder2,columns=["Price Level"])


# In[273]:

priceNumber2=[]
for x in priceHolder2["Price Level"]:
    priceNumber2.append(len(x))


# In[275]:

priceNumber2=DataFrame(priceNumber2,columns=["Price Number"])


# In[277]:

pageTwo=nameHolder2.merge(addressHolder2,left_index=True,right_index=True).merge(neighborhoodHolder2,left_index=True,right_index=True).merge(phoneHolder2,left_index=True,right_index=True).merge(priceHolder2,left_index=True,right_index=True).merge(priceNumber2,left_index=True,right_index=True)


# In[278]:

pageTwo


# # Page Three Scrape

# In[279]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco,+CA&start=20"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[280]:

name3=[]
neighborhood3=[]
address3=[]
city3=[]
phone3=[]
price3=[]


# In[281]:

result1_page3 = soup.find_all("div",{"class","media-story"})
result2_page3 = soup.find_all("div",{"class","biz-listing-large"})
priceCat_page3 = soup.find_all("div",{"class","price-category"})


# In[282]:

for x in result1_page3:
    try:
        name3.append(x.contents[1].find_all("span")[1].text)
    except:
        pass


# In[283]:

for x in result2_page3:
    try:
      address3.append(x.contents[3].find_all("address")[0].text)
    except:
        address3.append("N/A")


# In[284]:

for x in result2_page3:
    try:
      phone3.append(x.contents[3].find_all("span",{"class","biz-phone"})[0].text)
    except:
        phone3.append("N/A")


# In[285]:

for x in result2_page3:
    try:
      neighborhood3.append(x.contents[3].find_all("span",{"class","neighborhood-str-list"})[0].text)
    except:
        neighborhood3.append("N/A")


# In[286]:

for x in priceCat_page3:
    try:
        price3.append(x.contents[1].text)
    except:
        price3.append("N/A")


# In[291]:

price3.pop(0)
neighborhood3.pop(0)
phone3.pop(0)
address3.pop(0)


# In[292]:

nameHolder3=list(name3)
addressHolder3=list(address3)
phoneHolder3=list(phone3)
neighborhoodHolder3=list(neighborhood3)
priceHolder3=list(price3)


# In[ ]:

for x in nameHolder3:
    if x =="coffee":
        nameHolder3.remove(x)
    if x =="Coffee":
        nameHolder3.remove(x)
    if x =="coffeehouse":
        nameHolder3.remove(x)
    if x =="coffees":
        nameHolder3.remove(x)


# In[297]:

priceNumber3=[]
for x in priceHolder3:
    priceNumber3.append(len(x))


# In[293]:

for i,s in enumerate(neighborhoodHolder3):
    neighborhoodHolder3[i] = s.strip()


# In[294]:

for i,s in enumerate(phoneHolder3):
    phoneHolder3[i] = s.strip()


# In[295]:

for i,s in enumerate(addressHolder3):
    addressHolder3[i] = s.strip()


# In[296]:

for i,s in enumerate(priceHolder3):
    priceHolder3[i] = s.strip()


# In[298]:

nameHolder3=DataFrame(nameHolder3,columns=["Name"])
addressHolder3=DataFrame(addressHolder3,columns=["Address"])
neighborhoodHolder3=DataFrame(neighborhoodHolder3,columns=["Neighborhood"])
phoneHolder3=DataFrame(phoneHolder3,columns=["Phone Number"])
priceHolder3=DataFrame(priceHolder3,columns=["Price Level"])
priceNumber3=DataFrame(priceNumber3,columns=["Price Number"])


# In[309]:

pageThree=nameHolder3.merge(addressHolder3,left_index=True,right_index=True).merge(neighborhoodHolder3,left_index=True,right_index=True).merge(phoneHolder3,left_index=True,right_index=True).merge(priceHolder3,left_index=True,right_index=True).merge(priceNumber3,left_index=True,right_index=True)


# In[310]:

pageThree


# # Page Four Scrape

# In[311]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco,+CA&start=30"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[312]:

name4=[]
neighborhood4=[]
address4=[]
city4=[]
phone4=[]
price4=[]


# In[313]:

result1_page4 = soup.find_all("div",{"class","media-story"})
result2_page4 = soup.find_all("div",{"class","biz-listing-large"})
priceCat_page4 = soup.find_all("div",{"class","price-category"})


# In[314]:

for x in result1_page4:
    try:
        name4.append(x.contents[1].find_all("span")[1].text)
    except:
        pass


# In[315]:

for x in result2_page4:
    try:
      address4.append(x.contents[3].find_all("address")[0].text)
    except:
        address4.append("N/A")


# In[316]:

for x in result2_page4:
    try:
      phone4.append(x.contents[3].find_all("span",{"class","biz-phone"})[0].text)
    except:
        phone4.append("N/A")


# In[317]:

for x in result2_page4:
    try:
      neighborhood4.append(x.contents[3].find_all("span",{"class","neighborhood-str-list"})[0].text)
    except:
        neighborhood4.append("N/A")


# In[318]:

for x in priceCat_page4:
    try:
        price4.append(x.contents[1].text)
    except:
        price4.append("N/A")


# In[319]:

price4.pop(0)
neighborhood4.pop(0)
phone4.pop(0)
address4.pop(0)


# In[320]:

nameHolder4=list(name4)
addressHolder4=list(address4)
phoneHolder4=list(phone4)
neighborhoodHolder4=list(neighborhood4)
priceHolder4=list(price4)


# In[321]:

for x in nameHolder4:
    if x =="coffee":
        nameHolder4.remove(x)
    if x =="Coffee":
        nameHolder4.remove(x)
    if x =="coffeehouse":
        nameHolder4.remove(x)
    if x =="coffees":
        nameHolder4.remove(x)


# In[339]:

priceNumber4=[]
for x in priceHolder4["Price Level"]:
    priceNumber4.append(len(x))


# In[325]:

for i,s in enumerate(neighborhoodHolder4):
    neighborhoodHolder4[i] = s.strip()


# In[326]:

for i,s in enumerate(phoneHolder4):
    phoneHolder4[i] = s.strip()


# In[327]:

for i,s in enumerate(addressHolder4):
    addressHolder4[i] = s.strip()


# In[328]:

for i,s in enumerate(priceHolder4):
    priceHolder4[i] = s.strip()


# In[329]:

nameHolder4=DataFrame(nameHolder4,columns=["Name"])
addressHolder4=DataFrame(addressHolder4,columns=["Address"])
neighborhoodHolder4=DataFrame(neighborhoodHolder4,columns=["Neighborhood"])
phoneHolder4=DataFrame(phoneHolder4,columns=["Phone Number"])
priceHolder4=DataFrame(priceHolder4,columns=["Price Level"])
priceNumber4=DataFrame(priceNumber4,columns=["Price Number"])


# In[343]:

pageFour=nameHolder4.merge(addressHolder4,left_index=True,right_index=True).merge(neighborhoodHolder4,left_index=True,right_index=True).merge(phoneHolder4,left_index=True,right_index=True).merge(priceHolder4,left_index=True,right_index=True).merge(priceNumber4,left_index=True,right_index=True)


# In[344]:

pageFour


# # Page Five Scrape

# In[346]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco,+CA&start=40"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[347]:

name5=[]
neighborhood5=[]
address5=[]
city5=[]
phone5=[]
price5=[]


# In[348]:

result1_page5 = soup.find_all("div",{"class","media-story"})
result2_page5 = soup.find_all("div",{"class","biz-listing-large"})
priceCat_page5 = soup.find_all("div",{"class","price-category"})


# In[349]:

for x in result1_page5:
    try:
        name5.append(x.contents[1].find_all("span")[1].text)
    except:
        pass


# In[350]:

for x in result2_page5:
    try:
      address5.append(x.contents[3].find_all("address")[0].text)
    except:
        address5.append("N/A")


# In[351]:

for x in result2_page5:
    try:
      phone5.append(x.contents[3].find_all("span",{"class","biz-phone"})[0].text)
    except:
        phone5.append("N/A")


# In[352]:

for x in result2_page5:
    try:
      neighborhood5.append(x.contents[3].find_all("span",{"class","neighborhood-str-list"})[0].text)
    except:
        neighborhood5.append("N/A")


# In[353]:

for x in priceCat_page5:
    try:
        price5.append(x.contents[1].text)
    except:
        price5.append("N/A")


# In[358]:

price5.pop(0)
neighborhood5.pop(0)
phone5.pop(0)
address5.pop(0)


# In[359]:

nameHolder5=list(name5)
addressHolder5=list(address5)
phoneHolder5=list(phone5)
neighborhoodHolder5=list(neighborhood5)
priceHolder5=list(price5)


# In[361]:

for x in nameHolder5:
    if x =="coffee":
        nameHolder5.remove(x)
    if x =="Coffee":
        nameHolder5.remove(x)
    if x =="coffeehouse":
        nameHolder5.remove(x)
    if x =="coffees":
        nameHolder5.remove(x)


# In[365]:

nameHolder5.remove("Coffee'sâ€¦")


# In[372]:

for i,s in enumerate(neighborhoodHolder5):
    neighborhoodHolder5[i] = s.strip()


# In[373]:

for i,s in enumerate(phoneHolder5):
    phoneHolder5[i] = s.strip()


# In[374]:

for i,s in enumerate(addressHolder5):
    addressHolder5[i] = s.strip()


# In[375]:

for i,s in enumerate(priceHolder5):
    priceHolder5[i] = s.strip()


# In[376]:

priceNumber5=[]
for x in priceHolder5:
    priceNumber5.append(len(x))


# In[378]:

nameHolder5=DataFrame(nameHolder5,columns=["Name"])
addressHolder5=DataFrame(addressHolder5,columns=["Address"])
neighborhoodHolder5=DataFrame(neighborhoodHolder5,columns=["Neighborhood"])
phoneHolder5=DataFrame(phoneHolder5,columns=["Phone Number"])
priceHolder5=DataFrame(priceHolder5,columns=["Price Level"])
priceNumber5=DataFrame(priceNumber5,columns=["Price Number"])


# In[380]:

pageFive=nameHolder5.merge(addressHolder5,left_index=True,right_index=True).merge(neighborhoodHolder5,left_index=True,right_index=True).merge(phoneHolder5,left_index=True,right_index=True).merge(priceHolder5,left_index=True,right_index=True).merge(priceNumber5,left_index=True,right_index=True)


# In[381]:

pageFive


# In[385]:

coffeeDataframe=pd.concat([pageOne,pageTwo,pageThree,pageFour,pageFive],ignore_index=True)


# In[386]:

coffeeDataframe


# In[387]:

rating_page5 = soup.find_all("div",{"class","rating-large"})


# In[396]:

rating_page5[0]


# In[399]:

rating_page5[0].find_all("div",{"class","rating-large"})


# In[ ]:

rating5=[]


# In[488]:

for x in rating_page5:
    rating5.append(x('img')[0]['alt'])


# In[492]:

rating5.pop(0)

