import pymysql

try:
    with open('./ngrok.txt', 'r') as file:
        hostname = file.readline()
        forward_ip, forward_port = hostname.split('://')[1].split(':')
        forward_port = int(forward_port)
    db = pymysql.connect(host=forward_ip,
                        port=forward_port,
                        user="root",
                        database="test_con",
                        password="239mikuNFU@~@")
except pymysql.err.OperationalError as err:
    print("Error connecting to MySQL database, check your ngrok host and port.")
else:
    cursor = db.cursor()

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_table (
                rating INTEGER,
                txt NVARCHAR(1024))''')

    # Update table
    command = "INSERT INTO test_table (rating, text) VALUES (%s, %s)"
    rating = -1
    text = 'The food was terrible.'
    review = (rating, text)

    cursor.execute(command, review)
    db.commit()

    # Read the review
    cursor.execute("SELECT * FROM test_table")
    result = cursor.fetchall()

    for x in result:
        print(x)

    db.close()