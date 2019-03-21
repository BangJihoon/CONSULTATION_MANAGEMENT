import MySQLdb

def save_msg(nickname,chat_date,chat_time,manager,chat_msg,attach_url):
    # Open database connection
    db = MySQLdb.connect(host="localhost", user="root", passwd="bang", db="kakao")
    db.set_character_set('utf8')

    # Prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database
    sql = "INSERT INTO dialog VALUES (0 ,%s ,%s ,%s ,%s ,%s ,%s)" % \
          ("'"+nickname+"'","'"+chat_date+"'","'"+chat_time+"'","'"+manager+"'", "'"+chat_msg+"'", "'"+attach_url+"'")

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit changes in the database
        db.commit()

        # cursor.execute("""SELECT title, article, date, writer, vcnt FROM document""")
        # print(cursor.fetchall())
    except Exception as e:
        # print(str(e))
        # Rollback in case there is any error
        db.rollback()

    # Disconnect from database
    db.close()