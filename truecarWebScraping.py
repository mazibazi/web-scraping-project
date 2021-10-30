import requests
from bs4 import BeautifulSoup
import xlsxwriter

# search = input("Enter search term: ")
# params = {"q": search}

# r = requests.get("https://www.truecar.com/used-cars-for-sale/listings/", params=params)
r = requests.get("https://www.truecar.com/used-cars-for-sale/listings/acura/")
soup = BeautifulSoup(r.text, "html.parser")

cars = soup.find_all("div", class_="card-content")

workbook = xlsxwriter.Workbook('cars.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0

for car in cars:
    carName = car.find("span", class_="vehicle-header-make-model text-truncate").text
    carAge = car.find("span", class_="vehicle-card-year font-size-1").text
    carGear = car.find("div", class_="font-size-1 text-truncate").text
    carPrice = car.find("div",
                        class_="padding-left-3 padding-left-lg-2 vehicle-card-bottom-pricing-secondary vehicle-card-bottom-max-50").text
    carMile = car.find("div", class_="d-flex w-100 justify-content-between").text.split(" ")[0]
    carLocationCity = car.find("div", class_="vehicle-card-location font-size-1 margin-top-1").text.split(",")[0]
    carLocationState = car.find("div", class_="vehicle-card-location font-size-1 margin-top-1").text.split(",")[1]
    carColorEx = car.find("div", class_="vehicle-card-location font-size-1 margin-top-1 text-truncate").text.split(" ")[
        0]
    carColorIn = car.find("div", class_="vehicle-card-location font-size-1 margin-top-1 text-truncate").text.split(" ")[
        2]
    carAccident = (car.find_all("div", class_="vehicle-card-location font-size-1 margin-top-1"))[-1].text.split(",")[0]
    carOwner = (car.find_all("div", class_="vehicle-card-location font-size-1 margin-top-1"))[-1].text.split(" ")[2]
    carUsage = (car.find_all("div", class_="vehicle-card-location font-size-1 margin-top-1"))[-1].text.split(" ")[-2]

    print(carName, carAge, carGear, carPrice, carMile, carLocationCity,
          carLocationState, carColorEx, carColorIn, carAccident, carOwner, carUsage)
    worksheet.write(row, col, carName)
    worksheet.write(row, col + 1, carAge)
    worksheet.write(row, col + 2, carGear)
    worksheet.write(row, col + 3, carPrice)
    worksheet.write(row, col + 4, carMile)
    worksheet.write(row, col + 5, carLocationCity)
    worksheet.write(row, col + 6, carLocationState)
    worksheet.write(row, col + 7, carColorEx)
    worksheet.write(row, col + 8, carColorIn)
    worksheet.write(row, col + 9, carAccident)
    worksheet.write(row, col + 10, carOwner)
    worksheet.write(row, col + 11, carUsage)

    row += 1
workbook.close()
