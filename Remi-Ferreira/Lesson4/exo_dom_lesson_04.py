
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
from multiprocessing import Pool
from itertools import chain
import numpy as np


# In[2]:


def get_links(path):
    # Now we get html code from page
    soup = BeautifulSoup(urlopen(path), 'html.parser')
    
    
    # We extract the href corresponding to each car
    extracted_href = soup.findAll("a", {"href": re.compile("//www.leboncoin.fr/voitures/*")})
    s = str(extracted_href)
    
    # To have the titles corresponding to the links, we extract bot the links and titles for /voitures/
    # And store only the titles, because they are clean.
    titles = re.findall(r'title="(\S.*)"', s)
    titles = titles[:len(titles)-1]
    
    # title gathered one value more than it should have, it will always be the last one because it is in the page's footer.
    
    
    # Now we extract the links corresponding to cars ads. 
    links = re.findall(r'www.leboncoin.fr/voitures/\d+\.\w*.\w*.\w*', s)
    return links


# In[3]:


# Prendre les derniers chiffres pour les kilomètres, en général c'est 5 chiffres...
def check_number_digits_km(km):
    if(km == 'NA'):
        return 'NA'
    else:
        s = str(km)
        if(len(s)> 5):
             s= s[-5:]
        return int(s)


# In[4]:


def extract_info_from_link(link):
    # Now we get html code from page
    soup2 = BeautifulSoup(urlopen("https://" + link), 'html.parser')
    
    # We extract title of ad:
    extracted_title = soup2.find("h1", {"class":"no-border"}).text.strip()
    
    
    # We extract the price
    extracted_price = soup2.findAll("h2", {"class": re.compile("item_price clearfix")})
    price = re.findall(r'content="(.*?)"',str(extracted_price))[0] # price contient [prix, Currency]
    
    # We extract the year
    extracted_year = soup2.findAll("span", {"itemprop": re.compile("releaseDate")})
    year = extracted_year[0].text.strip()
    
    # Now we want to extract phone number, model, and kilometers of the car in the description:
    # We first extract the description and convert it to a string:
    extracted_description = soup2.findAll("div", {"class": "line properties_description"})
    extracted_description = str(extracted_description[0])
    
    # Extraction of the kilometers of the car:
    km = re.findall(r'(\d+).?(\d*)\s*(km|kms|KM|KMS|Km|Kms)', str(extracted_description))
    # This can find a lot of different values for the kilometers, we admit that the first one is the one we want.
    # But we check as well if we extracted at least one value for kilometers. If not we set it to NA
    if(len(km)>0):
        elements_of_km = ""
        for item in km[0][:len(km[0])-1]:
            elements_of_km = elements_of_km + item
        km = elements_of_km
    else:
        km="NA"
    km = check_number_digits_km(km)
    
    # Extraction of the car's model, it can be between 3 values, Zen, Intens and Life.
    model = re.findall(r'(zen|intens|life|Zen|Intens|Life)', str(extracted_description))
    if(len(model)>0):
        model = model[0]
    else:
        model = "NA"
        
    # Extraction of the seller's phone number:
    phone_number = re.findall(r'0[1-9]\d{8}', str(extracted_description))
    if(len(phone_number)>0):
        phone_number = phone_number[0]
    else:
        phone_number = "NA"
        
    # Check if seller is a pro or not:
    extracted_pro = soup2.findAll("span", {"class": "ispro"})
    if len(extracted_pro) > 0:
        ispro = True
    else:
        ispro = False
    
    # Return description, it could be useful:
    description = re.sub(r'<[^>]*>', " ", str(extracted_description))
    
    description.upper()
    
    return extracted_title, price, year, km, model, phone_number, ispro, description


# In[5]:


def get_zoe_links_for_region(region):
    print("start")
    root_link = "https://www.leboncoin.fr/annonces/offres/"
    car = "renault%20zo%E9"
    page = 1
    path = root_link + region + "/?th=" + str(page) + "&q=" + car
    links = []
    links.append(get_links(path))
    continuing = True
    while continuing == True :
        page = page + 1
        path = root_link + region + "/?th=" + str(page) + "&q=" + car
        new_links = get_links(path)
        if len(new_links) > 0:
            links.append(new_links)
        else:
            continuing = False
    print("end")
    return list(chain.from_iterable(links))


# In[6]:


regions = ["ile_de_france", "aquitaine", "provence_alpes_cote_d_azur"]

links = list(map(lambda x: get_zoe_links_for_region(x), regions))
links = list(chain.from_iterable(links))
#links


# In[7]:


pool = Pool(processes=8)
df_zoe = pool.map(extract_info_from_link, links)
df_zoe = pd.DataFrame(df_zoe, columns=["Title","Price","Year","km","Model","Phone","IsPro","Description"])


# In[8]:


df_zoe


# In[9]:


def check_title_model(title):
    model = re.findall(r'(zen|intens|life|Zen|Intens|Life|ZEN|INTENS|LIFE)', title)
    if(len(model)>0):
        return model[0]
    else:
        return "NA"

df_zoe['Model'].loc[df_zoe['Model'] == "NA"] = list(map(lambda x: check_title_model(x), df_zoe['Title'].loc[df_zoe['Model'] == "NA"]))
df_zoe['Model'] = list(map(lambda x: x.upper(), df_zoe['Model']))
df_zoe['Description'] = list(map(lambda x: x.upper(), df_zoe['Description']))
df_zoe.head(5)


# In[10]:


def extract_links_argus(year):
    path = "https://www.lacentrale.fr/cote-voitures-renault-zoe--" + str(year) + "-.html"
    soup3 = BeautifulSoup(urlopen(path), 'html.parser')
    
    # We extract values and labels for the ones that are in bold in the html code 
    extracted_href = soup3.findAll("a", {"href": re.compile("cote-auto-renault-zoe-*")})
    links_argus = re.findall(r'cote-auto-renault-zoe-(.*).html', str(extracted_href))
    return links_argus, list(np.repeat(year, len(links_argus)))
#links_argus = extract_links_argus(path_argus)


# In[11]:


def get_cote(path):
    soup4 = BeautifulSoup(urlopen(path), 'html.parser')
    # We extract values and labels for the ones that are in bold in the html code 
    extracted_cote = soup4.findAll("span", {"class": "jsRefinedQuot"})
    extracted_model = soup4.findAll("span", {"class": "sizeC clear txtGrey7C sizeC"})

    return extracted_cote[0].text.strip(), extracted_model[0].text.strip()
#get_cote(path_cote)


# In[14]:


years = [2013, 2014, 2015, 2016, 2017]
links_argus = list(map(lambda x: extract_links_argus(x), years))


links_argus = list(chain.from_iterable(links_argus))
years = links_argus[1::2]
years = list(chain.from_iterable(years))
links_argus = links_argus[0::2]
links_argus = list(chain.from_iterable(links_argus))

links_argus = list(map(lambda x: "https://www.lacentrale.fr/cote-auto-renault-zoe-" + str(x) + ".html", links_argus))
links_argus


# In[15]:


df_argus = pool.map(get_cote, links_argus)
df_argus = pd.DataFrame(df_argus, columns = ["Price", "Model"])
df_argus["Year"] = years
df_argus.head(5)


# In[16]:


# On créé pour argus une colonne modele en extrayant Zen, LIFE, on intens.
def get_first_word(sentence):
    split_sentence = sentence.split(" ")
    return split_sentence[0]
def delete_first_word(sentence):
    split_sentence = sentence.split(" ")
    if len(split_sentence) > 1:
        return ' '.join(split_sentence[1:])
    else:
        return sentence
df_argus["Gamme"] = list(map(lambda x: get_first_word(x), df_argus["Model"]))
df_argus["Model"] = list(map(lambda x: delete_first_word(x), df_argus['Model']))
df_argus.head(5)


# In[17]:


def check_cote(model, year, description):
    
    df_filtered = df_argus
    # On filtre sur l'année dans un premier temps
    df_filtered = df_filtered.loc[df_filtered['Year'] == int(year)].loc[df_filtered['Gamme'] == model]
    #print(df_filtered)
    # On filtre ensuite sur la gamme
    
    # Maintenant il faut vérifier si notre voiture est parmis l'un des modèles:
    count = 0
    for gamme in df_filtered['Model']:
        count = count +1
        #print(gamme)
        if gamme in description:
            #print(gamme)
            #print(count)
            return df_filtered['Price'].loc[df_filtered["Model"] == gamme].values[0].strip()
    return 'NA'

df_zoe['Argus'] = list(map(check_cote, df_zoe["Model"], df_zoe['Year'], df_zoe['Description']))
df_zoe.head(5)

