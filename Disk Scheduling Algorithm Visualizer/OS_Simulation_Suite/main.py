import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import threading

from disk.algorithms import run_algorithm
from disk.metrics import calculate_metrics
from disk.comparison import compare_all_algorithms
from disk.animation import animate_disk
from deadlock.rag import draw_rag
from smart_manufacturing.factory_sim import simulate_factory_deadlock
from synchronization.mutex_demo import simulate_mutex
from reports.pdf_export import export_pdf
from splash import show_splash
from architecture_dashboard import create_architecture_tab, push_log
from cpu_scheduling import create_cpu_tab
from filesystem_simulation import create_filesystem_tab
from process_states import create_process_state_tab

# Config
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Theme Colors based on screenshot
BG_COLOR = "#F4F7F9"
SIDEBAR_COLOR = "#FFFFFF"
CARD_COLOR = "#FFFFFF"
TEXT_PRIMARY = "#111827"
TEXT_SECONDARY = "#6B7280"
ACCENT_BLUE = "#0ea5e9"
ACCENT_LIGHT_BLUE = "#e0f2fe"

class OSSimulationSuite(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Talensync OS Simulation Engine")
        self.geometry("1400x850")
        self.configure(fg_color=BG_COLOR)

        # Main Grid Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.current_metrics = {}

        self.setup_sidebar()
        self.setup_main_content()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=SIDEBAR_COLOR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        # Logo Area
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(30, 40), sticky="w")
        
        logo_icon = ctk.CTkLabel(logo_frame, text="⚡", font=ctk.CTkFont(size=24), fg_color="#1E3A8A", text_color="white", corner_radius=8, width=40, height=40)
        logo_icon.pack(side="left")
        
        logo_texts = ctk.CTkFrame(logo_frame, fg_color="transparent")
        logo_texts.pack(side="left", padx=10)
        ctk.CTkLabel(logo_texts, text="talensync", font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(logo_texts, text="OS Management", font=ctk.CTkFont(size=10), text_color=TEXT_SECONDARY).pack(anchor="w")

        # Nav Buttons
        self.nav_btns = []
        self.btn_arch = self.create_nav_btn("🧩 Dashboard", 0, self.show_arch)
        self.btn_disk = self.create_nav_btn("📀 Disk I/O", 1, self.show_disk)
        self.btn_deadlock = self.create_nav_btn("📊 Deadlocks", 2, self.show_deadlock)
        self.btn_factory = self.create_nav_btn("🏭 Factory Sim", 3, self.show_factory)
        self.btn_sync = self.create_nav_btn("⚙️ Process Sync", 4, self.show_sync)
        self.btn_cpu = self.create_nav_btn("🖥 CPU Sched", 5, self.show_cpu)
        self.btn_fs = self.create_nav_btn("📁 File System", 6, self.show_fs)
        self.btn_states = self.create_nav_btn("🔄 Process States", 7, self.show_states)
        
        # Bottom Profile Simulation
        profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_frame.grid(row=9, column=0, padx=20, pady=30, sticky="ew")
        ctk.CTkLabel(profile_frame, text="👤", font=ctk.CTkFont(size=24)).pack(side="left")
        p_texts = ctk.CTkFrame(profile_frame, fg_color="transparent")
        p_texts.pack(side="left", padx=10)
        ctk.CTkLabel(p_texts, text="Rishvin Reddy", font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(p_texts, text="rishvin@mail.com", font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY).pack(anchor="w")

    def create_nav_btn(self, text, row, command):
        btn = ctk.CTkButton(self.sidebar, text=text, font=ctk.CTkFont(size=14, weight="bold"), 
                            fg_color="transparent", text_color=TEXT_SECONDARY, hover_color=BG_COLOR,
                            anchor="w", height=45, corner_radius=8, command=command)
        btn.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        self.nav_btns.append(btn)
        return btn

    def select_nav(self, selected_btn, title):
        for btn in self.nav_btns:
            btn.configure(fg_color="transparent", text_color=TEXT_SECONDARY)
        selected_btn.configure(fg_color=ACCENT_LIGHT_BLUE, text_color=ACCENT_BLUE)
        self.header_title.configure(text=title)

    def setup_main_content(self):
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_content.grid_rowconfigure(1, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_title = ctk.CTkLabel(header_frame, text="Overview", font=ctk.CTkFont(size=28, weight="bold"), text_color=TEXT_PRIMARY)
        self.header_title.pack(side="left")

        # Top Right Notifications/Icons placeholder
        ctk.CTkLabel(header_frame, text="🔍  🔔  ❓", font=ctk.CTkFont(size=18), text_color=TEXT_SECONDARY).pack(side="right")

        # Pages Container
        self.pages_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.pages_container.grid(row=1, column=0, sticky="nsew")
        self.pages_container.grid_rowconfigure(0, weight=1)
        self.pages_container.grid_columnconfigure(0, weight=1)

        # Pages
        self.page_arch = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.page_disk = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.page_deadlock = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.page_factory = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.page_sync = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.page_cpu = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.page_fs = ctk.CTkFrame(self.pages_container, fg_color="transparent")
        self.page_states = ctk.CTkFrame(self.pages_container, fg_color="transparent")

        for page in (self.page_arch, self.page_disk, self.page_deadlock, self.page_factory, self.page_sync, self.page_cpu, self.page_fs, self.page_states):
            page.grid(row=0, column=0, sticky="nsew")

        self.setup_arch_page()
        self.setup_disk_page()
        self.setup_deadlock_page()
        self.setup_factory_page()
        self.setup_sync_page()
        self.setup_cpu_page()
        self.setup_fs_page()
        self.setup_states_page()

        self.show_arch()

    # ----------------------------------------------------
    # TAB 1: Disk Dashboard Layout
    # ----------------------------------------------------
    def setup_disk_page(self):
        self.page_disk.grid_rowconfigure(1, weight=1)
        self.page_disk.grid_columnconfigure(0, weight=3)
        self.page_disk.grid_columnconfigure(1, weight=1)

        # TOP KPI CARDS
        kpi_frame = ctk.CTkFrame(self.page_disk, fg_color="transparent")
        kpi_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        kpi_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.kpi_total = self.create_kpi_card(kpi_frame, "Total Seek Time", "0", 0)
        self.kpi_avg = self.create_kpi_card(kpi_frame, "Avg Seek Time", "0.0", 1)
        self.kpi_var = self.create_kpi_card(kpi_frame, "Variance", "0.0", 2)
        self.kpi_best = self.create_kpi_card(kpi_frame, "Best Algorithm", "-", 3)

        # CENTER CHART
        chart_card = ctk.CTkFrame(self.page_disk, fg_color=CARD_COLOR, corner_radius=12)
        chart_card.grid(row=1, column=0, sticky="nsew", padx=(0, 20))
        
        ctk.CTkLabel(chart_card, text="Head Movement Trends", font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT_PRIMARY, anchor="w").pack(fill="x", padx=20, pady=(20, 0))
        self.disk_canvas_frame = ctk.CTkFrame(chart_card, fg_color="transparent")
        self.disk_canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # RIGHT CONTROLS
        controls_card = ctk.CTkFrame(self.page_disk, fg_color=CARD_COLOR, corner_radius=12)
        controls_card.grid(row=1, column=1, sticky="nsew")
        
        ctk.CTkLabel(controls_card, text="Simulation Controls", font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT_PRIMARY, anchor="w").pack(fill="x", padx=20, pady=(20, 10))

        # Inputs
        ctk.CTkLabel(controls_card, text="Algorithm", text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=12), anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.algo_var = ctk.StringVar(value="FCFS")
        ctk.CTkComboBox(controls_card, values=["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"], variable=self.algo_var, fg_color="#F9FAFB", border_color="#E5E7EB", text_color=TEXT_PRIMARY).pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(controls_card, text="Disk Requests", text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=12), anchor="w").pack(fill="x", padx=20)
        self.entry_req = ctk.CTkEntry(controls_card, placeholder_text="98 183 37 122", fg_color="#F9FAFB", border_color="#E5E7EB", text_color=TEXT_PRIMARY)
        self.entry_req.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(controls_card, text="Head Position", text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=12), anchor="w").pack(fill="x", padx=20)
        self.entry_head = ctk.CTkEntry(controls_card, placeholder_text="53", fg_color="#F9FAFB", border_color="#E5E7EB", text_color=TEXT_PRIMARY)
        self.entry_head.pack(fill="x", padx=20, pady=(5, 20))

        # Buttons
        ctk.CTkButton(controls_card, text="↻ Random Data", fg_color=BG_COLOR, text_color=TEXT_PRIMARY, hover_color="#E5E7EB", command=self.populate_random).pack(fill="x", padx=20, pady=5)
        
        # Simulation Controls
        sim_frame = ctk.CTkFrame(controls_card, fg_color="transparent")
        sim_frame.pack(fill="x", padx=20, pady=(10, 5))
        sim_frame.grid_columnconfigure((0,1,2), weight=1)
        
        ctk.CTkButton(sim_frame, text="▶ Start", fg_color="#10B981", hover_color="#059669", width=60, command=self.run_disk_sim).grid(row=0, column=0, padx=(0,5))
        ctk.CTkButton(sim_frame, text="⏸ Pause", fg_color="#F59E0B", hover_color="#D97706", width=60, command=self.pause_sim).grid(row=0, column=1, padx=5)
        ctk.CTkButton(sim_frame, text="⏹ Stop", fg_color="#EF4444", hover_color="#DC2626", width=60, command=self.stop_sim).grid(row=0, column=2, padx=(5,0))

        # Speed Slider
        ctk.CTkLabel(controls_card, text="Animation Speed", text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=11), anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        self.speed_slider = ctk.CTkSlider(controls_card, from_=100, to=1500, command=self.update_speed, button_color=ACCENT_BLUE)
        self.speed_slider.set(600)
        self.speed_slider.pack(fill="x", padx=20, pady=(5, 10))
        
        ctk.CTkFrame(controls_card, height=1, fg_color="#E5E7EB").pack(fill="x", padx=20, pady=15)
        
        ctk.CTkButton(controls_card, text="📊 Compare All", fg_color="#1F4ED8", hover_color="#1D4ED8", command=self.run_comparison).pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(controls_card, text="📄 Export PDF", fg_color="#6B7280", hover_color="#4B5563", command=self.export_report).pack(fill="x", padx=20, pady=5)

    def create_kpi_card(self, parent, title, value, col):
        card = ctk.CTkFrame(parent, fg_color=CARD_COLOR, corner_radius=12)
        card.grid(row=0, column=col, sticky="ew", padx=10 if col > 0 else (0, 10))
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13), text_color=TEXT_SECONDARY).pack(anchor="w", padx=20, pady=(15, 5))
        lbl_val = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color=TEXT_PRIMARY)
        lbl_val.pack(anchor="w", padx=20, pady=(0, 15))
        return lbl_val

    def show_disk(self):
        self.select_nav(self.btn_disk, "Disk I/O Management")
        self.page_disk.tkraise()

    def setup_arch_page(self):
        self.page_arch.grid_rowconfigure(0, weight=1)
        self.page_arch.grid_columnconfigure(0, weight=1)
        
        callbacks = {
            "cpu": self.show_cpu,
            "sync": self.show_sync,
            "deadlock": self.show_deadlock,
            "fs": self.show_fs,
            "disk": self.show_disk,
            "factory": self.show_factory
        }
        create_architecture_tab(self.page_arch, callbacks)
        
    def show_arch(self):
        self.select_nav(self.btn_arch, "OS Architecture & Core Dashboard")
        self.page_arch.tkraise()

    def populate_random(self):
        reqs = random.sample(range(200), 8)
        head = random.randint(0, 199)
        self.entry_req.delete(0, tk.END)
        self.entry_req.insert(0, " ".join(map(str, reqs)))
        self.entry_head.delete(0, tk.END)
        self.entry_head.insert(0, str(head))

    def get_inputs(self):
        try:
            reqs = list(map(int, self.entry_req.get().split()))
            head = int(self.entry_head.get())
            return reqs, head
        except ValueError:
            messagebox.showerror("Input Error", "Please provide space-separated integers for requests and a valid integer for the head.")
            return None, None

    def pause_sim(self):
        from disk.animation import get_paused, set_paused
        set_paused(not get_paused())

    def stop_sim(self):
        from disk.animation import set_running
        set_running(False)
        for widget in self.disk_canvas_frame.winfo_children():
            widget.destroy()

    def update_speed(self, value):
        from disk.animation import set_speed
        # reverse value so right is faster (lower ms)
        inverted = 1600 - value
        set_speed(inverted)

    def run_disk_sim(self):
        reqs, head = self.get_inputs()
        if reqs is None: return
        
        algo = self.algo_var.get()
        push_log("DISK", f"Running {algo} simulation with head at {head}...")
        
        sequence = run_algorithm(algo, reqs, head)
        metrics = calculate_metrics(sequence)
        self.current_metrics = metrics
        
        self.kpi_total.configure(text=str(metrics["Total Seek"]))
        self.kpi_avg.configure(text=str(metrics["Average Seek"]))
        self.kpi_var.configure(text=str(metrics["Variance"]))
        self.kpi_best.configure(text=algo)
            
        animate_disk(sequence, algo, self.disk_canvas_frame)

    def run_comparison(self):
        reqs, head = self.get_inputs()
        if reqs is None: return
        
        # Stop any active disk head animation and clear canvas
        self.stop_sim()
            
        results = compare_all_algorithms(reqs, head, self.disk_canvas_frame)
        self.kpi_best.configure(text=min(results, key=results.get))
        
        # Add animated text box to right controls for the ranked results overlaying the empty space in this tab
        # or we just use a tiny text box embedded inside
        sorted_algos = sorted(results.items(), key=lambda x: x[1])
        
        # We will render the animated ranking onto the disk_canvas_frame directly
        self.disk_canvas_frame.update()
        w = self.disk_canvas_frame.winfo_width()
        h = self.disk_canvas_frame.winfo_height()
        cv = tk.Canvas(self.disk_canvas_frame, bg="#FFFFFF", highlightthickness=0)
        cv.pack(fill="both", expand=True)
        cv.create_text(w/2, 40, text="🏆 ALGORITHM RANKING", font=("Arial", 16, "bold"), fill="#111827")
        
        def reveal(index=0):
            if index < len(sorted_algos):
                algo, val = sorted_algos[index]
                y_pos = 90 + (index * 35)
                
                # Draw bar container
                cv.create_rectangle(w/2 - 150, y_pos - 15, w/2 + 150, y_pos + 15, fill="#F9FAFB", outline="#E5E7EB", width=1, corner_radius=5 if hasattr(cv, "corner_radius") else 0)
                
                # Draw text inside bar
                cv.create_text(w/2 - 130, y_pos, text=f"#{index+1}  {algo}", font=("Arial", 12, "bold"), fill=ACCENT_BLUE, anchor="w")
                cv.create_text(w/2 + 130, y_pos, text=f"{int(val)} sequences", font=("Arial", 11), fill=TEXT_SECONDARY, anchor="e")
                
                self.after(400, lambda: reveal(index + 1))
        
        reveal()

    def export_report(self):
        if not self.current_metrics:
            messagebox.showwarning("No Data", "Please run a simulation first to export a report.")
            return
        export_pdf(self.current_metrics)
        
    def setup_cpu_page(self):
        self.page_cpu.grid_rowconfigure(0, weight=1)
        self.page_cpu.grid_columnconfigure(0, weight=1)
        create_cpu_tab(self.page_cpu)
        
    def show_cpu(self):
        self.select_nav(self.btn_cpu, "Process Management")
        self.page_cpu.tkraise()

    def setup_fs_page(self):
        self.page_fs.grid_rowconfigure(0, weight=1)
        self.page_fs.grid_columnconfigure(0, weight=1)
        create_filesystem_tab(self.page_fs)
        
    def show_fs(self):
        self.select_nav(self.btn_fs, "Disk File System Allocation")
        self.page_fs.tkraise()

    def setup_states_page(self):
        self.page_states.grid_rowconfigure(0, weight=1)
        self.page_states.grid_columnconfigure(0, weight=1)
        create_process_state_tab(self.page_states)

    def show_states(self):
        self.select_nav(self.btn_states, "Process Lifecycle States")
        self.page_states.tkraise()

    # ----------------------------------------------------
    # TAB 2: Deadlock Page
    # ----------------------------------------------------
    def setup_deadlock_page(self):
        self.page_deadlock.grid_rowconfigure(0, weight=1)
        self.page_deadlock.grid_columnconfigure(0, weight=1)
        self.page_deadlock.grid_columnconfigure(1, weight=3)

        controls = ctk.CTkFrame(self.page_deadlock, fg_color=CARD_COLOR, corner_radius=12)
        controls.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        self.rag_frame = ctk.CTkFrame(self.page_deadlock, fg_color=CARD_COLOR, corner_radius=12)
        self.rag_frame.grid(row=0, column=1, sticky="nsew")
        
        ctk.CTkLabel(controls, text="Process Actions", font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT_PRIMARY, anchor="w").pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkButton(controls, text="Simulate Safe State", fg_color="#10B981", hover_color="#059669", command=lambda: self.run_rag(safe=True)).pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(controls, text="Simulate Deadlock", fg_color="#EF4444", hover_color="#DC2626", command=lambda: self.run_rag(safe=False)).pack(fill="x", padx=20, pady=10)

        ctk.CTkFrame(controls, height=1, fg_color="#E5E7EB").pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(controls, text="Banker's Algorithm", font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT_PRIMARY, anchor="w").pack(fill="x", padx=20, pady=(10, 10))
        ctk.CTkButton(controls, text="Run Animated Steps", fg_color=ACCENT_BLUE, hover_color="#0284c7", command=self.run_bankers).pack(fill="x", padx=20, pady=10)

        self.matrix_frame = ctk.CTkFrame(controls, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E5E7EB")
        self.matrix_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        self.lbl_banker_status = ctk.CTkLabel(self.matrix_frame, text="Ready", font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_PRIMARY)
        self.lbl_banker_status.pack(pady=5)
        
        self.lbl_work_vec = ctk.CTkLabel(self.matrix_frame, text="Work Vector: []", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY)
        self.lbl_work_vec.pack()
        
        self.grid_container = ctk.CTkFrame(self.matrix_frame, fg_color="transparent")
        self.grid_container.pack(expand=True, pady=10)

    def show_deadlock(self):
        self.select_nav(self.btn_deadlock, "Deadlock Detection & Analysis")
        self.page_deadlock.tkraise()

    def run_rag(self, safe):
        processes = ["P1", "P2", "P3"]
        resources = ["R1", "R2"]
        if safe:
            edges = [("P1", "R1"), ("R1", "P2"), ("R2", "P3")]
        else:
            edges = [("P1", "R1"), ("R1", "P2"), ("P2", "R2"), ("R2", "P1")]
        draw_rag(processes, resources, edges, self.rag_frame)

    def run_bankers(self):
        push_log("BANKER", "Calculating Safe State Matrices (Allocation/Need/Available)")
        self.lbl_banker_status.configure(text="Initializing...", text_color=TEXT_PRIMARY)
        for widget in self.grid_container.winfo_children():
            widget.destroy()
            
        def update_output(state):
            # Must run UI updates in main thread if possible, but CustomTkinter handles thread updates decently well
            # if we don't trigger massive layout shifts, or we can use `self.after(0, ...)`
            def ui_tick():
                if state["type"] == "init":
                    self.lbl_work_vec.configure(text=f"Work Vector: {state['work']}")
                    self.lbl_banker_status.configure(text="Checking Processes", text_color=ACCENT_BLUE)
                    
                    # Create Header
                    for c, title in enumerate(["Proc", "Alloc", "Need", "Status"]):
                        ctk.CTkLabel(self.grid_container, text=title, font=ctk.CTkFont(weight="bold")).grid(row=0, column=c, padx=5, pady=2)
                        
                    self.row_labels = {}
                    for i in range(len(state["alloc"])):
                        l_p = ctk.CTkLabel(self.grid_container, text=f"P{i}", width=40)
                        l_p.grid(row=i+1, column=0, pady=2)
                        l_a = ctk.CTkLabel(self.grid_container, text=str(state["alloc"][i]))
                        l_a.grid(row=i+1, column=1, padx=5, pady=2)
                        l_n = ctk.CTkLabel(self.grid_container, text=str(state["need"][i]))
                        l_n.grid(row=i+1, column=2, padx=5, pady=2)
                        l_s = ctk.CTkLabel(self.grid_container, text="Wait", text_color=TEXT_SECONDARY, fg_color="#F3F4F6", corner_radius=4)
                        l_s.grid(row=i+1, column=3, padx=5, pady=2)
                        self.row_labels[i] = {"proc": l_p, "status": l_s}
                        
                elif state["type"] == "checking":
                    self.lbl_banker_status.configure(text=f"Evaluating P{state['proc']}", text_color=ACCENT_BLUE)
                    self.row_labels[state['proc']]["status"].configure(text="Checking", fg_color="#FEF3C7", text_color="#D97706") # Yellow
                    
                elif state["type"] == "finished_step":
                    self.lbl_work_vec.configure(text=f"Work Vector: {state['work']}")
                    self.row_labels[state['proc']]["status"].configure(text="Done", fg_color="#D1FAE5", text_color="#059669") # Green
                    
                elif state["type"] == "success":
                    self.lbl_banker_status.configure(text=f"SAFE STATE\n{' -> '.join(state['sequence'])}", text_color="#10B981")
                    
                elif state["type"] == "deadlock":
                    self.lbl_banker_status.configure(text="UNSAFE STATE - DEADLOCK", text_color="#EF4444")
                    for i, fin in enumerate(state["finish"]):
                        if not fin:
                            self.row_labels[i]["status"].configure(text="Blocked", fg_color="#FEE2E2", text_color="#DC2626") # Red
                            
            self.after(0, ui_tick)
            
        def worker():
            from deadlock.bankers import bankers_with_steps
            available = [3,3,2]
            max_matrix = [[7,5,3],[3,2,2],[9,0,2]]
            allocation = [[0,1,0],[2,0,0],[3,0,2]]
            bankers_with_steps(available, max_matrix, allocation, update_output)
            
        threading.Thread(target=worker, daemon=True).start()

    # ----------------------------------------------------
    # TAB 3: Factory Layout
    # ----------------------------------------------------
    def setup_factory_page(self):
        self.page_factory.grid_rowconfigure(0, weight=1)
        self.page_factory.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self.page_factory, fg_color=CARD_COLOR, corner_radius=12)
        card.grid(row=0, column=0, sticky="nsew")
        card.grid_rowconfigure(1, weight=1)
        card.grid_columnconfigure(0, weight=1)

        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        ctk.CTkLabel(top_frame, text="Smart Factory Deadlock Simulation", font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_PRIMARY).pack(side="left")
        
        canvas_frame = ctk.CTkFrame(card, fg_color="transparent")
        canvas_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        ctk.CTkButton(top_frame, text="Wait/Trigger Deadlock", fg_color="#EF4444", hover_color="#DC2626", command=lambda: simulate_factory_deadlock(canvas_frame)).pack(side="right")

    def show_factory(self):
        self.select_nav(self.btn_factory, "Factory Hardware Monitoring")
        self.page_factory.tkraise()

    # ----------------------------------------------------
    # TAB 4: Sync Layout
    # ----------------------------------------------------
    def setup_sync_page(self):
        self.page_sync.grid_rowconfigure(0, weight=1)
        self.page_sync.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self.page_sync, fg_color=CARD_COLOR, corner_radius=12)
        card.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(card, text="Mutex Synchronization Terminal", font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_PRIMARY, anchor="w").pack(fill="x", padx=30, pady=(30, 20))

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(0, 20))
        ctk.CTkButton(btn_frame, text="Run Safe (Mutex Enabled)", fg_color="#10B981", hover_color="#059669", command=lambda: simulate_mutex(log_box, use_mutex=True)).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_frame, text="Run Unsafe (Race Condition)", fg_color="#EF4444", hover_color="#DC2626", command=lambda: simulate_mutex(log_box, use_mutex=False)).pack(side="left")

        log_box = tk.Text(card, font=("Courier", 13), bg="#111827", fg="#10B981", relief="flat", highlightthickness=0)
        log_box.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    def show_sync(self):
        self.select_nav(self.btn_sync, "Process Synchronization Terminal")
        self.page_sync.tkraise()


if __name__ == "__main__":
    app = OSSimulationSuite()
    app.withdraw()
    show_splash(app)
    app.deiconify()
    app.mainloop()
