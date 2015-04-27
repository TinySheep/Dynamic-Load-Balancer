import os
import threading
import time

class StateManager:
	_const_queue_ref = None
	_network_manager = None
	_hardware_manager = None
	_pid = None
	_started = False
	_should_shutdown = threading.Event()
	_freq = 30

	def __init__(self, network_manager, const_job_queue, freq, hardware_manager):
		self._network_manager = network_manager
		self._const_queue_ref = const_job_queue
		self._hardware_manager = hardware_manager
		self._pid = os.getpid()
		self._freq = freq

	def start_comm(self):
		t = threading.Thread(target=self._comm_func)
		t.dameon = True
		t.start()

	def shutdown(self):
		if not self._started:
			return
		self._should_shutdown.set()

	def _comm_func(self):
		while not self._should_shutdown.isSet():
			info = self._hardware_manager.hardware_info()
			self._network_manager.send_comm(info)
			time.sleep(self._freq)
