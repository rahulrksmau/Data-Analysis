from bs4 import BeautifulSoup as soup
import requests
import csv
import time

url = "https://www.sugarcrm.com/partners/reselling-partners"
res = requests.get(url)

url_suffix = []
if res.status_code == 200 or res.status_code == "200":
    resource = soup(res.text, "lxml")
    resource = resource.find('div', {'id': 'resource_type'})
    urls = resource.findAll('a', {'class': 'dropdown-item'})
    for u in urls:
        print(url + u['href'])
        url_suffix.append(u['href'])

fieldnames = ['Company', 'Location', 'Email', 'Website']


# CSV file Open
def csv_file():
    with open('Partner Directory- Suparcrm.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# CSV file write row
def save_to_csv(data):
    with open('Partner Directory- Suparcrm.csv', 'a' , encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

csv_file()


def request_per_page(url_):
    response = requests.get(url_)
    if response.status_code == 200 or response.status_code == "200":
        html_soup = soup(response.text, "lxml")
        divs = html_soup.findAll('div', {'class': "card partner shadow"})
        for div in divs:
            row_data = []
            row_data.append(div.h4.text.strip().encode('utf-8').decode())
            data = div.findAll('p')
            for p in data:
                link,info = p.a,p.b
                if link or info:
                    if link:
                        row_data.append(link['href'].strip())
                    elif info.text:
                        row_data.append(info.text.strip())
            save_to_csv(row_data)
        return True
    else:
        return False


# requesting urls
for url_ in url_suffix:
    print("requesting %s" % (url + url_))
    if request_per_page(url + url_):
        print("Data scraped from %s" % (url + url_))
    else:
        print("%s Url Left" % (url + url_))
    time.sleep(10)
