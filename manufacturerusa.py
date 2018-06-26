import requests
import csv
import time
from bs4 import BeautifulSoup as Soup

BASE_URL = "http://www.manufacturerusa.com/"

fieldnames = ['Name', 'State', 'Website']


# CSV file Open
def csv_file():
    with open('US Manufacturer by State.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# CSV file write row
def save_to_csv(data):
    with open('US Manufacturer by State.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def Categories(link):
    cat_req = requests.get(link)
    html_cat = Soup(cat_req.content,"lxml")
    table_body = html_cat.find('div',{'class':'listings'}).find('table')
    State = requests.utils.urlparse(link).path.split('/')[1]
    child = table_body.findChild()
    while child:
        title = child.find('div',{'class':'title'}).text.replace("\n",'')
        website=child.find('div',{'class':'url'}).text.replace("\n",'')
        save_to_csv([title,State,website])
        print ([title,State,website])
        child = child.findNextSibling()


def main():
    res = requests.get(BASE_URL)
    if int(res.status_code) == 200:
        html = Soup(res.content, "lxml")
        div = html.find('div', {'class': 'categories'})
        ch = div.findChild()
        while ch:
            time.sleep(5)
            try:
                if ch.find('div', {'class': 'subcategories'}):
                    subcat = ch.find('div', {'class': 'subcategories'})
                    links = subcat.findAll('a')
                    for link in links:
                        # print (link["href"])
                        link = link["href"]
                        Categories(link)
                else:
                    cat = ch.find('div', {'class': 'categ'})
                    link = cat.a["href"]
                    Categories(link)
            except AttributeError :
                pass

            ch = ch.findNextSibling()


if __name__ == "__main__":
    csv_file()
    main()
