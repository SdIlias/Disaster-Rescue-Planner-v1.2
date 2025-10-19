# Disaster-Rescue-Planner

### 🏷️ **Project Context:** Operations Research & Graph Theory
### 🏫 **Module:** Recherche Opérationnelle (IAGI - ENSAM Casablanca)

---

## 🎯 Project Overview

The **Disaster-Rescue-Planner** is a computational model designed to optimize evacuation strategies in the event of a natural disaster. It applies fundamental principles of **Operations Research (OR)** and **Graph Theory** to create a robust, secure, and rapid evacuation network.

The core objective is to minimize the total evacuation distance (or time) from a specified risk area to the nearest rescue center, while simultaneously ensuring the safety of evacuees by routing them away from other active disaster zones.

## ⚙️ Technical Approach

The system models the disaster environment as an undirected, weighted graph, where the optimization problem is solved using an adapted version of Dijkstra's algorithm.

### 1. Graph Modeling (System Topology)

*   **Nodes:** Represent distinct locations within the evacuation zone:
    *   `Risk_Area`: Starting points for evacuation.
    *   `Evacuation_Route`: Intermediary points or junctions.
    *   `Rescue_Center`: Designated safe end-points.
*   **Edges:** Connect nodes and are assigned a `weight` attribute, representing the distance (or, conceptually, the travel time) between two points.

### 2. Network Security & Optimization

To maximize the security of the evacuation, the model incorporates a crucial network manipulation step before pathfinding:

1.  **Selection:** A single `start_node` (Risk Area) is chosen for evacuation.
2.  **Isolation (Avoidance):** All other `Risk_Area` nodes are assumed to be too dangerous to traverse or pass nearby.
3.  **Edge Removal:** Edges connected to the avoided risk areas are *temporarily removed* from the graph copy. This effectively isolates them, ensuring that the calculated path is secure and avoids active danger zones.
4.  **Shortest Path Calculation:** Dijkstra's algorithm (`nx.shortest_path`) is then executed on the modified graph copy to find the path with the minimum accumulated `weight` (distance) from the chosen starting point to the nearest `Rescue_Center`.

This method ensures the *shortest secure path* is identified for immediate action.

## ✨ Key Features

*   **Optimal Pathfinding:** Uses Dijkstra's algorithm to determine the minimal path to multiple end-centers.
*   **Security Constraint Implementation:** Models and enforces security by dynamically removing non-source risk routes.
*   **Dynamic Network Topology:** Supports the addition of new nodes (e.g., a newly established Rescue Center or a newly identified Risk Area) at runtime.
*   **Comprehensive Visualization:** Utilizes `matplotlib` and `networkx` to render the evacuation graph, including edge weights and highlighting the final optimal (shortest, secure) path in red.
*   **Flexible Interface:** Includes both command-line (CLI) and graphical user interface (GUI) implementations.

---


## 🖼️ Visual Demonstration

The images below illustrate the application running on the command line and on GUI, showcasing two distinct scenarios: the initial optimal path, and the system's ability to **dynamically add a new node and recalculate the optimal, secure path**.

### **Scenario 1: Initial Evacuation from `Risk_Area_1`**

Before any new nodes are added, the system isolates `Risk_Area_2` and calculates the shortest path from `Risk_Area_1` to all rescue centers. The optimal path (marked in **red**) is to `Rescue_Center_1` (Total Weight: **15**).

| Terminal Output (Input) | Graph Visualization (Initial State) |
| :--- | :--- |
| **<img width="415" height="59" alt="image1_1" src="https://github.com/user-attachments/assets/d061904e-fa10-48c3-9730-b838272c14f1" />** | **<img width="642" height="550" alt="image1_2" src="https://github.com/user-attachments/assets/fd6da407-8f18-4f52-b478-4e87ab6a7c45" />** |

### **Scenario 2: Dynamic Update - Adding New Risk Area (`Risk_Area_3`)**

A new node, `Risk_Area_3`, is added to the network. The source node for evacuation remains `Risk_Area_1`. The system must now avoid both **`Risk_Area_2`** AND the newly added **`Risk_Area_3`** to maintain security.

The path is recalculated to ensure it remains the *shortest secure path* from `Risk_Area_1`.

| Terminal Output (New Node & Final Path) | Graph Visualization (Updated Path) |
| :--- | :--- |
| **<img width="775" height="223" alt="image3" src="https://github.com/user-attachments/assets/0a4ee041-1386-4b19-8286-65e6d61dd9e1" />** | **<img width="641" height="551" alt="image 2_2" src="https://github.com/user-attachments/assets/e74c2095-a41b-4551-8fee-bc4e800fa3e0" />** |

**Calculation Result:** The shortest path remains the same as the new risk area does not force a change to the minimal path.
*   Minimal Path to Rescue Center 1: `['Risk_Area_1', 'Evacuation_Route_1', 'Rescue_Center_1']` (Total Weight: **15**)
*   Minimal Path to Rescue Center 2: `['Risk_Area_1', 'Evacuation_Route_2', 'Rescue_Center_2']` (Total Weight: **20**)

The system successfully recalculated and confirmed the shortest, secure route is still **`Risk_Area_1` → `Evacuation_Route_1` → `Rescue_Center_1`**.


### **Scenario 3: Graphical User Interface (GUI) - Dynamic Graph Creation**

This showcases the functionality of the `GRAPHICAL.txt` file, which allows a user to build a *completely custom* network from scratch using interactive dialog boxes (Tkinter). This highlights the project's flexibility and the dynamic nature of its topology.

| GUI Step 1: Input Count | GUI Step 2: Define Node Attributes |
| :--- | :--- |
| **<img width="358" height="195" alt="image4" src="https://github.com/user-attachments/assets/31212d56-b75e-4622-83bc-f4cc329048a7" />** | **<img width="323" height="182" alt="image5" src="https://github.com/user-attachments/assets/cb45e89c-16b8-4925-8311-be195df7c02b" />** |
| (Sets the size of the custom network) | (Defines the node's identifier) |

| GUI Step 3: Define Node Type | GUI Step 4: Define Edge Weights |
| :--- | :--- |
| **<img width="473" height="193" alt="image6" src="https://github.com/user-attachments/assets/c6c17dc0-3a22-48cf-a489-530b8a6f02bf" />** | **<img width="363" height="179" alt="image7" src="https://github.com/user-attachments/assets/52317212-3a7a-4a96-a7a7-f6b3af2e517c" />** |
| (Classifies the node for pathfinding logic) | (Sets the weighted distance between nodes) |

| Final Visualization of Custom Graph |
| :--- |
| **<img width="654" height="391" alt="image8" src="https://github.com/user-attachments/assets/62213248-8789-48ee-b65a-eb07f31205bd" />** |
| (The custom, 4-node network is successfully visualized) |


---

## 📂 Project File Analysis

| File Name | Interface Type | Primary Functionality | Description |
| :--- | :--- | :--- | :--- |
| **`p1.txt`** | CLI | Core Logic & Node Addition (Pre-defined Graph) | The fundamental implementation. It initializes a static graph, finds the minimal path, visualizes it, and then prompts the user to add a *single* new node (Risk Area, Route, or Center) dynamically. It recalculates and re-visualizes the graph with the new node. |
| **`SCRIPT.txt`** | CLI | Refined Dynamic Addition | A slight refinement of `p1.txt`. It includes improved logic within `add_node_to_graph` to better handle edge creation for new nodes and correctly updates the `end_nodes` list when a new `Rescue_Center` is added, ensuring the pathfinding includes the new target. |
| **`f.txt`** | GUI (Tkinter) | Dropdown Selection & Visualization | Focuses on user experience for the pre-defined graph. It uses the `tkinter` library to create a simple window with a dropdown menu, allowing the user to select the starting `Risk_Area` and immediately visualize the corresponding optimal path without needing CLI input. |
| **`GRAPHICAL.txt`** | GUI (Tkinter) | Full Dynamic Graph Creation | The most advanced version. It removes the static graph initialization and uses `tkinter.simpledialog` to prompt the user to build the *entire* network at runtime (number of nodes, names, types, and all inter-node distances). This demonstrates full control over dynamic graph topology creation. |
| **`p3.txt`** | N/A | Incomplete Draft | This file appears to be an early or incomplete draft, missing necessary Python syntax (colons, string quotes) for execution. |

## ▶️ Getting Started

### Prerequisites

*   Python 3.x
*   `networkx`
*   `matplotlib`
*   `tkinter` (Usually included with Python standard library)

### Installation

```bash
# Install the required libraries
pip install networkx matplotlib
```

### Usage (Using the Core SCRIPT.txt)

```bash
# Assuming SCRIPT.txt is saved as evacuation_planner.py
python evacuation_planner.py
```

The script will guide the user through selecting a source node and then dynamically adding a new node to see the updated evacuation routes.
