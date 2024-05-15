import pymysql
from pymysql.constants.ER import DUP_ENTRY
import csv
import json
from my_Packages.parse_ngrok import get_connection_args
from my_Packages import utils

def db_update(time: str,
              rating: int,
              text: str,
              db_name: str = 'reviews',
              table_name: str = '',
              ngrok_file: str = None):
    """Update database with new review
    Args:
        time: review time, ex: 2014/01
        rating: star in range 1 to 5
        text: review content
        db_name: database to connect, default connect to reviews database
        table_name: table to insert
        ngrok_file: default = './ReviewAPP/ngrok.txt'
    No returns
    """

    try:
        forward_ip, forward_port = get_connection_args(ngrok_file)
        db = pymysql.connect(host=forward_ip,
                            port=forward_port,
                            user="web",    # root
                            database=db_name,
                            password="password",   # 239mikuNFU@~@
                            charset='utf8mb4')
    except pymysql.err.OperationalError as err:
        print(f'Error connecting to MySQL database, check your ngrok host and port.\nhost: {forward_ip}\nport: {forward_port}')
    try:
        cursor = db.cursor()

        # Update table
        command = f"INSERT INTO {table_name}\
                        (time_range, rating, content) VALUES \
                        (%s, %s, %s)"
        review = (time, rating, text)
        cursor.execute(command, review)
        db.commit()
    except pymysql.IntegrityError as e:
        if e.args[0] == DUP_ENTRY:
            print(e)
            pass
    finally:
        db.close()

def db_upload_file(filename: str,
                   db_name: str = 'reviews',
                   ngrok_file: str = './ngrok.txt',
                   file_format: str = 'json'):
    """Upload reviews in given file
    Args:
        filename: File under ./SaveData/
        db_name: Database to connect, default connect to reviews database
        ngrok_file: Default = './ReviewAPP/ngrok.txt'
        file_format: Default = 'json'
    No returns
    """

    if file_format not in ['csv', 'json']:
        raise Exception('file_format must be csv or json')

    try:
        forward_ip, forward_port = get_connection_args(ngrok_file)
        db = pymysql.connect(host=forward_ip,
                            port=forward_port,
                            user="web",    # root
                            database=db_name,
                            password="password",   # 239mikuNFU@~@
                            charset='utf8mb4')
    except pymysql.err.OperationalError as err:
        print(f'Error connecting to MySQL database, check your ngrok host and port.\nhost: {forward_ip}\nport: {forward_port}')

    cursor = db.cursor()
    cursor.execute("SET NAMES utf8mb4")
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    tablename = utils.convert_to_tablename(filename)
    command = f"CREATE TABLE IF NOT EXISTS {tablename}\
        (time_range CHAR(8),\
        rating INTEGER,\
        content VARCHAR(530) PRIMARY KEY\
        COLLATE utf8mb4_unicode_ci)"
    # print('------------------>', command)
    cursor.execute(command)

    with open(filename, 'r', encoding='utf-8') as file:
        if file_format == 'csv':
            lines = csv.reader(file)
        if file_format == 'json':
            lines = json.load(file)

        for line in lines:
            # Update table
            command = f"INSERT INTO {tablename}\
                (time_range, rating, content) VALUES \
                (%s, %s, %s)"
            
            if file_format == 'csv':
                time, rating, text  = line[0], line[1], line[2]
            if file_format == 'json':
                time, rating, text  = line['time'], line['rating'], line['comment']

            if text == '':
                continue
            # rating = int(rating)
            review = (time, rating, text)
            # print(review)
            
            try:
                cursor.execute(command, review)
                db.commit()
            except pymysql.IntegrityError as e:
                if e.args[0] == DUP_ENTRY:
                    print(e)
                    pass
        db.close()
        print(f'{filename} uploaded successfully.')