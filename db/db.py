import sqlite3 as lite
from data.config import NAMESPACE
from aiocache import Cache
from aiocache.serializers import PickleSerializer

cache = Cache(Cache.MEMORY, serializer=PickleSerializer(), namespace=NAMESPACE)

class DatabaseManager(object):

    def __init__(self, path):
        self.conn = lite.connect(path)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.query('CREATE TABLE IF NOT EXISTS users (name text, lang text, phone text, is_admin bool, id INTEGER PRIMARY KEY)')
        self.query('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, cid INTEGER, ikpu text, name text, sex text, color text, art text, size text, price int, photo BLOB, units_code int, pack_code int, vat_percent int, FOREIGN KEY (cid) REFERENCES categories(id))')
        self.query('CREATE TABLE IF NOT EXISTS cart (cart_id INTEGER PRIMARY KEY AUTOINCREMENT, iid int, quantity int, uid int, FOREIGN KEY (iid) REFERENCES items(id), FOREIGN KEY (uid) REFERENCES users(id))')
        self.query('CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY AUTOINCREMENT, ru_label text, uz_label text, name text, is_sex_needed bool)')
        
    def query(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()

    def fetchone(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchone()

    def fetchall(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()