import pandas as pd
from sqlalchemy import create_engine

user = 'root'
password = input("PLease add password: ")
hostName = 'localhost'
port = 3306
database = 'truecar'

connectionMySql = create_engine('mysql+pymysql://' + user + ':' + password + '@' +
                                hostName + ':' + str(port) + '/' + database, echo=False)




df = pd.read_csv('./carReportedFinal.csv')

print(df.columns)




#Preparing query to create a database
sql = "CREATE database MYDATABASE";

try:
    df.to_sql(name='cardetail', con=connectionMySql, if_exists='replace', index=False)

except:
    print("Please Check you connection")
