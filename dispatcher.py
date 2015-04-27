import time
import threading
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt4Agg')
import numpy as np

#Throttling value is an integer
class Dispatcher:

	lock = threading.Lock()
	thread_event = threading.Event()
	t_v = 50
	jobs = [0]*1000

	#pyplot animation code inspired by http://stackoverflow.com/questions/16249466/dynamically-updating-a-bar-plot-in-matplotlib
	# def setup_backend(backend='TkAgg'):
	#     import sys
	#     del sys.modules['matplotlib.backends']
	#     del sys.modules['matplotlib.pyplot']
	#     import matplotlib as mpl
	#     mpl.use(backend)  # do this before importing pyplot
	#     import matplotlib.pyplot as plt
	#     return plt

	# def animate(clas):
	# 	mu, sigma = 100, 15
	#     N = 1200
	#     x = mu + sigma * np.random.randn(N)
	#     rects = plt.bar(range(N), jobs, align='center')
	#     for i in range(50):
	#         x = mu + sigma * np.random.randn(N)
	#         for rect, h in zip(rects, x):
	#             rect.set_height(h)
	#     plt.draw()

	@classmethod
	def setEvent(clas):
		# global thread_event
		clas.thread_event.set()

	@classmethod
	def setThrottling(clas, new_tv):
		grabbed = false
		while not grabbed:
			grabbed = clas.lock.acquire()
		clas.t_v = new_tv
		clas.lock.release()

	@classmethod
	def threaded_function(clas, job_queue):
		print ("thread generated\n")
		# global thread_event
		global jobs
		start_time = time.time()
		exec_time = clas.t_v * 0.001
		sleep_time = 0.1 - exec_time 
		while (not clas.thread_event.isSet()):
			if not clas.lock.acquire():
				if (time.time() - start_time) > exec_time:
					time.sleep(sleep_time)
					start_time = time.time()
			else:
				#print ("grabbed lock")
				job = job_queue.get()
				if job:
					exec_time = clas.t_v * 0.001
					sleep_time = 0.1 - exec_time 
					(start_index, length) = job
					#print (start_index)
					count = 0
					while count<length:
						if (time.time() - start_time) < exec_time:
							index = start_index+count
							for i in range(1000):
								clas.jobs[index] += 1.111111
							count += 1
						else:
							time.sleep(sleep_time)
							start_time = time.time()
				clas.lock.release()


	@classmethod
	def dispatch_task(clas, job_queue, throttling_value, n):
		threads = []
		# fig = plt.figure()
		# plt.show()
		clas.t_v = throttling_value
		for i in range(n):
			thread = threading.Thread(target=Dispatcher.threaded_function, args=(job_queue))
			thread.start()
			threads.append(thread)
		for th in threads:
			th.join()





