import requests
import csv
from bs4 import BeautifulSoup as Soup

url = "https://university.graduateshotline.com/ubystate.html#NC"

fieldnames = ['Name', 'State', 'Website']


# CSV file Open
def csv_file():
    with open('US Universities by State.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# CSV file write row
def save_to_csv(data):
    with open('US Universities by State.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)


def getData(div):
    try:
        raw = div.a
        name = raw.text.strip()
        url = raw["href"]
    except AttributeError:
        name = div.text.strip()
        url = None
    return name, url


def main():
    res = requests.get(url)
    if int(res.status_code) == 200:
        html_soup = Soup(res.content, "lxml")
        cont = html_soup.find('ol')  # List body
        university, State, website = None, "Alabama", None
        name = cont.findChild()
        while name:
            if name.find('big'):
                nState = name.find('big').text
            else:
                nState = State

            if name.find('ul'):
                try:
                    par = name.a.text.strip()
                except:
                    par = ""
                for li in name.findAll('li'):
                    university, website = getData(li)
                    university = par + ", " + university
                    print(university, website)
                    save_to_csv([university, State, website])
            else:
                university, website = getData(name)
                print(university, website)
                save_to_csv([university, State, website])

            if State!=nState: State= nState
            name = name.findNextSibling()
        return True
    else:
        return False

if __name__ == "__main__":
    csv_file()
    print ("Done " if main() else "Error ")
