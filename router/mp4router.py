import threading
import adaptor
import Queue
import time

class Router:
	_network_manager = None
	_should_shutdown = threading.Event()

	thor = Queue.Queue()

	def __init__(self, network_manager, dispatcher, hardware_info, aggregate_flag = None, logger = None, gui = None):
		self._network_manager = network_manager
		self._dispatcher = dispatcher
		self._hardware_info = hardware_info
		self.aggregate_flag = aggregate_flag
		self._logger = logger
		self.gui = gui
		t = threading.Thread(target=self._classify)
		t.daemon = True
		t.start()

	def _classify(self):
		while not self._should_shutdown.isSet():
			try:
				comm = self._network_manager.recved_comm.get(timeout=3)
			except:
				pass
			else:
				if comm["type"] == "bibi":
					if self._logger:
						self._logger("Received state information from client")
						self.gui.remote_info = comm
					adaptor.adaptor(comm, self._network_manager, self._dispatcher, self._hardware_info)
				elif comm["type"] == "thor":
					if comm["done"] + self._dispatcher.done_count == 1024: 
						info = {}
						info["type"] = "SEND"
						self.aggregate_flag.set()
						self._dispatcher.thread_event.set()
						time.sleep(5)
						self._network_manager.send_comm(info)
						print("local initiating aggregation")
						return
					self._dispatcher.setThrottling(comm["throttling"])
					self._hardware_info.throttle = comm["throttling"]
					if self._logger:
						self._logger("Setting throttle value to {0}...".format(comm["throttling"]))
					self.thor.put(comm)
				elif comm["type"] == "SEND" :
					print("remote received aggregation")
					for result in self._dispatcher.results:
						self._network_manager.send_jobs(result)
					while self._network_manager.recved_comm.qsize() > 0:
						self._network_manager.recved_comm.get()
					self.aggregate_flag.set()
					return
				else:
					print("911911")
					print(comm["type"])
	

