import pymysql
import csv
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
                            user="root",
                            database=db_name,
                            password="239mikuNFU@~@",
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

def db_upload_file(filename: str, db_name: str, ngrok_file: str | None = None):
    """Upload reviews in given file
    Args:
        filename: path under ./SaveData/
        db_name: database to connect, default connect to reviews database
        ngrok_file: default = './ReviewAPP/ngrok.txt'
    No returns
    """

    if db_name is None:
        db_name = 'reviews'

    table_name = '`' + filename + '`'
    # print('---------------------------------------------------->', filename, '--------------------------------')
    # print('---------------------------------------------------->', table_name, '--------------------------------')

    try:
        forward_ip, forward_port = get_connection_args(ngrok_file)
        db = pymysql.connect(host=forward_ip,
                            port=forward_port,
                            user="root",
                            database=db_name,
                            password="239mikuNFU@~@",
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

        filename = './SaveData/' + filename + '.csv'

        with open(filename, 'r', encoding='utf-8') as file:
            lines = csv.reader(file)
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
        db.close()
        print('File uploaded successfully')