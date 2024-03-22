import pandas as pd
import networkx as nx
from pyvis.network import Network
import random

# Load  data
df = pd.read_csv('grouped_updated_combined_data.csv', low_memory=False)


df = df.dropna(subset=['author', 'parent_post_author'])
df = df[df['author'].apply(lambda x: isinstance(x, str))]
df = df[df['parent_post_author'].apply(lambda x: isinstance(x, str))]
df = df[(df['author'] != '-') & (df['author'] != "[deleted]")]
df = df[(df['parent_post_author'] != '-') & (df['parent_post_author'] != "[deleted]")]
G = nx.DiGraph()

for _, row in df.iterrows():
    source = row['parent_post_author']
    target = row['author']
    if G.has_edge(source, target):
        G[source][target]['weight'] += 1
    else:
        G.add_edge(source, target, weight=1)


sample_size = 500  #  sample size
 
if len(G.nodes()) > sample_size:
    sampled_nodes = random.sample(list(G.nodes()), sample_size)
else:
    sampled_nodes = G.nodes()
    

H = G.subgraph(sampled_nodes)

nt = Network(notebook=False, height="750px", width="100%", bgcolor="#222222", font_color="white")
for node in H.nodes:
    nt.add_node(node)
for edge in H.edges(data=True):
    weight = edge[2]['weight']
    nt.add_edge(edge[0], edge[1], width=weight)

nt.from_nx(H)

html_out = nt.generate_html()

with open('sampled_network_visualization_alternative.html', 'w') as html_file:
    html_file.write(html_out)