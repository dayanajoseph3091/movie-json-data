import pyodbc
import teardown as db
import extract_transform as dp


def main():
    #For rerun purposes (incase of new daily feed)
    db.dbcleanup()

    #Extract Json and transform
    dataframe = dp.json_to_df()

    # DB_Connection
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};TrustServerCertificate=No;DATABASE=Movies_DB;WSID=LAPTOP-BLDSMT2E;APP={Microsoft® Windows® Operating System};Trusted_Connection=Yes;SERVER=(localdb)\MSSQLLocalDB;Description=movies')
    # create the connection cursor
    cursor = conn.cursor()
    # Create Tables
    cursor.execute('\n'
                   '\n'
                   ' CREATE TABLE [Top_rated_Movie] (\n'
                   '	Id int NOT NULL CONSTRAINT [Id] PRIMARY KEY,\n '
                   'title char (100) NULL ,\n'
                   '	[year] [date] NULL ,\n'
                   '[genres] [nvarchar] (50) NULL ,\n'
                   '[duration] [int] NULL ,\n'
                   '[releaseDate] [nvarchar] (50) NULL ,\n'
                   '[actors] [nvarchar] (500) NULL ,\n'
                   '[imdbRating] [varchar] (50) NULL ,\n'
                   ') ON [PRIMARY]\n'
                   '\n'
                   '               ')

    cursor.execute('\n'
                   '\n'
                   ' CREATE TABLE [Movie_Actor_Relationship] (\n'
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
    # Inserting data in SQL Table:-

    for index, row in dataframe.iterrows():
        cursor.execute(
            "INSERT INTO dbo.Top_rated_Movie(Id,title,year,genres,actors,duration,releaseDate,imdbRating) values (?,?,?,?,?,?,?,?)",
            index, row.title, row.year, row['genres'], row['actors'], row.duration, row.releaseDate, row.imdbRating)
        for actor in row['actors'].split(","):
            cursor.execute("INSERT INTO dbo.Movie_Actor_Relationship(movieID,actor,imdbRating) values (?,?,?)", index,
                           actor, row.imdbRating)
        for genre in row['genres'].split(","):
            cursor.execute("INSERT INTO dbo.Movie_Genre_Relationship(movieID,genre,imdbRating) values (?,?,?)", index,
                           genre, row.imdbRating)

    conn.commit()
    cursor.close()
    conn.close()
