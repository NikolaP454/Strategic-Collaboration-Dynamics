import pandas as pd
import networkx as nx


def normalise_author_ids(df: pd.DataFrame) -> None:
    '''
    Normalises the author IDs in the given DataFrame from 0 to N-1.
    '''
    
    authors = set(df['author1']).union(set(df['author2']))
    author_id_map = {}
    
    for i, author in enumerate(authors):
        author_id_map[author] = i
        
    df['author1'] = df['author1'].map(author_id_map)
    df['author2'] = df['author2'].map(author_id_map)
    

def read_graph(data_dir: str):    
    '''
    Extracts the MAG graph from the given data directory.
    
    Parameters:
    ----------
    
    data_dir: str
        Path to the edge list file.
        
    Returns:
    -------
    
    G: nx.Graph
        The MAG graph.
    '''
    
    # Read the edge list
    edge_list_df = pd.read_csv(data_dir, header=None, sep=' ', names=['author1', 'author2', 'strength'])
    
    edge_list_df = edge_list_df[edge_list_df['strength'] >= 5]
    edge_list_df = edge_list_df[edge_list_df['strength'] <= 200]
    
    edge_list_df = edge_list_df.head(100)
    
    print('Edge list read', flush=True)
    
    normalise_author_ids(edge_list_df)
    print('Author IDs normalised', flush=True)
    
    # Create the graph
    G = nx.Graph()
    G.add_edges_from(edge_list_df[['author1', 'author2']].values)
    
    for node in G.nodes():
        for new_node in G.nodes():
            if node == new_node:
                continue
            
            if not G.has_edge(node, new_node):
                G.add_edge(node, new_node)
    
    print('Graph created', flush=True)
    
    # Return the graph
    return G