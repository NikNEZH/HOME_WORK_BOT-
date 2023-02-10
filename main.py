import config
import logging
import filters

from aiogram import Bot, Dispatcher, executor, types

from filters import AdminFilter

# уровень логирования
logging.basicConfig(level=logging.INFO)

# инициализация бота
bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot)

# активация фильтр
dp.filters_factory.bind(AdminFilter)

# удаление сообщений о присоединении новых пользователей
@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joined(message: types.Message):
    await message.delete()

# фильтр бранных слов
@dp.message_handler()
async def filter(message: types.Message):
    if 'сука' in message.text:
        await message.delete()
    elif 'блять' in message.text:
        await message.delete()
# бан
@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='!/')
async def ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Эта команда должна быть ответом на сообщение!')
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply('Бан пользователя')

# вызываем long-polling
if __name__ == '__main__':
    # если работаем с важными данными лучше поставит False
    executor.start_polling(dp, skip_updates=True)


