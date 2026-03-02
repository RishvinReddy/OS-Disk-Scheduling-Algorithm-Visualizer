import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random

# Global logging variable where any module can push messages
_global_logger = None

def push_log(module_name, message):
    if _global_logger:
        _global_logger(module_name, message)

def create_architecture_tab(parent_frame, nav_callbacks):
    card = ctk.CTkFrame(parent_frame, fg_color="#F9FAFB", corner_radius=12)
    card.grid(row=0, column=0, sticky="nsew")
    card.grid_rowconfigure(0, weight=1)
    card.grid_columnconfigure(0, weight=2)
    card.grid_columnconfigure(1, weight=1)

    left_frame = ctk.CTkFrame(card, fg_color="#FFFFFF", corner_radius=12)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
    
    ctk.CTkLabel(left_frame, text="OS Architecture Layout", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111827").pack(pady=(15, 0))
    ctk.CTkLabel(left_frame, text="Click on a layer to navigate to its simulation module.", font=ctk.CTkFont(size=12), text_color="#6B7280").pack(pady=(0, 10))

    canvas = tk.Canvas(left_frame, bg="#FFFFFF", highlightthickness=0)
    canvas.pack(fill="both", expand=True, padx=20, pady=10)

    layers = [
        {"name": "User Space", "color": "#E5E7EB", "text": "#374151", "target": None},
        {"name": "System Call Interface", "color": "#D1D5DB", "text": "#1F2937", "target": None},
        {"name": "Process Management", "color": "#10B981", "text": "#FFFFFF", "target": "cpu"},
        {"name": "Process Synchronization", "color": "#8B5CF6", "text": "#FFFFFF", "target": "sync"},
        {"name": "Deadlock Handling", "color": "#EF4444", "text": "#FFFFFF", "target": "deadlock"},
        {"name": "Memory & File Systems", "color": "#F59E0B", "text": "#FFFFFF", "target": "fs"},
        {"name": "Device Drivers (I/O)", "color": "#3B82F6", "text": "#FFFFFF", "target": "disk"},
        {"name": "Hardware", "color": "#111827", "text": "#FFFFFF", "target": "factory"}
    ]

    layer_rects = {}

    def draw_architecture():
        canvas.delete("all")
        canvas.update()
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 100: w = 400
        if h < 100: h = 400
        
        box_h = h / len(layers) - 5
        y = 5
        
        for layer in layers:
            rect = canvas.create_rectangle(10, y, w-10, y+box_h, fill=layer["color"], outline="", tags=layer["name"])
            canvas.create_text(w/2, y + box_h/2, text=layer["name"], fill=layer["text"], font=("Arial", 14, "bold"), tags=layer["name"])
            
            layer_rects[layer["name"]] = rect
            
            if layer["target"]:
                def make_handler(target):
                    return lambda e: nav_callbacks.get(target, lambda: None)()
                canvas.tag_bind(layer["name"], "<Button-1>", make_handler(layer["target"]))
                canvas.tag_bind(layer["name"], "<Enter>", lambda e, r=rect, c=layer["color"]: canvas.itemconfig(r, fill="#4B5563"))
                canvas.tag_bind(layer["name"], "<Leave>", lambda e, r=rect, c=layer["color"]: canvas.itemconfig(r, fill=c))
                
            y += box_h + 5

    parent_frame.after(100, draw_architecture)

    # Right side: Kernel Status
    right_frame = ctk.CTkFrame(card, fg_color="transparent")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_rowconfigure(1, weight=1)
    
    # Kernel Log
    log_frame = ctk.CTkFrame(right_frame, fg_color="#FFFFFF", corner_radius=12)
    log_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
    ctk.CTkLabel(log_frame, text="Kernel Log Console", font=ctk.CTkFont(size=14, weight="bold"), text_color="#111827").pack(anchor="w", padx=15, pady=10)
    
    log_box = tk.Text(log_frame, font=("Courier", 11), bg="#111827", fg="#10B981", relief="flat", highlightthickness=0)
    log_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    global _global_logger
    def handle_log(module, msg):
        log_box.insert(tk.END, f"[{module}] {msg}\n")
        log_box.see(tk.END)
    _global_logger = handle_log

    # Randomizing charts for system aesthetic
    graph_frame = ctk.CTkFrame(right_frame, fg_color="#FFFFFF", corner_radius=12)
    graph_frame.grid(row=1, column=0, sticky="nsew")
    
    fig = Figure(figsize=(3,2), dpi=100)
    fig.patch.set_facecolor('#FFFFFF')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#FFFFFF')
    ax.set_title("System Resource Flow", fontsize=10)
    ax.axis('off')
    
    graph_canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    graph_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    line1, = ax.plot([], [], color="#3B82F6", linewidth=2)
    line2, = ax.plot([], [], color="#10B981", linewidth=2)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 100)
    
    cpu_data = [random.randint(20, 40) for _ in range(21)]
    mem_data = [random.randint(50, 80) for _ in range(21)]
    
    def update_graph():
        cpu_data.pop(0)
        cpu_data.append(random.randint(20, 90))
        mem_data.pop(0)
        mem_data.append(random.randint(50, 95))
        
        line1.set_data(range(21), cpu_data)
        line2.set_data(range(21), mem_data)
        graph_canvas.draw()
        parent_frame.after(1000, update_graph)
        
    update_graph()
