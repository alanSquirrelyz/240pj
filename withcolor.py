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

for _, row in df.iterrows():
    if row['author'] != '-' and row['author'] != "[deleted]" and row['parent_post_author'] != '-' and row['parent_post_author'] != "[deleted]":
        G.add_edge(row['parent_post_author'], row['author'])

# Create a list to store node colors
node_colors = {}

# Iterate through nodes to assign colors
for node in G.nodes:
    if node in df['author'].values and node in df['parent_post_author'].values:
        node_colors[node] = 'red'  # Color nodes that are both author and parent_post_author
    else:
        node_colors[node] = 'blue'  # Default color for other nodes

# Create a networkx graph with node attributes
nx.set_node_attributes(G, node_colors, 'color')

# Visualization with Gravis
fig = gv.three(G, use_node_size_normalization=True,
               use_edge_size_normalization=False, edge_size_data_source='weight', edge_curvature=0.0, zoom_factor=1.6)

# Export the visualization to HTML
fig.export_html('color.html')
