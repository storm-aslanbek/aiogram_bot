import sqlite3 as sq
from aiogram import Bot, Dispatcher
import os

bot = Bot("6658049624:AAEjMU1CSkAi6P8rJDSvhV759rMLAEoLHUU")
dp = Dispatcher(bot=bot)

async def db_start():
    global db, cur
    db = sq.connect('tg.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id INTEGER, "
                "cart_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT,"
                "desc TEXT, "
                "price TEXT, "
                "size TEXT, "
                "rest TEXT, "
                "photo TEXT, "
                "brand TEXT)")
    db.commit()


async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()

async def add_product(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO items (name, desc, price, size, rest, photo, brand) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (data['name'], data['desc'], data['price'], data['size'], data['rest'], data['photo'], data['type']))
        db.commit()

async def get_menu(message):
    for i in cur.execute('SELECT * FROM items').fetchall():
        await bot.send_photo(message.from_user.id, i[0], f'{i[1]}\ndesc {i[-1]}')