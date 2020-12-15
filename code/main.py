import pandas as pd
import json

import pyodbc

with open("../json/top-rated-indian-movies-02.json") as f:
    data = json.load(f)
    print(data)
    dataframe = pd.DataFrame(data)
    dataframe.head()
    dataframe.columns
    dataframe.shape
    #####connectionstring###
    #  conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};TrustServerCertificate=No;DATABASE=Movies_DB;WSID=LAPTOP-BLDSMT2E;APP={Microsoft® Windows® Operating System};
    #  Trusted_Connection=Yes;SERVER=(localdb)\MSSQLLocalDB;Description=movies')
    #########################################


    # Data Source=(localdb)\MSSQLLocalDB;
    # Initial Catalog=Movies;Integrated Security=True;
    # Connect Timeout=30;Encrypt=False;
    # TrustServerCertificate=False;A
    # pplicationIntent=ReadWrite;
    # MultiSubnetFailover=False

# with open ("C:\\Dayana\\GCU\\Upwork\\Moviedata.json") as f:
#    data=json.load(f)
import sys
import pyodbc as odbc

import pyodbc
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};TrustServerCertificate=No;DATABASE=Movies_DB;WSID=LAPTOP-BLDSMT2E;APP={Microsoft® Windows® Operating System};Trusted_Connection=Yes;SERVER=(localdb)\MSSQLLocalDB;Description=movies')

cursor = conn.cursor()
#cursor.execute("INSERT INTO [dbo].[Table_]  VALUES (7,'oDD')")
cursor.execute('''

               CREATE TABLE People
               (
               Name nvarchar(50),
               Age int,
               City nvarchar(50)
               )

               ''')

conn.commit()
cursor.execute("INSERT INTO [dbo].[People]  VALUES ('neenu',34,'oDD')")
cursor.commit()
cursor.execute("Select * from [dbo].[People]")

for row in cursor:
    print(row)

cursor.execute("DROP TABLE [dbo].[People]")
cursor.commit()
