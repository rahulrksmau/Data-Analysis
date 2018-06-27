import requests
from bs4 import BeautifulSoup as soup
import csv
import time
url = "https://www.alfresco.com/partners?page="

fieldnames = ['Partner level', 'Company', 'Location']


# CSV file Open
def csv_file():
    with open('Partner Directory- alfresco.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# CSV file write row
def save_to_csv(data):
    with open('Partner Directory- alfresco.csv', 'a' , encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

class Scraper:
    def __init__(self, link):
        self.url = link
        self.soupHtml()

    def getHtml(self):
        self.raw_html = requests.get(self.url)
        if self.raw_html.status_code == 200 or self.raw_html.status_code == "200":
            return True
        else:
            return False

    def soupHtml(self):
        if self.getHtml():
            self.html = soup(self.raw_html.content, "lxml")
            id = "block-views-98fdd4364577f71a850d4219ecbf73a3"
            container  = self.html.find('div',{'id':id})
            articles = container.select('article')
            for article in articles:
                row = []
                row.append(article.find('div',{'class':'cards__card-header'}).text.replace('\n','').strip())        # part_level
                #except: pass
                
                row.append(article.h4.text.replace('\n','').strip())             # title
                #except: pass
                
                row.append(article.find('div',{'class':'drupal__field-categorisation-region'}).text.replace('\n','').strip())  #region
                #except: pass
                #print (row)
                save_to_csv(row)

if __name__ == "__main__":
    # csv_file()
    for i in range(1,8):
        s = Scraper(url+str(i))
        print ("URL %s scrapped "%(url+str(i)))
        time.sleep(10)
