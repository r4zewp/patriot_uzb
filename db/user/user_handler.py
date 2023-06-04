from db.db import *
from data.config import *
from aiocache import Cache
from aiocache.serializers import PickleSerializer
from aiocache.decorators import cached

db = DatabaseManager(DATABASE)
cache = Cache(Cache.MEMORY, serializer=PickleSerializer(), namespace="fargobot")


def create_new_user(data: dict):
    db.query("INSERT INTO `users` (name, lang, phone, id, is_admin) VALUES (?, ?, ?, ?, ?)",
    (data['name'], data['language'], data['phone'], data['id'], data['is_admin'], ))

def make_user_admin(id: int):
    db.cur.execute('UPDATE `users` SET `is_admin` = ? WHERE id = ?', (1, id))
    db.conn.commit()

    return True

def does_user_exist(id: int):
    res = db.cur.execute("SELECT * FROM `users` WHERE id = ?", (id, ))
    user = res.fetchone()

    return user

async def get_user_lang(id: int):
    cache_key = f'language_{id}'

    lang = await cache.get(cache_key)

    if lang is not None:
        print('cached')
        return lang
       

    else:
        res = db.cur.execute("SELECT lang FROM `users` WHERE id = ?", (id, ))
        lang = res.fetchone()

        print('query')
        await cache.set(cache_key, lang[0], ttl=99999)
    
    return lang[0]