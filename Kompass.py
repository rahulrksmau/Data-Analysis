from bs4 import BeautifulSoup as soup
import urllib2
import csv
import time

BASE_URL = # Website URL
cls1 = "headerRowLeft col-xs-12 col-sm-12 col-md-5"
cls2 = "noLogo headerRowLeft col-xs-12 col-sm-12 col-md-5"


def Scrapper(start_id, end_id,writer):
    idx = start_id
    while idx<=end_id:
        builder = urllib2.build_opener()
        builder.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            a = builder.open(BASE_URL+str(idx))
            if a.code == 200:
                raw_html = soup(a.read(), 'lxml')
                iterator = raw_html.findAll('div',{'class':cls1})
                if len(iterator)==0: iterator = raw_html.findAll('div',{'class':cls2})
                name,adr = None,None
                # Name of Company
                if len(iterator):   
                    name = (iterator[0].findAll('h1')[0].text).strip()
                # Address 
                    for div_ in iterator:
                        div_.findAll('h1')[0].text
                        data = []
                    for p in div_.findAll('p')[:1]:
                        adr = ((p.text).replace('\n',',').replace('\r','').replace('  ','').strip())
                act_id = "secondaryActivitiesTree"  
                act = raw_html.find('div',{'id':act_id})
                act_iter = act.findAll('a')
                type_c = []
                for act in act_iter:
                    type_c.append(act.text.strip())
                type_c = ', '.join(type_c)
                csvfile =  open('revdata.csv', 'a')
                fieldnames = ['Name', 'Type', 'Address']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Name': name, 'Type': type_c, 'Address':adr})
                csvfile.close()
                print ('id %d is working ...'%idx)
        except :
            print ('id %d is not working ...'%idx)
            pass
        idx += 1
        time.sleep(120)
        if idx%10 == 0 : time.sleep(240)
        
if __name__ == "__main__":

    #writer.writeheader()
    start_id, end_id = map(int,raw_input('Start and end ids for Scrapping ').split())
    Scrapper(start_id, end_id)

