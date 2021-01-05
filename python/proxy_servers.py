import requests
from bs4 import BeautifulSoup
import csv

url="https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt"

response=requests.get(url)
assert(response.status_code==200)


with open("proxy_servers.csv", 'w', newline="") as csvfile:
    wr = csv.writer(csvfile)
    wr.writerow(["Server","HTTPS","Anonymous","Google","Country"])
    for l in response.text.split("\n")[9:]:
        l=l.split()
        try:
            server=l[0]
            info=l[1]
            google=l[2]
        except IndexError:
            continue
        G=google=="+"
        HTTPS="-S" in info
        ANON="-A-" in info or "-H-" in info
        CC=info.split("-")[0]
        wr.writerow([server,HTTPS,ANON,G,CC])