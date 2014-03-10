#!/usr/bin/python
import os
import time
import sys

# Input filename
filename = 'biz.dnsrecords'

# Remove file and create empty one
try:
	os.remove('biz.domains')
	os.system('touch biz.domains')
except OSError:
	os.system('touch biz.domains')


num_lines = sum(1 for line in open( filename ))
print "Number of lines in file: "+str(num_lines)
time.sleep(3)

counter = 0
ins = open( filename, "r" )
for line in ins:
	# Find hostname
	location = line.find('IN NS')
	domainNS = line[location+6:-2]
	# Remove DNS subdomain
	tmp = domainNS.split('.', 1)[1:]
	try:
		domain = tmp[0]+'\n'
	except:
    		pass

	# Print status info
	#print domain
	counter = counter + 1
	print '('+str(counter)+' of '+str(num_lines)+')'
	#percentDone = counter/num_lines
	#print "{0:.0f}%".format(float(percentDone) * 100)
	
	# Add to file
	open("biz.domains","a").write(domain)

ins.close()

# Get all unique domains
command = 'sort biz.domains | uniq -u > biz.domains.unique'
os.system(command)


