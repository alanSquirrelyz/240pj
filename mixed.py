import pandas as pd
import networkx as nx
import plotly.graph_objs as go
import plotly.io as pio
import gravis as gv

df = pd.read_csv('grouped_updated_combined_data.csv')

df = df.dropna(subset=['author', 'parent_post_author'])
df = df[df['author'].apply(lambda x: isinstance(x, str))]
df = df[df['parent_post_author'].apply(lambda x: isinstance(x, str))]
df = df.sample(n=1000)
# df = df.head(1000)

G = nx.DiGraph()

for _, row in df.iterrows():
    if row['author'] != '-' and row['author'] != "[deleted]" and row['parent_post_author'] != '-' and row['parent_post_author'] != "[deleted]":
            source = row['parent_post_author']
            target = row['author']
            if G.has_edge(source, target):
                G[source][target]['weight'] += 1
            else:
                G.add_edge(source, target, weight=1)
        # G.add_edge(row['parent_post_author'], row['author'])

def assign_properties(g):
    node_centralities = nx.eigenvector_centrality(g)
    edge_centralities = nx.edge_betweenness_centrality(g)

    # Community detection
    communities = nx.algorithms.community.greedy_modularity_communities(g)

    g.graph['node_border_size'] = 1.5
    g.graph['node_border_color'] = 'white'
    g.graph['edge_opacity'] = 0.9

    colors = ['red', 'blue', 'green', 'orange', 'pink', 'brown', 'yellow', 'cyan', 'magenta', 'violet']
    for node_id in g.nodes:
        node = g.nodes[node_id]
        # node['size'] = 10 + node_centralities[node_id] * 100
        # node['shape'] = 'circle' if node['size'] > 30 else 'circle'
        for community_counter, community_members in enumerate(communities):
            if node_id in community_members:
                break
        node['color'] = colors[community_counter % len(colors)]

    # Edge properties: Size by centrality, color by community (within=community color, between=black)
    for edge_id in g.edges:
        edge =  g.edges[edge_id]
        source_node = g.nodes[edge_id[0]]
        target_node = g.nodes[edge_id[1]]
        edge['size'] = edge_centralities[edge_id] * 100
        edge['color'] = source_node['color'] if source_node['color'] == target_node['color'] else 'black'


assign_properties(G)


fig = gv.d3(G, use_node_size_normalization=False, edge_label_data_source='weight', show_edge_label=True, edge_curvature=0.0,
      use_edge_size_normalization=True,  zoom_factor=0.5)
# pio.write_html(fig, 'user_relation_network_3d.html')
fig.export_html('mixed.html')
