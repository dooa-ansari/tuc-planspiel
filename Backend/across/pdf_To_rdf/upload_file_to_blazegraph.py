import requests
from rdflib import Graph
import os
from pymantic import sparql
import urllib.request as urllib2
import urllib.parse as parse

def upload_file_to_blazegraph(directory, file, isFile):
    if not isFile:
        # filelist = [ f for f in os.listdir(directory) if f.endswith(".rdf") ]
        graph = Graph()
        headers = {'Content-Type': 'application/rdf+xml'}
        for root, dirs, files in os.walk(os.path.abspath(directory)):
         for file in files:
          data1 = open(os.path.join(root, file),'r', encoding='utf-8').read()
          graph.parse(os.path.join(root, file),'r', encoding='utf-8')
          print(data1)
        #   datae = parse.urlencode(data1).encode("utf-8")
        #   req = urllib2.Request(url="http://13.51.109.79/blazegraph/namespace/kb/sparql", 
        #               data=datae, 
        #               headers={'Content-Type': 'application/xml'})
        #   urllib2.urlopen(req)
        #   result = requests.post("http://13.51.109.79/blazegraph/namespace/kb/sparql", files=data1)
        #   print(result)
        #   server = sparql.SPARQLServer('http://13.51.109.79/blazegraph/bigdata/sparql')
        #   server.update('load <http://bioimages.vanderbilt.edu/baskauf/12255>')
        # xml = """<?xml version='1.0' encoding='utf-8'?>
        #       <a>б</a>"""
        data_xml = graph.serialize(format='xml')
        # print(data_xml)
        result = requests.post("http://13.51.109.79/blazegraph/namespace/kb/sparql", data=data_xml, headers={'Content-Type': 'application/xml'})
        print(result.content)
        
    else:
       graph = Graph()
       graph.parse(file) 
       data_xml = graph.serialize(format='xml')
       payload = data_xml
       result = requests.post("http://13.51.109.79/blazegraph/namespace/kb/sparql", payload)


upload_file_to_blazegraph("/Users/dooaansari/Desktop/Across/web-wizards/Backend/across/uploads", "", False)

    