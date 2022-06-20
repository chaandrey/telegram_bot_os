import sqlite3
import logging

logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    filename='logs.log', 
    level=logging.INFO) 

def connection_to_db():
    connec=sqlite3.connect('users.db')
    return connec

def main():
    try:
        connec = connection_to_db()
        connec.execute('''CREATE TABLE IF NOT EXISTS users3(
            chat_id INT,
            name CHAR,
            collection CHAR,
            current_price INTEGER,
            percentage INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        logging.info('Connected to table successfully!') 
    except:
        print('Failed to connect to table!')


def add_user_to_db(chat_id, name, collection, current_price, percentage):
    """Adding user to DB."""
    try:
        connec = connection_to_db()
        connec.execute("INSERT INTO users3(chat_id, name, collection, current_price, percentage) VALUES(?, ?, ?, ?, ?)", (chat_id, name, collection, current_price, percentage));
        connec.commit()
        logging.info('Record was added successfully: {}, {}, {}, {}, {}'.format(chat_id, name, collection, current_price, percentage)) 
    except sqlite3.IntegrityError as err:
        logging.error('User {}, {} was not added {}'.format(chat_id, name, err)) 


def get_collection(chat_id):
    """Get collection for specific user."""
    connec = connection_to_db()
    output = connec.execute("SELECT collection FROM users3 WHERE chat_id = {}".format(chat_id))
    data_rows = output.fetchall()
    final_data = [i[0] for i in data_rows]
    return final_data


def check_user(chat_id):
    """Check if user exists in DB."""
    connec = connection_to_db()
    output = connec.execute("SELECT * FROM users3 WHERE chat_id = {}".format(chat_id))
    if output.fetchall():
        return True


def get_all_collections(chat_id):
    """Get all collection for particular user."""
    connec = connection_to_db()
    output = connec.execute("SELECT collection FROM users3 WHERE chat_id = {}".format(chat_id))
    return output.fetchall()


def check_unique(chat_id, new):
    """Check if new collection was not added previously."""
    connec = connection_to_db()
    output = connec.execute("SELECT * FROM users3 WHERE collection = {}".format(chat_id, new))
    if output.fetchall():
        return True


def get_users_for_update(): # need to add group by in order to update all users with same collection
    """Fetch all users that require update."""
    connec = connection_to_db()
    output = connec.execute("SELECT * FROM users3 WHERE percentage != 0 ORDER BY timestamp ASC")
    output = output.fetchone()
    return output


def update_record(chat_id, collection, updated_price):
    """Updating record with new price."""
    connec = connection_to_db()   # need to update timestamp as well.
    connec.execute("UPDATE users3 SET current_price = {} WHERE chat_id = {} AND collection = {}".format(updated_price, chat_id, collection))
    connec.commit()