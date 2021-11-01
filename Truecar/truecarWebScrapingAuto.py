import time

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


def findCar(url, start, finish):
    counter = 0
    dfTemp = pd.DataFrame(columns=columnName)

    for page in range(start, finish):
        updateUrl = url + str(page)
        r = requests.get(updateUrl)
        soup = BeautifulSoup(r.text, "html.parser")
        cars = soup.find_all("div", class_="card-content")

        for car in cars:
            counter += 1
            currentTimeDate = datetime.now()
            carName = car.find("span", class_="vehicle-header-make-model text-truncate").text
            carCompany = carName.split(" ")[0]
            carAge = car.find("span", class_="vehicle-card-year font-size-1").text
            carGear = car.find("div", class_="font-size-1 text-truncate").text
            carPrice = car.find("div",
                                class_="padding-left-3 padding-left-lg-2 vehicle-card-bottom-pricing-secondary vehicle-card-bottom-max-50").text
            carPrice = carPrice.replace("$", "")
            carMile = car.find("div", class_="d-flex w-100 justify-content-between").text.split(" ")[0]
            carLocationCity = car.find("div", class_="vehicle-card-location font-size-1 margin-top-1").text.split(",")[
                0]
            carLocationState = car.find("div", class_="vehicle-card-location font-size-1 margin-top-1").text.split(",")[
                1]
            carColorEx = \
                car.find("div", class_="vehicle-card-location font-size-1 margin-top-1 text-truncate").text.split(" ")[
                    0]
            carColorIn = \
                car.find("div", class_="vehicle-card-location font-size-1 margin-top-1 text-truncate").text.split(" ")[
                    2]
            carAccident = \
                (car.find_all("div", class_="vehicle-card-location font-size-1 margin-top-1"))[-1].text.split(",")[0]
            carAccident = carAccident.split(" ")[0]
            carOwner = \
                (car.find_all("div", class_="vehicle-card-location font-size-1 margin-top-1"))[-1].text.split(" ")[2]
            carUsage = \
                (car.find_all("div", class_="vehicle-card-location font-size-1 margin-top-1"))[-1].text.split(" ")[
                    -2]

            if carAccident == "No":
                carAccident = 0
            currentTime = currentTimeDate.strftime("%H:%M:%S")
            currentDay = currentTimeDate.strftime("%Y,%m,%d")
            listTemp = (carName, carCompany, carAge, carGear, carPrice, carMile, carLocationCity, carLocationState,
                        carColorEx, carColorIn, carAccident, carOwner, carUsage, currentTime, currentDay)
            dfTemp.loc[len(dfTemp)] = listTemp

    return dfTemp


if __name__ == '__main__':
    columnName = ["carName", "carCompany", "carAge", "carGear", "carPrice", "carMile", "carLocationCity",
                  "carLocationState",
                  "carColorEx", "carColorIn", "carAccident", "carOwner", "carUsage", "currentTime", "currentDay"]
    dfStore = pd.DataFrame(columns=columnName)
    url = "https://www.truecar.com/used-cars-for-sale/listings/?page="
    firstPage = 1
    lastPage = 334
    timeCounter = 0
    while True:
        timeCounter += 1
        time_wait = 60  # based on minute
        print("Start at: ", datetime.now().strftime("%H:%M:%S"))
        dfOutput = findCar(url, firstPage, lastPage)
        dfStore = dfStore.append(dfOutput, ignore_index=True)
        dfStore.drop_duplicates(subset=dfStore.columns[1:13], keep="last", inplace=True)
        print("Finish at: ", datetime.now().strftime("%H:%M:%S"))
        print(f'Waiting {time_wait} minutes ....')
        if timeCounter < 2:
            dfStore.to_csv("./carReported.csv")
            print(dfStore.head())
            print(dfStore.tail())
            time.sleep(time_wait * 60)
        else:
            dfStore.to_csv("./carReportedFinal.csv")
            break

    print(dfStore.head())
    print(dfStore.tail())
