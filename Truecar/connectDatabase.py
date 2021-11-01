import pandas as pd
from sqlalchemy import create_engine

user = 'root'
password = input("PLease add password: ")
hostName = 'localhost'  # either localhost or ip e.g. '172.17.0.2' or hostname address
port = 3306
database = 'truecar'

connectionMySql = create_engine('mysql+pymysql://' + user + ':' + password + '@' +
                                hostName + ':' + str(port) + '/' + database, echo=False)

df = pd.read_csv('./carReported.csv')

print(df.columns)

df.drop(df.columns[0], axis=1, inplace=True)

try:
    df.to_sql(name='cardetail', con=connectionMySql, if_exists='replace', index=False)

except:
    print("Please Check you connection")
