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

""" :parameter url: URL that should be converted into the soup
    :return returns a parsed html text
"""
def getSoup(url):
    response = session.get(url)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, 'html.parser')
    return soup


""" :parameter filePath: the path of the file to be cleared
    clears a file
 """
def clearFile(filePath):
    file = open(filePath, "w")
    file.write("")
    file.close()


""" :parameter soup:  the soup that should be searched
    this function stores every title, price, and url into a file called 'products.txt' and stores every item on discount
    into "discounts.txt". The array 'items' will also be filled with every item.
"""
def getProducts(soup):
    # array that holds all the products html code
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    for item in products:
        # attributes of the item get filtered out
        title = item.find("a", {"class": "a-link-normal a-text-normal"}).text.strip()
        short_title = item.find("a", {"class": "a-link-normal a-text-normal"}).text.strip()[:30]
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

        # replace € and " " with nothing so both 'oldPrice' and 'price' can be equal
        oldPrice = oldPrice.replace("€", "")
        oldPrice = oldPrice.strip()

        # dictionary storing every relevant variable
        productObject = {
            "short_title": short_title,
            "price": price,
            "oldPrice": oldPrice,
            "link": link
        }

        items.append(productObject)

        # if an item is on discount, add it to the text file
        if price != oldPrice:
            discount = open("discounts.txt", "a")
            discount.write("Title: " + short_title + "\nNew Price: " + price + "\nOld Price: " + oldPrice + "\nURL: " + link + "\n\n")
            discount.close()

        # add every item into a textfile regardless
        file = open("products.txt", "a")
        file.write(short_title + "\n" + price + " " + oldPrice + "\n" + link + "\n\n")
        file.close()


"""" :parameter soup: the whole html text of the current page
     :return the next url 
     opens the next page to iterate through
"""
def getNextPage(soup):
    # this will return the next page URL
    pages = soup.find('ul', {'class': 'a-pagination'})

    # if there is a next page available, get the link and return it
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.de' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        print(str(url))
        return url
    else:
        return


# clear files before starting
clearFile("discounts.txt")
clearFile("products.txt")

# loop runs as long as the program has URLs to iterate through
while True:
    # get the current page, extract data, open new page, repeat.
    try:
        data = getSoup(url)
        getProducts(data)
        url = getNextPage(data)
        if not url:
            break
    except:
        break

