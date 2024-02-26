import pymysql
from Packages.parse_ngrok import get_connection_args

def db_update(rating: int, text: str, db_name: str):
    """Update database with new review
    Args:
        rating: int in range 1 to 5
        text: string
        db: database to connect, default is None
            which connect to reviews database
    No returns
    """

    if db_name is None:
        db_name = 'reviews'

    try:
        forward_ip, forward_port = get_connection_args()
        db = pymysql.connect(host=forward_ip,
                            port=forward_port,
                            user="root",
                            database=db_name,
                            password="239mikuNFU@~@")
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