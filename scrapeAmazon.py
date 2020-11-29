from requests_html import HTMLSession
from bs4 import BeautifulSoup

s = HTMLSession()
searchterm=input("Enter a search term: ")
searchterm.replace(" ", "+")

url = f'https://www.amazon.de/s?k={searchterm}&i=electronics&ref=nb_sb_noss'

def getData(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def getProducts(soup, file):
    products = soup.find_all("div", {"data-component-type": "s-search-result"})
    for item in products:
        title = item.find("a", {"class": "a-link-normal a-text-normal"}).text.strip()
        short_title = item.find("a", {"class": "a-link-normal a-text-normal"}).text.strip()[:25]
        link = "https://amazon.de" + item.find("a", {"class": "a-link-normal a-text-normal"})["href"]
        try:
            price = item.find_all("span", {"class": "a-offscreen"})[0].text
        except:
            try:
                price = item.find("span", {"class": "a-offscreen"}).text
            except:
                price = "undefined"

        file.write(short_title + "\n" + price + "\n" + link + "\n\n")
        print("Page scraped!")

def getNextPage(soup):
    # this will return the next page URL
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.de' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return

file = open("products.txt", "w")
file.write("")
file.close()
file = open("products.txt", "a")
while True:
    try:
        data = getData(url)
        getProducts(data, file)
        url = getNextPage(data)
        if not url:
            break
    except:
        break
