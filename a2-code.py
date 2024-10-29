#part a)
import json
import gzip
import networkx as nx

# Load the dataset
def load_data(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Filter data for the year 2005
def filter_data_for_year(data, year):
    return [(entry[0], entry[1]) for entry in data if entry[2] == year]

# Create a weighted graph for co-authorship
def create_weighted_graph(coauthorships):
    G = nx.Graph()
    for author1, author2 in coauthorships:
        if G.has_edge(author1, author2):
            G[author1][author2]['weight'] += 1
        else:
            G.add_edge(author1, author2, weight=1)
    return G

# Get the giant connected component
def get_giant_connected_component(G):
    largest_cc = max(nx.connected_components(G), key=len)
    return G.subgraph(largest_cc).copy()

# Main function
def main():
    file_path = 'dblp_coauthorship.json.gz'
    
    # Load the dataset
    data = load_data(file_path)

    # Filter for 2005
    coauthorships_2005 = filter_data_for_year(data, 2005)

    # Create the weighted graph
    G2005w = create_weighted_graph(coauthorships_2005)

    # Extract the giant connected component
    giant_cc = get_giant_connected_component(G2005w)

    # Report the number of nodes and edges
    num_nodes = giant_cc.number_of_nodes()
    num_edges = giant_cc.number_of_edges()

    print(f"dblp2005w graph: #nodes = {num_nodes}, #edges = {num_edges}")

if __name__ == "__main__":
    main()

#part b)
import operator

# Function to calculate and report top PageRank nodes
def top_pagerank_nodes(G, top_n=50):
    pagerank_scores = nx.pagerank(G)
    top_nodes = sorted(pagerank_scores.items(), key=operator.itemgetter(1), reverse=True)[:top_n]
    print("Top 50 authors by PageRank:")
    for author, score in top_nodes:
        print(f"Author: {author}, PageRank Score: {score}")

# Function to calculate and report top edge betweenness
def top_edge_betweenness(G, top_n=20):
    edge_betweenness = nx.edge_betweenness_centrality(G)
    top_edges = sorted(edge_betweenness.items(), key=operator.itemgetter(1), reverse=True)[:top_n]
    print("Top 20 edges by Edge Betweenness:")
    for edge, score in top_edges:
        print(f"Edge: {edge}, Betweenness Score: {score}")

# Example usage on giant connected component
def analyze_graph(G):
    # Top 50 nodes by PageRank
    top_pagerank_nodes(G, top_n=50)
    
    # Top 20 edges by edge betweenness
    top_edge_betweenness(G, top_n=20)
