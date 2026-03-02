import customtkinter as ctk
import tkinter as tk

def create_process_state_tab(parent_frame):
    card = ctk.CTkFrame(parent_frame, fg_color="#FFFFFF", corner_radius=12)
    card.grid(row=0, column=0, sticky="nsew")
    card.grid_rowconfigure(1, weight=1)
    card.grid_columnconfigure(0, weight=1)

    top_frame = ctk.CTkFrame(card, fg_color="transparent")
    top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
    ctk.CTkLabel(top_frame, text="OS Process Lifecycle Diagram", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111827").pack(side="left")

    canvas_frame = ctk.CTkFrame(card, fg_color="transparent")
    canvas_frame.grid(row=1, column=0, sticky="nsew", padx=20)
    
    cv = tk.Canvas(canvas_frame, bg="#F9FAFB", highlightthickness=1, highlightbackground="#E5E7EB")
    cv.pack(fill="both", expand=True, pady=10)

    # State positions
    states = {
        "New": (150, 200),
        "Ready": (400, 200),
        "Running": (650, 200),
        "Waiting": (400, 350),
        "Terminated": (850, 200)
    }

    def draw_bg():
        # Draw Arrows between states
        cv.create_line(states["New"][0]+50, states["New"][1], states["Ready"][0]-50, states["Ready"][1], arrow=tk.LAST, width=3, fill="#9CA3AF")
        cv.create_line(states["Ready"][0]+50, states["Ready"][1]-10, states["Running"][0]-50, states["Running"][1]-10, arrow=tk.LAST, width=3, fill="#9CA3AF")
        cv.create_line(states["Running"][0]-50, states["Running"][1]+10, states["Ready"][0]+50, states["Ready"][1]+10, arrow=tk.LAST, width=3, fill="#9CA3AF", dash=(4,2))
        cv.create_line(states["Running"][0]+50, states["Running"][1], states["Terminated"][0]-50, states["Terminated"][1], arrow=tk.LAST, width=3, fill="#9CA3AF")
        
        cv.create_line(states["Running"][0], states["Running"][1]+50, states["Waiting"][0]+50, states["Waiting"][1], arrow=tk.LAST, width=3, fill="#9CA3AF")
        cv.create_line(states["Waiting"][0], states["Waiting"][1]-50, states["Ready"][0], states["Ready"][1]+50, arrow=tk.LAST, width=3, fill="#9CA3AF")

        # Draw State nodes
        for state, (x, y) in states.items():
            cv.create_oval(x-50, y-50, x+50, y+50, fill="#FFFFFF", outline="#3B82F6", width=3)
            cv.create_text(x, y, text=state, font=("Arial", 12, "bold"), fill="#1F2937")

    parent_frame.after(100, draw_bg)
    process_token = None
    
    def reset_process():
        nonlocal process_token
        if process_token:
            cv.delete(process_token)
            cv.delete("p_text")
        start_x, start_y = states["New"]
        process_token = cv.create_oval(start_x-20, start_y-20, start_x+20, start_y+20, fill="#10B981", outline="#059669", width=2)
        cv.create_text(start_x, start_y, text="P1", tags="p_text", font=("Arial", 10, "bold"), fill="white")

    parent_frame.after(200, reset_process)

    def move_to(state):
        x, y = states[state]
        cv.coords(process_token, x-20, y-20, x+20, y+20)
        cv.coords("p_text", x, y)

    def simulate_lifecycle():
        reset_process()
        states_order = ["Ready", "Running", "Waiting", "Ready", "Running", "Terminated"]
        index = 0

        def step():
            nonlocal index
            if index < len(states_order):
                move_to(states_order[index])
                index += 1
                parent_frame.after(1200, step)

        parent_frame.after(800, step)

    btn_frame = ctk.CTkFrame(card, fg_color="transparent")
    btn_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
    
    ctk.CTkButton(btn_frame, text="Manual: New → Ready", fg_color="#6B7280", command=lambda: move_to("Ready")).grid(row=0, column=0, padx=5, pady=5)
    ctk.CTkButton(btn_frame, text="Manual: Ready → Running", fg_color="#6B7280", command=lambda: move_to("Running")).grid(row=0, column=1, padx=5, pady=5)
    ctk.CTkButton(btn_frame, text="Manual: Running → Waiting", fg_color="#6B7280", command=lambda: move_to("Waiting")).grid(row=0, column=2, padx=5, pady=5)
    ctk.CTkButton(btn_frame, text="Manual: Waiting → Ready", fg_color="#6B7280", command=lambda: move_to("Ready")).grid(row=1, column=0, padx=5, pady=5)
    ctk.CTkButton(btn_frame, text="Manual: Running → Terminated", fg_color="#6B7280", command=lambda: move_to("Terminated")).grid(row=1, column=1, padx=5, pady=5)
    
    ctk.CTkFrame(btn_frame, width=2, fg_color="#E5E7EB").grid(row=0, column=3, rowspan=2, sticky="ns", padx=15)
    
    ctk.CTkButton(btn_frame, text="▶ Auto Simulate Full Lifecycle", fg_color="#3B82F6", hover_color="#2563EB", height=40, font=ctk.CTkFont(weight="bold"), command=simulate_lifecycle).grid(row=0, column=4, rowspan=2, padx=5)
