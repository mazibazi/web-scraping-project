import requests
from bs4 import BeautifulSoup


page = requests.get("https://divar.ir/s/tehran")


soup = BeautifulSoup(page.text, "html.parser")

products = soup.find_all("div", class_="kt-post-card__title")
price = soup.find_all("div", class_ = "kt-post-card__description")


agreementPrice = '\u062A\u0648\u0627\u0641\u0642\u06CC'


listProducts = []
for item in products:
    listProducts.append(item.text)
listPrice = []
for item in price:
    listPrice.append(item.text)
    
    
counterIndex = 0
targetCounter = []
for el in listPrice:
    if el == agreementPrice:
        targetCounter.append(counterIndex)
    counterIndex += 1

for el in targetCounter:
    print(listProducts[el],"--->",listPrice[el])
