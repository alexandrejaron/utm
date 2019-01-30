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
import copy
import numpy as np

import matplotlib.pyplot as plt        
import networkx as nx
from networkx.algorithms import all_pairs_dijkstra_path,all_shortest_paths
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

inputcsv = 'links_bidir_srx.csv'
fibrefile = 'fibre_section.csv'
distancePenalty = 99999   # Set a rediculous distance penalty if none exists.
subsfile = 'pesublist.csv'
plan='core-9-i.csv'
endnode="failover_new.csv"
sites="sites.csv"
srlg="srlg_new.csv"
def node_failure(routerlist,failover,linkdictzero,dem,G):
	destinations=[]
	routerlist=routerlist
	dem=dem

	for pop in routerlist:
		if pop[0:2]=="sr":
			destinations.append(pop)


		#print(destinations)
		#with open('firsttrystr.txt', 'r') as myfile:
		   # cq=myfile.read().replace('\n', '')

	rlwod=[x for x in routerlist if x not in destinations]
		#print(rlwod)


		#preparing demandlist in demlistkey
		
		#session = driver.session()
		#tx = session.begin_transaction()

		
	wctnode=copy.deepcopy(linkdictzero)
	for key,value in wctnode.items():
		wctnode[key]=[]
	temp=copy.deepcopy(linkdictzero)


	for key in sorted(rlwod):
		print(key)
		demlistkey=[]
		linkdict=copy.deepcopy(linkdictzero)


		


		if key[0:2]=="ar" or key[0:2]=="er":

			print("cdn" or "er")
			for demand in dem:
				if demand["source"] in list(G[key]):
					pass
				else:
					demlistkey.append(demand)




			for node in G[key]:
				
				
					if node in failover.keys():
						for demand in dem:
			#print("fail")

		

						
			
							if demand["source"]==node:
			
								for s in failover[node]:
									newdic={}
									newdic["terrafic"]=float(s[1])*demand["terrafic"]/100
									newdic["terrafic-level"]=demand["terrafic-level"]
									newdic["service-class"]=demand["service-class"]
									newdic["destination"]=demand["destination"]
									newdic["source"]=s[0]
									newdic["name"]=demand["name"]
									demlistkey.append(newdic)
				

		elif key in failover.keys():
			print("fail")

		

			for demand in dem:

				if demand["source"]==key:

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







		print(len(demlistkey))


		G.remove_node(key)
	   
		
		
		
		
		for demand in demlistkey:

		
			try:
				
				results=nx.all_shortest_paths(G,demand["source"],demand["destination"],weight="IGP",method="dijkstra")
				
				allpath=[]
				for result in results:
					
					
					linkspath=[]

				
					for i in list(range(1,len(result))):
						st=result[i-1]
						nd=result[i]
						ln=st+"--"+ nd
							
						linkspath.append(ln)
						
					
					allpath.append(linkspath)
				n=len(allpath)
				for path in allpath:


				
				
				
					for link in path:
						if link in linkdict:
							
							linkdict[link]=linkdict[link]+demand["terrafic"]/n
						else:
							
							linkdict[link]= demand["terrafic"]/n
					  
			except:

				pass         
	





		for key1 in linkdict.keys():
			
			if linkdict[key1]> linknormal[key1]:
				
			
				if temp[key1]<=linkdict[key1]:


					
					if temp[key1]==linkdict[key1] :
						temp[key1]=linkdict[key1]
						wctnode[key1].append(key)
					elif temp[key1]<linkdict[key1]:
						temp[key1]=linkdict[key1]
						wctnode[key1]=[]
						wctnode[key1].append(key)	
						
		G.clear()		
		G=nx.MultiGraph()
		G.add_weighted_edges_from(elist,weight="IGP")		


	return temp,wctnode

def srlg_failure(routerlist,failover,linkdictzero,srlgdict,dem,G):
	destinations=[]

	for pop in routerlist:
		if pop[0:2]=="sr":
			destinations.append(pop)




	wctnode=copy.deepcopy(linkdictzero)
	for key,value in wctnode.items():
		wctnode[key]=[]
	temp=copy.deepcopy(linkdictzero)

	for key in sorted(srlgdict.keys()):
		
		demlistkey=dem.copy()
		print(key)
		linkdict=copy.deepcopy(linkdictzero)
		


	#topology bedoone key o rasm kon link haii ke tahte tasirano az kar bendaz


		#delnode=Router.nodes.get(name=key)
		#for node in delnode.isislink.match():

		for t in srlgdict[key]:
			try:
				
				G.remove_edge(t[0],t[1])
				
			except:
				pass


		
			if t[1] in failover.keys():
				print("fail")

			

				for demand in demlistkey:

					if demand["source"]==t[1]:
						demlistkey.remove(demand)

						for s in failover[t[1]]:
							newdic={}
							newdic["terrafic"]=float(s[1])*demand["terrafic"]/100
							newdic["terrafic-level"]=demand["terrafic-level"]
							newdic["service-class"]=demand["service-class"]
							newdic["destination"]=demand["destination"]
							newdic["source"]=s[0]
							newdic["name"]=demand["name"]
							demlistkey.append(newdic)
					

				




			elif t[1] in destinations:

				
				for demand in demlistkey:


					if demand["destination"]==t[1]:
						demlistkey.remove(demand)


				
				


			
				
				

			elif  t[1] not in failover.keys() and (t[1][0:2]=="px" or t[1][0:2]=="tx"):
				print("ptnofail")

				for demand in demlistkey:
					

					if demand["source"]==t[1]:
						demlistkey.remove(demand)
					


			else:
				pass
				

		print("demlist compelete!")
		print(len(demlistkey))			
	   
		for demand in demlistkey:

			
			try:
				
				results=nx.all_shortest_paths(G,demand["source"],demand["destination"],weight="IGP",method="dijkstra")
				
				allpath=[]
				for result in results:
					
					
					linkspath=[]

				
					for i in list(range(1,len(result))):
						st=result[i-1]
						nd=result[i]
						ln=st+"--"+ nd
							
						linkspath.append(ln)
						
					
					allpath.append(linkspath)
				n=len(allpath)
				for path in allpath:


				
				
				
					for link in path:
						if link in linkdict:
							
							linkdict[link]=linkdict[link]+demand["terrafic"]/n
						else:
							
							linkdict[link]= demand["terrafic"]/n
					  
			except:

					pass         
		





		for key1 in linkdict.keys():
			
			if linkdict[key1]> linknormal[key1]:
				
			
				if temp[key1]<=linkdict[key1]:


					
					if temp[key1]==linkdict[key1] :
						temp[key1]=linkdict[key1]
						wctnode[key1].append(key)
					elif temp[key1]<linkdict[key1]:
						temp[key1]=linkdict[key1]
						wctnode[key1]=[]
						wctnode[key1].append(key)	
						
		G.clear()		
		G=nx.MultiGraph()
		G.add_weighted_edges_from(elist,weight="IGP")		


	return temp,wctnode


def list_of_links():
	


	edgeset=[]
	linkset={}
	with open(inputcsv, 'r+') as file:
		
		linksetdict={}
		file = csv.reader(file, delimiter=',', quotechar='"')
		for row in file:
			print(row)
			if (row[0],row[1]) in edgeset:
				pass
				print("duplicate")
			else:
				
				
				edgeset.append((row[0],row[1]))
				linksetdict["nodea"]=row[0]
				linksetdict["nodeb"]=row[1]
				linksetdict["sitea"]=row[2]
				linksetdict["siteb"]=row[3]
				linksetdict["IGP"]=row[4]
				linksetdict["capacity"]=row[5]
				linkset[row[0]+"--"+row[2]]=linksetdict
					

	return linkset     
def fetchsites():
	siteslist=list(csv.reader(open(sites,"rt")))
	sitesdict=defaultdict(lambda:[])

	sitesset=set()


	for item in siteslist:#injaro dorost konnnnnnnnnnnnnnnnnnnnnnnnnnnn
		k=item[0].split("\t")
		sitesdict[k[1]].append(k[0])
		sitesset.add(k[1])
	return sitesdict,sitesset




def fetchsrlg():
	srlglist=list(csv.reader(open(srlg,"rt")))
	srlgdict=defaultdict(lambda:[])

	segset=set()


	for item in srlglist:#injaro dorost konnnnnnnnnnnnnnnnnnnnnnnnnnnn
		k=item[0].split("\t")
		srlgdict[k[0]].append((k[1],k[3]))
		srlgdict[k[0]].append((k[3],k[1]))
		segset.add(k[0])
	return srlgdict,segset
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






	


def failover(routerlist):
	exendset, exendlist=externalendpoints()


	routerlist=routerlist
	

	
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
			l_index=matches.index(l)
			matches.pop(l_index)
		
			n=len(matches)
			print(n)
			for key,value in dictr.items():
				if key==l:
					for match in matches:

						value.append((match,100/n))








	return dictr,left

 

def demandslist():
	



	#terlist=terlist[4911:38558]
	
	planf=open(plan, 'rt')
	terlist=list(csv.reader(planf))
	terlist=terlist[4944:41110]
	
	upt=len(terlist)
	demandslist=[]
	for line in list(range(0,upt,1)):
		
		newterdic={}
		try:
			pass
			x=terlist[line][0].split("\t")
			y=x[1].split(":")
			newterdic["source"]=y[1]
			newterdic["name"]=y[0]
			newterdic["terrafic"]=float(x[5])
			newterdic["terrafic-level"]=x[4]
			newterdic["service-class"]=x[3]
			newterdic["destination"]=x[2]
			demandslist.append(newterdic)
		except:
			pass
			x=terlist[line][0].split("\t")
			#print(x)

			y=x[1][5:]
			
			newterdic["terrafic"]=float(x[5])
			newterdic["terrafic-level"]=x[4]
			newterdic["service-class"]=x[3]
			newterdic["destination"]=x[2]
			newterdic["source"]=y[:-1]
			newterdic["name"]="Endpoint"
			demandslist.append(newterdic)
	return demandslist




def linkdictzero(elist):
	#returns a dictionary containing links names and their traffic as zero
	linkdictzero={}


	for tuples in elist:
		linkdictzero[tuples[0]+"--"+tuples[1]]=0

	return linkdictzero



def links_and_routers():
	elist=[]
	elist2=[]
	routerlist=[]   
	routerset=set() 
	edgeset=[]
	linkset={}
	with open(inputcsv, 'r+') as file:
		
		
		file = csv.reader(file, delimiter=',', quotechar='"')
		for row in file:
			linksetdict={}
			print(row)
			routerset.add(row[0])
		   
			if (row[0],row[1]) in edgeset:
				pass
				print("duplicate")
			else:
				
				
				edgeset.append((row[0],row[1]))
				linksetdict["nodea"]=row[0]
				linksetdict["nodeb"]=row[1]
				linksetdict["sitea"]=row[2]
				linksetdict["siteb"]=row[3]
				linksetdict["IGP"]=float(row[4])
				linksetdict["bandwidth"]=row[5]
				linksetdict["distance"]=row[6]
				linksetdict["name"]=row[0]+"--"+row[1]
				linkset[row[0]+"--"+row[1]]=linksetdict
				elist.append((row[0],row[1],float(row[4])))
				elist2.append((row[0],row[1],1))
				
					
			routerlist=list(routerset) 
			

	return linkset,routerlist,elist,elist2
		

def normalTraffic(demandslist,linkdict1):
	dem=demandslist
	linkdict=linkdict1
	
	
	for demand in dem:
		
		if demand["terrafic-level"]=="Y18.09":
			try:
				results=nx.all_shortest_paths(G,demand["source"],demand["destination"],weight="IGP",method="dijkstra")
				
				allpath=[]
				for result in results:
					
					
					linkspath=[]

				
					for i in list(range(1,len(result))):
						st=result[i-1]
						nd=result[i]
						ln=st+"--"+ nd
							
						linkspath.append(ln)
						
					
					allpath.append(linkspath)
				n=len(allpath)
				for path in allpath:


				
				
				
					for link in path:
						if link in linkdict:
							
							linkdict[link]=linkdict[link]+demand["terrafic"]/n
						else:
							
							linkdict[link]= demand["terrafic"]/n
					  
			except:

				pass         
	


	return linkdict



# -- Main
if __name__ == '__main__':

	t0 = time.time()

	
	demandslist=demandslist()
	linkset,routerlist,elist,elist2=links_and_routers() 
  
	linkdictzero=linkdictzero(elist)
	#linkset=list_of_links()
	
	failover,left=failover(routerlist)
	srlgdict,segset=fetchsrlg()

	
	linknormal=normalTraffic(demandslist,copy.deepcopy(linkdictzero))

	#print(demandslist[-1])
	
	gaph=np.ndarray([177,177])

	   
	properties=4
  
	graph=np.ndarray([len(routerlist),len(routerlist),properties])
	#for item in linkset:
#	
#	for dic in linkset:
#
#		graph[routerlist.index(dic["nodea"])][routerlist.index(dic["nodeb"])][0]=dic["IGP"]
#		graph[:,:,1]=1
#		graph[routerlist.index(dic["nodea"])][routerlist.index(dic["nodeb"])][2]=dic["distance"]
#		graph[routerlist.index(dic["nodea"])][routerlist.index(dic["nodeb"])][3]=dic["IGP"]



	G=nx.MultiGraph()
	G.add_weighted_edges_from(elist,weight="IGP")
	nx.draw(G) 
	routerlist=nx.nodes(G)


	dem=demandslist
	dem=[x for x in dem if x["terrafic-level"]=="Y18.09"]
	linkdict=copy.deepcopy(linkdictzero) 


	wctdict={}
	linkdictlist=[]
	wctlist=[]
	wctnode=[]
	destinations=[]




		#print(destinations)
		#with open('firsttrystr.txt', 'r') as myfile:
		   # cq=myfile.read().replace('\n', '')

	
		#print(rlwod)


		#preparing demandlist in demlistkey
		
		#session = driver.session()
		#tx = session.begin_transaction()

	temp_node,wct_node=node_failure(routerlist,copy.deepcopy(failover),copy.deepcopy(linkdictzero),copy.deepcopy(dem),G)	
	
	temp_srlg,wct_srlg=srlg_failure(routerlist,copy.deepcopy(failover),copy.deepcopy(linkdictzero),copy.deepcopy(srlgdict),copy.deepcopy(dem),G)


	
	g=copy.deepcopy(linkdictzero)
	for keyf,valuef in temp_node.items():
	    if linknormal[keyf]!=0:
	        g[keyf]=max(temp_node[keyf],temp_srlg[keyf])/linknormal[keyf]


	
	with open("ecmp-all-path-wct-allfailures-test-v1-Y18-09python.csv", 'w') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			myhead=["Node","RemoteNode","IGP","NormTraffic","WCTFailures","WCTraffic"]
			wr.writerow(myhead)
			
			for keyf,valuef in temp_node.items():
				
				mylist=[]
				mylist=keyf.split("--")
				mylist.append(linkset[keyf]["IGP"])
				mylist.append(linknormal[keyf])
				
				
				
				if valuef==0:
					mylist.append("none")
					mylist.append(valuef)
				elif valuef==linknormal[keyf]:
					mylist.append("none")
					mylist.append(0)



				
				else:

					if temp_srlg[keyf]>temp_node[keyf]:

						mylist.append(wct_srlg[keyf])
						mylist.append(temp_srlg[keyf])

					elif temp_srlg[keyf]<temp_node[keyf]: 
						mylist.append(wct_node[keyf])
						mylist.append(temp_node[keyf])
						
					else:
						mylist.append([wct_node[keyf],wct_srlg[keyf]])
						mylist.append(temp_node[keyf])
						


					
					
				wr.writerow(mylist)
