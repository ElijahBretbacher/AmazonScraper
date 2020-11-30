from requests_html import HTMLSession
from bs4 import BeautifulSoup

# HTMLSession() stores the current Session inside a variable
session = HTMLSession()

# the term to search for on amazon. Spaces converted to + for the url
searchterm = input("Enter a search term: ")
searchterm.replace(" ", "+")

# array that stores dictionaries of products
items = []

url = f'https://www.amazon.de/s?k={searchterm}'

# returns the whole html of 1 site
def getSoup(url):
    response = session.get(url)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, 'html.parser')
    return soup

def clearFile(filePath):
    file = open(filePath, "w")
    file.write("")
    file.close()

def getProducts(soup):
    counter = 1
    products = soup.find_all("div", {"data-component-type": "s-search-result"})
    for item in products:
        title = item.find("a", {"class": "a-link-normal a-text-normal"}).text.strip()
        short_title = item.find("a", {"class": "a-link-normal a-text-normal"}).text.strip()[:25]
        link = "https://amazon.de" + item.find("a", {"class": "a-link-normal a-text-normal"})["href"]
        try:
            price = item.find_all("span", {"class": "a-price-whole"})[0].text
        except:
            try:
                price = item.find("span", {"class": "a-price-whole"}).text
            except:
                price = "undefined"

        try:
            oldPrice = item.find_all("span", {"class": "a-offscreen"})[1].text
        except:
            try:
                oldPrice = item.find("span", {"class": "a-offscreen"}).text
            except:
                oldPrice = "undefined"

        oldPrice = oldPrice.replace("€", "")
        oldPrice = oldPrice.strip()
        productObject = {
            "short_title": short_title,
            "price": price,
            "oldPrice": oldPrice,
            "link": link
        }
        items.append(productObject)

        if price != oldPrice:
            discount = open("discounts.txt", "a")
            discount.write("Title: " + short_title + "\nNew Price: " + price + "\nOld Price: " + oldPrice + "\nURL: " + link + "\n\n")
            discount.close()

        file = open("products.txt", "a")
        file.write(short_title + "\n" + price + " " + oldPrice + "\n" + link + "\n\n")
        file.close()
        print("Item scraped! " + str(counter))
        counter+=1

def getNextPage(soup):
    # this will return the next page URL
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.de' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        print(str(url))
        return url
    else:
        return


clearFile("discounts.txt")
clearFile("products.txt")
while True:
    try:
        data = getSoup(url)
        getProducts(data)
        url = getNextPage(data)
        if not url:
            break
    except:
        break

