#! /usr/bin/python

import time
from scapy.all import *

#seconds = int(raw_input("Enter the amount of seconds you wish to scan\n"))

def scan(command):
	launchresults = subprocess.check_output(command, shell=True)
	return launchresults


def BaseLineTest():
	print "++++++++++++++++++++++++++++++++"
	print "+++RUNNING BASELINE CHECKS +++++"
	print "+++ ROOT | BaseDir etc     +++++"
	print "++++++++++++++++++++++++++++++++"
	# Checking Running as root, for write perms
	try:
		checkPermissions = 'whoami'
		checkPermissionsResults = scan(checkPermissions)
	except Exception as e:
		print e

	if 'root' in checkPermissionsResults:
		print "====You are Root that is good! Continuing===="
	else:
		"You are not root, please run as root!"
		"EXITING"
		exit()

	#finding full full path of script
	checkPath = 'pwd'
	FullPath = scan(checkPath).strip() + '/'
	print "The Full path to be used for script is ", FullPath


	baseDir = "base"
	# create base sub dir to place all files
	try:
		mkBaseDir = "mkdir %s" % baseDir
		scan(mkBaseDir)
	except Exception as e:
		print e

	# check dir was created
	checkDir = "ls | grep base"
	checkDirDirResults = scan(checkDir)
	if 'base' in checkDirDirResults:
		print "BASE directory found.. continuing"

	FullPath = ''.join((FullPath, baseDir)) + '/'
	print "Full path and baseDir for script will be ", FullPath
	return FullPath


def packet_callback(packet):

	if (ARP in packet and packet[ARP].op == 2):
		arpIP = packet[ARP].psrc
		print "%s => %s"%(packet[ARP].hwsrc,packet[ARP].psrc)
		IPlist.append(packet[ARP].psrc)
				#packet.show()
# prevents IP address being written twice
		if arpIP not in IPlist:
			IPlist.append(arpIP)


def arpPing(IPRange):
	print " Running Arp Ping"
	#arping(IPRange)
	ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=IPRange), timeout=5)
	#ans.summary(lambda (s,r):  r.sprintf("%Ether.src% %ARP.psrc%"))
	packet = ans
	return packet
"""====START OF MAIN ====="""

if __name__ == '__main__':
	seconds = 2
	bpf = 'arp'
	outPutFile = 'testip.txt'
	IPlist = []
	FullPath = BaseLineTest()
	time.sleep(2)

	print "====starting Sniffer====="
	print "Running Sniffer for %s " % seconds

	sniff(filter=bpf, prn=packet_callback, timeout=seconds)


	#print "Running Arp Ping"
	arpPingResults = arpPing("192.168.0.*")
	print "ARP PING RESULTS "
	results = arpPingResults.summary(lambda (s,r):  r.sprintf("%ARP.psrc%"))
	print "RESULTS", results

	print "Sniffer finished"
	#print "IP LIST:"
	#print IPlist

	FileFullPath = FullPath + outPutFile

	print "[!] Writing contents to %s" % outPutFile
	if IPlist:
		ipFile = open(FileFullPath, 'w')
		ipFile.write("===Hosts identified via ARP Sniffing==" '\n')
		for IP in IPlist:
			print "Found Host: %s, writing to file" % IP
			ipFile.write(IP + '\n')
		ipFile.close()


"""


ARP Ping

The fastest way to discover hosts on a local ethernet network is to use the ARP Ping method:

>>> ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.0.0/24"),timeout=2)

Answers can be reviewed with the following command:

>>> ans.summary(lambda (s,r): r.sprintf("%Ether.src% %ARP.psrc%") )

Scapy also includes a built-in arping() function which performs similar to the above two commands:

>>> arping("192.168.1.*")



"""
