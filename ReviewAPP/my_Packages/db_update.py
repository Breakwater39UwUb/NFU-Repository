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

    db = init_db(ngrok_file, db_name)

    if db is None:
        log = utils.Debug_Logger('init_db')
        log.log('Failed to connect to MySQL database.', 30)
        return
        
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
            log.log(e)
            pass
    finally:
        db.close()

def db_upload_file(filename: str,
                   db_name: str = 'reviews',
                   table_name: str = None,
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
    
    db = init_db(ngrok_file, db_name)
    log = utils.Debug_Logger('init_db')

    if db is None:
        log.log('Failed to connect to MySQL database.', 30)
        return

    cursor = db.cursor()
    cursor.execute("SET NAMES utf8mb4")
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    if table_name is None:
        table_name = utils.convert_to_tablename(filename)
    command = f"CREATE TABLE IF NOT EXISTS {table_name}\
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
            command = f"INSERT INTO {table_name}\
                (time_range, rating, content) VALUES \
                (%s, %s, %s)"
            
            if file_format == 'csv':
                time, rating, text  = line[0], line[1], line[2]
            if file_format == 'json':
                time, rating, text  = line['time'], line['rating'], line['comment']

            if text == '':
                continue

            if len(text) > 510:
                text = text[:510]

            review = (time, rating, text)

            
            try:
                cursor.execute(command, review)
                db.commit()
            except pymysql.IntegrityError as e:
                if e.args[0] == DUP_ENTRY:
                    log.log(e)
                    pass
        db.close()
        log.log(f'{filename} uploaded successfully.')

def insert_review(rating: int, content: str):
    '''Insert filtered review to database
    
    rating: star rating
    content: review text
    '''

    log = utils.Debug_Logger('insert_review')
    db = init_db()
    if db is None:
        return
    cursor = db.cursor()
    command = f"INSERT INTO filtered\
        (rating, content) VALUES \
        (%s, %s)"
    review = (rating, content)
    try:
        cursor.execute(command, review)
        db.commit()
    except pymysql.IntegrityError as e:
        if e.args[0] == DUP_ENTRY:
            log.log(e)
    finally:
        db.close()
    log.log('Review insert to databse', 20)

def fetch_by_range(time_range: str, table: str):
    '''Download reviews from given table within given time range
    
    time_range: string, ex: '2024/02 2024/05'
    '''

    db = init_db()
    if db is None:
        return
    cursor = db.cursor()
    command = f"SELECT * FROM `{table}`\
            WHERE time_range >= %s AND \
            time_range <= %s \
            ORDER BY time_range DESC"
    cursor.execute(command, time_range)
    reviews = cursor.fetchall()
    db.close()

    path = table + '.json'
    
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(reviews, file, ensure_ascii=False, indent=4)

def fetch_all(table: str):
    '''Download all reviews from given table'''

    db = init_db()
    if db is None:
        return
    cursor = db.cursor()
    command = f"SELECT * FROM `{table}`"
    cursor.execute(command)
    reviews = cursor.fetchall()
    db.close()

    path = table + '.json'
    
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(reviews, file, ensure_ascii=False, indent=4)
    print(f'Table saved to: {path}')

def get_top_review(table_name: str):
    if table_name is None:
        raise ValueError('Must given table name exist in database.')
    
    db = init_db()
    if db is None:
        return
    cursor = db.cursor()
    cursor.execute(f"SELECT content FROM `{table_name}` ORDER BY time_range DESC LIMIT 1;")
    newest = cursor.fetchone()
    db.close()
    return newest

def get_years(table_name: str, json_like: bool=False):
    '''Get the number of years
    which there are reviews.

    table_name: table to get years.
    json_like: default = False
        Whether return json format.
    '''

    if table_name is None:
        raise ValueError('Must given table name exist in database.')

    logger = utils.Debug_Logger('get_years')
    db = init_db()
    if db is None:
        logger.log('Failed to connect Database.')
        return
    
    if check_exist_table(table_name, db) == False:
        return

    cursor = db.cursor()
    years = None
    table_name = utils.convert_to_tablename(table_name, True)
    try:
        cursor.execute(f'''SELECT SUBSTRING_INDEX(time_range, '/', 1) AS year
                            FROM reviews.{table_name}
                            GROUP BY year
                            ORDER BY year DESC;''')
        years = cursor.fetchall()
    except:
        logger.log(f'Failed to get years from table, {table_name}.')
        raise
    finally:
        db.close()
        if json_like:
            years = [{'year': year[0]} for year in years]
            return json.dumps(years, ensure_ascii=False, indent=4)
        return years

def check_exist_table(table_name: str, db=None):
    '''Check if the table is exist in database
    
    table_name: web title from web scraper
    '''

    # TODO: Add detection of Foodpanda
    table_name = utils.convert_to_tablename(table_name, False)

    if db is None:
        # No db object passed, init one
        db = init_db()

        if db is None:
            return
        cursor = db.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        db.close()
    else:
        # Use given db object
        cursor = db.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()

    if result is None:
        return False
    return True

def init_db(ngrok_file: str = './ngrok.txt',
            db_name: str = 'reviews'):
    log = utils.Debug_Logger('init_db')

    try:
        forward_ip, forward_port = get_connection_args(ngrok_file)
    except:
        forward_ip, forward_port = 'localhost', 3306
    
    try:
        return pymysql.connect(host=forward_ip,
                            port=forward_port,
                            user="web",    # root
                            database=db_name,
                            password="password",   # 239mikuNFU@~@
                            charset='utf8mb4')
    except pymysql.err.OperationalError as err:
        log.log(f'Error connecting to MySQL database, check your ngrok host and port.\nhost: {forward_ip}\nport: {forward_port}', 30)

    try:
        log.log(f'Trying localhost:3306')
        return pymysql.connect(host='localhost',
                            port=3306,
                            user="web",    # root
                            database=db_name,
                            password="password",   # 239mikuNFU@~@
                            charset='utf8mb4')
    except:
        return None
