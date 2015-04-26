import mp4networking

mp4obj = mp4networking.MP4networking()

comm1 = {"msg": "cs"}
comm2 = {"msg": "423"}

job1 = {"pos": (10, 5), "job": [11, 12, 13, 14, 15]}
job2 = {"pos": (15, 5), "job": [16, 17, 18, 19, 20]}

while not mp4obj.running:
	pass

print("server up and running")

mp4obj.send_job(job1)
mp4obj.send_job(job2)
mp4obj.send_comm(comm1)
mp4obj.send_comm(comm2)

print(mp4obj.recved_jobs.get())
print(mp4obj.recved_jobs.get())
print(mp4obj.recved_comm.get())
print(mp4obj.recved_comm.get())