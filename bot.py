import os
from dotenv import load_dotenv
import psutil  
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from aggregateDB import *

load_dotenv()

bot = Bot(os.environ['TOKEN'])
dp = Dispatcher(bot)

start_keyboard = ReplyKeyboardMarkup(
  keyboard=[
    
    [
      KeyboardButton('Get metrics 📊')
    ],

    [
       KeyboardButton('Get report📝')
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

  data = [f"CPU: {cpu_load}%",f"Load Average{psutil.getloadavg()}",f"Memory: {memory_usage}%","HDD total: %.2f Gb" % (hdd.total / (2**30)),"HDD used: %.2f Gb" % (hdd.used / (2**30)),"HDD free: %.2f Gb" % (hdd.free / (2**30))]
  parss_data = "\n".join(data) 
 
  await message.answer(f"*Server load:*\n\n {parss_data}", parse_mode='markdown', reply_markup=start_keyboard)


@dp.message_handler(text='Get report📝')
async def send_report(message:types.Message):
   
  all_reports = []

  for doc in result:
     date = doc.get("_id")
     cpu_load_report = doc.get("cpu")
     Load_average_report = doc.get("load")
     memory_report = doc.get("memory")


     report_data = [f"CPU load: {cpu_load_report}%", f"Load average: {Load_average_report}",f"Memory: {memory_report}%"]
     process_report_data = "\n".join(report_data)
      
     all_reports.append(f"*Report of: *{date} \n {process_report_data}")

  final_report = "\n\n\n".join(all_reports)

  await message.answer(final_report, parse_mode='markdown', reply_markup=start_keyboard)




if __name__ == '__main__':
    executor.start_polling(dp,  skip_updates=True)
