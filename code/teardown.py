import config_handler as db


def db_cleanup():
    conn = db.ms_sql_connection()
    cursor = conn.cursor()
    drop_tables = "DROP TABLE IF EXISTS [dbo].[Top_rated_Movie];" \
                  + "DROP TABLE IF EXISTS  [dbo].[Movie_Actor_Relationship];" \
                  + "DROP TABLE IF EXISTS  [dbo].[Movie_Genre_Relationship]"
    cursor.execute(drop_tables)
    cursor.commit()
    conn.close()
