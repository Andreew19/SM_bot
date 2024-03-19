import os
from dotenv import load_dotenv
import psutil  
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove

load_dotenv()

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot)

start_keyboard = ReplyKeyboardMarkup(
  keyboard=[
    
    [
      KeyboardButton('Get metrics 📊')
    ]

  ],
  
  resize_keyboard=True
)

@dp.message_handler(CommandStart())
@dp.message_handler(text='Get metrics 📊')
async def send_welcome(message: types.Message):
  
 
  def get_cpu_load(): 
    return psutil.cpu_percent(interval=1) 
 
  def get_memory_usage(): 
    mem = psutil.virtual_memory() 
    return mem.percent 
 
 
  cpu_load = get_cpu_load() 
  memory_usage = get_memory_usage() 
 
  hdd = psutil.disk_usage('/') 

  data = [f"CPU: {cpu_load}%",f"Memory: {memory_usage}%","Total: %.2f Gb" % (hdd.total / (2**30)),"Used: %.2f Gb" % (hdd.used / (2**30)),"Free: %.2f Gb" % (hdd.free / (2**30))]
  parss_data = "\n".join(data) 
 
  await message.answer(f"*Server load:*\n\n {parss_data}", parse_mode='markdown', reply_markup=start_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp,  skip_updates=True)