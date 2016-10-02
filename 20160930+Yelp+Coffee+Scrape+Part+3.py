
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


# In[2]:

os.chdir("/Users/adeniyiharrison/Documents")


# In[4]:

df=pd.read_csv("yelpWebScrape.csv")


# In[5]:

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


# In[12]:

df=pd.merge(left=df,right=DataFrame(coordinates),left_on="neighborhood",right_on="Name",how="outer")
df.drop("Name",axis=1,inplace=True)


# In[16]:

import plotly.plotly as py


# In[21]:

credentials={
    "username": "aaharrison31",
    "api_key": "rt8mj4cauw"
}


# In[22]:

import plotly.tools as tls
tls.set_credentials_file(credentials)


# In[24]:

tls.set_credentials_file(username='aaharrison31', api_key='rt8mj4cauw')


# In[25]:

import plotly.plotly as py
from plotly.graph_objs import *

trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace0, trace1])

py.plot(data, filename = 'basic-line')


# In[26]:

df.head()


# In[136]:

def name(y):
    if y in df["neighborhood"].unique():
        return df[df["neighborhood"]==y]["Shop Name"]
    return "No Shops"


# In[141]:

print(name("Mission"))


# In[146]:

hood_group=df.groupby("neighborhood")


# In[169]:

hood=hood_group.mean()


# In[186]:

DataFrame(hood_group["Shop Name"].count()).reset_index()


# In[191]:

hood=hood.merge(DataFrame(hood_group["Shop Name"].count()).reset_index(),left_on="neighborhood",right_on="neighborhood")
hood.columns = ["Neighborhood","Price Average","Rating Average","Lat","Long","Shop Count"]


# In[192]:

hood


# In[202]:

mapbox_access_token = 'pk.eyJ1IjoiY2hlbHNlYXBsb3RseSIsImEiOiJjaXFqeXVzdDkwMHFrZnRtOGtlMGtwcGs4In0.SLidkdBMEap9POJGIe1eGw'



data = Data([
    Scattermapbox(
        lat= hood["Lat"],
        lon= hood["Long"],
        mode='markers',
        marker=Marker(
            size=9
        ),
        text=hood["Neighborhood"]
    )
])
layout = Layout(
    title = "First 50 Coffee Shops from Yelp Scrape",
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=37.776845,
            lon=-122.419535
        ),
        pitch=0,
        zoom=10
    ),
)

fig = dict(data=data, layout=layout)
py.iplot(fig, filename='Yelp Coffee Scatter Map', validate=False)


# In[200]:

hood.to_csv("neighborhoodAverage.csv")

