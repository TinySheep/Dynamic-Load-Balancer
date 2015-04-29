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

from gui import GUI

def main_func(network_manager, dispatcher, hardware_manager, gui):
	# Busy wait :)
	while not network_manager.running:
		pass
	gui.log("Connection has been established!")

	aggregate_flag = threading.Event()

	router_obj = router.mp4router.Router(network_manager, dispatcher.Dispatcher, hardware_manager, aggregate_flag = aggregate_flag, logger=gui.log, gui=gui)

	while True:
		time.sleep(5)
		if aggregate_flag.isSet():
			gui.log("No more jobs to do, waiting for data transfer to finish...")
			network_manager.recved_comm.get()
			gui.log("Server is safe to exit")
			exit(0)

network_manager = networking.mp4networking.MP4networking()

init_throttle = 100
num_workers = 4

dispatcher.Dispatcher.dispatch_task(network_manager.recved_jobs, init_throttle, num_workers)

hardware_manager = state_manager.hardware_info.HardwareInfo(os.getpid(), network_manager.recved_jobs)

gui = GUI(network_manager=network_manager, hardware_manager=hardware_manager, dispatcher=dispatcher.Dispatcher)

hardware_manager.logger = gui.log

threading.Thread(target=main_func, args=[network_manager, dispatcher, hardware_manager, gui]).start()

gui.run()
