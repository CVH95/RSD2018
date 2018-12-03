import pymysql.cursors
import pymysql

# Get ticket from database
def get_ticket(_id, _host):
    # Connect to database
    # On localhost use utf8 charset
    conn = pymysql.connect(host=_host,
                           user='mirex',
                           password='robot2018',
                           db='RSD MES master',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with conn.cursor() as cursor:
            # Select ticket 
            select_stmt = "select id, ticket from rsd2018.jobs where id = %s"
            cursor.execute(select_stmt, _id)
            result = cursor.fetchone()
    finally:
            # Close connection
        conn.close()
    
    return result


_host = '192.168.100.200'
_id = 656

ticket = get_ticket(_id, _host)
print ticket