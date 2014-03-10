import os

hostnames = ['badwolf', 'k9', 'thedoctor']
hostnames = ['k9']

# Remove file and create empty one
for host in hostnames:
	try:
		os.remove('domains'+host)
		os.system('touch domains'+host)
	except OSError:
		os.system('touch domains'+host)


# Split up domain file across nodes
largeDomainFileList = ''

numOfWorkers=len(hostnames)
filename = "biz.domains.unique" 
counter = 0
worker = 0
Domains = sum(1 for line in open(filename))
domains4Worker = [0]*len(hostnames)

ins = open( filename , "r" )

for line in ins:
	if float(counter)/(Domains) <= float(1)/(numOfWorkers):
		counter = counter + 1
		open("domains"+hostnames[worker],"wb").write(line)
	else:
		domains4Worker[worker] = counter 
		worker = worker + 1
		counter = 0

# Save last # of entries and close file
domains4Worker[worker] = counter 
ins.close()

# Spawn DC on client
numSubs = 1000 
numOfProcesses = 1000 
counter = 0
for worker in hostnames:

	print 'Copying code to:'+worker
	command = 'scp -r ~/git/traviscollins/domain-controller sdruser@'+worker+':~/git/traviscollins/'
	os.system(command)


	print "Copying domain file to: "+worker
	command = 'scp domains'+worker+' sdruser@'+worker+':~/git/traviscollins/domain-controller/findDCs/domains.txt'
	os.system(command)

	print "Starting DC search on: "+worker
	command = 'ssh sdruser@'+worker+' "cd ~/git/traviscollins/domain-controller/findDCs/; echo Hello ;screen -d -m -S findDC /home/sdruser/git/traviscollins/domain-controller/findDCs/findDCs_remote '+str(numSubs)+' '+str(domains4Worker[counter])+' '+str(numOfProcesses)+'"'
	os.system(command)

	counter = counter + 1

