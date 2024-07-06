import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Tk, Label, StringVar, OptionMenu, Button

def create_evacuation_graph():
    # Create an empty graph
    evacuation_graph = nx.Graph()

    # Add nodes for risk areas, evacuation routes, and rescue centers
    evacuation_graph.add_nodes_from(["Risk_Area_1", "Risk_Area_2", "Evacuation_Route_1", "Evacuation_Route_2", "Rescue_Center_1", "Rescue_Center_2"])

    # Add edges with distances
    evacuation_graph.add_edge("Risk_Area_1", "Evacuation_Route_1", weight=5)
    evacuation_graph.add_edge("Risk_Area_1", "Evacuation_Route_2", weight=8)
    evacuation_graph.add_edge("Risk_Area_2", "Evacuation_Route_1", weight=7)
    evacuation_graph.add_edge("Risk_Area_2", "Evacuation_Route_2", weight=6)
    evacuation_graph.add_edge("Evacuation_Route_1", "Rescue_Center_1", weight=10)
    evacuation_graph.add_edge("Evacuation_Route_2", "Rescue_Center_2", weight=12)

    return evacuation_graph

def find_minimal_path(graph, start_node, end_nodes, risk_areas_to_avoid):
    minimal_paths = {}
    
    for end_node in end_nodes:
        # Create a copy of the graph
        graph_copy = graph.copy()

        # Remove edges connecting risk areas to evacuation routes
        for risk_area in risk_areas_to_avoid:
            for neighbor in graph.neighbors(risk_area):
                graph_copy.remove_edge(risk_area, neighbor)

        # Find the minimal path using Dijkstra's algorithm
        try:
            minimal_path = nx.shortest_path(graph_copy, source=start_node, target=end_node, weight='weight')
            minimal_paths[end_node] = minimal_path
        except nx.NetworkXNoPath:
            minimal_paths[end_node] = None  # No path exists

    return minimal_paths

def visualize_evacuation_graph(graph, path_edges=None):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black', font_size=8)

    # Add edge labels with distances for all edges
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    if path_edges:
        # Find the shortest path among all minimal paths
        shortest_path = min(path_edges.values(), key=lambda x: len(x) if x is not None else float('inf'))

        # Check if shortest_path is not None before converting to edge tuples
        if shortest_path is not None:
            edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2)

    plt.show()

def on_source_node_selected(*args):
    start_node = source_node_var.get()
    risk_areas_to_avoid = [node for node in evacuation_graph.nodes if node.startswith("Risk_Area") and node != start_node]
    minimal_paths = find_minimal_path(evacuation_graph, start_node, end_nodes, risk_areas_to_avoid)
    visualize_evacuation_graph(evacuation_graph, path_edges=minimal_paths)

    for end_node, minimal_path in minimal_paths.items():
        print(f"Minimal Path from {start_node} to {end_node}:", minimal_path)

# GUI initialization
root = Tk()
root.title("Evacuation Route Planner")

evacuation_graph = create_evacuation_graph()

# Define available source nodes and end nodes
source_nodes = ["Risk_Area_1", "Risk_Area_2"]
end_nodes = ["Rescue_Center_1", "Rescue_Center_2"]

# Tkinter variables
source_node_var = StringVar(root)
source_node_var.set(source_nodes[0])  # Set the default value

# Create widgets
source_node_label = Label(root, text="Choose Source Node:")
source_node_menu = OptionMenu(root, source_node_var, *source_nodes)
visualize_button = Button(root, text="Visualize Evacuation Routes", command=on_source_node_selected)

# Pack widgets
source_node_label.pack()
source_node_menu.pack()
visualize_button.pack()

# Tkinter main loop
root.mainloop()
