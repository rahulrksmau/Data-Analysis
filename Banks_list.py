from bs4 import BeautifulSoup as soup
import requests
import random 
import csv
import time
import re
import os
BASE_URL = "https://www.bankbranchlocator.com/banks-in-usa.html"
header = {'user-agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
fieldnames = ['Bank Name','Branch Name','Service Type','State & County','City or Town','Zip Code','Phone Number','Office Address', 'Url']
delay = [3,2,5,1,6,4,0.5]
# CSV file Open
csv_file_name = "US Banks"
try:
    pattern = re.compile(r'US Banks[0-9]*\.csv$')
    last_file = pattern.search(' '.join(os.listdir(os.getcwd())))
    last_file =  last_file.group()
    s,e = last_file.find('s'), last_file.find('.')
    index = last_file[s+1:e]
    csv_file_name = csv_file_name+str(int(index)+1)+".csv"
except :
    csv_file_name += ".csv"

def csv_file():
    with open(csv_file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# CSV file write row
def save_to_csv(data):
    with open(csv_file_name, 'a') as csvfile:
        writer = csv.writer(csvfile)
        print (data)
        writer.writerow(data)

def bank_info(url,name):
    try:
        resp = requests.get(url, headers=header, timeout = 10)
        if int(resp.status_code) == 200:
            html_soup = soup(resp.content, "lxml")
            bank_information = html_soup.find('div', {'class':'bank_information'})
            informations = bank_information.findChildren('div')
            data = [name]
            for info in informations[:-1]:
                txt = info.text.split(':')
                if txt[0]=='Phone Number':
                    data.append(txt[1][:12])
                else:
                    data.append(txt[1])
            data.append(url)
            save_to_csv(data)
    except:
        return  None

def state_office_branch(url,name):
    try:
        res = requests.get(url, headers=header, timeout = 10)
        if int(res.status_code)==200:
            html_soup = soup(res.content, "lxml")
            cls = "showlist"
            cont = html_soup.find('div',{'id':cls})
            branches = cont.findAll('div', {'class':'left_branches'})
            for branch in branches:
                url = branch.a['href']
                bank_info(url,name)
                time.sleep(random.choice(delay))
    except:
        return None


def banks_office(url):
    try:
        res = requests.get(url, headers=header, timeout = 10)
        if int(res.status_code)==200:
            html_soup = soup(res.content, "lxml")
            cls = "showlist"
            name = html_soup.h1.text
            container = html_soup.find('div',{'id':cls})
            state_offices = container.findAll('li')
            print (len(state_offices))
            for state_office in state_offices:
                url = state_office.a['href']
                state_office_branch(url,name)
                time.sleep(random.choice(delay))
            print (count)
    except:
        return None
'''
# Read from previous csv , so that iteration start from next
# bank information
def read_last_file(filename):
    url_list = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                url_list.append(row[-1])
            except:
                pass
    return url_list
'''
# Page where all bank names 
# iterate through per bank name
def main():
    try:
        req = requests.get(BASE_URL, headers=header, timeout = 10)
        if int(req.status_code)==200:
            html_soup = soup(req.content, "lxml")
            cls = "leftdiv clearleft"
            container = html_soup.find('div', {'class':cls})
            banks = container.findAll('li')
            for bank in banks:
                url = bank.a['href']
                banks_office(url)
                time.sleep(random.choice(delay))
    except:
        return None

import sys
if __name__=="__main__":
    csv_file()
    #old_csv = input('old CSV file')
    # old_csv = sys.argv[1]
    main()
