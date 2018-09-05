# -*- coding: utf-8 -*-
#
# License:          This module is released under the terms of the LICENSE file 
#                   contained within this applications INSTALL directory

'''
	Graph database population
'''

# -- Coding Conventions
#    http://www.python.org/dev/peps/pep-0008/   -   Use the Python style guide
#    http://sphinx.pocoo.org/rest.html          -   Use Restructured Text for docstrings

# -- Public Imports
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
					  RelationshipTo, RelationshipFrom, Relationship,
					  StructuredRel,
					  BooleanProperty)
from neomodel import db, config
import uuid
import csv
import requests
import re
import socket
import time
from collections import defaultdict
from neomodel import core
#from neo4j.v1 import GraphDatabase, basic_auth, TRUST_ON_FIRST_USE, CypherError

#driver = GraphDatabase.driver("bolt://localhost:7687",
                              #auth=basic_auth("neo4j", "admin"),
                              #encrypted=False,
                              #trust=TRUST_ON_FIRST_USE)
# -- Private Imports
#from nsa.network_topology import configuration
from sky_classes import (ISISLink, Router)

# -- Globals
config.DATABASE_URL = 'bolt://neo4j:admin@localhost:7687' #configuration.neo_database

inputcsv = 'links.csv'
fibrefile = 'fibre_section.csv'
distancePenalty = 99999   # Set a rediculous distance penalty if none exists.
subsfile = 'pesublist.csv'
plan='plan_file.csv'
endnode="ExternalEndpointMembers.csv"
# -- Functions

def fetch_section():
	links = open(fibrefile, 'rt')
	# Read each line as CSV and import into a list
	newlist = []
	#linkslist = list(links.iter_lines())
	linkslist = list(csv.reader(links))
	# decode bytes into text
	#for line in linkslist:
	#    newlist.append(line.decode(encoding='UTF-8'))

	#result = list(csv.reader(newlist))
	#added thid
	results=linkslist

	return results
def externalendpoints():
	endpoints=[]

	exendlist2=[]
	#list az external end point ha mide
	exendlist=[]
	#exendset ye set az external endpoint ha mide
	exendset=[]

	endpoints=open(endnode, 'rt')
	exendlist=list(csv.reader(endpoints))
	for items in exendlist:
		
		k=items[0].split("\t")
		exendset.append(k[0][2:])
		exendlist2.append([k[0][2:],k[1],k[3],k[2]])

	return exendset, exendlist2






	


def failover():
	exendset, exendlist=externalendpoints()


	routerlist=[]
	for pop in Router.nodes:
		routerlist.append(pop.name)
	print(routerlist)

	print(exendset)


	
	listenddict=[]
	enddict={}
	left=[]
	#exendlist i ke endpoints barmigardoone ye liste ke har itemesh ye liste ba ye element ke kolesatre ba tab joda shode
	for item in routerlist:
		if item not in exendset:
			left.append(item)
	print(left)



	dictr={}
	for x in routerlist :
		if (x in exendset or x[0]=="c"):
			dictr[x]=[]
		else:
			pass


		
		
		
	

	for r in exendlist:
		
		for key,value in dictr.items():
			if (key==r[0] and r[3]=="2"):
				value.append((r[1],r[2]))

	for l in left:
		if l[0]=="c" or l[0]=="d":

			m=l.split(".")
			print(m)
			matches=[x for x in left if (x.split(".")[0]==m[0] and x.split(".")[1]==m[1])]
			n=len(matches)
			print(n)
			for key,value in dictr.items():
				if key==l:
					for match in matches:

						value.append((match,100/n))








	return dictr,left

 

def demandslist():
	demandslist=[]


	planf=open(plan, 'rt')
	terlist=list(csv.reader(planf))
	terlist=terlist[4910:38558]


	for line in range(0,33648,1):
		
		newterdic={}
		try:
			pass
			x=terlist[line][0][3:].split()
			y=x[0].split(":")
			newterdic["source"]=y[1]
			newterdic["name"]=y[0]
			newterdic["terrafic"]=float(x[4])
			newterdic["terrafic-level"]=x[3]
			newterdic["service-class"]=x[2]
			newterdic["destination"]=x[1]
			demandslist.append(newterdic)
		except:
			pass
			x=terlist[line][0][3:].split()
			y=x[0][5:]
			newterdic["terrafic"]=float(x[4])
			newterdic["terrafic-level"]=x[3]
			newterdic["service-class"]=x[2]
			newterdic["destination"]=x[1]
			newterdic["source"]=y[:-1]
			newterdic["name"]="Endpoint"
			demandslist.append(newterdic)
	return demandslist


def run():
	

	results, meta = db.cypher_query('MATCH (n)-[r]-() DELETE n, r')
	results, meta = db.cypher_query('MATCH (n) DELETE n')




	


	



	# Get fibre section distance
	distdict = {}
	rownum = 0
	for row in fetch_section():
		#create dictionary index value using site1+site2
		index = row[0]+'-'+row[1]
		if rownum is not 0:
			# Add up all the hops from router1 to router2
		   
			if not distdict.get(index):
				distdict[index] = float(row[5])
			else:
				distdict[index] = distdict[index] + float(row[5])
		rownum += 1

	# Get subscribers
	subscribers = {}
	with open(subsfile, 'rt') as file:
		file = csv.reader(file, delimiter=',')
		for PE in file:
			if re.match('^sr[19][0-9]\.', PE[1]):
				subscribers[PE[1]] = PE[2]
			if re.match('^tr[12][0-9]\.', PE[1]):
				subscribers[PE[1]] = PE[2]
			if re.match('^br0\.', PE[0]):
				subscribers[PE[1]] = PE[2]

	# Read link with ISIS metrics
	with open(inputcsv, 'r+') as file:
		file = csv.reader(file, delimiter=',', quotechar='"')
		for link in file:
			linkf=link
			# Make the routers if this is the first time we found them.
			for linkend in [0, 1]:
				if link[linkend][0:2]=="sr" and link[linkend]!="sr10.enbel" and link[linkend]!="sr11.enbel":



					try:

						router = Router.nodes.get(name="srx"+link[linkend][4:])
						linkf[linkend]=router.name

						
					except:
						router = Router()
						router.name="srx"+link[linkend][4:]
						linkf[linkend]=router.name
						print(linkf[linkend])
				else:
					try:
						router = Router.nodes.get(name=link[linkend])
						linkf[linkend]=router.name
					except:
						router=Router()
						router.name=link[linkend]
						linkf[linkend]=router.name
						print(linkf[linkend])

					# Not all routers have subscribers, so pass gracefully
				try:
						router.subscribers = subscribers[link[linkend]]
						#print(link[linkend]+' has '+subscribers[link[linkend]]+' subscribers')
				except:
					pass
				try:
					router.loopback = socket.gethostbyname(link[linkend]+'.isp.sky.com')
				except:
					pass
				try:
					router.product = link[linkend+7] # 8th and 9th columns
				except:
					pass
				router.save() #save the router to neo4j


				


			# Make the links
			#routera = Router.nodes.get(name=link[0])
			#routerb = Router.nodes.get(name=link[1])
			routera = Router.nodes.get(name=linkf[0])
			routerb = Router.nodes.get(name=linkf[1])

			# First check if a link exists between A and B (or B to A).
			forwardlink = False
			backwardlink = False
			if routera.isislink.is_connected(routerb):
				forwardlink = True
			if routerb.isislink.is_connected(routera):
				backwardlink = True

			sitea = link[2]
			siteb = link[3]

			# Fetch the distance if it exists, or set distance as 0 if local
			# otherwise set a rediculous arbitrary value to help exclude this path
			distance = None
			if sitea == siteb:      # a site that isn't directly connected shouldn't hit this
				distance = 0
			else:
				try:
					# Try forward direction first
					distance = round(float(distdict[sitea+'-'+siteb]))

				except:
					try:
						# If forward fails, try reverse direction
						distance = round(float(distdict[siteb+'-'+sitea]))
					except:
						# Failing that, set penalty
						distance = distancePenalty

			# Calculate latency in ms as 100km = 0.5ms
			latency = round(distance * 0.005, 2)

			# If neither link exists, we can create this one and it will be the forward link.
			if forwardlink == False and backwardlink == False:
				#print('Adding link: ' + routera.name + ' --> ' + routerb.name + ' distance: ' + str(distance) + ' / latency=' + str(latency))

				routera.isislink.connect(routerb, {'forward_metric': int(link[4]),
												   'rate': str(link[5]),
												   'bandwidth': int(link[6]),
												   'distance': int(distance),
												   'latency': latency,
												   'name': f"{routera.name}--{routerb.name}"

													})

			if forwardlink == False and backwardlink == True:
				#print('Adding reverse link data for: ' + routera.name + ' --> ' + routerb.name + ' distance: ' + str(distance))
				r = routerb.isislink.relationship(routera)
				r.reverse_metric = int(link[4])
				r.distance = int(distance)
				r.latency = latency
				r.name=f"{routera.name}--{routerb.name}"
				r.save()
				

			if forwardlink == True and backwardlink == False:
				pass
				# print('WARNING: Trying to create a link twice !. Using first data given only.')
				#print('  FOR ' + routera.name + ' AND ' + routerb.name)
#test
	
			

# -- Main
if __name__ == '__main__':

	t0 = time.time()

	# Main function call
	demandslist=demandslist()
	run()
	failover,left=failover()
	print(failover.keys())

	t1 = time.time()
	print ('\nElapsed time: %s' % str(t1-t0))
	print ('DONE!')
	#print(demandslist[-1])
	routerlist=[]
	for pop in Router.nodes:
		routerlist.append(pop.name)

	print(routerlist)



	dem=demandslist
	 
	wctdict={}
	linkdictlist=[]
	wctlist=[]
	wctnode=[]
	destinations=[]

	for pop in Router.nodes:
		if pop.name[0:2]=="sr":
			destinations.append(pop.name)
	

	print(destinations)

	#preparing demandlist in demlistkey
	
	#session = driver.session()
	#tx = session.begin_transaction()

	temp={}
	wctnode=defaultdict(lambda: 'Vanilla')
	temp=defaultdict(lambda:0)
	for key in routerlist:
		print(key)
		demlistkey=[]
		linkdict={}

		if key in failover.keys():
			print("fail")

		

			for demand in dem:

				if demand["terrafic-level"]=="Y18.09" and demand["source"]==key:

					for s in failover[key]:
						newdic={}
						newdic["terrafic"]=float(s[1])*demand["terrafic"]/100
						newdic["terrafic-level"]=demand["terrafic-level"]
						newdic["service-class"]=demand["service-class"]
						newdic["destination"]=demand["destination"]
						newdic["source"]=s[0]
						newdic["name"]=demand["name"]
						demlistkey.append(newdic)
				else:
					demlistkey.append(demand)

			print("dem compelete!")




		elif key in destinations:
			print("dest")


		
			for demand in dem:
				

				if demand["destination"]==key:
					pass
				else:
					demlistkey.append(demand)
			print("dem compelete!")

		elif  key not in failover.keys() and (key[0:2]=="px" or key[0:2]=="tx"):
			print("ptnofail")

			for demand in dem:
				

				if demand["source"]==key:
					pass
				else:
					demlistkey.append(demand)
			print("dem compelete!")


		else:
			print("pop")
			demlistkey=dem
			print("dem compelete!")


		




	#topology bedoone key o rasm kon 


		delnode=Router.nodes.get(name=key)
		for node in delnode.isislink.match():
			
			r=delnode.isislink.relationship(node)
			
			
			

			r.reverse_metric=r.reverse_metric*20000
			r.forward_metric=r.forward_metric*20000
			r.save()





      

		for demand in demlistkey:
			if demand["terrafic-level"]=="Y18.09":



			
				try:


					bloody='"'
					q="MATCH(r1:Router{name:" +bloody +demand["source"]+bloody+  "}),(r2:Router{name:"  + bloody+demand["destination"]+bloody + "}),p=(r1)-[*..5]-(r2) RETURN nodes(p),RELATIONSHIPS(p),REDUCE(totalweight=0,r IN RELATIONSHIPS(p)|totalweight+r.forward_metric) AS totalCost ORDER by totalCost ASC limit 1"
				#print(q)
				#print(bloody)

					results, columns=db.cypher_query("MATCH(r1:Router{name:" +bloody +demand["source"]+bloody+  "}),(r2:Router{name:"  + bloody+demand["destination"]+bloody + "}),p=(r1)-[*..5]-(r2) RETURN nodes(p),RELATIONSHIPS(p),REDUCE(totalweight=0,r IN RELATIONSHIPS(p)|totalweight+r.forward_metric) AS totalCost ORDER by totalCost ASC limit 1")
					#results, columns=tx.run("MATCH(r1:Router{name:" +bloody +demand["source"]+bloody+  "}),(r2:Router{name:"  + bloody+demand["destination"]+bloody + "}),p=(r1)-[*..5]-(r2) RETURN nodes(p),RELATIONSHIPS(p),REDUCE(totalweight=0,r IN RELATIONSHIPS(p)|totalweight+r.forward_metric) AS totalCost ORDER by totalCost ASC limit 1")





				#print(len(results))
				#print(results)

			##results, columns=db.cypher_query('MATCH(r1:Router{name:"px1.appl.thlon"}),(r2:Router{name:"sr10.bllon"}),p=(r1)-[*..5]-(r2) RETURN nodes(p),RELATIONSHIPS(p),REDUCE(totalweight=0,r IN RELATIONSHIPS(p)|totalweight+r.forward_metric) AS totalCost ORDER by totalCost ASC limit 1')
					linkpath=results[0][1]
			#finallist=[]
					for links in linkpath:

						linkpath0=vars(links)
						if linkpath0["_properties"]["name"] in linkdict:
							linkdict[linkpath0["_properties"]["name"]]=linkdict[linkpath0["_properties"]["name"]]+demand["terrafic"]
							
						else:
							linkdict[linkpath0["_properties"]["name"]]= demand["terrafic"]
				except:
					pass



		
		for key1 in linkdict.keys():
			
				if temp[key1]<linkdict[key1]:


					temp[key1]=linkdict[key1]
				
					wctnode[key1]=key
				

				
			

		


		

		for node in delnode.isislink.match():

			
			r=delnode.isislink.relationship(node)
			r.reverse_metric=r.reverse_metric/20000
			r.forward_metric=r.forward_metric/20000
			r.save()


	

	print("done!")


	with open("wct-node-Y18-09.csv", 'w') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		for keyf,valuef in temp.items():
			mylist=[]
			mylist=keyf.split("--")
			mylist.append(valuef)
			mylist.append(wctnode[keyf])

			wr.writerow(mylist)

	#print(wctlist)
	#print(wctnode)
	

	#print(failover.keys())
	#print(wctlist)
	#print(wctnode)
	#print(routerlist)
	#print(len(routerlist))
	#print(len(demlistkey))
	#print(len(dem))
	#print(failover)
	

	#for obj in ISISLink.get_objects():

		#print (alllinks)
	#print(linkpath0["_properties"]["name"])


	
	#lfinallist={}
	#terraficfanal=[]
	

  




