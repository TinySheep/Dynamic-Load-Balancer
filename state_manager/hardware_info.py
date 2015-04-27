
class HardwareInfo:
	def __init__(self): 
		self.last_time = -1
		self.last_num_jobs = -1


	def hardware_info():
		ret = {}
		#need to compute speed
		if self.last_time == -1:
			self.last_time = time.time()
		else:
			time_elapsed = time.time() - self.last_time
			self.last_time = time.time()
			print("time is " + str(time_elapsed))

		ret["time"] = time_elapsed

		if self.last_num_jobs == -1:
			self.last_num_jobs = len(jobs)
		elif len(jobs) == 0:
			res["status"] = "Done"
		else: 
			jobs_done = len(jobs) - self.last_num_jobs
			self.last_num_jobs = len(jobs)
			res["status"] = "Runnning"
		

		pid = os.getpid()
		proc = psutil.Process(pid)
		ret["my_cpu"] = proc.get_cpu_percent(0.1)
		ret["free_cpu"] = 100 - psutil.cpu_percent(interval=0.1)
		throttling_val = int(config.read())	
		ret["num"] = len(jobs)
		with open('throttling.config', 'r') as config:
			throttling_val = int(config.read())
		ret["throttling"] = throttling_val
		ret["type"] = "bibi"

		print(ret)
		return ret
