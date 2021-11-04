import pandas as pd

# from sqlalchemy import create_engine
#
# password = input("PLease add password: ")
# user = 'root'
# hostName = 'localhost'
# port = 3306
# database = 'truecar'
#
# connectionMySql = create_engine('mysql+pymysql://' + user + ':' + password + '@' +
#                                 hostName + ':' + str(port) + '/' + database, echo=False)
#
#
# df = pd.read_sql('SELECT * FROM cardetail', con=connectionMySql)
#

# data preparing
df = pd.read_csv("carReportedFinal.csv")
df.drop(df.columns[0], axis=1, inplace=True)
df.drop(df.columns[14:16], axis=1, inplace=True)
print(df.columns)
