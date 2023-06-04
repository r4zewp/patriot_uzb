from db.db import *
from data.config import DATABASE, NAMESPACE
from aiocache import Cache
from aiocache.serializers import PickleSerializer

db = DatabaseManager(DATABASE)
cache = Cache(Cache.MEMORY, serializer=PickleSerializer(), namespace=NAMESPACE)


async def item_to_cart(item_id: int, user_id: int, amount: int):
    db.cur.execute('INSERT INTO `cart` (iid, quantity, uid) VALUES (?, ?, ?)', (item_id, amount, user_id))
    db.conn.commit()
    await cache.clear()


async def get_items_from_cart_by_user(user_id: int):
    cache_key = f"order_uid_{user_id}"
    items = await cache.get(cache_key)

    if items is not None and len(items) != 0:
        print("from cache")
        return items
    else:
        print('querying db')
        res = db.cur.execute(f"SELECT * FROM `cart` JOIN `items` ON items.id = cart.iid WHERE uid = '{user_id}'")
        items = res.fetchall()
        await cache.set(cache_key, items, ttl=60)

    return items


async def delete_item_from_cart(user_id: int, item_id: int):
    db.cur.execute("DELETE FROM `cart` WHERE uid = ? AND cart_id = ?", (user_id, item_id))
    db.conn.commit()
    await cache.clear()


async def delete_order_after_success(user_id: int, items: list):
    db.cur.execute("DELETE FROM `cart` WHERE uid = ? and (cart_id BETWEEN ? and ?)", (user_id, items[0][0], items[-1][0]))
    db.conn.commit()

    await cache.clear()
