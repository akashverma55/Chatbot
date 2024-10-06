import mysql.connector
global connects

connects=mysql.connector.connect(
    host="localhost",
    user="root",
    password="akankara",
    database="pandeyji_eatery"
)

def insert_order_item(food_item, quantity, order_id):
    try:
        cursor=connects.cursor()

        cursor.callproc('insert_order_item',(food_item, quantity, order_id))

        connects.commit()

        cursor.close()

        print("Order item inserted successfully!")

        return 1
    
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        connects.rollback()
        return -1


    except Exception as e:
        print(f"An error occurred: {e}")

        connects.rollback()

        return -1
    
def get_total(order_id):
    
    cursor= connects.cursor()

    query=(f"select pandeyji_eatery.get_total_order_price({order_id})")

    cursor.execute(query)

    total=cursor.fetchone()[0]

    cursor.close()

    if total is None:
        return None
    else:
        return total
    
# def insert_status(order_id):


def get_new_order_id():
    cursor=connects.cursor()

    query=("select max(order_id) from orders")
    cursor.execute(query)

    new_order_id=cursor.fetchone()[0]

    cursor.close()

    if new_order_id is not None:
        return new_order_id + 1
    else:
        return 1
    
def insert_status(order_id, status):
    cursor=connects.cursor()

    insert_query="insert into order_tracking (order_id, status) values (%s,%s)"
    cursor.execute(insert_query,(order_id,status))

    connects.commit()
    cursor.close()

def get_order_status(order_ID: int):
    # creates a connection to the database
    value=(order_ID,)
    #create a cursor object
    cursor=connects.cursor()

    # write the sql query
    query=("SELECT status FROM order_tracking where order_id = %s")

    # execute the query
    cursor.execute(query,value)

    # fetch the result
    result=cursor.fetchone()

    # close the cursor  and connection
    cursor.close()
    

    if result is not None:
        return result[0]
    else:
        return None