import subprocess
import csv
import time
import threading

filename = raw_input('Enter file name: ')

def log(filename):
	with open(filename+'.csv', 'a') as csvfile:
		csvwriter = csv.writer(csvfile)

		# get mac addresses of connected devices
		procMAC = subprocess.Popen("iw dev wlan0 station dump | grep 'Station' | awk '{print $2}'", 
			shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		MACs = []

		for line in procMAC.stdout.readlines():
			MACs.append(line.strip())

		csvwriter.writerow([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())] + MACs)

		print MACs

		# get IPs from MACs
		ipCommand = "&&".join(["arp -a | grep '"+MAC+"' | tr -d '()' | awk '{print $2}'" for MAC in MACs])

		procIP = subprocess.Popen(ipCommand,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		IPs = []

		for line in procIP.stdout.readlines():
			IPs.append(line.strip())

		csvwriter.writerow([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())] + IPs)

		print IPs

		# ping connected devices (updates RSSI as no inactive time)
		pingCommand = "&&".join(["ping -c 1 "+IP for IP in IPs])
		subprocess.Popen(pingCommand,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		# get signal levels
		signals = []
		sigCommand = "&&".join(["iw dev wlan0 station get '"+MAC+"' | grep 'signal' | awk '{print $2}'" for MAC in MACs])

		procSig = subprocess.Popen(sigCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		for line in procSig.stdout.readlines():
			signals.append(line.strip())

		print signals

		csvwriter.writerow([time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())] + signals)


while True:
	t = threading.Thread(target=log,args=[filename])
	t.start()
	time.sleep(2)