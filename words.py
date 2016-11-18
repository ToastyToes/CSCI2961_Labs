import networkx as nx
from itertools import permutations

#-------------------------------------------------------------------
#   The Words/Ladder graph of Section 1.1
#-------------------------------------------------------------------
def generate_graph(words):
    from string import ascii_lowercase as lowercase
    G = nx.Graph(name="words")
    lookup = dict((c,lowercase.index(c)) for c in lowercase)
    def edit_distance_one(word):
    	perms = [''.join(p) for p in permutations(word)]
    	for perm in perms:
	        for i in range(len(perm)):
	            left, c, right = perm[0:i], perm[i], perm[i+1:]
	            j = lookup[c] # lowercase.index(c)
	            for cc in lowercase[j+1:]:
					yield left + cc + right

    candgen = ((word, cand) for word in sorted(words)
               for cand in edit_distance_one(word) if cand in words)
    G.add_nodes_from(words)
    for word, cand in candgen:
        G.add_edge(word, cand)
    return G

def words_graph():
    """Return the words example graph from the Stanford GraphBase"""
    fh=open('words_dat.txt','r')
    words=set()
    for line in fh.readlines():
        line = line.decode()
        if line.startswith('*'):
            continue
        w=str(line[0:5])
        words.add(w)
    return generate_graph(words)

if __name__ == '__main__':
    from networkx import *
    G=words_graph()
    print("Loaded words_dat.txt containing 5757 five-letter English words.")
    print("Two words are connected if they differ in one letter.")
    print("Graph has %d nodes with %d edges"
          %(number_of_nodes(G),number_of_edges(G)))
    print("%d connected components" % number_connected_components(G))

    for (source,target) in [('chaos','order'),
                            ('nodes','graph'),
                            ('pound','marks'),
			    ('moron','smart')]:
        print("Shortest path between %s and %s is"%(source,target))
        try:
            sp=shortest_path(G, source, target)
            for n in sp:
                print(n)
        except nx.NetworkXNoPath:
            print("None")
