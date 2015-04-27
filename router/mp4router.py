import threading
import adaptor
import Queue


class Router:
	_network_manager = None
	_should_shutdown = threading.Event()

	thor = Queue.Queue()

	def __init__(self, network_manager, dispatcher, hardware_info):
		self._network_manager = network_manager
		self._dispatcher = dispatcher
		self._hardware_info = hardware_info
		t = threading.Thread(target=self._classify)
		t.daemon = True
		t.start()

	def _classify(self):
		while not self._should_shutdown.isSet():
			try:
				comm = self._network_manager.recved_comm.get(timeout=3)
			except:
				print("911")
			else:
				if comm["type"] == "bibi":
					adaptor.adaptor(comm, self._network_manager, self._dispatcher, self._hardware_info)
				elif comm["type"] == "thor":
					dispatcher.setThrottling(comm["throttling"])
					self.thor.put(comm)
				else:
					print("911911")
	

