import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from disk.algorithms import run_algorithm
from disk.metrics import calculate_metrics

def compare_all_algorithms(requests, head, parent_frame, disk_size=200):
    # Clear previous widgets
    for widget in parent_frame.winfo_children():
        widget.destroy()

    algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]
    results = {}

    for algo in algorithms:
        sequence = run_algorithm(algo, requests, head, disk_size=disk_size)
        metrics = calculate_metrics(sequence)
        results[algo] = metrics["Total Seek"]

    # Create Figure
    fig = plt.Figure(figsize=(8, 5), dpi=100)
    fig.patch.set_facecolor('#F4F6F8')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#FFFFFF')
    
    bars = ax.bar(results.keys(), results.values(), color="#1F77B4")
    ax.set_xlabel("Scheduling Algorithms", weight='bold')
    ax.set_ylabel("Total Seek Time", weight='bold')
    ax.set_title("Algorithm Performance Comparison", weight='bold', pad=15)
    
    # Add value labels
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', va='bottom', fontsize=10, weight='bold', color='#333333')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return results

def rank_algorithms(results):
    sorted_algos = sorted(results.items(), key=lambda x: x[1])
    ranking_text = "\n🏆 ALGORITHM RANKING\n\n"
    for i, (algo, value) in enumerate(sorted_algos, 1):
        ranking_text += f"{i}. {algo} → {int(value)} movements\n"
    return ranking_text
