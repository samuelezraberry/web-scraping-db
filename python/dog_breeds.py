import requests
from bs4 import BeautifulSoup
import csv

url="https://dogtime.com/dog-breeds/profiles"

response=requests.get(url)
soup=BeautifulSoup(response.text, 'html.parser')

breeds=soup.find_all("a",{"class":"list-item-title"})

with open("dog_breeds.csv", 'w', newline="") as csvfile:
    wr = csv.writer(csvfile)
    for breed in breeds:
        wr.writerow([breed.text])