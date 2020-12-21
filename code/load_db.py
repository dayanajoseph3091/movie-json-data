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
    # Queries
    create_top_rated_movie = """CREATE TABLE [Top_rated_Movie] (
                   Id int NOT NULL CONSTRAINT [Id] PRIMARY KEY,
                   title char (100) NULL ,
                   [year] [date] NULL ,
                   [genres] [nvarchar] (50) NULL ,
                   [duration] [int] NULL ,
                   [releaseDate] [nvarchar] (50) NULL ,
                   [actors] [nvarchar] (500) NULL ,
                   [imdbRating] [varchar] (50) NULL ,
                   ) ON [PRIMARY] """
    create_movie_actor_relationship = """CREATE TABLE [Movie_Actor_Relationship] (
                   	[movieID] [int] NOT NULL , 
                   	[actor] [nvarchar] (500) NULL ,
                   	[imdbRating] [float] (50) NULL ,) 
                   """
    create_movie_genre_relationship = """
                    CREATE TABLE [Movie_Genre_Relationship] (
                   	[movieID] [int] NOT NULL , 
                   	[genre] [nvarchar] (50) NULL ,
                   	[imdbRating] [float] (50) NULL ,
                   )"""
    # write to MS SQL db
    create_query = '{0};{1};{2}'.format(create_top_rated_movie, create_movie_actor_relationship,
                                        create_movie_genre_relationship)
    conn = db_.ms_sql_connection()
    cursor = conn.cursor()
    # Create Tables
    cursor.execute(create_query)
    conn.commit()

    # Inserting data in SQL Table:-
    insert_top_rated_movie = """INSERT INTO dbo.Top_rated_Movie(Id,title,year,genres,actors,duration,
                releaseDate,imdbRating) values (?,?,?,?,?,?,?,?)"""
    insert_movie_actor_relationship = """INSERT INTO dbo.Movie_Actor_Relationship
    (movieID,actor,imdbRating) values (?,?,?) """
    insert_movie_genre_relationship = """INSERT INTO dbo.Movie_Genre_Relationship
    (movieID,genre,imdbRating) values (?,?,?)"""
    for index, row in dataframe.iterrows():

        cursor.execute(insert_top_rated_movie,
                       index, row.title, row.year, row['genres'], row['actors'], row.duration,
                       row.releaseDate, row.imdbRating)
        for actor in row['actors'].split(","):
            cursor.execute(insert_movie_actor_relationship,
                           index, actor, row.imdbRating)
        for genre in row['genres'].split(","):
            cursor.execute(insert_movie_genre_relationship,
                           index, genre, row.imdbRating)

    conn.commit()
    cursor.close()
    conn.close()
