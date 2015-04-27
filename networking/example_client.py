import mp4networking

mp4obj = mp4networking.MP4networking("127.0.0.1")

comm1 = {"msg": "hello"}
comm2 = {"msg": "world"}

job1 = {"pos": (0, 5), "job": [1.111, 1.111, 1.111, 1.111, 1.111, 1.111, 1.111, 1.111, 1.111, 1.111]}
job2 = {"pos": (5, 5), "job": [1.111, 1.111, 1.111, 1.111, 1.111, 1.111, 1.111, 1.111, 1.111, 1.111]}

while not mp4obj.running:
	pass

print("client up and running")

mp4obj.send_job(job1)
mp4obj.send_job(job2)
mp4obj.send_comm(comm1)
mp4obj.send_comm(comm2)

print(mp4obj.recved_jobs.get())
print(mp4obj.recved_jobs.get())
print(mp4obj.recved_comm.get())
print(mp4obj.recved_comm.get())