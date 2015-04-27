import threading
import Queue


class Router:
	_network_manager = None
	_should_shutdown = threading.Event()

	bibi = Queue.Queue()
	thor = Queue.Queue()

	def __init__(self, network_manager):
		self._network_manager = network_manager
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
					self.bibi.put(comm)
				elif comm["type"] == "thor":
					self.thor.put(comm)
				else:
					print("911911")

