from bs4 import BeautifulSoup as soup
import requests
import csv

url = "https://www.sagepay.co.uk/partners-and-developers/partner-directory"
BASE_URL = "https://www.sagepay.co.uk"

fieldnames = ['Company']

# CSV file Open
def csv_file():
    with open('Partner Directory- Sagepay.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
# CSV file write row
def save_to_csv(data):
    with open('Partner Directory- Sagepay.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def sagepay(res, url):
    html = soup(res, "lxml")
    container = html.find('div', {'class':'view-content'})
    names = container.findAll('h2')
    for name in names:
        name = name.text.strip()
        save_to_csv([name])
    print (url)
    nxt = html.find('li',{'class':'next last'})
    return nxt

def webpage(url):
    res = requests.get(url)
    if res.status_code=="200" or res.status_code==200:
        nxt = sagepay(res.text, url)
        try:
            a = nxt.find('a',href=True)['href']
            url = BASE_URL + a
            webpage(url)
        except:
            return

csv_file()
webpage(url)
