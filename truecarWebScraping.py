import requests
from bs4 import BeautifulSoup

search = input("Enter search term: ")
params = {"q": search}

r = requests.get("https://www.truecar.com/used-cars-for-sale/listings/", params=params)
soup = BeautifulSoup(r.text, "html.parser")

cars = soup.find_all("div", class_="card-content")
for el in cars:
    print(el.text)
