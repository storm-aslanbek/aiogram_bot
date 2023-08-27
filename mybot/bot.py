from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import keyboards

import database as db

from dotenv import load_dotenv # для получения информация из файла .env
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)

async def start_db(_):
    await db.db_start()
    print("База данных успешно запущен!")

class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    size = State()
    rest = State()
    photo = State()


# обработчик команды старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    if message.from_user.id == int(os.getenv("admin_id")): # если id совподает id администратора
        await message.answer(f'Добро пожаловать администратор!', reply_markup=keyboards.admin_main)
    else: # если нет, то у пользователя будет меню покупателя
        await message.answer(f'Добро пожаловать {message.from_user.first_name}', reply_markup=keyboards.start_main)

# обработчик меню админа
@dp.message_handler(text="Админ панель")
async def admin(message: types.Message):
    if message.from_user.id == int(os.getenv("admin_id")):
        await message.answer(f'Выберите действие', reply_markup=keyboards.admin_panel)


@dp.message_handler(text="Добавить товар")
async def add_product(messege: types.Message):
    if messege.from_user.id == int(os.getenv("admin_id")):
        await NewOrder.type.set()
        await messege.answer('Выберите тип товара', reply_markup=keyboards.catalog_main)

@dp.callback_query_handler(state=NewOrder.type)
async def add_product_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Напишите название товара', reply_markup=keyboards.cancel)
    await NewOrder.next()

@dp.message_handler(state=NewOrder.name)
async def add_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите описание товара')
    await NewOrder.next()

@dp.message_handler(state=NewOrder.desc)
async def add_product_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Напишите цену товара')
    await NewOrder.next()

@dp.message_handler(state=NewOrder.price)
async def add_product_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Напишите размер товара в формате: размер(количество)')
    await NewOrder.next()

@dp.message_handler(state=NewOrder.size)
async def add_product_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await message.answer('Напишите общий остаток товара')
    await NewOrder.next()

@dp.message_handler(state=NewOrder.rest)
async def add_product_rest(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['rest'] = message.text
    await message.answer('Отправьте фото товара')
    await NewOrder.next()

@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_product_photo_is_none(message: types.Message, state: FSMContext):
    await message.answer('Это не фотография')

@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_product_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_product(state)
    await message.answer('Товар успешно создан!', reply_markup=keyboards.admin_panel)
    await state.finish()

@dp.message_handler(commands='a')
async def send_info(message: types.Message):
    await db.get_menu(message)


# обработчик для изменения товара администратором
@dp.message_handler(text="Изменить товар")
async def edit(messege: types.Message):
    if messege.from_user.id == int(os.getenv("admin_id")):
        await messege.answer('Выберите что вы хотите изменить', reply_markup=keyboards.edit)

# обработчик для изменения конкретного пункта
@dp.callback_query_handler()
async def inlines_edits(callback_query: types.CallbackQuery):
    if callback_query.data == 'discription':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Напишите новое описание')
    if callback_query.data == 'text':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Напишите новый текст к товару')
    if callback_query.data == 'photo':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Отправьте новое фото к товару')
    if callback_query.data == 'price':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Новая цена (в тенге)')
    if callback_query.data == 'size':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Напишите какие разверы и в каком количестве иммет'
                                                                         'данный товар (Размер: количество, ...)')
    if callback_query.data == 'rest':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Напишите общий остаток')

@dp.message_handler(text='Удалить товар')
async def delete(message: types.Message):
    # Здесь будет список всех товаров
    await message.reply('Напишите id товара который вы хотите удалить')
    # Здесь будет подтверждение на удаление товара с фото


@dp.message_handler(text='Каталог')
async def catalog(messege: types.Message):
    await messege.reply('Выберите тип товара из списка',reply_markup=keyboards.catalog_main)

@dp.callback_query_handler()
async def catalog_handler(callback_query: types.CallbackQuery):
    if callback_query.data == 't-shirts':
        print(db.get_product())

# обработка неизвестных боту сообщении и команд
@dp.message_handler()
async def unfamiliar_message(message: types.Message):
    await message.reply("Я вас не понимаю")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start_db, skip_updates=True)