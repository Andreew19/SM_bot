#!/usr/bin/env python3
import pymongo 
import psutil

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["SMB"]


server_load = db["server_load"]

def get_cpu_load(): 
    return psutil.cpu_percent(interval=1) 
 
def get_memory_usage(): 
  mem = psutil.virtual_memory() 
  return mem.percent 
 
 
cpu_load = get_cpu_load() 
memory_usage = get_memory_usage() 

getLA = psutil.getloadavg()

hdd = psutil.disk_usage('/') 

load = {
    "CPU_load_percent": cpu_load,
    "Load_verage": getLA,
    "Memory_load_percent": memory_usage,
    "disk_total_gigabyte": hdd.total / (2**30),
    "disk_used_gigabyte": hdd.used / (2**30),
    "disk_free_gigabyte": hdd.free / (2**30),
}


x = server_load.insert_one(load)

print(x.inserted_id)