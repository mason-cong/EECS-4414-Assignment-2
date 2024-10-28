import networkx as nx
import igraph as ig
import json
import random

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
        #graph_gcc(dblp2006, "dblp2006") #comment this out when doing fof calculation


def graph_gcc(G, fileName):
        gcc = max(nx.connected_components(G), key=len)
        gcc_graph = G.subgraph(gcc).copy()

        file = open("graph_data_" + fileName, "w")
        file.write("Number of nodes: %s\n" % gcc_graph.number_of_nodes())
        file.write("Number of edges: %s\n" % gcc_graph.number_of_edges())
        
        file.close()

        #pageRankCalc(gcc_graph, fileName)
        #edgeBetweennessCalc(gcc_graph, fileName)
        core_graph(gcc_graph, fileName)

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

        graph_deg3 = G.subgraph(nodes_deg3)
        file = open("coregraph_" + fileName, "wb")
        nx.write_edgelist(graph_deg3, file, delimiter="*")
        file.close()

        fof_graph(graph_deg3)

def fof_graph(G):
        fofGraph = nx.Graph()
        file = open("fof_edges_dblp2005", "wb")

        for x in G.nodes():
	        for y in G.neighbors(x):		#y = friends of x
		        for z in G.neighbors(y):        #z = friends of y
			        if z != x and z != y and z not in G.neighbors(x):
                                        fofGraph.add_edge(x,z)

        nx.write_edgelist(fofGraph, file, delimiter="*")
        file.close()


def findTEdges(G2005, G2006):
        edgeGraph = nx.Graph()
        file = open("t_edges_", "wb")
        
        for x in G2006.edges():
                if not G2005.edges(*x):
                        edgeGraph.add_edge(*x)

        nx.write_edgelist(edgeGraph, file, delimiter="*")
        file.close()


#C. V. predicted edges
def random_edge():
        file = open("fof_edges_dblp2005", "rb")
        G = nx.read_edgelist(file)
        file.close()

        randG = nx.Graph()
        edges = list(G.edges())

        for x in range(252968):
                randG.add_edge(random.choice(edges))
        write_file = open("random_edgelist_dblp2005", "wb")
        nx.write_edgelist(randG, write_file, delimiter="*")
        write_file.close()

def common_neighbor_edge():
        file = open("coregraph_dblp2005", "rb")
        G2005 = nx.read_edgelist(file, delimiter="*")
        file.close()

        file = open("fof_edges_dblp2005", "rb")
        fof = nx.read_edgelist(file, delimiter="*")
        file.close()

        predictG = nx.Graph()
        for x in fof.edges():
                predictG.add_edge(x, score = len(nx.common_neighbors(x, G2005)))
        write_file = open("common_neighbors_edgelist", "wb")
        nx.write_edgelist(predictG, write_file, delimiter="*")
        write_file.close()

def jaccard_edge():
        file = open("coregraph_dblp2005", "rb")
        G2005 = nx.read_edgelist(file, delimiter="*")
        file.close()

        file = open("fof_edges_dblp2005", "rb")
        fof = nx.read_edgelist(file, delimiter="*")
        file.close()

        predictJaccard = nx.Graph()
        prediction = nx.jaccard_coefficient(G2005, ebunch = fof.edges())
        for u, v, p in prediction:
                predictJaccard.add_edge(u, v, score = p)

        write_file = open("jaccard_coefficient_edgelist", "wb")
        nx.write_edgelist(predictJaccard, write_file, delimiter="*")
        write_file.close()

def pref_attach_edge():
        file = open("coregraph_dblp2005", "rb")
        G2005 = nx.read_edgelist(file, delimiter="*")
        file.close()

        file = open("fof_edges_dblp2005", "rb")
        fof = nx.read_edgelist(file, delimiter="*")
        file.close()

        predictPrefAttach = nx.Graph()
        prediction = nx.preferential_attachment(G2005, ebunch = fof.edges())
        for u, v, p in prediction:
                predictPrefAttach.add_edge(u, v, score = p)

        write_file = open("pref_attach_edgelist", "wb")
        nx.write_edgelist(predictPrefAttach, write_file, delimiter="*")
        write_file.close()

def adamic_edge():
        file = open("coregraph_dblp2005", "rb")
        G2005 = nx.read_edgelist(file, delimiter="*")
        file.close()

        file = open("fof_edges_dblp2005", "rb")
        fof = nx.read_edgelist(file, delimiter="*")
        file.close()

        predictAdamic = nx.Graph()
        prediction = nx.adamic_adar_index(G2005, ebunch = fof.edges())
        for u, v, p in prediction:
                predictAdamic.add_edge(u, v, score = p)

        write_file = open("pref_attach_edgelist", "wb")
        nx.write_edgelist(predictAdamic, write_file, delimiter="*")
        write_file.close()

def precision(fileName, k):
        file = open(fileName, "rb")
        G = nx.read_edgelist(file, delimiter="*")
        file.close()

        file = open("t_edges_", "rb")
        T = nx.read_edgelist(file, delimiter="*")
        file.close()

        edges = nx.get_edge_attributes(G, "score")
        k_values = sorted(edges.items(), key = lambda x:-x[1][:k])

        predicted = 0
        for val in k_values:
                if T.has_edge(val[0]):
                                predicted += 1

        write_file = open("k_" + fileName, "ab+")
        print ("K Value: %s, Predicted Value: %s", k, predicted)
        write_file.close()

#graph_generators()
print(1)
file = open("coregraph_dblp2005", "rb")
G2005 = nx.read_edgelist(file, delimiter="*")
file.close()
print(1)
file = open("coregraph_dblp2006", "rb")
G2006 = nx.read_edgelist(file, delimiter="*")
file.close()
print(1)
findTEdges(G2005, G2006)
print(1)
#common_neighbor_edge()