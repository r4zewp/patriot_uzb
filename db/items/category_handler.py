from db.db import *
from data.config import *
from aiocache import Cache
from aiocache.serializers import PickleSerializer
from aiocache.decorators import cached

db = DatabaseManager(DATABASE)
cache = Cache(Cache.MEMORY, serializer=PickleSerializer(), namespace="fargobot")

async def create_new_category(data: dict):
    db.cur.execute("INSERT INTO `categories` (ru_label, uz_label, name, is_sex_needed) VALUES (?, ?, ?, ?)", (data['name_ru'], data['name_uz'], data['name'], data['is_sex_needed']))
    db.conn.commit()

    await cache.clear()

async def get_all_names_of_cats(language: str):
    cache_key = 'names_cats'

    items = await cache.get(cache_key)

    if items is not None:
        return items
    else:
        if language == 'ru':
            res = db.cur.execute(f"SELECT ru_label FROM `categories`")
            items = res.fetchall()
        else:
            res = db.cur.execute(f"SELECT uz_label FROM `categories`")
            items = res.fetchall()

        final_items = []

        for item in items:
            final_items.append(item[0])

        await cache.set(cache_key, final_items, ttl=60)

    return final_items

async def get_all_categories():
    cache_key = "categories"

    items = await cache.get(cache_key)

    if items is not None:
        return items
    else:
        res = db.cur.execute("SELECT * FROM `categories`")
        items = res.fetchall()

        await cache.set(cache_key, items, ttl=60)
        
    
    return items

async def get_category_by_id(id: int):
    res = db.cur.execute(f"SELECT * FROM `categories` WHERE id = ?", (id,))
    category = res.fetchone()

    return category 

async def get_category_by_name(name: str):
    res = db.cur.execute(f"SELECT * FROM `categories` WHERE name = ?", (name, ))
    category = res.fetchone()

    return category


    
