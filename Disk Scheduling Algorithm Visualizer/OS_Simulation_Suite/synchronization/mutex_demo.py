import threading
import time
import tkinter as tk

def simulate_mutex(log_textbox, use_mutex=True):
    log_textbox.delete("1.0", tk.END)
    
    lock = threading.Lock()
    shared_resource = 0
    
    def access_disk(process_id):
        nonlocal shared_resource
        
        if use_mutex:
            with lock:
                log_textbox.insert(tk.END, f"[LOCKED] Process {process_id} entering critical section...\n")
                log_textbox.see(tk.END)
                # simulate work
                local_copy = shared_resource
                time.sleep(0.5)
                shared_resource = local_copy + 1
                log_textbox.insert(tk.END, f"  -> Process {process_id} updated resource to {shared_resource}.\n")
                log_textbox.insert(tk.END, f"[RELEASED] Process {process_id} done.\n\n")
                log_textbox.see(tk.END)
        else:
            log_textbox.insert(tk.END, f"[RACING] Process {process_id} accessing disk... (No Lock)\n")
            log_textbox.see(tk.END)
            # simulate work
            local_copy = shared_resource
            time.sleep(0.5)
            shared_resource = local_copy + 1
            log_textbox.insert(tk.END, f"  -> Process {process_id} overwrote resource to {shared_resource}.\n\n")
            log_textbox.see(tk.END)

    # Launch threads
    threads = []
    for i in range(1, 4):
        t = threading.Thread(target=access_disk, args=(i,), daemon=True)
        threads.append(t)
        t.start()
