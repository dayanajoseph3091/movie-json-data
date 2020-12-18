import config_handler as db


def db_cleanup():
    conn = db.ms_sql_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS [dbo].[Top_rated_Movie]")
    cursor.execute("DROP TABLE IF EXISTS  [dbo].[Movie_Actor_Relationship]")
    cursor.execute("DROP TABLE IF EXISTS  [dbo].[Movie_Genre_Relationship]")
    cursor.commit()
    conn.close()
