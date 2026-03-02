import tkinter as tk

def simulate_factory_deadlock(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(parent_frame, bg="#FFFFFF", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.update()
    
    w = canvas.winfo_width()
    if w < 100: w = 600

    # Draw resources
    canvas.create_rectangle(w/2 - 50, 50, w/2 + 50, 100, fill="#FCA5A5", outline="#EF4444", width=2)
    canvas.create_text(w/2, 75, text="Conveyor (R1)", font=("Arial", 12, "bold"), fill="#7F1D1D")

    canvas.create_rectangle(w/2 - 50, 300, w/2 + 50, 350, fill="#FCA5A5", outline="#EF4444", width=2)
    canvas.create_text(w/2, 325, text="CNC (R2)", font=("Arial", 12, "bold"), fill="#7F1D1D")

    # Draw processes
    canvas.create_oval(w/4 - 40, 175 - 40, w/4 + 40, 175 + 40, fill="#86EFAC", outline="#22C55E", width=2)
    canvas.create_text(w/4, 175, text="Robot 1", font=("Arial", 12, "bold"), fill="#14532D")

    canvas.create_oval(w*3/4 - 40, 175 - 40, w*3/4 + 40, 175 + 40, fill="#86EFAC", outline="#22C55E", width=2)
    canvas.create_text(w*3/4, 175, text="Robot 2", font=("Arial", 12, "bold"), fill="#14532D")

    def step1():
        canvas.create_line(w/4 + 20, 145, w/2 - 20, 95, arrow=tk.LAST, width=3, fill="#3B82F6")
        canvas.create_text(w*3/8, 110, text="Holds", font=("Arial", 10), fill="#3B82F6")
        
    def step2():
        canvas.create_line(w/2 + 20, 95, w*3/4 - 20, 145, arrow=tk.LAST, width=3, fill="#EF4444", dash=(4, 2))
        canvas.create_text(w*5/8, 110, text="Requests", font=("Arial", 10), fill="#EF4444")
        
    def step3():
        canvas.create_line(w*3/4 - 20, 205, w/2 + 20, 305, arrow=tk.LAST, width=3, fill="#3B82F6")
        canvas.create_text(w*5/8, 260, text="Holds", font=("Arial", 10), fill="#3B82F6")
        
    def step4():
        canvas.create_line(w/2 - 20, 305, w/4 + 20, 205, arrow=tk.LAST, width=3, fill="#EF4444", dash=(4, 2))
        canvas.create_text(w*3/8, 260, text="Requests", font=("Arial", 10), fill="#EF4444")
        
    def show_alert():
        canvas.create_text(w/2, 200, text="⚠ DEADLOCK DETECTED ⚠", font=("Arial", 16, "bold"), fill="#DC2626")
        canvas.create_text(w/2, 225, text="Circular Wait Condition Resolved", font=("Arial", 12), fill="#7F1D1D")

    # Queue animations non-blocking using tkinter after
    parent_frame.after(1000, step1)
    parent_frame.after(2500, step2)
    parent_frame.after(4000, step3)
    parent_frame.after(5500, step4)
    parent_frame.after(6500, show_alert)
