import os

import adaptor
import networking.mp4networking
import router.mp4router
import state_manager.mp4statemanager
import state_manager.hardware_info
import dispatcher

network_manager = networking.mp4networking.MP4networking()

with open('throttling.config', 'r') as config:
	init_throttle = int(config.read())

dispatcher.Dispatcher.dispatch_task(network_manager.recved_jobs, init_throttle, 4)

hardware_manager = state_manager.hardware_info.HardwareInfo(os.getpid(), network_manager.recved_jobs)
hardware_manager.hardware_info()

# Busy wait :)
while not network_manager.running:
	pass

router = router.mp4router.Router(network_manager)

while True:
	try:
		comm = router.bibi.get(3)
	except:
		print("timed out getting bibi")
	else:
		adaptor.adaptor(comm, network_manager, dispatcher.Dispatcher, hardware_manager)

	if network_manager.recved_jobs.qsize() == 0:
		print("Completed {0} jobs".format(dispatcher.Dispatcher.done_count))