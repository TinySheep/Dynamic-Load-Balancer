import os, psutil, time

config = open('throttling.config', 'r')

jobs = []

insMP4Networking # Networking object

last_time =	-1
last_num_jobs = -1

def hardware_info():
	global last_time
	global last_num_jobs
	ret = {}
	#need to compute speed
	if last_time == -1:
		last_time = time.time()
	else:
		time_elapsed = time.time() - last_time
		last_time = time.time()
		print("time is " + str(time_elapsed))

	ret["time"] = time_elapsed

	if last_num_jobs == -1:
		last_num_jobs = len(jobs)
	elif len(jobs) == 0:
		res["status"] = "Done"
	else: 
		jobs_done = len(jobs) - last_num_jobs
		last_num_jobs = len(jobs)
		res["status"] = "Runnning"
	

	pid = os.getpid()
	proc = psutil.Process(pid)
	ret["my_cpu"] = proc.get_cpu_percent(0.1)
	ret["free_cpu"] = 100 - psutil.cpu_percent(interval=0.1)
	throttling_val = int(config.read())	
	ret["num"] = len(jobs)
	ret["throttling"] = throttling_val
	ret["type"] = "bibi"

	print(ret)
	return ret


hardware_info()
time.sleep(1)
test = hardware_info()
print(test)

def adaptor(remote_info):
	local_info = hardware_info()
	new_throttling = local_info["throttling"]
	remote_throttling = remote_info["throttling"]
	
	#Update local throttling 
	if local_info["free_cpu"] <= 10:
		if local_info["throttling"] > 50: 
			new_throttling = local_info["throttling"] - 20
		else: 
			new_throttling = local_info["throttling"] / 2
	
	elif local_info["free_cpu"] >= 50:
		if local_info["throttling"] < 50:
			new_throttling = local_info["throttling"] * 2
		elif local_info["throttling"] < 75: 
			new_throttling = local_info["throttling"] + 20
	#Update remote throttling 
	if remote_info["free_cpu"] <= 10:
		if remote_info["throttling"] > 50: 
			remote_throttling = remote_info["throttling"] - 20
		else: 
			remote_throttling = remote_info["throttling"] / 2
	
	elif remote_info["free_cpu"] >= 50:
		if remote_info["throttling"] < 50:
			remote_throttling = remote_info["throttling"] * 2
		elif remote_info["throttling"] < 75: 
			remote_throttling = remote_info["throttling"] + 20

# Call worker thread function 
	Dispatcher.setThrottling(new_throttling)

	ret = {}
	ret["type"] = "thor"
	ret["throttling"] = remote_throttling

	local_speed = local_info["num"] / local_info["time"] * (new_throttling / local_info["throttling"])
	local_rem = local_info["num"] / local_speed 
	remote_speed = remote_info["num"] / remote_info["time"] * (remote_throttling / remote_info["throttling"])
	remote_rem = remote_info["num"] / remote_speed 

	num_jobs_in = 0
	if local_info["status"] == "Done": 
		num_jobs_in = remote_info["num"] * local_info["throttling"]/(local_info["throttling"] + remote_info["throttling"])
	
	elif remote_info["status"] == "Done": 
		num_jobs_in = (-1) * remote_info["num"] * local_info["throttling"]/(local_info["throttling"] + remote_info["throttling"])

	else: 
		if local_rem - remote_rem > 20: 
			num_jobs_in = (-1) * (local_rem - remote_rem) * remote_speed / 2 
		else remote_rem - local_rem > 20: 
			num_jobs_in = (remote_rem - local_rem) * local_speed / 2 

	if num_jobs_in > 0: 
		ret["reqJobs"] = num_jobs_in
	else: 
		ret["reqJobs"] = 0
		# Call transfer manager
		
	

	insMP4Networking.send(ret)

