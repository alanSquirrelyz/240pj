import pandas as pd
import networkx as nx
import plotly.graph_objs as go

df = pd.read_csv('grouped_updated_combined_data.csv')
df = df.dropna(subset=['author', 'parent_post_author'])
df = df[df['author'].apply(lambda x: isinstance(x, str))]
df = df[df['parent_post_author'].apply(lambda x: isinstance(x, str))]

# df = df.head(1000)

G = nx.DiGraph()

for _, row in df.iterrows():
    G.add_edge(row['author'], row['parent_post_author'])

pos = nx.spring_layout(G, seed=42)

edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))


node_degrees = dict(G.degree())

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    color = node_degrees[node]
    node_trace['marker']['color'] += tuple([color])
    node_info = f'User: {node}<br># of connections: {node_degrees[node]}'
    node_trace['text'] += tuple([node_info])

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='User Relation Network',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

# Save the graph to an HTML file
fig.write_html('user_relation_network_beautiful.html')