import requests
from bs4 import BeautifulSoup
import xlsxwriter
from datetime import datetime

# search = input("Enter search term: ")
# params = {"q": search}

# r = requests.get("https://www.truecar.com/used-cars-for-sale/listings/" + search)
url = "https://www.truecar.com/used-cars-for-sale/listings/?page="
counter = 0
row = 0
workbook = xlsxwriter.Workbook('truecarSite/cars.xlsx')
worksheet = workbook.add_worksheet()
for page in range(1, 2):
    updateUrl = url + str(page)

    r = requests.get(updateUrl)
    soup = BeautifulSoup(r.text, "html.parser")

    cars = soup.find_all("div", class_="card-content")

    col = 0

    for car in cars:
        counter += 1
        currentTimeDate = datetime.now()
        carName = car.find("span", class_="vehicle-header-make-model text-truncate").text
        carAge = car.find("span", class_="vehicle-card-year font-size-1").text
        carGear = car.find("div", class_="font-size-1 text-truncate").text
        carPrice = car.find("div",
                            class_="padding-left-3 padding-left-lg-2 vehicle-card-bottom-pricing-secondary vehicle-card-bottom-max-50").text
        carMile = car.find("div", class_="d-flex w-100 justify-content-between").text.split(" ")[0]
        carLocationCity = car.find("div", class_="vehicle-card-location font-size-1 margin-top-1").text.split(",")[0]
        carLocationState = car.find("div", class_="vehicle-card-location font-size-1 margin-top-1").text.split(",")[1]
        carColorEx = \
            car.find("div", class_="vehicle-card-location font-size-1 margin-top-1 text-truncate").text.split(" ")[
                0]
        carColorIn = \
            car.find("div", class_="vehicle-card-location font-size-1 margin-top-1 text-truncate").text.split(" ")[
                2]
        carAccident = \
            (car.find_all("div", class_="vehicle-card-location font-size-1 margin-top-1"))[-1].text.split(",")[0]
        carOwner = (car.find_all("div", class_="vehicle-card-location font-size-1 margin-top-1"))[-1].text.split(" ")[2]
        carUsage = (car.find_all("div", class_="vehicle-card-location font-size-1 margin-top-1"))[-1].text.split(" ")[
            -2]
        carLink = car.find_all("a", class_="linkable order-2 vehicle-card-overlay")

        currentTime = currentTimeDate.strftime("%H:%M:%S")
        currentDay = currentTimeDate.strftime("%Y,%m,%d")

        # print(counter, carName, carAge, carGear, carPrice, carMile, carLocationCity,
        #      carLocationState, carColorEx, carColorIn, carAccident, carOwner, carUsage)
        print(counter, carName, carPrice, currentDay, currentTime, carLink)


