import pandas as pd
import networkx as nx
import plotly.graph_objs as go
import plotly.io as pio
import gravis as gv

df = pd.read_csv('grouped_updated_combined_data.csv')

df = df.dropna(subset=['author', 'parent_post_author'])
df = df[df['author'].apply(lambda x: isinstance(x, str))]
df = df[df['parent_post_author'].apply(lambda x: isinstance(x, str))]
df = df.sample(n=500)

G = nx.DiGraph()

# Dictionary to store edge weights
edge_weights = {}

for _, row in df.iterrows():
    if row['author'] != '-' and row['author'] != "[deleted]" and row['parent_post_author'] != '-' and row['parent_post_author'] != "[deleted]":
        source = row['parent_post_author']
        target = row['author']
        # Check if the edge already exists
        if G.has_edge(source, target):
            # Increment edge weight if the edge exists
            if (source, target) in edge_weights:
                edge_weights[(source, target)] += 1
            else:
                edge_weights[(source, target)] = 2  # Start weight from 2 since we are adding the second edge
        else:
            G.add_edge(source, target)
            edge_weights[(source, target)] = 1  # Start weight from 1 for the first edge

# Add edge weights to the graph
for edge, weight in edge_weights.items():
    G[edge[0]][edge[1]]['weight'] = weight

# Visualization with Gravis
fig = gv.three(G, use_node_size_normalization=True,
               use_edge_size_normalization=True, edge_size_data_source='weight', edge_curvature=0.3, zoom_factor=0.8)

# Export the visualization to HTML
fig.export_html('weight.html')
