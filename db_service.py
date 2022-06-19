import sqlite3
import logging

logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    filename='logs.log', 
    level=logging.INFO) 

def connection_to_db():
    connec=sqlite3.connect('users1.db')
    return connec

def main():
    try:
        connec = connection_to_db()
        connec.execute('''CREATE TABLE IF NOT EXISTS users1(
            chat_id INT,
            name CHAR,
            collection CHAR,
            update_price INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        logging.info('Connected to table successfully!') 
    except:
        print('Failed to connect to table!')


def add_user_to_db(chat_id, name, collection):
    """Adding user to DB."""
    try:
        connec = connection_to_db()
        connec.execute("INSERT INTO users1(chat_id, name, collection) VALUES(?, ?, ?)", (chat_id, name, collection));
        connec.commit()
        logging.info('Record was added successfully: {}, {}, {}'.format(chat_id, name, collection)) 
    except sqlite3.IntegrityError as err:
        logging.error('User {}, {} was not added {}'.format(chat_id, name, err)) 


def get_collection(chat_id):
    """Get collection for specific user."""
    connec = connection_to_db()
    output = connec.execute("SELECT * FROM users1 WHERE chat_id = {}".format(chat_id))
    data_rows=output.fetchall()
    for row in data_rows:
        return row[2]


def check_user(chat_id):
    """Check if user exists in DB."""
    connec = connection_to_db()
    output = connec.execute("SELECT * FROM users1 WHERE chat_id = {}".format(chat_id))
    if output.fetchall():
        return True


def get_all_collections(chat_id):
    """Get all collection for particular user."""
    connec = connection_to_db()
    output = connec.execute("SELECT collection FROM users1 WHERE chat_id = {}".format(chat_id))
    collection_list = []
    for collection in output:
        collection_list.append(collection)
    return collection_list


def check_unique(chat_id, new):
    """Check if new collection was not added previously."""
    connec = connection_to_db()
    output = connec.execute("SELECT * FROM users1 WHERE collection = {}".format(chat_id, new))
    if output.fetchall():
        return True
