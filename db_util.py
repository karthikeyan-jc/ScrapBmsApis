import configparser
import mysql.connector

def get_connection():
    config= configparser.ConfigParser()
    config.read('config.ini')
    config_info=config['mysqlDB']

    connection = mysql.connector.connect(host=config_info['host'],
                                         database=config_info['database'],
                                         user=config_info['user'],
                                         password=config_info['password'])
    return connection
