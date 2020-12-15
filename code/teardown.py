import pandas as pd
import json

import pyodbc
from dask.dataframe.methods import values

import pyodbc


def dbcleanup():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};TrustServerCertificate=No;DATABASE=Movies_DB;WSID=LAPTOP-BLDSMT2E;APP={Microsoft® Windows® Operating System};Trusted_Connection=Yes;SERVER=(localdb)\MSSQLLocalDB;Description=movies')

    cursor = conn.cursor()

    cursor.execute("DROP TABLE [dbo].[Top_rated_Movie]")
    cursor.execute("DROP TABLE [dbo].[Movie_Actor_Relationship]")
    cursor.execute("DROP TABLE [dbo].[Movie_Genre_Relationship]")
    cursor.commit()
    conn.close()
