import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from sqlalchemy import create_engine

# Connect to MySQL
user = 'root'
password = input("PLease add password: ")
hostName = 'localhost'
port = 3306
database = 'truecar'

cnx = mysql.connector.connect(user=user, password=password,
                              host=hostName)
cursor = cnx.cursor()


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)



try:
    cursor.execute("USE {}".format(database))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(database))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(database))
        cnx.database = database
    else:
        print(err)
        exit(1)
cnx.close()


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
            carPrice = carPrice.replace(",", "")
            carMile = car.find("div", class_="d-flex w-100 justify-content-between").text.split(" ")[0]
            carMile = carMile.replace(",", "")
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
    connectionMySql = create_engine('mysql+pymysql://' + user + ':' + password + '@' +
                                    hostName + ':' + str(port) + '/' + database, echo=False)

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
            # dfStore.to_csv("./carReported.csv")
            print(dfStore.head(5))
            try:
                dfStore.to_sql(name='cardetail', con=connectionMySql, if_exists='replace', index=False)
            except:
                print("Please Check you connection")
            time.sleep(time_wait * 60)  # 60*24
        else:
            # dfStore.to_csv("./carReportedFinalNew.csv")
            try:
                dfStore.to_sql(name='cardetail', con=connectionMySql, if_exists='replace', index=False)
            except:
                print("Please Check you connection")
            break

    print(dfStore.head())
    print(dfStore.tail())
