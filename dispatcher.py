from time import sleep
from threading import Thread

#Throttling value is an integer
class Dispatcher:
	
	@staticmethod
	def threaded_function(arg):
		(job, t_v) = arg
		(start_index, length) = job
		exec_time = t_v * 0.001
		sleep_time = 0.1 - sleep_time 
		start_time = time.time()
		count = 0
		while count<length:
			if (time.time() - start_time) < exec_time:
				jobs[start_index+count] += 1.111111
				count++
			else:
				time.sleep(sleep_time)
				start_time = time.time()

	@staticmethod
	def dispatch_task(job_queue, throttling_value):
		job = job_queue.pop()
		thread = Thread(target=threaded_function, args=(job, throttling_value))
		thread.start()
		thread.join()
