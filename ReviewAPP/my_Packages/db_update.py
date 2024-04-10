import pymysql
import csv
import json
from Packages.parse_ngrok import get_connection_args

def db_update(rating: int, text: str, db_name: str, ngrok_file: str | None = None):
    """Update database with new review
    Args:
        rating: int in range 1 to 5
        text: string
        db_name: database to connect, default connect to reviews database
        ngrok_file: default = './ReviewAPP/ngrok.txt'
    No returns
    """

    if db_name is None:
        db_name = 'reviews'

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
    else:
        cursor = db.cursor()

        # Update table
        # this if-else statement is used to debug, delete before publishing
        if db_name == 'test_con':
            command = "INSERT INTO test_table (rating, text) VALUES (%s, %s)"
        else:
            command = "INSERT INTO reviews (rating, txt) VALUES (%s, %s)"

        review = (rating, text)

        cursor.execute(command, review)
        db.commit()

        db.close()

def db_upload_file(filename: str, db_name: str, ngrok_file: str | None = None, file_format: str = None):
    """Upload reviews in given file
    Args:
        filename: File under ./SaveData/
        db_name: Database to connect, default connect to reviews database
        ngrok_file: Default = './ReviewAPP/ngrok.txt'
        file_format: Default = 'csv'
    No returns
    """

    if db_name is None:
        db_name = 'reviews'

    if file_format is None:
        file_format = 'csv'
    elif file_format not in ['csv', 'json']:
        raise Exception('file_format must be csv or json')

    table_name = '`' + filename + '`'

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
    else:
        cursor = db.cursor()
        cursor.execute("SET NAMES utf8mb4")
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        command = f'CREATE TABLE IF NOT EXISTS {table_name} (rating INTEGER, txt VARCHAR(1024) COLLATE utf8mb4_unicode_ci)'
        print('------------------>', command)
        cursor.execute(command)

        filename = './SaveData/' + filename + '.' + file_format

        if file_format == 'csv':
            with open(filename, 'r', encoding='utf-8') as csv_file:
                lines = csv.reader(csv_file)
                for line in lines:
                    # Update table
                    # this if-else statement is used to debug, delete before publishing
                    if db_name == 'test_con':
                        command = f"INSERT INTO {table_name} (rating, txt) VALUES (%s, %s)"
                    else:
                        command = "INSERT INTO reviews (rating, txt) VALUES (%s, %s)"
                    rating, text  = line[0], line[1]
                    if text == '':
                        continue
                    # rating = int(rating)
                    review = (rating, text)
                    # print(review)
                    cursor.execute(command, review)
                    db.commit()
        elif file_format == 'json':
            with open(filename, 'r', encoding='utf-8') as json_file:
                lines = json.load(json_file)
                for line in lines:
                    # Update table
                    # this if-else statement is used to debug, delete before publishing
                    if db_name == 'test_con':
                        command = f"INSERT INTO {table_name} (rating, txt) VALUES (%s, %s)"
                    else:
                        command = "INSERT INTO reviews (rating, txt) VALUES (%s, %s)"
                    rating, text  = line['rating'], line['comment']
                    if text == '':
                        continue
                    # rating = int(rating)
                    review = (rating, text)
                    # print(review)
                    cursor.execute(command, review)
                    db.commit()
                
        db.close()
        print(f'{filename} uploaded successfully.')