import psutil
import docker
import os, sys
import time 


# Stop and remove container
def removeCon(containerId, containerName ):
	#Removing from HAProxy.cfg
	readFile = open("/etc/haproxy/haproxy.cfg")
	lines = readFile.readlines()
	lines = lines[:-1]
	readFile.close()

	w = open("/etc/haproxy/haproxy.cfg",'w')
	w.writelines([item for item in lines])
	w.close()

	#Stopping container
	containerId[containerName].stop()
	containerId[containerName].remove()
	print "Container: ", containerId[containerName] , " removed"

#Add and Launch container
def addCon(containerId, containerName, port):
	containerId[containerName] =  client.containers.run("flask-image:latest", detach=True, ports={'5000/tcp': port})

	print "Container launched:"
	print "Name ", containerName, " containerId ", containerId[containerName]

	#Writing in HAProxy.cfg
	config_file = open("/etc/haproxy/haproxy.cfg", "a+")
	config_file.write("\n   server " + containerName + " 127.0.0.1:" + str(port) + " check")
	config_file.close()
	os.system("sudo service haproxy restart")


# Container & Port Info
port = 5049
containerBase = "flask-container"
containerNum = 2
containerId= {}

# Checking cpu usage
usage = psutil.cpu_percent(interval=1)
print "cpu usage", usage


#Figuring how many to lanuch
toLaunch = 1
if usage < 10:
	print "Initially launch only ", toLaunch
else:
	toLaunch = int(usage) / 10
	print "Initially launch  ", toLaunch


#Launching containers
client = docker.from_env()
i = 0
while ( i < toLaunch):
	containerNum += 1
	containerName = containerBase + `containerNum`
	port += 1
	addCon(containerId, containerName, port)
	i += 1
print "\n---------------"
print "waiting 10 seconds to start continous monitoring\n---------------"
time.sleep(10)

while (1):
	usage = psutil.cpu_percent(interval=1)
	print "cpu usage", usage

	if usage < 10:
		
		if port != 5050:
			print "Usage below 10, removing one container"
			
			removeCon(containerId, containerName)
			containerNum -= 1
			containerName = containerBase + `containerNum`
			port -= 1
		else:
			print "Usage below 10, only one container running"
	else:
		#toLaunch = int(usage) / 10
		print ""
		#containerNum += 1
		#containerName = containerBase + `containerNum`
		#port += 1
		#addCon(containerId, containerName, port)

