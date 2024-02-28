import pandas as pd
import networkx as nx
import plotly.graph_objs as go
import plotly.io as pio

df = pd.read_csv('grouped_updated_combined_data.csv')

df = df.dropna(subset=['author', 'parent_post_author'])
df = df[df['author'].apply(lambda x: isinstance(x, str))]
df = df[df['parent_post_author'].apply(lambda x: isinstance(x, str))]

df = df.sample(n=500)

G = nx.DiGraph()

for _, row in df.iterrows():
    if row['author'] != '-' and row['author'] != "[deleted]" and row['parent_post_author'] != '-' and row['parent_post_author'] != "[deleted]":
        G.add_edge(row['author'], row['parent_post_author'])

subsample_nodes = list(G.nodes())[:500]  # Take the first 500 nodes
G_sub = G.subgraph(subsample_nodes)

pos = nx.spring_layout(G_sub, dim=3, seed=42)

edge_trace = go.Scatter3d(
    x=[],
    y=[],
    z=[],
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G_sub.edges():
    x0, y0, z0 = pos[edge[0]]
    x1, y1, z1 = pos[edge[1]]
    edge_trace['x'] += (x0, x1, None)  # Change square brackets to parentheses for tuple
    edge_trace['y'] += (y0, y1, None)  # Change square brackets to parentheses for tuple
    edge_trace['z'] += (z0, z1, None)  # Change square brackets to parentheses for tuple

# Add arrows for directed edges
for edge in G_sub.edges():
    x0, y0, z0 = pos[edge[0]]
    x1, y1, z1 = pos[edge[1]]
    arrow_length = 0.05  # Length of the arrow
    arrow_start = 0.9  # Start the arrow before the end of the edge
    arrow_x = x1 + arrow_start * (x0 - x1)
    arrow_y = y1 + arrow_start * (y0 - y1)
    arrow_z = z1 + arrow_start * (z0 - z1)
    dx = arrow_length * (x0 - x1)
    dy = arrow_length * (y0 - y1)
    dz = arrow_length * (z0 - z1)
    edge_trace['x'] += (arrow_x, arrow_x + dx, None, arrow_x, arrow_x - dx, None)  # Change square brackets to parentheses for tuple
    edge_trace['y'] += (arrow_y, arrow_y + dy, None, arrow_y, arrow_y - dy, None)  # Change square brackets to parentheses for tuple
    edge_trace['z'] += (arrow_z, arrow_z + dz, None, arrow_z, arrow_z - dz, None)  # Change square brackets to parentheses for tuple



node_trace = go.Scatter3d(
    x=[],
    y=[],
    z=[],
    mode='markers',
    hoverinfo='text',  
    text=list(G_sub.nodes()),  
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=5,  # Reduce node size
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        )
    ))

node_degrees = dict(G_sub.degree())

for node in G_sub.nodes():
    x, y, z = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['z'] += tuple([z])
    color = node_degrees[node]
    node_trace['marker']['color'] += tuple([color])

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='User Relation Network',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    scene=dict(
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        zaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        dragmode='turntable',  # Enable rotation
                    )
                ))

pio.write_html(fig, 'user_relation_network.html')