import tkinter as tk
from tkinter import ttk

# Global animation state
is_running = False
is_paused = False
animation_speed = 600

def set_running(val):
    global is_running
    is_running = val

def set_paused(val):
    global is_paused
    is_paused = val

def set_speed(val):
    global animation_speed
    animation_speed = int(val) 

def get_running():
    return is_running

def get_paused():
    return is_paused

def get_speed():
    return animation_speed

def animate_disk(sequence, title, parent_frame):
    global is_running, is_paused, animation_speed

    # Clear previous widgets (matplotlib or canvas)
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Create native Tkinter Canvas
    canvas = tk.Canvas(parent_frame, bg="#FFFFFF", highlightthickness=0)
    canvas.pack(fill="both", expand=True, padx=10, pady=10)

    # Scale max width
    max_val = max(sequence) if sequence else 200
    if max_val == 0:
        max_val = 200

    def get_x(val, width):
        # map 0 -> max_val to 50 -> width-50
        usable = width - 100
        return 50 + (val / max_val) * usable

    canvas.update()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    if w < 100: w = 600
    if h < 100: h = 250
    
    y_center = h / 2

    # Draw track line
    canvas.create_line(50, y_center, w - 50, y_center, width=4, fill="#E5E7EB")

    # Draw start label
    start_x = get_x(sequence[0], w)
    canvas.create_text(start_x, y_center - 30, text="Start", fill="#10B981", font=("Arial", 10, "bold"))
    
    # Draw disk head
    head = canvas.create_oval(start_x - 10, y_center - 10, start_x + 10, y_center + 10, fill="#1F4ED8", outline="#1E3A8A")

    is_running = True
    is_paused = False
    current_index = 0
    path_points = []
    
    def step():
        nonlocal current_index, path_points

        if not is_running:
            return

        if is_paused:
            parent_frame.after(100, step)
            return

        if current_index < len(sequence):
            x = get_x(sequence[current_index], w)
            
            # Animate movement
            canvas.coords(head, x - 10, y_center - 10, x + 10, y_center + 10)
            
            # Draw trail dot and label
            if current_index > 0:
                prev_x = get_x(sequence[current_index-1], w)
                canvas.create_line(prev_x, y_center, x, y_center, fill="#3B82F6", width=2, stipple="gray50")
                canvas.create_oval(x - 4, y_center - 4, x + 4, y_center + 4, fill="#EF4444", outline="")
                canvas.create_text(x, y_center + 20, text=str(sequence[current_index]), fill="#6B7280", font=("Arial", 9))
                
            current_index += 1
            parent_frame.after(animation_speed, step)

    step()
