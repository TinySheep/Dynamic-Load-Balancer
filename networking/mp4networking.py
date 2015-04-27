import pickle
import socket
import struct
import sys
import threading
import Queue

# The port to use, should be the same on both ends
MP4NETWORKING_PORT = 24646
# Length of string returned by calling struct.pack() on an int
INT_SIZE = 4

class MP4networking:
	_job_chanel = None
	_comm_chanel = None
	_jobs_buffer = Queue.Queue()
	_comm_buffer = Queue.Queue()
	_con_established = threading.Event()

	# Public
	running = False
	recved_jobs = Queue.Queue()
	recved_comm = Queue.Queue()

	def __init__(self, server_addr = None):
		if not server_addr:
			t = threading.Thread(target=self._init_server)
			t.daemon = True
			t.start()
		else:
			t = threading.Thread(target=self._init_client, args=[server_addr])
			t.daemon = True
			t.start()
		t1 = threading.Thread(target=self._recv, args=["job"])
		t2 = threading.Thread(target=self._recv, args=["comm"])
		t1.daemon = True
		t2.daemon = True
		t1.start()
		t2.start()

	def _init_client(self, server_addr):
		s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s1.connect((server_addr, MP4NETWORKING_PORT))
		s2.connect((server_addr, MP4NETWORKING_PORT))
		self._job_chanel = s1
		self._comm_chanel = s2
		s1.send("job")
		s2.send("comm")
		ack1 = s1.recv(4)
		ack2 = s2.recv(4)
		if ack1 == "cool" and ack2 == "cool":
			print("Connected to {0}:{1}".format(server_addr, MP4NETWORKING_PORT))
			self._con_established.set()
		else:
			print("_init_client failed")
			return

	def _init_server(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(("", MP4NETWORKING_PORT))
		s.listen(2)
		con1, addr1 = s.accept()
		con2, addr2 = s.accept()
		s.close()
		con1_name = con1.recv(1024)
		con2_name = con2.recv(1024)
		if(con1_name == "job"):
			if con2_name != "comm":
				print("_init_server failed!")
				return
			self._job_chanel = con1
			self._comm_chanel = con2
		else:
			if con1_name != "comm" or con2_name != "job":
				print("_init_server failed!")
				return
			self._job_chanel = con2
			self._comm_chanel = con1
		con1.send("cool")
		con2.send("cool")
		print("{0}:{1} connected".format(addr1[0], addr1[1]))
		print("{0}:{1} connected".format(addr2[0], addr2[1]))
		self._con_established.set()

	def _recv(self, type):
		self._con_established.wait()
		self.running = True
		t = threading.Thread(target=self._process_buffer, args=[type])
		t.daemon = True
		t.start()
		if type == "job":
			conn = self._job_chanel
			buff = self._jobs_buffer
		else:
			conn = self._comm_chanel
			buff = self._comm_buffer

		while True:
			try:
				msg = conn.recv(4096)
			except socket.error, e:
				print e
				print("_recv failed!")
				return
			else:
				if len(msg) == 0:
					print("shutting down!")
					return
				buff.put(msg)

	def _process_buffer(self, type):
		if type == "job":
			store = self.recved_jobs
			buff = self._jobs_buffer
		else:
			store = self.recved_comm
			buff = self._comm_buffer
		buf = ""
		buf_size = 0
		obj_size_to_read = 0
		while True:
			if obj_size_to_read == 0 or buf_size < obj_size_to_read:
				msg = buff.get()
			else:
				msg = ""
			buf = buf + msg
			buf_size += len(msg)
			if obj_size_to_read > 0:
				if buf_size >= obj_size_to_read:
					data = buf[:obj_size_to_read]
					buf = buf[obj_size_to_read:]
					buf_size -= obj_size_to_read
					obj_size_to_read = 0
					obj_read = pickle.loads(data)
					store.put(obj_read)
			if obj_size_to_read == 0:
				if buf_size >= INT_SIZE:
					data = buf[:INT_SIZE]
					buf = buf[INT_SIZE:]
					buf_size -= INT_SIZE
					obj_size_to_read = struct.unpack("I", data)[0]

	def _send(self, conn, data):
		data_str = pickle.dumps(data)
		msg = struct.pack("I", len(data_str))
		msg += data_str
		size = len(msg)
		while size > 0:
			sent = conn.send(msg)
			if sent == 0:
				print("send is 0")
			size -= sent

	def close(self):
		self._job_chanel.close()
		self._comm_chanel.close()
		self.running = False

	def send_job(self, job):
		t = threading.Thread(target=self._send, args=[self._job_chanel, job])
		t.daemon = True
		t.start()

	def send_comm(self, comm):
		t = threading.Thread(target=self._send, args=[self._comm_chanel, comm])
		t.daemon = True
		t.start()

	


