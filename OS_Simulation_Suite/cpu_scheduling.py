import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

def create_cpu_tab(parent_frame):
    card = ctk.CTkFrame(parent_frame, fg_color="#FFFFFF", corner_radius=12)
    card.grid(row=0, column=0, sticky="nsew")
    card.grid_rowconfigure(2, weight=1)
    card.grid_columnconfigure(0, weight=1)

    top_frame = ctk.CTkFrame(card, fg_color="transparent")
    top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
    ctk.CTkLabel(top_frame, text="CPU Scheduling & Analytics", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111827").pack(side="left")

    # Layout: Top is Queues & Gantt, Bottom is Graph & Stats
    visual_frame = ctk.CTkFrame(card, fg_color="transparent")
    visual_frame.grid(row=1, column=0, sticky="nsew", padx=20)
    
    ctk.CTkLabel(visual_frame, text="Ready Queue (Process Creation)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w", pady=(10,0))
    queue_canvas = tk.Canvas(visual_frame, height=80, bg="#F9FAFB", highlightthickness=1, highlightbackground="#E5E7EB")
    queue_canvas.pack(fill="x", pady=5)

    ctk.CTkLabel(visual_frame, text="Execution Gantt Chart", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w", pady=(10,0))
    cv = tk.Canvas(visual_frame, height=120, bg="#F9FAFB", highlightthickness=1, highlightbackground="#E5E7EB")
    cv.pack(fill="x", pady=5)
    
    bottom_frame = ctk.CTkFrame(card, fg_color="transparent")
    bottom_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
    bottom_frame.grid_columnconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(1, weight=1)
    
    # Graph Area
    graph_parent = ctk.CTkFrame(bottom_frame, fg_color="transparent")
    graph_parent.grid(row=0, column=0, sticky="nsew", padx=(0,10))
    fig = Figure(figsize=(4,3), dpi=100)
    fig.patch.set_facecolor('#F9FAFB')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#FFFFFF')
    ax.set_title("Real-Time Waiting Time Trend")
    ax.set_ylabel("Waiting Time")
    ax.set_xlabel("Process Index")
    graph_canvas = FigureCanvasTkAgg(fig, master=graph_parent)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(fill="both", expand=True)

    # Stats Area
    stats_frame = ctk.CTkFrame(bottom_frame, fg_color="#F9FAFB", corner_radius=8, border_width=1, border_color="#E5E7EB")
    stats_frame.grid(row=0, column=1, sticky="nsew", padx=(10,0))
    ctk.CTkLabel(stats_frame, text="Simulation Output", font=ctk.CTkFont(weight="bold"), text_color="#111827").pack(pady=10)
    result_box = tk.Text(stats_frame, height=10, width=30, font=("Courier", 11), bg="#F9FAFB", fg="#111827", relief="flat")
    result_box.pack(fill="both", expand=True, padx=10, pady=10)

    processes = [
        {"id": "P1", "burst": 4, "priority": 2},
        {"id": "P2", "burst": 3, "priority": 1},
        {"id": "P3", "burst": 5, "priority": 3}
    ]

    def draw_queue(procs):
        queue_canvas.delete("all")
        x = 20
        for p in procs:
            queue_canvas.create_rectangle(x, 20, x+60, 60, fill="#FFD166", outline="#F59E0B", width=2)
            queue_canvas.create_text(x+30, 40, text=p["id"], font=("Arial", 11, "bold"), fill="#78350F")
            x += 80
            
    def calculate_waiting_times(procs):
        waiting_times = []
        for i, p in enumerate(procs):
            if i == 0:
                waiting_times.append(0)
            else:
                wait = sum(prev["burst"] for prev in procs[:i])
                waiting_times.append(wait)
        return waiting_times

    def update_graph(waiting_times):
        ax.clear()
        ax.plot(waiting_times, marker='o', color="#1F4ED8")
        ax.set_title("Real-Time Waiting Time Trend")
        ax.set_ylabel("Waiting Time")
        ax.set_xlabel("Process Index")
        graph_canvas.draw()

    def simulate(algo="FCFS"):
        cv.delete("all")
        result_box.delete("1.0", tk.END)
        cv.update()
        queue_canvas.update()
        w = cv.winfo_width()
        
        procs = processes.copy()
        
        if algo == "Priority":
            procs.sort(key=lambda x: x["priority"])
        elif algo == "SJF":
            procs.sort(key=lambda x: x["burst"])
            
        y_pos = 60
        cv.create_line(50, y_pos+30, w-50, y_pos+30, fill="#E5E7EB", width=2)

        wait_times = calculate_waiting_times(procs)
        
        # Process Creation Animation (Move to Ready Queue)
        queue_canvas.delete("all")
        
        def animate_creation(idx=0):
            if idx < len(procs):
                p = procs[idx]
                x_start = -50
                x_end = 20 + (idx * 80)
                
                rect = queue_canvas.create_rectangle(x_start, 20, x_start+60, 60, fill="#4CAF50", outline="#22C55E", width=2)
                txt = queue_canvas.create_text(x_start+30, 40, text=p["id"], font=("Arial", 11, "bold"), fill="#14532D")
                
                def slide(cx):
                    if cx < x_end:
                        queue_canvas.move(rect, 15, 0)
                        queue_canvas.move(txt, 15, 0)
                        parent_frame.after(30, lambda: slide(cx+15))
                    else:
                        animate_creation(idx+1)
                slide(x_start)
            else:
                # Proceed to Gantt rendering
                run_gantt()
        
        def run_gantt():
            x = 50
            index = 0
            live_waits = []
            
            def step():
                nonlocal x, index
                if index < len(procs):
                    p = procs[index]
                    width = p["burst"] * 30
                    
                    # Update Ready Queue visually (remove process)
                    draw_queue(procs[index+1:])
    
                    # Draw Block
                    cv.create_rectangle(x, y_pos-30, x+width, y_pos+30, fill="#10B981", outline="#059669", width=2)
                    cv.create_text(x+width/2, y_pos, text=p["id"], font=("Arial", 12, "bold"), fill="#064E3B")
                    
                    # Draw Time Ticks
                    cv.create_text(x, y_pos+45, text=str(sum(pr["burst"] for pr in procs[:index])), font=("Arial", 10), fill="#6B7280")
                    if index == len(procs) - 1:
                        cv.create_text(x+width, y_pos+45, text=str(sum(pr["burst"] for pr in procs)), font=("Arial", 10), fill="#6B7280")
    
                    live_waits.append(wait_times[index])
                    update_graph(live_waits)
                    
                    result_box.insert(tk.END, f"{algo} -> Executed {p['id']} (Wait: {wait_times[index]})\n")
    
                    x += width
                    index += 1
                    parent_frame.after(1000, step)
                else:
                    avg_wait = sum(wait_times)/len(wait_times)
                    avg_ta = sum(wait_times[i] + procs[i]["burst"] for i in range(len(procs))) / len(procs)
                    result_box.insert(tk.END, f"\nAvg Waiting Time: {avg_wait:.2f}\n")
                    result_box.insert(tk.END, f"Avg Turnaround: {avg_ta:.2f}\n")
    
            step()

        animate_creation()

    def simulate_starvation():
        cv.delete("all")
        queue_canvas.delete("all")
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, "Low priority process P5 waiting...\n")
        
        draw_queue([{"id": "P5", "burst": 2, "priority": 10}])
        
        def sim_starve():
            result_box.insert(tk.END, "-> High priority P1 arrived and executed\n")
            result_box.insert(tk.END, "-> High priority P2 arrived and executed\n")
            result_box.insert(tk.END, "-> High priority P3 arrived and executed\n")
            result_box.insert(tk.END, "\n⚠ Starvation occurred:\n P5 never executed due to continuous high-priority arrivals.\n")
            result_box.see(tk.END)
        
        parent_frame.after(1500, sim_starve)


    btn_frame = ctk.CTkFrame(card, fg_color="transparent")
    btn_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
    
    ctk.CTkButton(btn_frame, text="FCFS", fg_color="#10B981", hover_color="#059669", command=lambda: simulate("FCFS"), width=100).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="SJF", fg_color="#F59E0B", hover_color="#D97706", command=lambda: simulate("SJF"), width=100).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Priority", fg_color="#8B5CF6", hover_color="#7C3AED", command=lambda: simulate("Priority"), width=100).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Starvation Demo", fg_color="#EF4444", hover_color="#DC2626", command=simulate_starvation, width=150).pack(side="left", padx=5)
