import requests
from lxml import html
from openpyxl import Workbook
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import traceback
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

tree = html.fromstring(response.content)

movies = []
rank = 1

for movie in tree.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 iMNUXk compact-list-view ipc-metadata-list--base']/li"):

    try:
        img_url = movie.xpath(f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{rank}]/div[1]/div/div[2]/img/@src')[0]
        urllib.request.urlretrieve(img_url, f'{rank}.jpg')
    except:
        print("Traceback:", traceback.format_exc())
        title = None
    
    
    # Store the information in a dictionary or other data structure  
    rank = rank + 1
    # movie_info = {
    #     'rank': rank,
    #     'title': title,
    #     'year': year,
    #     'rate': rate,
    #     'genre': genre,
    #     'country': country,
    #     'director': director,
    #     'team': team,
    #     'time': time,
    #     'release_day': release_day,
    #     'gross': gross,
    #     'url': murl
        
    #     # Add other relevant information here...
    # }

    # Append the movie information to the list
    # movies.append(movie_info)


# Now, 'movies' list contains information about each movie
# for movie in movies:
#     print(movie)

# Create a DataFrame from the list of dictionaries
# df = pd.DataFrame(movies)

# # Export the DataFrame to an Excel file
# df.to_excel('movie_data.xlsx', index=False)

print("Data written to movie_data.xlsx")