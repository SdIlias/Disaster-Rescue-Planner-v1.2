import networkx as nx
import matplotlib.pyplot as plt

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
def add_node_to_graph(graph, node_name, node_type, distances):
    # Add the new node to the graph
    graph.add_node(node_name, node_type=node_type)

    # Add edges with distances from the new node to existing nodes
    for existing_node, distance in distances.items():
        if node_type == "Risk_Area" and existing_node != node_name:
            # If the new node is a Risk_Area, consider not adding edges to other Risk_Area nodes
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
        # Add the new node to the original graph before creating a copy
        if end_node not in graph.nodes:
            graph.add_node(end_node)

        # Create a copy of the graph
        graph_copy = graph.copy()

        # Prepare a list of edges to be removed
        edges_to_remove = []
        for risk_area in risk_areas_to_avoid:
            for neighbor in graph_copy.neighbors(risk_area):
                edges_to_remove.append((risk_area, neighbor))

        # Remove edges connecting risk areas to evacuation routes
        for edge in edges_to_remove:
            graph_copy.remove_edge(edge[0], edge[1])

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

def main():
    evacuation_graph = create_evacuation_graph()

    # Define available source nodes and end nodes
    source_nodes = ["Risk_Area_1", "Risk_Area_2"]
    end_nodes = ["Rescue_Center_1", "Rescue_Center_2"]

    # User chooses the source node
    print("Available source nodes:", source_nodes)
    start_node = input("Choose the source node: ")

    # Validate the user input
    if start_node not in source_nodes:
        print("Invalid source node. Please choose from the available options.")
        return
    v = start_node
    # Create risk_areas_to_avoid based on all risk areas except the chosen source node
    risk_areas_to_avoid = [node for node in evacuation_graph.nodes if node.startswith("Risk_Area") and node != start_node]
    minimal_paths = find_minimal_path(evacuation_graph, start_node, end_nodes, risk_areas_to_avoid)

    visualize_evacuation_graph(evacuation_graph, path_edges=minimal_paths)

    # Allow the user to add a new node to the graph
    new_node_name = input("Enter the name of the new node: ")
    new_node_type = input("Enter the type of the new node (Risk_Area, Rescue_Center, Evacuation_Route): ")

    # Validate the user input for node type
    if new_node_type not in ["Risk_Area", "Rescue_Center", "Evacuation_Route"]:
        print("Invalid node type. Please choose from the available options.")
        return

    distances = {}
    for existing_node in evacuation_graph.nodes:
        if existing_node != new_node_name:
            distance = float(input(f"Enter the distance between {new_node_name} and {existing_node}: "))
            distances[existing_node] = distance

    add_node_to_graph(evacuation_graph, new_node_name, new_node_type, distances)


    print(f"Node {new_node_name} has been added to the graph.")

    # Update risk_areas_to_avoid to include the new Risk_Area
    if new_node_type == "Risk_Area":
        risk_areas_to_avoid.append(new_node_name)
    if new_node_type == "Rescue_Center":
        end_nodes.append(new_node_name)
    # Find minimal paths after adding the new node
    minimal_paths = find_minimal_path(evacuation_graph, v, end_nodes, risk_areas_to_avoid)

    visualize_evacuation_graph(evacuation_graph, path_edges=minimal_paths)

    for end_node, minimal_path in minimal_paths.items():
        print(f"Minimal Path from {start_node} to {end_node}:", minimal_path)

if __name__ == "__main__":
    main()
