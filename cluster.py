import pandas as pd
import networkx as nx
import plotly.graph_objs as go
import plotly.io as pio
import gravis as gv

df = pd.read_csv('grouped_updated_combined_data.csv')

df = df.dropna(subset=['author', 'parent_post_author'])
df = df[df['author'].apply(lambda x: isinstance(x, str))]
df = df[df['parent_post_author'].apply(lambda x: isinstance(x, str))]
df = df.sample(n=3000)
# df = df.head(1000)

G = nx.DiGraph()

for _, row in df.iterrows():
    if row['author'] != '-' and row['author'] != "[deleted]" and row['parent_post_author'] != '-' and row['parent_post_author'] != "[deleted]":
        G.add_edge(row['parent_post_author'], row['author'])

# subsample_nodes = list(G.nodes())[:500]  # Take the first 500 nodes
# G_sub = G.subgraph(subsample_nodes)

# pos = nx.spring_layout(G_sub, dim=3, seed=42)

# node_trace = go.Scatter3d(
#     x=[],
#     y=[],
#     z=[],
#     mode='markers',
#     hoverinfo='text',  # Adjusted to display author name
#     text=list(G_sub.nodes()),  # Author names as text labels
#     marker=dict(
#         showscale=True,
#         colorscale='YlGnBu',
#         reversescale=True,
#         color=[],
#         size=5,  # Reduce node size
#         colorbar=dict(
#             thickness=15,
#             title='Node Connections',
#             xanchor='left',
#             titleside='right'
#         )
#     ))

# node_degrees = dict(G_sub.degree())

# for node in G_sub.nodes():
#     x, y, z = pos[node]
#     node_trace['x'] += tuple([x])
#     node_trace['y'] += tuple([y])
#     node_trace['z'] += tuple([z])
#     # Set node color based on degree
#     color = node_degrees[node]
#     node_trace['marker']['color'] += tuple([color])

# edge_traces = []
# for edge in G_sub.edges():
#     x0, y0, z0 = pos[edge[0]]
#     x1, y1, z1 = pos[edge[1]]
#     edge_trace = go.Scatter3d(
#         x=[x0, x1],
#         y=[y0, y1],
#         z=[z0, z1],
#         mode='lines',
#         line=dict(color='red', width=1),  # Adjust edge properties
#         hoverinfo='none'
#     )
#     edge_traces.append(edge_trace)

# fig = go.Figure(data=[node_trace, *edge_traces],
#                 layout=go.Layout(
#                     title='User Relation Network',
#                     titlefont=dict(size=16),
#                     showlegend=False,
#                     hovermode='closest',
#                     margin=dict(b=20, l=5, r=5, t=40),
#                     scene=dict(
#                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                         zaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                         dragmode='turntable',  # Enable rotation
#                     )
#                 ))

# fig = go.Figure(
#     data=[node_trace, *edge_traces],
#     layout=go.Layout(
#         title='User Relation Network',
#                     titlefont=dict(size=16),
#                     showlegend=False,
#                     hovermode='closest',
#                     margin=dict(b=20, l=5, r=5, t=40),
#                     scene=dict(
#                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                         zaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                         dragmode='turntable',  # Enable rotation
#                     ),
#         annotations = [
#             dict(ax=x0[i], ay=y0[i], axref='x', ayref='y',
#                 x=x1[i], y=y1[i], xref='x', yref='y',
#                 showarrow=True, arrowhead=1,) for i in range(0, len(x0))
#         ]
#     )
# )

#

def assign_properties(g):
    # Centrality calculation
    node_centralities = nx.eigenvector_centrality(g)
    edge_centralities = nx.edge_betweenness_centrality(g)

    # Community detection
    communities = nx.algorithms.community.greedy_modularity_communities(g)

    # Graph properties
    g.graph['node_border_size'] = 1.5
    g.graph['node_border_color'] = 'white'
    g.graph['edge_opacity'] = 0.9

    # Node properties: Size by centrality, shape by size, color by community
    colors = ['red', 'blue', 'green', 'orange', 'pink', 'brown', 'yellow', 'cyan', 'magenta', 'violet']
    for node_id in g.nodes:
        node = g.nodes[node_id]
        node['size'] = 10 + node_centralities[node_id] * 100
        node['shape'] = 'rectangle' if node['size'] > 30 else 'circle'
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


# Create a graph with a generator function
# G = nx.powerlaw_cluster_graph(n=250, m=2, p=0.9)

# Assign node and edge properties
assign_properties(G)


fig = gv.three(G, use_node_size_normalization=True,
      use_edge_size_normalization=False, edge_size_data_source='weight', edge_curvature=0.3, zoom_factor=0.8)
# pio.write_html(fig, 'user_relation_network_3d.html')
fig.export_html('cluster.html')
