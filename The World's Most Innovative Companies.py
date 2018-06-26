#!/bin/python

from selenium.webdriver import Firefox
import csv
import time

fieldnames = ['Rank', 'Company', 'Country', '12-Month Sales Growth', 'Innovation Premium' ]

# CSV file Open
def csv_file():
    with open('The World\'s Most Innovative Companies.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
# CSV file write row
def save_to_csv(data):
    with open('The World\'s Most Innovative Companies.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

# Scraper 
forbes = Firefox()
# url listing throught last
url = "https://www.forbes.com/innovative-companies/list/100/#tab:rank"
forbes.get(url)
time.sleep(10)
# Open CSV file
csv_file()

from bs4 import BeautifulSoup as soup
# extract data from webpage
html = soup(forbes.page_source, "html.parser")
# close browser
forbes.close()

container = html.find('tbody',{'id':'list-table-body'})
divs = container.findAll('tr', {'class':'data'})

for div in divs:
    col = div.findAll('td')
    data = []
    for field in col:
        field = field.text.encode('utf-8')
        if len(field):
            data.append(field)
    save_to_csv(data)

print ('%d data has been written'%len(divs))
print ('Process Done...')

