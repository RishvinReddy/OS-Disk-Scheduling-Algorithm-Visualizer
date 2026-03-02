<<<<<<< HEAD
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import random

DISK_SIZE = 200

# ---------------- Algorithms ----------------
def fcfs(requests, head):
    seq = [head] + requests
    movement = sum(abs(seq[i] - seq[i+1]) for i in range(len(seq)-1))
    return seq, movement

def sstf(requests, head):
    req = requests.copy()
    seq = [head]
    movement = 0

    while req:
        closest = min(req, key=lambda x: abs(x - head))
        movement += abs(head - closest)
        head = closest
        seq.append(head)
        req.remove(closest)

    return seq, movement

def scan(requests, head, direction):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    seq = [head]
    if direction == "Right":
        seq += right + [DISK_SIZE - 1] + left[::-1]
    else:
        seq += left[::-1] + [0] + right

    movement = sum(abs(seq[i] - seq[i+1]) for i in range(len(seq)-1))
    return seq, movement

# ---------------- Graph ----------------
def plot(seq, title):
    plt.figure(figsize=(8, 5))
    plt.plot(seq, range(len(seq)), marker='o')
    plt.gca().invert_yaxis()
    plt.xlabel("Disk Track Number")
    plt.ylabel("Request Order")
    plt.title(title)
    plt.grid()
    plt.show()

# ---------------- Helpers ----------------
def get_requests():
    try:
        return list(map(int, entry_requests.get().split()))
    except:
        messagebox.showerror("Error", "Enter valid disk requests")
        return None

def get_head():
    try:
        return int(entry_head.get())
    except:
        messagebox.showerror("Error", "Enter valid head position")
        return None

# ---------------- Random Generator ----------------
def generate_random():
    try:
        n = int(spin_count.get())
        if n <= 0: raise ValueError
    except:
        n = 8  # Default fallback
    
    requests = random.sample(range(DISK_SIZE), n)
    head = random.randint(0, DISK_SIZE - 1)

    entry_requests.delete(0, tk.END)
    entry_requests.insert(0, " ".join(map(str, requests)))

    entry_head.delete(0, tk.END)
    entry_head.insert(0, str(head))

# ---------------- Run All ----------------
def run_all():
    requests = get_requests()
    head = get_head()
    direction = direction_var.get()

    if requests is None or head is None:
        return

    fcfs_seq, fcfs_mov = fcfs(requests, head)
    sstf_seq, sstf_mov = sstf(requests, head)
    scan_seq, scan_mov = scan(requests, head, direction)

    for row in table.get_children():
        table.delete(row)

    table.insert("", "end", values=("FCFS", fcfs_mov))
    table.insert("", "end", values=("SSTF", sstf_mov))
    table.insert("", "end", values=(f"SCAN ({direction})", scan_mov))

    best = min(fcfs_mov, sstf_mov, scan_mov)
    result_label.config(text=f"Best Algorithm → {best} Head Movements")

    plot(fcfs_seq, "FCFS Disk Scheduling")
    plot(sstf_seq, "SSTF Disk Scheduling")
    plot(scan_seq, f"SCAN Disk Scheduling ({direction})")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Disk Scheduling Algorithm Visualizer")
root.geometry("560x520")

tk.Label(root, text="Disk Requests (space separated):").pack()
entry_requests = tk.Entry(root, width=50)
entry_requests.pack()

tk.Label(root, text="Initial Head Position:").pack()
entry_head = tk.Entry(root, width=20)
entry_head.pack()

# Random Controls
frame_rand = tk.Frame(root)
frame_rand.pack(pady=5)

tk.Label(frame_rand, text="Number of Requests:").pack(side="left")
spin_count = tk.Spinbox(frame_rand, from_=5, to=20, width=5)
spin_count.delete(0, "end")
spin_count.insert(0, 8) # Default value
spin_count.pack(side="left", padx=5)

tk.Button(frame_rand, text="Generate Random Test", command=generate_random).pack(side="left")

# Direction
direction_var = tk.StringVar(value="Right")
tk.Label(root, text="SCAN Direction:").pack()

frame_dir = tk.Frame(root)
frame_dir.pack()

tk.Radiobutton(frame_dir, text="Left", variable=direction_var, value="Left").pack(side="left")
tk.Radiobutton(frame_dir, text="Right", variable=direction_var, value="Right").pack(side="left")

# Run Button
tk.Button(
    root,
    text="Run All Algorithms",
    command=run_all,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
).pack(pady=10)

# Table
table = ttk.Treeview(root, columns=("Algorithm", "Total Head Movement"), show="headings")
table.heading("Algorithm", text="Algorithm")
table.heading("Total Head Movement", text="Total Head Movement")
table.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack()

root.mainloop()
=======
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import random

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

plt.style.use('dark_background') # Apply dark theme to graphs

class DiskSchedulingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Disk Scheduling Algorithm Visualizer")
        self.geometry("1100x700")

        # Grid layout (2 columns)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar
        self.create_sidebar()

        # Create main area
        self.create_main_area()

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Disk Scheduler", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Inputs
        self.req_label = ctk.CTkLabel(self.sidebar_frame, text="Requests (space-sep):", anchor="w")
        self.req_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.entry_requests = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 98 183 37 122")
        self.entry_requests.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.head_label = ctk.CTkLabel(self.sidebar_frame, text="Head Position:", anchor="w")
        self.head_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.entry_head = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 53")
        self.entry_head.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.disk_size_label = ctk.CTkLabel(self.sidebar_frame, text="Disk Size:", anchor="w")
        self.disk_size_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.entry_disk_size = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 200")
        self.entry_disk_size.insert(0, "200")
        self.entry_disk_size.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Random Generator
        self.rand_label = ctk.CTkLabel(self.sidebar_frame, text="Random Requests:", anchor="w")
        self.rand_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.rand_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.rand_frame.grid(row=8, column=0, padx=20, sticky="ew")
        
        self.spin_count = ctk.CTkComboBox(self.rand_frame, values=[str(i) for i in range(5, 21)], width=70)
        self.spin_count.set("8")
        self.spin_count.pack(side="left", padx=(0, 10))
        
        self.btn_rand = ctk.CTkButton(self.rand_frame, text="Generate", width=100, command=self.generate_random)
        self.btn_rand.pack(side="left")

        # Direction
        self.dir_label = ctk.CTkLabel(self.sidebar_frame, text="SCAN Direction:", anchor="w")
        self.dir_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")
        self.direction_var = ctk.StringVar(value="Right")
        self.seg_dir = ctk.CTkSegmentedButton(self.sidebar_frame, values=["Left", "Right"], variable=self.direction_var)
        self.seg_dir.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Run Button
        self.btn_run = ctk.CTkButton(self.sidebar_frame, text="Run Analysis", font=ctk.CTkFont(weight="bold"), command=self.run_analysis)
        self.btn_run.grid(row=11, column=0, padx=20, pady=20, sticky="ew")

    def create_main_area(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.tab_results = self.tabview.add("Results")
        self.tab_fcfs = self.tabview.add("FCFS Graph")
        self.tab_sstf = self.tabview.add("SSTF Graph")
        self.tab_scan = self.tabview.add("SCAN Graph")

        # Results Tab
        self.results_frame = ctk.CTkFrame(self.tab_results, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create a grid for cards
        self.results_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)

        # FCFS Card
        self.card_fcfs = ctk.CTkFrame(self.results_frame, corner_radius=15)
        self.card_fcfs.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.lbl_title_fcfs = ctk.CTkLabel(self.card_fcfs, text="FCFS", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_title_fcfs.pack(pady=(20, 5))
        self.lbl_fcfs = ctk.CTkLabel(self.card_fcfs, text="-", font=ctk.CTkFont(size=24))
        self.lbl_fcfs.pack(pady=(5, 20))

        # SSTF Card
        self.card_sstf = ctk.CTkFrame(self.results_frame, corner_radius=15)
        self.card_sstf.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.lbl_title_sstf = ctk.CTkLabel(self.card_sstf, text="SSTF", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_title_sstf.pack(pady=(20, 5))
        self.lbl_sstf = ctk.CTkLabel(self.card_sstf, text="-", font=ctk.CTkFont(size=24))
        self.lbl_sstf.pack(pady=(5, 20))

        # SCAN Card
        self.card_scan = ctk.CTkFrame(self.results_frame, corner_radius=15)
        self.card_scan.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.lbl_title_scan = ctk.CTkLabel(self.card_scan, text="SCAN", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_title_scan.pack(pady=(20, 5))
        self.lbl_scan = ctk.CTkLabel(self.card_scan, text="-", font=ctk.CTkFont(size=24))
        self.lbl_scan.pack(pady=(5, 20))

        self.lbl_best = ctk.CTkLabel(self.results_frame, text="Best Algorithm: -", font=ctk.CTkFont(size=20, weight="bold"), text_color="#00FF00")
        self.lbl_best.grid(row=1, column=0, columnspan=3, pady=(30, 10))
        
    def get_disk_size(self):
        try:
            return int(self.entry_disk_size.get())
        except ValueError:
            return 200

    def generate_random(self):
        try:
            n = int(self.spin_count.get())
        except:
            n = 8
        
        disk_size = self.get_disk_size()
        requests = random.sample(range(disk_size), n)
        head = random.randint(0, disk_size - 1)

        self.entry_requests.delete(0, tk.END)
        self.entry_requests.insert(0, " ".join(map(str, requests)))

        self.entry_head.delete(0, tk.END)
        self.entry_head.insert(0, str(head))

    # ---------------- Algorithms ----------------
    def fcfs(self, requests, head):
        seq = [head] + requests
        movement = sum(abs(seq[i] - seq[i+1]) for i in range(len(seq)-1))
        return seq, movement

    def sstf(self, requests, head):
        req = requests.copy()
        seq = [head]
        movement = 0

        while req:
            closest = min(req, key=lambda x: abs(x - head))
            movement += abs(head - closest)
            head = closest
            seq.append(head)
            req.remove(closest)

        return seq, movement

    def scan(self, requests, head, direction):
        left = sorted([r for r in requests if r < head])
        right = sorted([r for r in requests if r >= head])
        disk_size = self.get_disk_size()

        seq = [head]
        if direction == "Right":
            seq += right + [disk_size - 1] + left[::-1]
        else:
            seq += left[::-1] + [0] + right

        movement = sum(abs(seq[i] - seq[i+1]) for i in range(len(seq)-1))
        return seq, movement

    def plot_graph(self, seq, title, parent_frame):
        # Clear previous widgets in the tab
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Create Figure
        fig = plt.Figure(figsize=(6, 5), dpi=100)
        # Match matplotlib chart inner face to the dark customtkinter theme
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#242424')
        
        ax.plot(seq, range(len(seq)), marker='o', linestyle='-', color='#1f6aa5', markerfacecolor='#1f6aa5', markersize=8, linewidth=2) 
        
        # Add Annotations
        for i, txt in enumerate(seq):
            if i == 0:
                ax.annotate(f"Start\n({txt})", (txt, i), textcoords="offset points", xytext=(0,10), ha='center', color='#00FF00', fontsize=9, weight='bold')
            else:
                ax.annotate(str(txt), (txt, i), textcoords="offset points", xytext=(0,10), ha='center', color='white', fontsize=8)

        ax.invert_yaxis()
        ax.set_title(title, color='white', pad=20)
        ax.set_xlabel("Disk Track Number", color='#a0a0a0')
        ax.set_ylabel("Request Order", color='#a0a0a0')
        ax.tick_params(colors='#a0a0a0')
        ax.spines['bottom'].set_color('#555555')
        ax.spines['top'].set_color('#555555') 
        ax.spines['right'].set_color('#555555')
        ax.spines['left'].set_color('#555555')
        ax.grid(True, color='#444444', linestyle='--', alpha=0.7)

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        
        # Add Toolbar
        toolbar_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        toolbar_frame.pack(side="bottom", fill="x", padx=10, pady=5)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        toolbar.config(background='#2b2b2b')
        for button in toolbar.winfo_children():
            try:
                button.config(background='#2b2b2b')
            except:
                pass
                
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def run_analysis(self):
        try:
            req_str = self.entry_requests.get()
            if not req_str:
                messagebox.showerror("Error", "Please enter requests!")
                return
            requests = list(map(int, req_str.split()))
            head = int(self.entry_head.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Input! Please enter numbers.")
            return

        direction = self.direction_var.get()

        # Run Algorithms
        fcfs_seq, fcfs_mov = self.fcfs(requests, head)
        sstf_seq, sstf_mov = self.sstf(requests, head)
        scan_seq, scan_mov = self.scan(requests, head, direction)

        # Update Results
        self.lbl_fcfs.configure(text=f"{fcfs_mov}\nMovements")
        self.lbl_sstf.configure(text=f"{sstf_mov}\nMovements")
        self.lbl_scan.configure(text=f"{scan_mov}\nMovements")

        best_mov = min(fcfs_mov, sstf_mov, scan_mov)
        
        # Reset colors
        self.card_fcfs.configure(border_width=0)
        self.card_sstf.configure(border_width=0)
        self.card_scan.configure(border_width=0)

        best_algos = []
        if fcfs_mov == best_mov: 
            best_algos.append("FCFS")
            self.card_fcfs.configure(border_width=2, border_color="#00FF00")
        if sstf_mov == best_mov: 
            best_algos.append("SSTF")
            self.card_sstf.configure(border_width=2, border_color="#00FF00")
        if scan_mov == best_mov: 
            best_algos.append("SCAN")
            self.card_scan.configure(border_width=2, border_color="#00FF00")
        
        self.lbl_best.configure(text=f"Best Algorithm: {', '.join(best_algos)} ({best_mov} Head Movements)")

        # Plot Graphs
        self.plot_graph(fcfs_seq, "FCFS Disk Scheduling", self.tab_fcfs)
        self.plot_graph(sstf_seq, "SSTF Disk Scheduling", self.tab_sstf)
        self.plot_graph(scan_seq, f"SCAN Disk Scheduling ({direction})", self.tab_scan)
        
        # Focus on results
        self.tabview.set("Results")

if __name__ == "__main__":
    app = DiskSchedulingApp()
    app.mainloop()
>>>>>>> 71fd2fa (Initial commit for Talensync OS Simulation Engine)
