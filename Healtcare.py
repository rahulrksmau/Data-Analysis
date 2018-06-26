import requests
import csv
import time
from bs4 import BeautifulSoup as Soup

BASE_URL = "https://www.healthcare-informatics.com/"
URL = "https://www.healthcare-informatics.com/hci100/optum-4"  # First Rank company url

fieldnames = ['Name', 'Company-info', 'Website', 'Revenue']


# CSV file Open
def csv_file():
    with open('US Healthcare by State.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# CSV file write row
def save_to_csv(data):
    with open('US Healthcare by State.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)


def check(test_):
    return isinstance(type(test_), type(Soup))


def get_next_url(body):
    botton = body.find('div', {'class': 'hci100-buttons'}).find('span',{'class':'right-btn'})
    try:
        return (BASE_URL + botton.a["href"])
    except:
        return None


def main(url):
    ress = requests.get(url)
    next_url = None
    if int(ress.status_code) == 200:
        html_f = Soup(ress.content, "lxml")
        body = html_f.find('article', {'class': 'node node-hci100 clearfix'})
        divs = body.find('div', {'class': 'content'})
        next_url = get_next_url(divs)
        datas = divs.findAll('div', {'class': 'hci100-field'})
        info = []
        for data in datas:
            raw = data.text
            if ':' in raw:
                info.append(raw.split(':')[-1])
        save_to_csv(info)
        print(info)
        print (next_url)
        time.sleep(10)
    if next_url:
        main(next_url)

if __name__ == "__main__":
    csv_file()
    main(URL)
