import os, psutil, time
'''
hardware_info()
time.sleep(1)
test = hardware_info()
print(test)
'''
def adaptor(remote_info, insNetworking, dispatcher, hardware_info):
	local_info = hardware_info.hardware_info()
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
	dispatcher.setThrottling(new_throttling)

	ret = {}
	ret["type"] = "thor"
	ret["throttling"] = remote_throttling

	local_speed = local_info["num"] / local_info["time"] * (new_throttling / local_info["throttling"])
	remote_speed = remote_info["num"] / remote_info["time"] * (remote_throttling / remote_info["throttling"])
	if local_speed == 0 or remote_speed == 0:
		return

	local_rem = local_info["num"] / local_speed 
	remote_rem = remote_info["num"] / remote_speed 

	num_jobs_in = 0
	if local_info["status"] == "Done" and remote_info["status"] == "Done":
		ret["type"] = "Done"
	elif local_info["status"] == "Done": 
		num_jobs_in = remote_info["num"] * local_info["throttling"]/(local_info["throttling"] + remote_info["throttling"])
	
	elif remote_info["status"] == "Done": 
		num_jobs_in = (-1) * remote_info["num"] * local_info["throttling"]/(local_info["throttling"] + remote_info["throttling"])

	else: 
		if local_rem - remote_rem > 20: 
			num_jobs_in = (-1) * (local_rem - remote_rem) * remote_speed / 2 
		elif remote_rem - local_rem > 20: 
			num_jobs_in = (remote_rem - local_rem) * local_speed / 2 

	if num_jobs_in > 0: 
		ret["reqJobs"] = num_jobs_in
	else: 
		ret["reqJobs"] = 0
		# Call transfer manager

	insNetworking.send_comm(ret)

