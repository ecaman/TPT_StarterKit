
# coding: utf-8

# In[11]:


from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd


# In[28]:


path_acer = "https://www.cdiscount.com/search/10/acer.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.ContentTypeId=16&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=acer&page="
path_dell = "https://www.cdiscount.com/search/10/dell.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.ContentTypeId=16&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=acer&page="


def count_promotions(path_cdiscount, number_of_pages = 10):
    counter = 0
    for i in range(1,number_of_pages):
        path_cdiscount = path_cdiscount + str(i) + "&_his_#_his_"
        soup = BeautifulSoup(urlopen(path_cdiscount), 'html.parser')
        extracted_values = soup.findAll("div", { "class" : "prdtPrSt" })
        counter = counter + len(extracted_values)
    return counter



        


# In[29]:


count_acer = count_promotions(path_acer, 20)


# In[30]:


count_dell = count_promotions(path_dell, 20)


# In[31]:


print("Il y a ", count_acer, " promos acer")
print("Il y a ", count_dell, " promos dell")

