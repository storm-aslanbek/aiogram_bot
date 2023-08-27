# программа для получения id пользователя и группы

from aiogram import Bot, Dispatcher, executor, types

from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot)

# обработчик для получения id пользователя
@dp.message_handler(text="my_id")
async def get_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')

# теперь нужно написать обработчик для получения id группы
# для дальнейшей рассылки

if __name__ == '__main__':
    executor.start_polling(dp)