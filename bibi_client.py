import os

import networking.mp4networking
import router.mp4router
import state_manager.mp4statemanager
import state_manager.hardware_info
import dispatcher



def populate_jobs(queue, num_jobs):
	length = 1024 * 1024 * 16
	job_length = length / num_jobs
	result = []
	for i in range(num_jobs):
		job = {}
		job['index'] = (i * job_length, job_length)
		job['data'] = [111.1111] * job_length
		if i > num_jobs / 2:
			result.append(job)
		else:
			queue.put(job)
	return result






addr = "127.0.0.1"
network_manager = networking.mp4networking.MP4networking(addr)

to_server = populate_jobs(network_manager.recved_jobs, 1024)

with open('throttling.config', 'r') as config:
	init_throttle = int(config.read())

dispatcher.Dispatcher.dispatch_task(network_manager.recved_jobs, init_throttle, 4)

hardware_manager = state_manager.hardware_info.HardwareInfo(os.getpid(), network_manager.recved_jobs)
hardware_manager.hardware_info()

# Busy wait :)
while not network_manager.running:
	pass

network_manager.send_jobs(to_server)

state_manager_obj = state_manager.mp4statemanager.StateManager(network_manager, network_manager.recved_jobs, 15, hardware_manager)

router = router.mp4router.Router(network_manager)

state_manager_obj.start_comm()

while True:
	try:
		comm = router.thor.get(3)
	except:
		print("timed out getting thor")
	else:
		num_req = comm['reqJobs']
		num_jobs = network_manager.recved_jobs.qsize()
		to_send = []
		if num_req > num_jobs / 2:
			num_req = num_jobs / 2
		while num_req > 0:
			try:
				job = network_manager.recved_jobs.get(3)
			except:
				print("timed out getting job")
			else:
				to_send.append(job)
		if len(to_send) > 0:
			network_manager.send_jobs(to_send)

	if network_manager.recved_jobs.qsize() == 0:
		print("Completed {0} jobs".format(dispatcher.Dispatcher.done_count))



