import os, psutil

config = open('throttling.config', 'r')

jobs = []

def hardware_info():
	pid = 6150
	proc = psutil.Process(pid)
	ret = {}
	ret["my_cpu"] = proc.get_cpu_percent(0.1)
	throttling_val = int(config.read())	
	ret["num"] = len(jobs)
	ret["throttling"] = throttling_val
	
	


	print(ret)

	return ret


hardware_info()
