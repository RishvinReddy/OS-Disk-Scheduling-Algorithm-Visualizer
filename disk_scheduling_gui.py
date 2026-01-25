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
