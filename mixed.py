import pandas as pd
import networkx as nx
import gravis as gv

df = pd.read_csv('final_data.csv')

df = df.dropna(subset=['author', 'parent_post_author'])

df = df[df['author'].apply(lambda x: isinstance(x, str))]
df = df[df['parent_post_author'].apply(lambda x: isinstance(x, str))]

df = df[df['group_per_month'].between(13, 36)]

# Sample or limit to first 10000 rows if needed (remove or comment out if not desired)
df = df.sample(n=4000)
# df = df.head(10000)

G = nx.DiGraph()

for _, row in df.iterrows():
    if row['author'] not in ['-', '[deleted]'] and row['parent_post_author'] not in ['-', '[deleted]']:
        source = row['parent_post_author']
        target = row['author']
        if G.has_edge(source, target):
            G[source][target]['weight'] += 1
        else:
            G.add_edge(source, target, weight=1)

fig = gv.d3(G, use_node_size_normalization=False, edge_label_data_source='weight', show_node_label=False, show_edge_label=True, edge_curvature=0.0,
      use_edge_size_normalization=True, zoom_factor=0.5)
fig.export_html('__mixed.html')
