"""This file extracts the UK MPs data. It corresponds to the first part of the UK.ipynb notebook. Data is saved in data/uk_mps_dataframe.csv."""

# Import libraries----------------------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

# England Data-------------------------------------------------------------------------------------------------------------------------------

# I want to use the Wikipedia API to get the html for the page that lists current sitting England MPs
eng_page_key = 'List_of_MPs_for_constituencies_in_England_(2019–present)'
eng_page_endpoint = 'page/' + eng_page_key + '/html'
stem_url = 'https://en.wikipedia.org/w/rest.php/v1/'
universal_url = 'https://en.wikipedia.org/wiki/'
headers = {'User-Agent': 'Student Project'}

eng_url = stem_url + eng_page_endpoint

def get_html(url):
    '''Gives HTML of a given URL as a BeautifulSoup object'''
    r = requests.get(url, headers=headers)
    s = BeautifulSoup(r.text, 'html.parser')
    return s

# I want to get a list of all the wikitables on the page
def get_wikitables(s):
    '''Gives a list of all the wikitables on a given page'''
    wikitables = s.find_all('table', class_='wikitable')
    return wikitables

# I want to get only the 3rd, 5th, 7th, 9th, 11th, 13th, 15th, 17th and 19th tables in one list, as these contain the MPs
england_mp_wikitables = get_wikitables(get_html(eng_url))[2:20:2]
england_mp_wikitables

# I want to get the links from the mp tables and put them in a list
eng_names = [link.text for table in england_mp_wikitables for link in table.find_all('span', class_='fn')]
eng_names = [link.replace(" ", "_") for link in eng_names]
eng_links = [link.find('a')['href'] for table in england_mp_wikitables for link in table.find_all('span', class_='fn')]
england_mp_links = [link.replace("./", universal_url) for link in eng_links]

# I need to get rid of the 12 MPs who have resigned or died since the last election - they are only in the england page, and are italicised in the page
page_html = get_html(eng_url).find_all('i')
relevant_lines = page_html[1:13]
resigned_MP_links = [link.get('href') for i in relevant_lines for link in i.find_all('a')]
resigned_MP_links = [link.replace("./", universal_url) for link in resigned_MP_links]
resigned_MP_links = [link.replace(" ", "_") for link in resigned_MP_links]
len(resigned_MP_links)

# I want to get rid of the resigned MPs from the list of links
england_mp_links_final = [link for link in england_mp_links if link not in resigned_MP_links]
len(england_mp_links_final)
# I encounter an issue here - there is one too few MP for England (532 instead of 533)
# I will investigate the missing MP later, using TheyWorkForYou's database of sitting MPs, after completing analysis for other parts of the UK.

# Wales Data---------------------------------------------------------------------------------------------------------------------------------

# I want to use the Wikipedia API to get the html for the page that lists current sitting Welsh MPs
wal_page_key = 'List_of_MPs_for_constituencies_in_Wales_(2019–present)'
wal_page_endpoint = 'page/' + wal_page_key + '/html'
stem_url = 'https://en.wikipedia.org/w/rest.php/v1/'
universal_url = 'https://en.wikipedia.org/wiki/'
headers = {'User-Agent': 'Student Project'}

wal_url = stem_url + wal_page_endpoint
wales_mp_wikitables = get_wikitables(get_html(wal_url))[1]

wal_names = [link.text for link in wales_mp_wikitables.find_all('span', class_='fn')]
wal_names = [link.replace(" ", "_") for link in wal_names]
wal_links = [link.find('a')['href'] for link in wales_mp_wikitables.find_all('span', class_='fn')]
wales_mp_links = [link.replace("./", universal_url) for link in wal_links]

# Scotland Data------------------------------------------------------------------------------------------------------------------------------

# I want to use the Wikipedia API to get the html for the page that lists current sitting Scottish MPs
sco_page_key = 'List_of_MPs_for_constituencies_in_Scotland_(2019–present)'
sco_page_endpoint = 'page/' + sco_page_key + '/html'
stem_url = 'https://en.wikipedia.org/w/rest.php/v1/'
universal_url = 'https://en.wikipedia.org/wiki/'
headers = {'User-Agent': 'Student Project'}

sco_url = stem_url + sco_page_endpoint
scotland_mp_wikitables = get_wikitables(get_html(sco_url))[1]

# I want to get the links from the MP tables and put them in a list
sco_names = [link.text for link in scotland_mp_wikitables.find_all('span', class_='fn')]
sco_names = [link.replace(" ", "_") for link in sco_names]
sco_links = [link.find('a')['href'] for link in scotland_mp_wikitables.find_all('span', class_='fn')]
scotland_mp_links = [link.replace("./", universal_url) for link in sco_links]

# Northern Ireland Data----------------------------------------------------------------------------------------------------------------------

ni_page_key = 'List_of_MPs_for_constituencies_in_Northern_Ireland_(2019–present)'
ni_page_endpoint = 'page/' + ni_page_key + '/html'
stem_url = 'https://en.wikipedia.org/w/rest.php/v1/'
universal_url = 'https://en.wikipedia.org/wiki/'
headers = {'User-Agent': 'Student Project'}

ni_url = stem_url + ni_page_endpoint
northern_ireland_mp_wikitables = get_wikitables(get_html(ni_url))[2]

# I want to get the links from the mp tables and put them in a list
ni_names = [link.text for link in northern_ireland_mp_wikitables.find_all('span', class_='fn')]
ni_names = [link.replace(" ", "_") for link in ni_names]
ni_links = [link.find('a')['href'] for link in northern_ireland_mp_wikitables.find_all('span', class_='fn')]
northern_ireland_mp_links = [link.replace("./", universal_url) for link in ni_links]

# Combine the lists to get a UK list of MPs Wikipedia links (650)--------------------------------------------------------------------

uk_mp_links = england_mp_links_final + wales_mp_links + scotland_mp_links + northern_ireland_mp_links
len(uk_mp_links)
# Something is wrong - there are 650 sitting MPs, but I have 649 links. I need to find out which one is missing.
# Now I return to the question of why England has one too few MPs after removing the 12 MPs who are no longer serving

# I will use the TheyWorkForYou webpage for sitting MPs to crosscheck
pages_html = get_html('https://www.theyworkforyou.com/mps/')
mp_names_twfy = pages_html.find_all('h2', class_='people-list__person__name')
mp_names_twfy = [link.text for link in mp_names_twfy]
mp_names_twfy = [link.replace(" ", "_") for link in mp_names_twfy]
len(mp_names_twfy)

# Now using regex I want to see which name is missing from my list of 649 UK MPs
missing_by_regex = [name for name in mp_names_twfy if re.search(name, str(uk_mp_links)) == None]
missing_by_regex

# Given the nature of some names (eg Jon Ashworth vs Jonathan Ashworth) I need to find the missing MP by hand from this list of 23 anomalies identified by regex search
# I have found that the missing MP is Kim Leadbeater, who was elected in July 2021 - this is a mistake on Wikipedia's part, for not including her in the longlist of MPs at time of writing (she replaced Tracy Babin post-resignation, but her name was not added to the England list)
# I will add her to the list of links manually, but add a check in case she is added to the Wikipedia list in the future
missing_mp_link = 'https://en.wikipedia.org/wiki/Kim_Leadbeater'
def add_missing_link(link):
    if link not in uk_mp_links:
        uk_mp_links.append(link)
    else:
        pass
    return uk_mp_links

uk_mp_links_final = add_missing_link(missing_mp_link)
# I now have 650 links, which is correct

# Extracting information for UK analysis: birth date & alma mater---------------------------------------------------------------------------

def get_mp_info(link):
        '''Takes a link to a UK MP's Wikipedia page and returns a dictionary of their name, birth date, party and university'''
        mp_info = {}
        mp_page_html = get_html(link)
        mp_page_infobox = mp_page_html.find('table', class_='infobox')
        try: 
            mp_info['name'] = mp_page_html.find('div', class_='fn').text
        except: 
            mp_info['name'] = None
        if mp_info['name'] == 'Nigel Evans':
            mp_info['birth date'] = '1957-11-10' # This is becuase of an error in his wikipedia page giving his birth date as 2017
        else:
            try:
                mp_info['birth date'] = mp_page_html.find('span', class_ = 'bday').text
            except:
                mp_info['birth date'] = None
        all_mp_page_links = mp_page_infobox.find_all('a', title = True)
        try:
            mp_info['party'] = [link.text for link in all_mp_page_links if re.search('Party|Liberal Democrats|Co-operative|Sinn|Independent|Conservative|Labour|Plaid', str(link)) != None][0]
        except:
            mp_info['party'] = None
        try:
            mp_info['university'] = [link.text for link in all_mp_page_links if re.search('University|London School of Economics|Imperial|Guildhall|Malachy|, Oxford|, Cambridge|Oxford$|Cambridge$', str(link)) != None][0]
        except:
            mp_info['university'] = None
        return mp_info

# Get a dataframe of all sitting MPs birth date, party, alma mater and name
uk_mps_df = pd.DataFrame([get_mp_info(link) for link in uk_mp_links_final])
# Takes <5 mins to run
uk_mps_df['birth date'] = pd.to_datetime(uk_mps_df['birth date'])
uk_mps_df['age'] = round((pd.to_datetime('today') - uk_mps_df['birth date'])/np.timedelta64(1,'Y'), 1)

# Save data file
uk_mps_df.to_csv('../data/uk_mps_dataframe.csv', index=False)