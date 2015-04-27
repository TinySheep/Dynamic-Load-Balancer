import psutil

def hardware_info(pid):
	proc = psutil.Process(pid)
	ret = {}
	with open('throttling.config', 'r') as config:
		throttling_val = int(config.read())	
	ret["my_cpu"] = proc.get_cpu_percent(0.1)
	ret["throttling"] = throttling_val
	return ret