import requests
from bs4 import BeautifulSoup
import random
import csv
import time

userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Vivaldi/3.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",    
]

def headers():
    return {'User-Agent':random.choice(userAgents),
    'referer':'https://google.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Pragma': 'no-cache',
    }

url="https://www.google.com/search?q=site%3Alinkedin.com+%22{0}%22+%22gmail.com%22+OR+%22yahoo.com%22+OR+%22mail.com%22&start={1}"

def extractEmails(text):
    emails=[]
    for c in ["'","[","]","\"","(",")","/",":",";","\"",","]: text=text.replace(c," ")
    for s in text.split():
        if "." in s and "@" in s:
            if s[-1]==".":
                s=s[:-1]
            emails.append(s)
    return emails

def scrapeEmails(keyword,page):
    emailAddresses=[]
    
    while True:
        response=requests.get(url.format(keyword,page*20),headers=headers())
        if response.status_code != 200:
            print("sleeping due to response code",response.status_code)
            time.sleep(60*3)
        else:
            break
        
    soup=BeautifulSoup(response.text, 'html.parser')
    spans=soup.find_all("span",{"class":"aCOpRe"})
    for span in spans:
        emailAddresses.extend(extractEmails(span.text))
    return list(set(emailAddresses))

kw=input("keyword: ")
start=int(input("start at page: "))

zeroCount=0

with open(kw+"_emails.csv", 'a', newline="") as csvfile:
    wr = csv.writer(csvfile)
    myEmails=[]
    for i in range(start,start+10,1):
        scraped=scrapeEmails(kw,i)
        print("mined",len(scraped),"emails from page",i)
        if len(scraped) == 0:
            zeroCount+=1
        else:
            zeroCount=0
        if zeroCount>=2:
            break # no more pages
        for e in scraped:
            wr.writerow([e])
        time.sleep(random.randint(1,10))