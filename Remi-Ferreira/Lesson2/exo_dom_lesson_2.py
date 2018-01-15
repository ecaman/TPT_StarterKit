
# coding: utf-8

# # Construction d'un Crawler du site des comptes des communes de Paris

# ## Packages nécéssaires

# In[1]:


from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd


# In[99]:


def extract_finances(year):
    
    # We first assemble our path to have it for correct year
    path_to_website = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
    path = path_to_website + str(year)
    
    # Now we get html code from page
    soup = BeautifulSoup(urlopen(path), 'html.parser')
    
    # We extract values and labels for the ones that are in bold in the html code 
    #(class = libellepetit G and montantpetitG)
    extracted_label = soup.findAll('td', {"class" : "libellepetit G"})
    extracted_values = soup.findAll("td", { "class" : "montantpetit G" })
    
    # We create a list containing only the labels inside the html <></>
    labels = []
    for label in extracted_label:
        labels.append(label.text)
    
    # We now want to create a list of values grouped 3 by 3 as they all are from same line, so same label
    values_triplet = []
    list_of_three = []
    for i in range(0,len(extracted_values)):
        if len(list_of_three) == 0:
            list_of_three.append(int(extracted_values[i].text.replace(' ', '')))
        elif len(list_of_three)%3 != 0:
            list_of_three.append(int(extracted_values[i].text.replace(' ', '')))
        else:
            values_triplet.append(list_of_three)
            list_of_three = []
            list_of_three.append(int(extracted_values[i].text.replace(' ', '')))
    
    # We insert Year label and year value in the first position of our lists
    labels.insert(0, "Year")
    values_triplet.insert(0, year)
    
    # To avoid a bug with some years where we get more values than labels we add the following line
    if(len(values_triplet) > len(labels)):
        del values_triplet[-1]
    
    return(values_triplet, labels)


# ### We now go through the different years and construct a dataframe containing for each line the values

# In[100]:


years = range(2010,2014)
total_result_over_years = pd.DataFrame(columns = ['Year','TOTAL DES PRODUITS DE FONCTIONNEMENT = A', 'TOTAL DES CHARGES DE FONCTIONNEMENT = B', 
                                                  'RESULTAT COMPTABLE = A - B = R', "TOTAL DES RESSOURCES D'INVESTISSEMENT = C", 
                                                  "TOTAL DES EMPLOIS D'INVESTISSEMENT = D", 
                                                  "Besoin ou capacité de financement Résiduel de la section d'investissement = D - C", 
                                                  "= Besoin ou capacité de financement de la section d'investissement = E", 
                                                  "Résultat d'ensemble = R - E"])
count = 0
for year in years:
    values, labels = extract_finances(year)
    total_result_over_years.loc[count] = values
    count = count + 1
    #print(total_result_over_years)


# In[101]:


total_result_over_years

