from db.db import *
from data.config import *
from aiocache import Cache
from aiocache.serializers import PickleSerializer
from aiocache.decorators import cached

db = DatabaseManager(DATABASE)
cache = Cache(Cache.MEMORY, serializer=PickleSerializer(), namespace="fargobot")

## TODO: Update with admin things
async def create_new_item(data: dict):
    db.cur.execute(f"INSERT INTO `items` (cid, ikpu, name, sex, color, art, size, price, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (data['category'], data['ikpu'], data['name'], data['sex'], data['color'], data['art'], data['size'], data['price'], data['first_photo']))
    db.conn.commit()

    await cache.clear()

async def get_item_by_id(id: int):
    res = db.cur.execute(f"SELECT * FROM `items` WHERE id = '{id}'")
    item = res.fetchone()
    
    return item

async def get_all_items_by_category_sex(sex: str, category_id: int):
    cache_key = f"items_{category_id}_{sex}"
    
    items = await cache.get(cache_key)
    if items is not None:
        print("from cache")
        return items
    else:
        print("querying db")
        res = db.cur.execute(f"SELECT * FROM `items` WHERE cid = ? and sex = ?", (category_id, sex))
        items = res.fetchall()
        await cache.set(cache_key, items, ttl=60)

    return items

async def get_all_items_by_category_id(category_id: int):
    cache_key = f"items_{category_id}"
    
    items = await cache.get(cache_key)
    if items is not None:
        print("from cache")
        return items

    else:
        print("querying db")
        res = db.cur.execute(f"SELECT * FROM `items` WHERE cid = ?", (category_id,))
        items = res.fetchall()
        await cache.set(cache_key, items, ttl=60)

    return items



