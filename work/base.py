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


fig = gv.three(G, use_node_size_normalization=True,
      use_edge_size_normalization=False, edge_size_data_source='weight', edge_curvature=0.3, zoom_factor=0.8)
# pio.write_html(fig, 'user_relation_network_3d.html')
fig.export_html('user_inter.html')
