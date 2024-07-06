import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

def create_evacuation_graph():
    return nx.Graph()

def add_node_to_graph(graph, node_name, node_type, distances):
    graph.add_node(node_name, node_type=node_type)
    for existing_node, distance in distances.items():
        if node_type == "Risk_Area" and existing_node != node_name:
            if not existing_node.startswith("Risk_Area"):
                graph.add_edge(node_name, existing_node, weight=distance)
                graph.add_edge(existing_node, node_name, weight=distance)
        else:
            graph.add_edge(node_name, existing_node, weight=distance)
            graph.add_edge(existing_node, node_name, weight=distance)
    if node_type == "Rescue_Center":
        graph.add_edge(node_name, existing_node, weight=distance)
        graph.add_edge(existing_node, node_name, weight=distance)

def find_minimal_path(graph, start_node, end_nodes, risk_areas_to_avoid):
    minimal_paths = {}
    for end_node in end_nodes:
        if end_node not in graph.nodes:
            graph.add_node(end_node)
        graph_copy = graph.copy()
        edges_to_remove = []
        for risk_area in risk_areas_to_avoid:
            for neighbor in graph_copy.neighbors(risk_area):
                edges_to_remove.append((risk_area, neighbor))
        for edge in edges_to_remove:
            graph_copy.remove_edge(edge[0], edge[1])
        try:
            minimal_path = nx.shortest_path(graph_copy, source=start_node, target=end_node, weight='weight')
            minimal_paths[end_node] = minimal_path
        except nx.NetworkXNoPath:
            minimal_paths[end_node] = None
    return minimal_paths

def visualize_evacuation_graph(graph, path_edges=None):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black',
            font_size=8)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    if path_edges:
        shortest_path = min(path_edges.values(), key=lambda x: len(x) if x is not None else float('inf'))
        if shortest_path is not None:
            edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2)
    plt.show()

def create_dynamic_graph():
    evacuation_graph = create_evacuation_graph()

    # Get the number of nodes to enter
    num_nodes = simpledialog.askinteger("Input", "Enter the number of nodes:")

    # User input for each node
    for _ in range(num_nodes):
        node_name = simpledialog.askstring("Node Information", "Enter node name:")
        node_type = simpledialog.askstring("Node Information", "Enter node type (Risk_Area, Rescue_Center, Evacuation_Route):")
        distances = {}
        for existing_node in evacuation_graph.nodes:
            if existing_node != node_name:
                distance = simpledialog.askfloat("Edge Information", f"Enter distance between {node_name} and {existing_node}:")
                distances[existing_node] = distance
        add_node_to_graph(evacuation_graph, node_name, node_type, distances)

    # Define available source nodes and end nodes
    source_nodes = list(evacuation_graph.nodes)
    end_nodes = simpledialog.askstring("End Nodes", "Enter end nodes (comma-separated):").split(',')

    # User chooses the source node
    start_node = simpledialog.askstring("Source Node", "Choose the source node:", initialvalue=source_nodes[0])

    # Validate the user input
    if start_node not in source_nodes:
        print("Invalid source node. Please choose from the available options.")
        return

    risk_areas_to_avoid = [node for node in evacuation_graph.nodes if node.startswith("Risk_Area") and node != start_node]
    minimal_paths = find_minimal_path(evacuation_graph, start_node, end_nodes, risk_areas_to_avoid)

    visualize_evacuation_graph(evacuation_graph, path_edges=minimal_paths)

    for end_node, minimal_path in minimal_paths.items():
        print(f"Minimal Path from {start_node} to {end_node}:", minimal_path)

if __name__ == "__main__":
    create_dynamic_graph()
