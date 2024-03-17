import psutil  
 
def get_cpu_load(): 
    return psutil.cpu_percent(interval=1) 
 
def get_memory_usage(): 
    mem = psutil.virtual_memory() 
    return mem.percent 
 
 
cpu_load = get_cpu_load() 
memory_usage = get_memory_usage() 
 
hdd = psutil.disk_usage('/') 
 


