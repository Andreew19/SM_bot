import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import CommandStart

from data import hdd,cpu_load,memory_usage

load_dotenv()

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot)

data = [f"CPU: {cpu_load}%",f"Memory: {memory_usage}%","Total: %.2f Gb" % (hdd.total / (2**30)),"Used: %.2f Gb" % (hdd.used / (2**30)),"Free: %.2f Gb" % (hdd.free / (2**30))]
parss_data = "\n".join(data) 


@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
  await message.answer(f"*Server load:*\n\n {parss_data}", parse_mode='markdown')


if __name__ == '__main__':
    executor.start_polling(dp,  skip_updates=True)