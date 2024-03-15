import pandas as pd
import networkx as nx
from pyvis.network import Network
import random
import pandas as pd
import networkx as nx
import plotly.graph_objs as go
import plotly.io as pio
import gravis as gv


# Load  data
df = pd.read_csv('grouped_updated_combined_data.csv', low_memory=False)


df = df.dropna(subset=['author', 'parent_post_author'])
df = df[df['author'].apply(lambda x: isinstance(x, str))]
df = df[df['parent_post_author'].apply(lambda x: isinstance(x, str))]
df = df[(df['author'] != '-') & (df['author'] != "[deleted]")]
df = df[(df['parent_post_author'] != '-') & (df['parent_post_author'] != "[deleted]")]

graph = nx.DiGraph()
graph.graph['node_label_size'] = 14
graph.graph['node_label_color'] = 'green'
graph.graph['edge_label_size'] = 10
graph.graph['edge_label_color'] = 'blue'

# Nodes and node attributes
graph.add_node(0, label='first node', color='red', size=15, shape='rectangle', opacity=0.7,
               label_color='red', label_size=20, border_color='black', border_size=3)
graph.add_node(3, color='green', size=15, shape='hexagon', opacity=0.7,
               label_color='green', label_size=10, border_color='blue', border_size=3)
graph.add_node(6, label='last node')

# Edges and edge attributes
graph.add_edge(0, 1)  # add_edge creates nodes if they don't exist yet
graph.add_edge(1, 2, label='e2')
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 5, label='e5', color='orange', label_color='gray', label_size=14, size=4.0)
graph.add_edge(5, 6)
graph.add_edge(6, 2, label='e7')

gv.d3(graph, graph_height=200,
      node_label_data_source='label',
      show_edge_label=True, edge_label_data_source='label')

gv.show()