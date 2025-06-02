import sys
from itertools import combinations, permutations
from collections import defaultdict

def read_input():
    """
    Read n and the graph edges from input.
    """
    n = int(input())
    edges = []
    vertices = set()
    
    for line in sys.stdin:
        line = line.strip()
        if line:
            u, v = map(int, line.split())
            edges.append((u, v))
            vertices.add(u)
            vertices.add(v)
    
    return n, edges, sorted(list(vertices))

def get_subgraph_edges(vertex_subset, edges):
    """
    Get all edges that exist within a subset of vertices.
    """
    vertex_set = set(vertex_subset)
    subgraph_edges = []
    
    for u, v in edges:
        if u in vertex_set and v in vertex_set:
            subgraph_edges.append((u, v))
    
    return subgraph_edges

def graph_to_canonical(n_vertices, edge_list):
    """
    Convert a graph to its canonical form for isomorphism checking.
    """
    # Create adjacency matrix
    adj = [[0] * n_vertices for _ in range(n_vertices)]
    for u, v in edge_list:
        adj[u][v] = 1
    
    # Find the lexicographically smallest adjacency matrix
    best_adj = None
    
    for perm in permutations(range(n_vertices)):
        # Create permuted adjacency matrix
        perm_adj = [[0] * n_vertices for _ in range(n_vertices)]
        for i in range(n_vertices):
            for j in range(n_vertices):
                perm_adj[i][j] = adj[perm[i]][perm[j]]
        
        # Convert to tuple for comparison
        perm_tuple = tuple(tuple(row) for row in perm_adj)
        
        if best_adj is None or perm_tuple < best_adj:
            best_adj = perm_tuple
    
    return best_adj

def subgraph_to_canonical(vertices, edges):
    """
    Convert a subgraph with arbitrary vertex labels to canonical form.
    """
    # Map vertices to 0-based indices
    vertex_list = sorted(vertices)
    vertex_map = {v: i for i, v in enumerate(vertex_list)}
    
    # Convert edges to 0-based
    edge_list = [(vertex_map[u], vertex_map[v]) for u, v in edges]
    
    return graph_to_canonical(len(vertices), edge_list)

def generate_all_unique_motifs(n):
    """
    Generate all unique directed graph motifs on n vertices.
    Creates all possible non-isomorphic directed graphs with n vertices
    Each graph represents a different motif pattern
    Includes graphs with self-loops and all edge combinations
    """
    unique_motifs = {}
    
    # Generate all possible adjacency matrices
    for mask in range(2 ** (n * n)):
        # Create edge list from mask
        edge_list = []
        bit = 0
        for i in range(n):
            for j in range(n):
                if mask & (1 << bit):
                    edge_list.append((i, j))
                bit += 1
        
        # Get canonical form
        canonical = graph_to_canonical(n, edge_list)
        
        # Store first occurrence of each canonical form
        if canonical not in unique_motifs:
            unique_motifs[canonical] = edge_list
    
    # Sort by canonical form
    sorted_motifs = sorted(unique_motifs.items())
    return sorted_motifs

def write_motifs_to_file(all_motifs, motif_counts, n, filename):
    """
    Write motifs and their counts to a file.
    """
    with open(filename, "w") as f:
        f.write(f"Motif size: n={n}\n")
        f.write(f"Total unique motifs: {len(all_motifs)}\n\n")
        
        for idx, (canonical_form, edge_list) in enumerate(all_motifs, 1):
            f.write(f"#{idx}\n")
            
            # Write edges
            for u, v in edge_list:
                f.write(f"{u+1} {v+1}\n")
            
            # Write count
            count = motif_counts.get(canonical_form, 0)
            f.write(f"count={count}\n")
            
            if idx < len(all_motifs):
                f.write("\n")

def print_and_save_results(all_motifs, motif_counts, n):
    """
    Print results to console and save to file.
    """
    # Generate filename based on motif size
    output_filename = f"motifs_n{n}.txt"
    
    # Write to file
    write_motifs_to_file(all_motifs, motif_counts, n, output_filename)
    print(f"Output saved to {output_filename}")
    
    # Also print to console
    print(f"\nMotif size: n={n}")
    print(f"Total unique motifs: {len(all_motifs)}\n")
    
    for idx, (canonical_form, edge_list) in enumerate(all_motifs, 1):
        print(f"#{idx}")
        
        # Output edges
        for u, v in edge_list:
            print(f"{u+1} {v+1}")
        
        # Output count
        count = motif_counts.get(canonical_form, 0)
        print(f"count={count}")
        
        if idx < len(all_motifs):
            print()

def main():
    # Read input
    n, edges, vertices = read_input()
    
    # Generate all unique motifs for graphs of size n
    all_motifs = generate_all_unique_motifs(n)
    
    # Count occurrences of each motif in the input graph
    motif_counts = defaultdict(int)
    
    if n <= len(vertices):
        # Find all subgraphs of size n
        for vertex_subset in combinations(vertices, n):
            # Get edges in this subgraph
            subgraph_edges = get_subgraph_edges(vertex_subset, edges)
            
            # Convert to canonical form
            canonical = subgraph_to_canonical(vertex_subset, subgraph_edges)
            motif_counts[canonical] += 1
    
    # Output results to both console and file
    print_and_save_results(all_motifs, motif_counts, n)

if __name__ == "__main__":
    main()
