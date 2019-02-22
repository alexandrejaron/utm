# -*- coding: utf-8 -*-
#
# License:          This module is released under the terms of the LICENSE file 
#                   contained within this applications INSTALL directory

'''
	Graph database population
'''
import re
import itertools
import copy
import argparse
from argparse import ArgumentParser
import uuid
import csv
import requests
import re
import socket
import time
from collections import defaultdict
import copy
import numpy as np
import matplotlib.pyplot as plt        
import networkx as nx
from networkx.algorithms import all_pairs_dijkstra_path,all_shortest_paths
plan='core-9-i.csv'
source_pattern=re.compile(r'([a-z]+?x+?[0-9]*?\.[a-z0-9]+\.\w+)')
def srlg_failure(routerlist,failover,linkdictzero,srlgdict,dem,IGPlinks,linknormal,metric):
	destinations=[]
	failed_by_seg=defaultdict(lambda:[])
	for pop in routerlist:
		if pop[0:2]=="sr":
			destinations.append(pop)




	wctnode=copy.deepcopy(linkdictzero)
	for key,value in wctnode.items():
		wctnode[key]=[]
	temp=copy.deepcopy(linkdictzero)

	for key in sorted(srlgdict.keys()):
		seg_failed=[]
		G=nx.MultiGraph()
		G.add_weighted_edges_from(IGPlinks,weight=metric)
		
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

					if demand["Source"]==t[1]:
						demlistkey.remove(demand)

						for s in failover[t[1]]:
							newdic={}
						newdic["Traffic"]=float(s[1])*float(demand["Traffic"])/100
						newdic["TrafficLevel"]=demand["TrafficLevel"]
						newdic["ServiceClass"]=demand["ServiceClass"]
						newdic["Destination"]=demand["Destination"]
						newdic["Source"]=s[0]
						newdic["Name"]=demand["Name"]
						demlistkey.append(newdic)
					

				




			elif t[1] in destinations:

				
				for demand in demlistkey:


					if demand["Destination"]==t[1]:
						demlistkey.remove(demand)
						seg_failed.append(demand)


				
				


			
				
				

			elif  t[1] not in failover.keys() and (t[1][0:2]=="px" or t[1][0:2]=="tx"):
				print("ptnofail")

				for demand in demlistkey:
					

					if demand["Source"]==t[1]:
						demlistkey.remove(demand)
						seg_failed.append(demand)
					


			else:
				pass
				
	    
		print("demlist compelete!")
		print(len(demlistkey))			
	   
		for demand in demlistkey:

		
			try:
		
#		print(demand)
#		if demand["terrafic-level"]=="Y18.09":
			
#				b=re.search(source_pattern,demand["Source"])
#
#				Source=b.group(0)
				
				
	#			print(Source)
	#			print(demand["Destination"])
				results=nx.all_shortest_paths(G,demand["Source"],demand["Destination"],weight=metric,method="dijkstra")
				
				allpath=[]
				for result in results:
	#				print(result)
					
					linkspath=[]

					for i in list(range(1,len(result))):
						st=result[i-1]
						nd=result[i]
						ln=st+"--"+ nd
							
						linkspath.append(ln)
						
					
					allpath.append(linkspath)
	#				print(allpath)
				
				n=min(len(allpath),num)
	#			print(n)
				for path in allpath[:n]:
				
					for link in path:
						if link in linkdict:
							
							linkdict[link]=linkdict[link]+int(demand["Traffic"])/n
						else:
							
							linkdict[link]= int(demand["Traffic"])/n
					  
			except:
			
				pass
				
				seg_failed.append(demand)
	




		failed_by_seg[key]=seg_failed





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
						
				
			


	return temp,wctnode,failed_by_seg


def node_failure(routerlist,failover,linkdictzero,dem,IGPlink,linknormal,metric):
	

		
	wctnode=copy.deepcopy(linkdictzero)
	for key,value in wctnode.items():
		wctnode[key]=[]
	temp=copy.deepcopy(linkdictzero)
	failed_by_node=defaultdict(lambda:[])

	for key in sorted(routerlist):
		
		G=nx.MultiGraph()
		G.add_weighted_edges_from(IGPlinks,weight=metric)
		print(key)
		demlistkey=[]
		node_failed=[]
		linkdict=copy.deepcopy(linkdictzero)


		


		if key[0:2]=="ar" or key[0:2]=="er":

			print("cdn or er")
			for demand in dem:
				if demand["Source"] in list(G[key]):
					pass
					node_failed.append(demand)
					
					
				else:
					demlistkey.append(demand)




			for node in G[key]:
				
					#print(node)
				
				
					if node in failover.keys():
						for demand in dem:
			#print("fail")

		

						
			
							if demand["Source"]==node:
			
								for s in failover[node]:
									newdic={}
									newdic["Traffic"]=float(s[1])*float(demand["Traffic"])/100
									newdic["TrafficLevel"]=demand["TrafficLevel"]
									newdic["ServiceClass"]=demand["ServiceClass"]
									newdic["Destination"]=demand["Destination"]
									newdic["Source"]=s[0]
									newdic["Name"]=demand["Name"]
									demlistkey.append(newdic)
#									node_failed.remove(demand)
						
				

		elif key in failover.keys():
			print("fail")

		

			for demand in dem:

				if demand["Source"]==key:

					for s in failover[key]:
						newdic={}
						newdic["Traffic"]=float(s[1])*float(demand["Traffic"])/100
						newdic["TrafficLevel"]=demand["TrafficLevel"]
						newdic["ServiceClass"]=demand["ServiceClass"]
						newdic["Destination"]=demand["Destination"]
						newdic["Source"]=s[0]
						newdic["Name"]=demand["Name"]
						demlistkey.append(newdic)
				else:
					demlistkey.append(demand)

			print("dem compelete!")




		elif key in [d for d in routerlist if d[0:2]=="sr"]:
			node_failed=[d for d in dem if d["Destination"]==key]
			print("dest")


		
			
			print("dem compelete!")

		elif  key not in failover.keys() and (key[0:2]=="px" or key[0:2]=="tx"):
			print("ptnofail")

			for demand in dem:
				

				if demand["Source"]==key:
					pass
					node_failed.append(demand)
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
		
#		print(demand)
#		if demand["terrafic-level"]=="Y18.09":
			
#				b=re.search(source_pattern,demand["Source"])
#
#				Source=b.group(0)
				
				
	#			print(Source)
	#			print(demand["Destination"])
				results=nx.all_shortest_paths(G,demand["Source"],demand["Destination"],weight=metric,method="dijkstra")
				
				allpath=[]
				for result in results:
	#				print(result)
					
					linkspath=[]

					for i in list(range(1,len(result))):
						st=result[i-1]
						nd=result[i]
						ln=st+"--"+ nd
							
						linkspath.append(ln)
						
					
					allpath.append(linkspath)
	#				print(allpath)
				
				n=min(len(allpath),num)
	#			print(n)
				for path in allpath[:n]:
				
					for link in path:
						if link in linkdict:
							
							linkdict[link]=linkdict[link]+int(demand["Traffic"])/n
						else:
							
							linkdict[link]= int(demand["Traffic"])/n
					  
			except:
			
				pass
				
				node_failed.append(demand)
	




		failed_by_node[key]=node_failed
		
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
						
				
#		G=nx.MultiGraph()
#		G.add_weighted_edges_from(IGPlink,weight=metric)		
		
	

	return temp,wctnode,failed_by_node





def Segment(tables):
	keys=tables['<SRLGCircuits>'][0].split('\t')
	values=tables['<SRLGCircuits>'][1:]
	t1=[item.split("\t") for item in values ]
	srlgdict=defaultdict(lambda:[])
	h=[srlgdict[t[0]].extend([(t[3],t[1]),(t[1],t[3])]) for t in t1]
	return srlgdict


def Failover(routerlist,tables):
	keys=tables['<ExternalEndpointMembers>'][0].split('\t')
	values=tables['<ExternalEndpointMembers>'][1:]
	t1=[item.split("\t") for item in values ]

	dict1=dict([(t[0][2:],[]) for t in t1])
	h=[dict1[t[0][2:]].append((t[1],float(t[3]))) for t in t1 if t[2]=="2"]
	dict2=dict([(t,[]) for t in routerlist if t[0:2]=="cx" ])
	def matches(l,routerlist):
		return [x for x in routerlist if x[0:2]=="cx" and x.split(".")[1]==l.split(".")[1]]
	for l in dict2.keys():
		match=matches(l,routerlist)
		match.pop(match.index(l))
		hh=[dict2[l].append((m,100/len(match))) for m in match]
		dict1.update(dict2)
	return dict1



def linkdictzero(elist):
	#returns a dictionary containing links names and their traffic as zero
	linkdictzero={}


	for tuples in elist:
		linkdictzero[tuples[0]+"--"+tuples[1]]=0.0

	return linkdictzero

def Interfaces(tables):
	keys=tables['<Interfaces>'][0].split('\t')
	values=tables['<Interfaces>'][1:]
	t=[item.split("\t") for item in values ]
	IGPlinks=[(item[0],item[1][3:],float(item[2])) for item in t]
	routerlist=list({item[0] for item in t})
	Hoplinks=[(item[0],item[1][3:],1) for item in t]
	
	return routerlist,Hoplinks,IGPlinks	
	
	
def get_individual_tables(selftxtfile):
	table_name_pattern = re.compile(r'(<)+?[A-Za-z]+(>)+?$')
	comment_pattern = re.compile(r'\s*#\s*')
	with open(selftxtfile, 'r') as txtfile:
		
		
		
		tables_to_read=[]
		tables = {}
		table_being_read = ''
		READ_TABLE = False
		j=[]
		for line in txtfile:
			#print(line)
			
			# a comment line is encountered so ignore it
			if comment_pattern.match(line):
				continue
			# new table encountered! set the reading flag to true and initialise the table
			if table_name_pattern.match(line):
				#catch the matched pattern
				m=table_name_pattern.match(line)
				
				print(line.split())
				
				
				
				tables_to_read.append(m.group(0))
				
				#print 'found table', line
				if m.group(0) in tables_to_read:
					print ('reading table', line)
					READ_TABLE = True
					table_being_read = m.group(0)
					tables[table_being_read] = []
					continue
				
			if line=='\n':
				READ_TABLE=False
			if READ_TABLE:
				tables[table_being_read].append(line.rstrip())
			# reached the end of the table so stop accumulating data in it

		
		return tables,tables_to_read
def DemandsTraffic(tables):
	keys=tables['<DemandTraffic>'][0].split('\t')
	values=tables['<DemandTraffic>'][1:]
	t=[item.split("\t") for item in values ]
	demandslist=[dict(zip(keys,item)) for item in t]
	def source_update(dict1):
	
	
		for key,values in dict1.items():
			try:
		
		
				source_pattern=re.compile(r'([a-z]+?x+?[0-9]*?\.[a-z0-9]+\.\w+)')
		
				b=re.search(source_pattern,dict1["Source"])
		
				dict1["Source"]=b.group(0)
		    
			except:
				pass
		return dict1

	demandslist=[source_update(dict1) for dict1 in demandslist]
    
	return demandslist

def normalTraffic(G,demandslist,linkdict1,metric,num):
	dem=demandslist
	linkdict=linkdict1
	G=G
	metric=metric
	cnt=0
	failed=[]
	for demand in dem:
		try:
		
#		print(demand)
#		if demand["terrafic-level"]=="Y18.09":
			
#			b=re.search(source_pattern,demand["Source"])
#
#			Source=b.group(0)
#			
#			cnt=cnt+1
#			print(Source)
#			print(demand["Destination"])
			results=nx.all_shortest_paths(G,demand["Source"],demand["Destination"],weight=metric,method="dijkstra")
			
			allpath=[]
			for result in results:
#				print(result)
				
				linkspath=[]

				for i in list(range(1,len(result))):
					st=result[i-1]
					nd=result[i]
					ln=st+"--"+ nd
						
					linkspath.append(ln)
					
				
				allpath.append(linkspath)
#				print(allpath)
			
			n=min(len(allpath),num)
#			print(n)
			for path in allpath[:n]:
			
				for link in path:
					if link in linkdict:
						
						linkdict[link]=linkdict[link]+int(demand["Traffic"])/n
					else:
						
						linkdict[link]= int(demand["Traffic"])/n
				  
		except:
			
			pass
			failed.append(demand)

					 
	return linkdict,failed

# -- Main
if __name__ == '__main__':

	t0 = time.time()
	
	
	
	#input plan file
	filename = 'core-9-i.txt'
	#extract tables from text file
	tables,tables_to_read = get_individual_tables(filename)
	#get list of demands to calculate the traffic
	demandslist=DemandsTraffic(tables)
	#get list of router, links, their IGP metrics to creat the network 
	routerlist,Hoplinks,IGPlinks=Interfaces(tables) 
	#TrafficLevels
	TrafficLevels=tables['<TrafficLevels>'][1:]
	parser = ArgumentParser()
	parser.add_argument('Metric',help='Metric for shortest path calculation',type=str)
	parser.add_argument('Period',help='Perio in which you wish to calculate WCT with format:Yxx.xx',type=str)
	parser.add_argument('Num',help='Number of shortest path for ECMP',type=int)
	args=parser.parse_args()
	metric=args.Metric
	period=args.Period
	num=args.Num
#	linkdictzero=linkdictzero(elist)
	failover=Failover(routerlist,tables)
	srlgdict=Segment(tables)
#	linknormal=normalTraffic(demandslist,copy.deepcopy(linkdictzero))
#	properties=4
#
	G=nx.MultiGraph()
	G.add_weighted_edges_from(IGPlinks,weight=metric)
#	G.add_weighted_edges_from(IGPlinks,weight="IGP")
#	nx.draw(G) 
#	routerlist=nx.nodes(G)
#	dem=demandslist
	dem=[x for x in demandslist if x["TrafficLevel"]==period]
	linkdictzero=linkdictzero(IGPlinks)
	linknormal,failed=normalTraffic(G,dem,copy.deepcopy(linkdictzero),metric,num)
	
	temp_node,wct_node,failed_by_node=node_failure(routerlist,copy.deepcopy(failover),copy.deepcopy(linkdictzero),copy.deepcopy(dem),IGPlinks,linknormal,metric)

	temp_srlg,wct_srlg,failed_by_srlg=srlg_failure(routerlist,copy.deepcopy(failover),copy.deepcopy(linkdictzero),copy.deepcopy(srlgdict),copy.deepcopy(dem),IGPlinks,linknormal,metric)	
#Writing output file


    
	g=copy.deepcopy(linkdictzero)
	for keyf,valuef in temp_node.items():
		if linknormal[keyf]!=0:
		    
			 g[keyf]=max(temp_node[keyf],temp_srlg[keyf])/linknormal[keyf]
	    
	    
	    
	with open("ecmp-all-path-wct-allfailures-pythonversion.csv", 'w') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		myhead=["Node","RemoteNode","IGP","NormTraffic","WCTFailures","WCTraffic"]
		wr.writerow(myhead)
			
		for keyf,valuef in temp_node.items():
				
			mylist=[]
			mylist=keyf.split("--")
	   
			mylist.append([t[2] for t in IGPlinks if t[0]==mylist[0] and t[1]==mylist[1] ][0])
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






