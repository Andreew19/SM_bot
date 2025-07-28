#!/usr/bin/env python3
import sqlite3
import psutil
from datetime import *


connection = sqlite3.connect("/app/db/smb.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS server_load (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    CPU_load_percent REAL,
    Load_avg_1 REAL,
    Load_avg_2 REAL,
    Load_avg_3 REAL,
    Memory_load_percent REAL,
    disk_total_gigabyte REAL,
    disk_used_gigabyte REAL,
    disk_free_gigabyte REAL,
    created_at TEXT
)
''')


def get_cpu_load(): 
    return psutil.cpu_percent(interval=1) 
 
def get_memory_usage(): 
  mem = psutil.virtual_memory() 
  return mem.percent 
 
 
cpu_load = get_cpu_load() 
memory_usage = get_memory_usage() 

getLA = psutil.getloadavg()

hdd = psutil.disk_usage('/') 



cursor.execute('''
INSERT INTO server_load (
    CPU_load_percent,
    Load_avg_1,
    Load_avg_2,
    Load_avg_3,
    Memory_load_percent,
    disk_total_gigabyte,
    disk_used_gigabyte,
    disk_free_gigabyte,
    created_at
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    cpu_load,
    getLA[0],
    getLA[1],
    getLA[2],
    memory_usage,
    hdd.total / (2**30),
    hdd.used / (2**30),
    hdd.free / (2**30),
    datetime.now().isoformat()
))

connection.commit()
print("Data inserted with rowid:", cursor.lastrowid)
connection.close()