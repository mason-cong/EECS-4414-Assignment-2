import networkx as nx
import igraph as ig
import json

def graph_generators():
        fileName = "dblp_coauthorship.json"
        data = json.load(open(fileName))

        dblp2005 = nx.Graph()
        dblp2006 = nx.Graph()

        for dblpdata in data:
                #we get each piece of data from json 
                auth1 = dblpdata[0]
                auth2 = dblpdata[1]
                year = dblpdata[2]

                if (year == 2005):
                        dblp2005.add_edge(auth1, auth2)

                elif (year == 2006):
                        dblp2006.add_edge(auth1, auth2)

        graph_gcc(dblp2005, "dblp2005")
        #graph_gcc(dblp2006, "dblp2006")

def graph_gcc(G, fileName):
        gcc = max(nx.connected_components(G), key=len)
        gcc_graph = G.subgraph(gcc).copy()

        file = open("graph_data_" + fileName, "w")
        file.write("Number of nodes: %s\n" % gcc_graph.number_of_nodes())
        file.write("Number of edges: %s\n" % gcc_graph.number_of_edges())
        
        file.close()

        #pageRankCalc(gcc_graph, fileName)
        edgeBetweennessCalc(gcc_graph, fileName)

def pageRankCalc(G, fileName):
        #pagerank calculation
        file = open("page_rank" + fileName, "w")
        sorted_pageRank = sorted(nx.pagerank(G).items(), reverse = True)

        for x in range(50):
                file.write(str(sorted_pageRank[x]))
                file.write("\n")

        file.close()

def edgeBetweennessCalc(G, fileName):
        #pagerank calculation
        file = open("edge_betweenness" + fileName, "w")
        sorted_betweenness = sorted(nx.edge_betweenness_centrality(G, k = 10000).items(), reverse = True)

        for x in range(20):
                file.write(str(sorted_betweenness[x]))
                file.write("\n")

        file.close()

#C link prediction
def core_graph(G, fileName):
        degrees = G.degree()
        nodes_deg3 = [n for n,v in dict(degrees).items() if v >= 3]	
        file = open("coregraph_" + fileName, "wb")
        nx.write_edgelist(nodes_deg3, file)
        file.close()

def fof_graph(G):
        fofGraph = nx.Graph()
        file = open("fof_edges_", "wb")

        for x in G.nodes():
	        for y in G.neighbors(x):		#y = friends of x
		        for z in G.neighbors(y):        #z = friends of y
			        if z != y and z != x and z not in G.neighbors(x):
                                        fofGraph.add_edge(x,z)

        nx.write_edgelist(fofGraph, file)
        file.close()


def findTEdges(G2005, G2006):
        edgeGraph = nx.Graph()
        file = open("t_edges_", "wb")

        for x in G2006.edges():
                if not G2005.edges():
                        edgeGraph.add_edge(x)

        nx.write_edgelist(edgeGraph, file)
        file.close()


graph_generators()