import sys
import networkx as nx
from itertools import combinations
import time

def generate_weakly_connected_graphs(n):
    """
    Function generates all possible directed graphs with n vertices, then filters only those that are weakly connected.
    It then removes isomorphic duplicates to keep only unique graphs. 
    """
    graphs = []
    
    # Generate all possible directed edges between n vertices
    all_edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    
    # Try all possible subsets of edges
    for r in range(1, len(all_edges) + 1):
        for edge_subset in combinations(all_edges, r):
            G = nx.DiGraph()
            G.add_nodes_from(range(n))
            G.add_edges_from(edge_subset)
            
            # Check if the graph is weakly connected
            if nx.is_weakly_connected(G):
                # Check if this graph is isomorphic to any previously found graph
                # This prevents us from counting the same graph multiple times
                is_new = True
                for existing in graphs:
                    if nx.is_isomorphic(G, existing):
                        is_new = False
                        break
                
                if is_new:
                    graphs.append(G)
    
    return graphs

def write_graphs_to_file(graphs, n, filename):
    """
    Write the generated graphs to a file in the specified format.
    
    """
    with open(filename, "w") as f:
        f.write(f"n={n}\n")
        f.write(f"count={len(graphs)}\n")
        
        for idx, G in enumerate(graphs, 1):
            f.write(f"#{idx}\n")
            
            edges = sorted(G.edges())
            
            for u, v in edges:
                f.write(f"{u+1} {v+1}\n")

def print_graphs_to_console(graphs, n):
    """
    Print the generated graphs to console.
    """
    print(f"\nn={n}")
    print(f"count={len(graphs)}")
    
    for idx, G in enumerate(graphs, 1):
        print(f"#{idx}")
        edges = sorted(G.edges())
        for u, v in edges:
            print(f"{u+1} {v+1}")

def main():
    # Record start time
    start_time = time.time()
    
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = int(input("Enter n: "))
    
    print(f"Generating all weakly connected graphs with {n} vertices...")
    
    # Time the graph generation
    generation_start = time.time()
    graphs = generate_weakly_connected_graphs(n)
    generation_time = time.time() - generation_start
    
    output_filename = f"n={n}.txt"
    
    write_graphs_to_file(graphs, n, output_filename)
    
    print(f"Output written to {output_filename}")
    
    # Also print results to console
    print_graphs_to_console(graphs, n)
    
    
    print(f"Graph generation time: {generation_time:.4f} seconds")


if __name__ == "__main__":
    main()
