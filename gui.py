from Tkinter import *
from label import ReadOnlyText

class GUI(object):
	values = []
	values_remote = []
	remote_info = None

	def __init__(self, **kwargs):
		self.root = Tk()

		self.network_manager = kwargs.pop('network_manager')
		self.hardware_manager = kwargs.pop('hardware_manager')
		self.dispatcher = kwargs.pop('dispatcher')

		self.frame = Frame(self.root, **kwargs)
		self.frame.grid()
		self.create_labels()
		self.create_log()

		self.update_gui()

	def create_labels(self):
		local = Label(self.frame, text="Local")
		local.grid(row=0, columnspan=6)
		remote = Label(self.frame, text="Remote")
		remote.grid(row=3, columnspan=6)
		for i in range(2):
			labels = []
			labels.append(Label(self.frame, text="Network status", bg='blue'))
			labels.append(Label(self.frame, text="My CPU usage", bg='cyan'))
			labels.append(Label(self.frame, text="Free CPU", bg='blue'))
			labels.append(Label(self.frame, text="Throttle value", bg='cyan'))
			labels.append(Label(self.frame, text="Jobs remaining", bg='blue'))
			labels.append(Label(self.frame, text="Jobs completed", bg='cyan'))
			for j in range(6):
				labels[j].grid(row=i*3+1, column=j)
		# self.nstatus_label = Label(self.frame, text="Network status", bg='blue')
		# self.nstatus_label.grid(row=0, column=0)
		# self.cpu_usage_label = Label(self.frame, text="My CPU usage", bg='cyan')
		# self.cpu_usage_label.grid(row=0, column=1)
		# self.free_cpu_label = Label(self.frame, text="Free CPU", bg='blue')
		# self.free_cpu_label.grid(row=0, column=2)
		# self.throttle_label = Label(self.frame, text="Throttle value", bg='cyan')
		# self.throttle_label.grid(row=0, column=3)
		# self.jobs_label = Label(self.frame, text="Jobs remaining", bg='blue')
		# self.jobs_label.grid(row=0, column=4)
		# self.jobs_done_label = Label(self.frame, text="Jobs completed", bg='cyan')
		# self.jobs_done_label.grid(row=0, column=5)
		for i in range(6):
			var = StringVar()
			var_remote = StringVar()
			self.values.append(var)
			self.values_remote.append(var_remote)
			label = Label(self.frame, textvariable=var)
			label.grid(row=2, column=i)
			label_remote=Label(self.frame, textvariable=var_remote)
			label_remote.grid(row=5, column=i)
			var.set("value")
			var_remote.set("remote value")

	def create_log(self):
		l = Label(self.frame, text="Log")
		l.grid(row=0, column=6)
		self._log = ReadOnlyText(self.frame, bg="black", fg="green")
		self._log.grid(row=1, rowspan=6, column=6)
		self.frame.rowconfigure(6, weight=1)

	def update_gui(self):
		hardware_info = self.hardware_manager.hardware_info()
		self.values[0].set("Connected" if self.network_manager.running else "Disconnected")
		self.values[1].set(hardware_info['my_cpu'])
		self.values[2].set(hardware_info['free_cpu'])
		self.values[3].set(hardware_info['throttling'])
		self.values[4].set(self.network_manager.recved_jobs.qsize())
		self.values[5].set(self.dispatcher.done_count)

		if self.remote_info:
			flag = self.remote_info["type"] == "bibi"
			self.values_remote[0].set("Connected" if self.network_manager.running else "Disconnected")
			self.values_remote[1].set(self.remote_info['my_cpu'])
			self.values_remote[2].set(self.remote_info['free_cpu'])
			self.values_remote[3].set(self.remote_info['my_throttle'] if not flag else self.remote_info["throttling"])
			self.values_remote[4].set(self.remote_info['qed'] if not flag else self.remote_info["num"])
			self.values_remote[5].set(self.remote_info.get('done'))

		self.root.update()
		self.frame.after(1000, self.update_gui)

	def run(self):
		self.root.mainloop()

	def log(self, message):
		self._log.insert(END, message + '\n')