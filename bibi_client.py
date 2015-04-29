import os
import threading
import sys

import networking.mp4networking
import router.mp4router
import state_manager.mp4statemanager
import state_manager.hardware_info
import dispatcher

from gui import GUI


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



def main_func(to_server, network_manager, dispatcher, hardware_manager, logger, gui):
	# Busy wait :)
	while not network_manager.running:
		pass
	logger("Connection has been established!")

	network_manager.send_jobs(to_server)
	logger("Sending initial {0} jobs to the server".format(len(to_server)))

	state_manager_obj = state_manager.mp4statemanager.StateManager(network_manager, network_manager.recved_jobs, 15, hardware_manager, logger=logger, dispatcher = dispatcher)

	aggregate_flag = threading.Event()

	router_obj = router.mp4router.Router(network_manager, dispatcher.Dispatcher, hardware_manager, aggregate_flag = aggregate_flag, logger=logger)

	state_manager_obj.start_comm()

	while True:
		try:
			comm = router_obj.thor.get(timeout=3)
		except:
			pass
		else:
			logger("Received comm from server")
			gui.remote_info = comm
			num_req = comm['reqJobs']
			num_jobs = network_manager.recved_jobs.qsize()
			to_send = []
			if num_req > num_jobs / 2:
				num_req = num_jobs / 2
			while num_req > 0:
				try:
					job = network_manager.recved_jobs.get(timeout=3)
				except:
					print("timed out getting job")
					num_req = 0
					break
				else:
					to_send.append(job)
					num_req -= 1
			if len(to_send) > 0:
				network_manager.send_jobs(to_send)
				logger("Sending {0} jobs".format(len(to_send)))

		# if network_manager.recved_jobs.qsize() and not aggregate_flag.isSet() == 0:
		# 	print("Completed {0} jobs".format(dispatcher.Dispatcher.done_count))

		if aggregate_flag.isSet():
			logger("All jobs are done on both ends")
			logger("Waiting for data transfer from server...")
			state_manager_obj.shutdown()
			me_done = 0
			for result in dispatcher.Dispatcher.results:
				me_done += len(result)
			while network_manager.recved_jobs.qsize() + me_done != 1024:
				pass
			logger("Aggregating...")
			network_manager.send_comm({"lol":"shutdown"})
			final_result = [0] * (1024 * 1024 * 16)
			for result in dispatcher.Dispatcher.results:
				for job in result:
					start_idx, length = job['index']
					data = job['data']
					final_result[start_idx:(start_idx + length)] = data
			while network_manager.recved_jobs.qsize() > 0:
				job = network_manager.recved_jobs.get()
				start_idx, length = job['index']
				data = job['data']
				final_result[start_idx:(start_idx + length)] = data
			prev = final_result[0]
			logger("First value is {0}".format(prev))
			for val in final_result:
				if val != prev:
					logger("NOOOOOOOOOOOOOO")
				prev = val
			logger("Aggregated values are correct!")
			sys.exit(0)


addr = "127.0.0.1"
network_manager = networking.mp4networking.MP4networking(addr)

to_server = populate_jobs(network_manager.recved_jobs, 1024)

init_throttle = 100
num_threads = 4

dispatcher.Dispatcher.dispatch_task(network_manager.recved_jobs, init_throttle, num_threads)

hardware_manager = state_manager.hardware_info.HardwareInfo(os.getpid(), network_manager.recved_jobs)

gui = GUI(network_manager=network_manager, hardware_manager=hardware_manager, dispatcher=dispatcher.Dispatcher)

hardware_manager.logger = gui.log

threading.Thread(target=main_func, args=[to_server, network_manager, dispatcher, hardware_manager, gui.log, gui]).start()

gui.run()




