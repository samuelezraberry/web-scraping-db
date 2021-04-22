import requests
from bs4 import BeautifulSoup
import csv

url="https://en.wikipedia.org/wiki/List_of_Microsoft_Windows_versions"

response=requests.get(url)
soup=BeautifulSoup(response.text, 'html.parser')

table=soup.find("table",{"class":"wikitable sortable"})
rows=table.find_all("tr")
with open("windows_versions.csv", 'w', newline="") as csvfile:
    wr = csv.writer(csvfile)
    for row in rows:
        r=row.find("td")
        if r is not None:
            wr.writerow([r.text])

