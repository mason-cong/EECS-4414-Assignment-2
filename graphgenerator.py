import networkx as nx
import igraph as ig
import itertools
import json
import random

#create graphs for dblp2005 and dblp2006
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
        
        #graph_gcc(dblp2005, "dblp2005")
        #graph_gcc(dblp2006, "dblp2006") #comment this out when doing fof calculation

        sampled_edges = random.sample(list(dblp2005.nodes()), 10000)
        sampled_graph2 = dblp2005.subgraph(sampled_edges)

        #part d calculation
        detectCommunities2(sampled_graph2)

#giant connected component of graph
def graph_gcc(G, fileName):
        gcc = max(nx.connected_components(G), key=len)
        gcc_graph = G.subgraph(gcc).copy()

        file = open("graph_data_" + fileName, "w")
        file.write("Number of nodes: %s\n" % gcc_graph.number_of_nodes())
        file.write("Number of edges: %s\n" % gcc_graph.number_of_edges())
        
        file.close()

        #part b calculations, can comment out if not needed to calculate
        pageRankCalc(gcc_graph, fileName)
        edgeBetweennessCalc(gcc_graph, fileName)

        #part c calculation, used for dblp2005
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
        file = open("edge_betweenness" + fileName, "w")
        #use k size 10000 to reduce size of nodes, and reduce computation time
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
                if not G2005.has_edge(*x):
                        edgeGraph.add_edge(*x)

        nx.write_edgelist(edgeGraph, file, delimiter="*")
        file.close()


#C. V. predicted edges
def random_edge():
        file = open("fof_edges_dblp2005", "rb")
        G = nx.read_edgelist(file, delimiter="*")
        file.close()

        randG = nx.Graph()
        edges = list(G.edges())

        for x in range(252968):
                cur_edge = random.choice(edges)
                randG.add_edge(*cur_edge)

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
                predictG.add_edge(*x, score=len(nx.common_neighbors(G2005, *x)))
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

        write_file = open("adamic_adar_edgelist", "wb")
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
        k_values = sorted(edges.items(), key = lambda x:-x[1])[:k]

        predicted = 0
        for val in k_values:
                if T.has_edge(*val[0]):
                                predicted += 1

        write_file = open("k_" + fileName, "a+")
        write_file.write("K Value: %s, Predicted Value: %s\n" % (k, (predicted/k)))
        write_file.close()

#part d
def detectCommunities2(G):
        communitySizes = []
        k = 10 #number of clusters
        g = ig.Graph.from_networkx(G)
        data = g.community_edge_betweenness(directed=False, weights=None)
        clusterData = data.as_clustering()
        clusterList = list(clusterData)
        for clusters in clusterList:
                communitySizes.append(len(clusters))
        saveCommunities(sorted(communitySizes, reverse=True))

def saveCommunities(communityLengths):
        file = open("dblp_communities2.txt", "w")
        file.write(str(communityLengths))
        file.close()
        
graph_generators()

file = open("coregraph_dblp2005", "rb")
G2005 = nx.read_edgelist(file, delimiter="*")
file.close()

file = open("coregraph_dblp2006", "rb")
G2006 = nx.read_edgelist(file, delimiter="*")
file.close()

findTEdges(G2005, G2006)
random_edge()
common_neighbor_edge()
jaccard_edge()		
pref_attach_edge()
adamic_edge()

#random predict
precision("random_edgelist_dblp2005", k = 10)
precision("random_edgelist_dblp2005", k = 20)
precision("random_edgelist_dblp2005", k = 50)
precision("random_edgelist_dblp2005", k = 100)
precision("random_edgelist_dblp2005", k = 252968)

#common neighbor
precision("common_neighbors_edgelist", k = 10)
precision("common_neighbors_edgelist", k = 20)
precision("common_neighbors_edgelist", k = 50)
precision("common_neighbors_edgelist", k = 100)
precision("common_neighbors_edgelist", k = 252968)

#jaccard
precision("jaccard_coefficient_edgelist", k = 10)
precision("jaccard_coefficient_edgelist", k = 20)
precision("jaccard_coefficient_edgelist", k = 50)
precision("jaccard_coefficient_edgelist", k = 100)
precision("jaccard_coefficient_edgelist", k = 252968)

#pref attach
precision("pref_attach_edgelist", k = 10)
precision("pref_attach_edgelist", k = 20)
precision("pref_attach_edgelist", k = 50)
precision("pref_attach_edgelist", k = 100)
precision("pref_attach_edgelist", k = 252968)

#adamic adar
precision("adamic_adar_edgelist", k = 10)
precision("adamic_adar_edgelist", k = 20)
precision("adamic_adar_edgelist", k = 50)
precision("adamic_adar_edgelist", k = 100)
precision("adamic_adar_edgelist", k = 252968)