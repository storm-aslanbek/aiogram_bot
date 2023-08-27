from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# меню для покупателей
start_main = ReplyKeyboardMarkup(resize_keyboard=True)
start_main.add('Каталог').add('Корзина').add('Контакты').add('WhatsApp группа')

# меню администратора
admin_main = ReplyKeyboardMarkup(resize_keyboard=True)
admin_main.add('Каталог').add('Корзина').add('Контакты').add('WhatsApp группа').add('Админ панель')

catalog_main = InlineKeyboardMarkup(row_width=3)
catalog_main.add(InlineKeyboardButton(text='Футболки', callback_data='t-shirts'),
                 InlineKeyboardButton(text='Брюки', callback_data='trousers'),
                 InlineKeyboardButton(text='Двойки/Тройки', callback_data='deuceses'),
                 InlineKeyboardButton(text='Платья', callback_data='dresses'),
                 InlineKeyboardButton(text='Обувь', callback_data='shoes'),
                 InlineKeyboardButton(text='Другое', callback_data='other'))

# меню админ панеля
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Изменить товар').add('Сделать рассылку').add('Другое')

# изменение информации о существующих товаров
edit = InlineKeyboardMarkup(row_width=3)
edit.add(InlineKeyboardButton(text='Описание', callback_data='discription'),
         InlineKeyboardButton(text='Текст', callback_data='text'),
         InlineKeyboardButton(text='Фото', callback_data='photo'),
         InlineKeyboardButton(text='Цена', callback_data='price'),
         InlineKeyboardButton(text='Размеры', callback_data='size'),
         InlineKeyboardButton(text='Остаток', callback_data='rest'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')