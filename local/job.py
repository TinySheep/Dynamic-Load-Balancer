import time
num = 1024 * 1024 * 16
num_jobs = 1024*32

class Job:
	def __init__(self, jid, _size = 0, _first = 0):
		self._id = jid
		self.size = _size
		self.first = _first
arr = [0] * num

# List of jobs (job queue)
jobs = [] 

# Initialize job queue
job_size = num / num_jobs
for i in range(num_jobs): 
	currJob = Job(i, job_size, i*job_size)
	jobs.append(currJob)
	print("Job " + str(jobs[len(jobs)-1]._id) + " has been created")


print(len(jobs))

for j in range(1000):
	for i in range(num):
		arr[i] += 1.11
