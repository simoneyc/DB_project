import requests
from lxml import html
from openpyxl import Workbook
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

tree = html.fromstring(response.content)

movies = []
rank = 0
soup = BeautifulSoup(response.text, 'html.parser')

for movie in tree.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 iMNUXk compact-list-view ipc-metadata-list--base']/li"):
    if rank==5:
        break
    # title = movie.xpath(".//div[@class='ipc-metadata-list-summary-item__c']/div/div/div/a/h3/text()")[0]
    year = movie.xpath(".//div[@class='ipc-metadata-list-summary-item__c']/div/div/div/span/text()")[0]
    rate = movie.xpath(".//div[@class='ipc-metadata-list-summary-item__c']/div/div/span/div/span/text()")[0]
    murl = 'https://www.imdb.com/'+movie.xpath(".//div[@class='ipc-metadata-list-summary-item__c']/div/div/div/a/@href")[0]
    print(murl) # title+' '+year+' '+rate+' '+

    # Make a request to the movie page
    movie_response = requests.get(murl, headers=headers)
    movie_tree = html.fromstring(movie_response.content)
    # Extract additional information from the movie page
    # Example: Extracting the movie title 
    try:
        title = movie_tree.xpath("//h1[@data-testid='hero__pageTitle']/span/text()")[0]
    except:
        title = None
    try:
        director = movie_tree.xpath("//ul[@class='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base']/li/a/text()")[0]
    except:
        director = None
    try:
        time = movie_tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]/text()')[0]
    except:
        time = None
    try:
        release_day = movie_tree.xpath('////*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[11]/div[2]/ul/li[1]/div/ul/li/a/text()')[0]
        release_day= re.sub(r'\([^)]*\)', '', release_day).strip()
    except:
        release_day = None
    try:
        genre = movie_tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a/span/text()')[0]
    except:
        genre = None
    try:
        country = movie_tree.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[12]/div[2]/ul/li[2]/div/ul/li/a/text()')[0]
    except:
        country = None
    try:
        team = movie_tree.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[12]/div[2]/ul/li[7]/div/ul/li/a/text()')[0]
    except:
        team = None
    try:
        gross = movie_tree.xpath('//*[@id="__next"]/main/div/section[0]/div/section/div/div[1]/section[13]/div[2]/ul/li[4]/div/ul/li/span/text()')[0]
    except:
        gross = None
    
    # Store the information in a dictionary or other data structure  
    rank = rank + 1
    movie_info = {
        'rank': rank,
        'title': title,
        'year': year,
        'rate': rate,
        'genre': genre,
        'country': country,
        'director': director,
        'team': team,
        'time': time,
        'release_day': release_day,
        'gross': gross,
        'url': murl
        
        # Add other relevant information here...
    }

    # Append the movie information to the list
    movies.append(movie_info)


# Now, 'movies' list contains information about each movie
# for movie in movies:
#     print(movie)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(movies)

# Export the DataFrame to an Excel file
df.to_excel('movie_data.xlsx', index=False)

print("Data written to movie_data.xlsx")