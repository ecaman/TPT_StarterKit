
# coding: utf-8

# In[7]:


import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re
import requests


# In[100]:


# Trouver les villes:
path = "https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/"

# Now we get html code from page
soup = BeautifulSoup(urlopen(path), 'html.parser')

# We extract values and labels for the ones that are in bold in the html code 
extracted_td = soup.tbody.find_all("td", {"class": "xl65"})
cities = []
for i in range (1, 400, 3):
    cities.append(extracted_td[i].text.strip())
cities


# In[28]:


# Distance Paris Lyon:
depart = "Paris"
arrivee = "Lyon"
url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + depart + "&destinations=" + arrivee

response_cities = requests.get(url=url).json()#, auth = (username, password)).json()
distance = response_cities["rows"]
print(distance[0]['elements'][0]['distance']['value'], "mètres")


# In[71]:


def calculate_distance_between_cities(start, end):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + start + "&destinations=" + end
    response_cities = requests.get(url=url).json()
    distance = response_cities["rows"][0]['elements'][0]['distance']['value']
    return distance


# In[104]:


# Dataframe
df = pd.DataFrame()
df['Distance_Ville'] = cities[:10]
df


# In[106]:


for city in cities[:10]:
    list_distance_one_city = []
    for city2 in cities[:10]:
        list_distance_one_city.append(calculate_distance_between_cities(city, city2))
    df[city] = list_distance_one_city
df


# In[107]:


df.to_csv("Distance_top_100_cities.csv")

