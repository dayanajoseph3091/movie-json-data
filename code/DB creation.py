import json

import pandas as pd
import pyodbc

import teardown as db

db.dbcleanup()
with open("../json/top-rated-indian-movies-02.json") as f:
    data = json.load(f)
    # print(data)
    dataframe = pd.DataFrame(data)
dataframe
dataframe['genres'] = dataframe['genres'].astype('str').apply(
    lambda x: x.lower().strip().replace("[", "").replace("]", "").replace("\'", "").replace("\"", "").strip())
dataframe['ratings'] = dataframe['ratings'].astype('str')
dataframe['imdbRating'] = dataframe['imdbRating'].astype('float')
dataframe['actors'] = dataframe['actors'].astype('str').apply(
    lambda x: x.lower().strip().replace("[", "").replace("]", "").replace("\'", "").replace("\"", "").strip())

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};TrustServerCertificate=No;DATABASE=Movies_DB;WSID=LAPTOP-BLDSMT2E;APP={Microsoft® Windows® Operating System};Trusted_Connection=Yes;SERVER=(localdb)\MSSQLLocalDB;Description=movies')
# create the connection cursor
cursor = conn.cursor()
cursor.execute('\n'
               '\n'
               '              CREATE TABLE [Top_rated_Movie] (\n'
               '	Id int NOT NULL CONSTRAINT [Id] PRIMARY KEY,\n '
               'title char (100) NULL ,\n'
               '	[year] [date] NULL ,\n'
               '[genres] [nvarchar] (50) NULL ,\n'
               '[ratings] [nvarchar] (50) NULL ,\n'
               '[poster] [varchar] (50) NULL ,\n'
               '[contentRating] [nvarchar] (50) NULL ,\n'
               '[duration] [nvarchar] (50) NULL ,\n'
               '[releaseDate] [nvarchar] (50) NULL ,\n'
               '[averageRating] [float ] (50) NULL ,\n'
               '[originalTitle] [varchar] (50) NULL ,\n'
               '	[storyline] [varchar] (50) NULL ,\n'
               '	[actors] [nvarchar] (500) NULL ,\n'
               '	[imdbRating] [varchar] (50) NULL ,\n'
               '[posterurl] [float] (50) NULL ,\n'
               ') ON [PRIMARY]\n'
               '\n'
               '               ')

cursor.execute('\n'
               '\n'
               '              CREATE TABLE [Movie_Actor_Relationship] (\n'
               '	[movieID] [int] NOT NULL , '
               '	[actor] [nvarchar] (500) NULL ,\n'
               '	[imdbRating] [float] (50) NULL ,\n'
               ') \n'
               '\n'
               '               ')

cursor.execute('\n'
               '\n'
               '              CREATE TABLE [Movie_Genre_Relationship] (\n'
               '	[movieID] [int] NOT NULL , '
               '	[genre] [nvarchar] (50) NULL ,\n'
               '	[imdbRating] [float] (50) NULL ,\n'
               ') \n'
               '\n'
               '               ')

conn.commit()
# define insert query
# dataframe['genres'] = dataframe['genres'] .astype('str')
conn.commit()
# Inserting data in SQL Table:-
for index, row in dataframe.iterrows():
    cursor.execute("INSERT INTO dbo.Top_rated_Movie(Id,title,year,genres,actors) values (?,?,?,?,?)",index, row.title, row.year,
                   row['genres'], row['actors'])
    for actor in row['actors'].split(","):
        cursor.execute("INSERT INTO dbo.Movie_Actor_Relationship(movieID,actor,imdbRating) values (?,?,?)", index, actor, row.imdbRating)
    for genre in row['genres'].split(","):
        cursor.execute("INSERT INTO dbo.Movie_Genre_Relationship(movieID,genre,imdbRating) values (?,?,?)", index, genre, row.imdbRating)

conn.commit()
cursor.close()
conn.close()
