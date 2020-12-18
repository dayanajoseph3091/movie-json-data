import pyodbc
import teardown as td
import extract_transform as et
import config_handler as db_


# import pyodbc
# from configparser import ConfigParser


def main():
    # For rerun purposes (incase of new daily feed)
    td.db_cleanup()

    # Extract Json and transform
    dataframe = et.json_to_df()

    # write to MS SQL db
    conn = db_.ms_sql_connection()
    cursor = conn.cursor()
    # Create Tables
    cursor.execute("""CREATE TABLE [Top_rated_Movie] (
                   Id int NOT NULL CONSTRAINT [Id] PRIMARY KEY,
                   title char (100) NULL ,
                   [year] [date] NULL ,
                   [genres] [nvarchar] (50) NULL ,
                   [duration] [int] NULL ,
                   [releaseDate] [nvarchar] (50) NULL ,
                   [actors] [nvarchar] (500) NULL ,
                   [imdbRating] [varchar] (50) NULL ,
                   ) ON [PRIMARY] """)

    cursor.execute("""CREATE TABLE [Movie_Actor_Relationship] (
                   	[movieID] [int] NOT NULL , 
                   	[actor] [nvarchar] (500) NULL ,
                   	[imdbRating] [float] (50) NULL ,) 
                   """)

    cursor.execute("""
                    CREATE TABLE [Movie_Genre_Relationship] (
                   	[movieID] [int] NOT NULL , 
                   	[genre] [nvarchar] (50) NULL ,
                   	[imdbRating] [float] (50) NULL ,
                   )""")
    conn.commit()

    # Inserting data in SQL Table:-
    for index, row in dataframe.iterrows():
        cursor.execute(
            """INSERT INTO dbo.Top_rated_Movie(Id,title,year,genres,actors,duration,
            releaseDate,imdbRating) values (?,?,?,?,?,?,?,?)""",
            index, row.title, row.year, row['genres'], row['actors'], row.duration,
            row.releaseDate, row.imdbRating)
        for actor in row['actors'].split(","):
            cursor.execute("""INSERT INTO dbo.Movie_Actor_Relationship(movieID,actor,imdbRating) values (?,?,?)""",
                           index, actor, row.imdbRating)
        for genre in row['genres'].split(","):
            cursor.execute("""INSERT INTO dbo.Movie_Genre_Relationship(movieID,genre,imdbRating) values (?,?,?)""",
                           index, genre, row.imdbRating)

    conn.commit()
    cursor.close()
    conn.close()
