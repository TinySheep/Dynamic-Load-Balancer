import os
import time
import threading
import sys

import adaptor
import networking.mp4networking
import router.mp4router
import state_manager.mp4statemanager
import state_manager.hardware_info
import dispatcher

network_manager = networking.mp4networking.MP4networking()

init_throttle = 100

dispatcher.Dispatcher.dispatch_task(network_manager.recved_jobs, init_throttle, 4)

hardware_manager = state_manager.hardware_info.HardwareInfo(os.getpid(), network_manager.recved_jobs)
hardware_manager.hardware_info()

# Busy wait :)
while not network_manager.running:
	pass

aggregate_flag = threading.Event()

router = router.mp4router.Router(network_manager, dispatcher.Dispatcher, hardware_manager, aggregate_flag = aggregate_flag)

while True:
	time.sleep(5)
	if network_manager.recved_jobs.qsize() == 0:
		print("Completed {0} jobs".format(dispatcher.Dispatcher.done_count))
	if aggregate_flag.isSet():
		print("server exiting")
		network_manager.recved_comm.get()
		print("Server is safe to exit")
		exit(0)

