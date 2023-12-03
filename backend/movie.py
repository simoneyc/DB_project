import requests
import csv
from lxml import html
from openpyxl import workbook
import re


url = 'https://www.imdb.com/chart/top/'

headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)


tree = html.fromstring(response.content)

movies = []
rank = 0
for movie in tree.xpath("//ul[@class='ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 iMNUXk compact-list-view ipc-metadata-list--base']/li"):
    # if rank == 5:
    #     break
    murl = 'https://www.imdb.com/'+movie.xpath(".//div[@class='ipc-metadata-list-summary-item__c']/div/div/div/a/@href")[0]
    # Make a request to the movie page
    movie_response = requests.get(murl, headers=headers)
    movie_tree = html.fromstring(movie_response.content)

    try:
        # Extract additional information from the movie page
        title = movie_tree.xpath("//h1[@data-testid='hero__pageTitle']/span/text()")[0]
    except IndexError:
        title = None

    try:
        director = movie_tree.xpath("//ul[@class='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base']/li/a/text()")[0]
    except IndexError:
        director = None

    try:
        time = movie_tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]/text()')[0]
    except IndexError:
        time = None

    try:
        release_day = movie_tree.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[11]/div[2]/ul/li[1]/div/ul/li/a/text()')[0]
        release_day = release_day.replace(' (Taiwan)', '')
    except IndexError:
        release_day = None

    try:
        genre = movie_tree.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a/@href')[0]
        pattern = re.compile(r'genres=([^&]+)')

        match = pattern.search(genre)
        if match:
            genre_value = match.group(1)
            
        else:
            print("No match found.")
        if match:
            genres_string = match.group(0)
    except IndexError:
        genres_string = None
    # try:
    #     world_gross = movie_tree.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[13]/div[2]/ul/li[4]/div/ul/li/span/text()')[0]
    # except IndexError:
    #     world_gross = None
    # actor = []
    # i = 0
    # for i in range(0,5):
    #     try:
    #         actor[i] = movie_tree.xpath(f'//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[4]/div[2]/div[2]/div[{i}]/div[2]/a/text()')[0]
    #     except IndexError:
    #         actor[i] = None
    
    # try:
    #     world_gross = movie_tree.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[13]/div[2]/ul/li[4]/div/ul/li/span/text()')[0]
    # except IndexError:
    #     world_gross = None
    # Process the extracted information as needed
    # print(f"Title: {title}, Director: {director}, Time: {time}, Release Day: {release_day}, Genre: {genre}")
    rank = rank + 1
    movie_info = {
        # 'url': murl,
        'title': title,
        # 'director': director,
        'time': time,
        'release_day': release_day,
        'genre': genre_value,
        # 'world_gross': world_gross,
        # 'actor': actor[i],
        # 'rank': rank
        # Add other relevant information here...
    }

    movies.append(movie_info)
    print(rank)


with open('movie_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
     fieldnames = ['url', 'title', 'director', 'time', 'release_day', 'genre', 'rank']
     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

     writer.writeheader()

     # Write the data to the CSV file
     for movie in movies:
         writer.writerow(movie)

print("Data written to movie_data.csv")