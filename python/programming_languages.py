import requests
from bs4 import BeautifulSoup
import csv

url="https://en.wikipedia.org/wiki/List_of_programming_languages"

response=requests.get(url)
soup=BeautifulSoup(response.text, 'html.parser')

divs=soup.find_all("div",{"class":"div-col"})

with open("programming_languages.csv", 'w', newline="", encoding="utf-8") as csvfile:
    wr = csv.writer(csvfile)
    for div in divs:
        for a in div.find_all("a"):
            wr.writerow([a.text])