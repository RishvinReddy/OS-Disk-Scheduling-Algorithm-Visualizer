import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def detect_deadlock(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    try:
        cycles = list(nx.simple_cycles(G))
        return cycles
    except nx.NetworkXNoCycle:
        return []

def draw_rag(processes, resources, edges, parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    G = nx.DiGraph()
    for p in processes:
        G.add_node(p, color='blue', type='process')
    for r in resources:
        G.add_node(r, color='red', type='resource')
        
    G.add_edges_from(edges)
    
    fig = plt.Figure(figsize=(6, 5), dpi=100)
    fig.patch.set_facecolor('#F4F6F8')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#FFFFFF')

    # Color mapping
    color_map = ['#1F77B4' if G.nodes[node]['type'] == 'process' else '#FF7F0E' for node in G]
    
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, ax=ax, with_labels=True, node_color=color_map, node_size=2000, font_size=12, font_color='white', font_weight='bold', arrows=True, arrowsize=20)
    
    cycles = detect_deadlock(edges)
    if cycles:
        ax.set_title("Deadlock Detected! (Cycle Present)", color='#D62728', weight='bold', pad=15)
    else:
        ax.set_title("System in Safe State (No Cycles)", color='#2CA02C', weight='bold', pad=15)

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return cycles
