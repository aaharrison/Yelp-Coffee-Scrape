
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


# In[8]:

df=pd.read_excel("YelpScrape.xlsx")


# # Page One Rating Scrape
# 

# In[2]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco%2C+CA&ns=1"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[10]:

rating_page1 = soup.find_all("div",{"class","rating-large"})


# In[15]:

rating0=[]
for x in rating_page1:
    rating0.append(x('img')[0]['alt'])


# In[18]:

rating0.pop(0)


# In[20]:

rating_page1=[]
for x in rating0:
    rating_page1.append(x[0:3])


# In[24]:

rating_page1=DataFrame(rating_page1,columns=["Ratings"])


# In[33]:

rating_page1


# # Page Two Rating Scrape

# In[25]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco,+CA&start=10"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[26]:

rating_page2 = soup.find_all("div",{"class","rating-large"})


# In[28]:

rating2=[]
for x in rating_page2:
    rating2.append(x('img')[0]['alt'])


# In[29]:

rating2.pop(0)


# In[30]:

rating_page2=[]
for x in rating2:
    rating_page2.append(x[0:3])


# In[32]:

rating_page2=DataFrame(rating_page2,columns=["Ratings"])


# In[34]:

rating_page2


# # Page Three Rating Scrape

# In[35]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco,+CA&start=20"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[36]:

rating_page3 = soup.find_all("div",{"class","rating-large"})


# In[37]:

rating3=[]
for x in rating_page3:
    rating3.append(x('img')[0]['alt'])


# In[38]:

rating3.pop(0)


# In[39]:

rating_page3=[]
for x in rating3:
    rating_page3.append(x[0:3])


# In[48]:

rating_page3=DataFrame(rating_page3,columns=["Ratings"])


# In[49]:

rating_page3


# # Page Four Rating Scrape

# In[43]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco,+CA&start=30"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[44]:

rating_page4 = soup.find_all("div",{"class","rating-large"})


# In[45]:

rating4=[]
for x in rating_page4:
    rating4.append(x('img')[0]['alt'])


# In[46]:

rating4.pop(0)


# In[47]:

rating_page4=[]
for x in rating4:
    rating_page4.append(x[0:3])


# In[50]:

rating_page4=DataFrame(rating_page4,columns=["Ratings"])


# In[51]:

rating_page4


# # Page Five Rating Scrape

# In[52]:

url = "https://www.yelp.com/search?find_desc=coffee&find_loc=San+Francisco,+CA&start=40"
r = requests.get(url)
soup = BeautifulSoup(r.content)


# In[53]:

rating_page5 = soup.find_all("div",{"class","rating-large"})


# In[54]:

rating5=[]
for x in rating_page5:
    rating5.append(x('img')[0]['alt'])


# In[55]:

rating5.pop(0)


# In[56]:

rating_page5=[]
for x in rating5:
    rating_page5.append(x[0:3])


# In[58]:

rating_page5=DataFrame(rating_page5,columns=["Ratings"])


# # Concat and Merge

# In[62]:

ratings=pd.concat([rating_page1,rating_page2,rating_page3,rating_page4,rating_page5],ignore_index=True)


# In[68]:

df=df.merge(ratings,how='outer',left_index=True,right_index=True)


# In[70]:

df.head(10)


# In[71]:

df.to_csv("yelpWebScrape.csv")


# In[81]:

df.groupby("Neighborhood")["Name"].count()


# # Combine Neighborhoods

# If two neighborhoors are listed, only the first are retained

# In[24]:

hood=[]
for x in df['Neighborhood']:
    if x == "Bernal Heights, Mission":
        hood.append("Bernal Heights")
    elif x == "Inner Richmond, Laurel Heights":
        hood.append("Inner Richmond")
    elif x == "Marina/Cow Hollow":
        hood.append("Marina")
    elif x == "Excelsior, Portola":
        hood.append("Excelsior")
    elif x =="North Beach/Telegraph Hill":
        hood.append("North Beach")
    elif x == "SoMa, Mission Bay":
        hood.append("SoMa")
    elif x == "Nob Hill, Union Square":
        hood.append("Nob Hill")
    elif x == "Nob Hill, Lower Nob Hill":
        hood.append("Nob Hill")
    elif x == "North Beach/Telegraph Hill":
        hood.append("North Beach")
    else:
        hood.append(x)


# In[29]:

df=df.merge(DataFrame(hood,columns=["neighborhood"]),left_index=True,right_index=True)
df.drop("Neighborhood",axis=1,inplace=True)
df.head()


# # Cleaning up repeated Coffee Shops

# In[56]:

df.replace(to_replace="Blue Bottle Coffee Co",value="Blue Bottle Coffee",inplace=True)


# In[118]:

df["Name"].value_counts()[:10]


# In[107]:

shops=[]
id = 0
for x in df["Name"]:
    if x not in shops:
        shops.append(x)
    else:
        id+=1
        shops.append(x+" "+str(id))


# In[122]:

df=df.merge(DataFrame(shops,columns=["Shop Name"]),left_index=True,right_index=True)
df.drop("Name",axis=1)
cols=["Shop Name","Address","Phone Number","Price Level","Price Number","Ratings","neighborhood"]
df=df[cols]
df.head()


# In[132]:

df.set_index("Shop Name",inplace=True)


# # Aggregation

# In[145]:

neighborhood=df.groupby("neighborhood")


# In[146]:

neighborhood["Price Number"].mean()


# In[149]:

df["neighborhood"].value_counts()


# # Adding Neighborhood Coordinates

# In[153]:

hoodlist=df['neighborhood'].unique()
hoodlist=DataFrame(hoodlist,columns={"Neighborhood"})
hoodlist["Lat"]=0;hoodlist["Long"]=0
hoodlist.set_index("Neighborhood",inplace=True)


# In[194]:

hoodlist.index.unique()


# In[301]:

coordinates=[{u"Name":"Mission", "Lat":37.759955,"Long":-122.41542},
{"Name": "SoMa", "Lat":37.779186,"Long":-122.405079},
{"Name": "Bernal Heights","Lat":37.742830,"Long":-122.413523},
{"Name":"Russian Hill", "Lat":37.801035,"Long":-122.417671},
{"Name": "Outer Sunset","Lat":37.755497,"Long": -122.493965},
{"Name": "Inner Sunset","Lat":37.760346,"Long":-122.468265},
{"Name": "Castro","Lat":37.761846,"Long":-122.434794},
{"Name": "Marina","Lat":37.803292,"Long": -122.436745},
{"Name": "Alamo Square","Lat":37.777507,"Long":-122.433010},
{"Name": "The Haight","Lat":37.770197,"Long":-122.445334},
{"Name": "Hayes Valley","Lat":37.775133,"Long":-122.426029},
{"Name": "Bayview-Hunters Point","Lat":37.730583,"Long":-122.382521},
{"Name": "Excelsior","Lat":37.727595,"Long":-122.422405},
{"Name": "Nob Hill","Lat":37.793011,"Long":-122.415855},
{"Name": "North Beach","Lat":37.805458,"Long":-122.406694},
{"Name": "Dogpatch","Lat":37.756953,"Long":-122.389044},
{"Name": "Potrero Hill","Lat":37.758639,"Long":-122.398771},
{"Name": "Noe Valley","Lat":37.749971,"Long":-122.433405},
{"Name": "Visitacion Valley","Lat":37.715185,"Long":-122.407118},
{"Name": "Lower Haight","Lat":37.772060,"Long":-122.432059},
{"Name": "Glen Park","Lat":37.737570,"Long":-122.432082},
{"Name": "Pacific Heights","Lat":37.792339,"Long":-122.434486},
{"Name": "Embarcadero","Lat":37.795489,"Long":-122.393983},
{"Name": "Inner Richmond","Lat":37.780242,"Long":-122.467832}]


# In[303]:

df=pd.merge(left=df2,right=DataFrame(coordinates),left_on="neighborhood",right_on="Name",how="outer")
df.drop("Name",axis=1,inplace=True)


# In[306]:

df.head()

