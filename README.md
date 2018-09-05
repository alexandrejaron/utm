UTM
===

------------------------------------------------------------------------------------

This repository hosts code for the Universal Topology Model. It uses Graph DBMS `neo4j` to build any topology given as an input, and determine the worst-case traffic on any given links between sources and destinations.

Dev Notes
=========

Installation
------------
	virtualenv virtual
	source virtual/bin/activate
	pip install yolk yolk3k
	deactivate                      # required step
	source virtual/bin/activate     # required step
	python setup.py develop
	yolk -l

