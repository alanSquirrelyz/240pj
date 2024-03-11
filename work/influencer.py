import pandas as pd
import networkx as nx
from plotly.graph_objs import Scatter3d, Figure, Layout, Marker, Line, ColorBar
import plotly.io as pio
from datetime import datetime

# Load dataset
df = pd.read_csv('grouped_updated_combined_data.csv') 
df = df.dropna(subset=['author', 'parent_post_author'])
df = df[df['author'].apply(lambda x: isinstance(x, str))]
df = df[df['parent_post_author'].apply(lambda x: isinstance(x, str))]

df['created'] = pd.to_datetime(df['created'])
start_date = df['created'].min()
end_date = df['created'].max()

delta = pd.DateOffset(days=15) # 15 days result in the clearest visualizations

start_date = df['created'].min()
end_date = df['created'].max()
delta = pd.DateOffset(days=15)

current_start_date = start_date

while current_start_date < end_date:
    current_end_date = current_start_date + delta
    current_df = df[(df['created'] >= current_start_date) & (df['created'] < current_end_date)]
    
    if not current_df.empty:
        G = nx.DiGraph()
        for _, row in current_df.iterrows():
            if row['author'] != '-' and row['author'] != "[deleted]" and row['parent_post_author'] != '-' and row['parent_post_author'] != "[deleted]":
                G.add_edge(row['author'], row['parent_post_author'])
        
        if not nx.number_of_edges(G):
            current_start_date += delta
            continue

        pos = nx.spring_layout(G, dim=3, seed=42)
        edge_trace = Scatter3d(x=[], y=[], z=[], line=Line(color='rgba(50,50,50,0.5)'), hoverinfo='none', mode='lines')
        
        for edge in G.edges():
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)
            edge_trace['z'] += (z0, z1, None)
        
        degrees = dict(G.degree())
        max_degree = max(degrees.values())
        node_color = [degrees[node] for node in G.nodes()]
        colors = ['#1f78b4' if degree < max_degree else '#e31a1c' for degree in node_color]

        node_sizes = [10 if degree < max_degree else 20 for degree in node_color]  # size 10 for normal, 20 for highest degree

        node_trace = Scatter3d(x=[], y=[], z=[], mode='markers', hoverinfo='text',
                               marker=Marker(size=node_sizes, color=colors, colorscale='Viridis', colorbar=ColorBar(title='Node Degree')))
        
        for node in G.nodes():
            x, y, z = pos[node]
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)
            node_trace['z'] += (z,)
        
        fig = Figure(data=[edge_trace, node_trace], layout=Layout(
                      title=f'Network from {current_start_date.date()} to {current_end_date.date()}',
                      showlegend=False, hovermode='closest',
                      margin=dict(b=0, l=0, r=0, t=40),
                      scene=dict(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                 yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                 zaxis=dict(showgrid=False, zeroline=False, showticklabels=False))))

        filename = f'network_visualization_{current_start_date.date()}_to_{current_end_date.date()}.html'
        pio.write_html(fig, filename)
        print(f"Saved {filename}")
    
    current_start_date += delta