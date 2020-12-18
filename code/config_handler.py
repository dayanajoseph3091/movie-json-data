from configparser import ConfigParser

import pyodbc


def load_config():
    # Read configuration file
    parser = ConfigParser()
    parser.read('../dev.ini')
    return parser


def get_SQLCONFIG():
    parser = load_config()
    # Read corresponding file parameters
    _driver = parser.get("db", "driver")
    _database = parser.get("db", "database")
    _trusted_connection = parser.get("db", "trusted_connection")
    _server = parser.get("db", "server")
    return _driver, _database, _trusted_connection, _server  # return required parameters


def ms_sql_connection():
    c = get_SQLCONFIG()
    driver_ = c[0]
    db_name = c[1]
    server_ = c[3]
    conn_info = ('DRIVER=' + driver_ + ';TrustServerCertificate=No;'
                                       'DATABASE=' + db_name + ';SERVER=' + server_)
    return pyodbc.connect(conn_info)


# load json path from configuration file
def json_path():
    parser = load_config()
    return parser.get("json", "movie_list")

############create .ini file

# config = ConfigParser()
# config['db'] = {
#     "driver": "{ODBC Driver 17 for SQL Server}",
#     "database": "Movies_DB",
#     "trusted_Connection": "yes",
#     "server": "(localdb)\MSSQLLocalDB"
#
# }
# with open('../dev.ini', 'w') as f:
#     config.write(f)
