import customtkinter as ctk
import tkinter as tk
import random

def create_filesystem_tab(parent_frame):
    card = ctk.CTkFrame(parent_frame, fg_color="#FFFFFF", corner_radius=12)
    card.grid(row=0, column=0, sticky="nsew")
    card.grid_rowconfigure(2, weight=1)
    card.grid_columnconfigure(0, weight=1)

    top_frame = ctk.CTkFrame(card, fg_color="transparent")
    top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
    ctk.CTkLabel(top_frame, text="File System Simulation", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111827").pack(side="left")

    visual_frame = ctk.CTkFrame(card, fg_color="transparent")
    visual_frame.grid(row=1, column=0, sticky="nsew", padx=20)
    
    ctk.CTkLabel(visual_frame, text="Disk Blocks Allocation", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w", pady=(10,0))
    cv = tk.Canvas(visual_frame, height=200, bg="#F9FAFB", highlightthickness=1, highlightbackground="#E5E7EB")
    cv.pack(fill="x", pady=10)
    
    status_label = ctk.CTkLabel(visual_frame, text="Free Blocks: 20", font=ctk.CTkFont(size=12, weight="bold"), text_color="#059669")
    status_label.pack(anchor="e")

    disk_blocks = [0] * 20

    def draw_disk():
        cv.delete("all")
        cv.update()
        w = cv.winfo_width()
        if w < 100: w = 800
        
        block_width = (w - 100) / 20
        x = 50
        
        for i, block in enumerate(disk_blocks):
            if block == 0:
                color = "#E5E7EB"
                outline = "#D1D5DB"
            elif block == 1:
                color = "#10B981" # Contiguous
                outline = "#059669"
            elif block == 2:
                color = "#F59E0B" # Linked
                outline = "#D97706"
            elif block == 3:
                color = "#3B82F6" # Indexed
                outline = "#2563EB"
            elif block == 4:
                color = "#8B5CF6" # Index Pointer Block
                outline = "#6D28D9"
                
            cv.create_rectangle(x, 50, x+block_width-5, 120, fill=color, outline=outline, width=2)
            cv.create_text(x+(block_width/2)-2, 85, text=str(i), font=("Arial", 9, "bold"), fill="#374151")
            
            x += block_width
            
        free = disk_blocks.count(0)
        status_label.configure(text=f"Free Blocks: {free}")
        return block_width

    def allocate_contiguous():
        size = random.randint(2, 5)
        start = random.randint(0, 15)
        
        # Check if requested space is free
        if all(b == 0 for b in disk_blocks[start:start+size]):
            for i in range(start, start+size):
                disk_blocks[i] = 1
            draw_disk()
        else:
            status_label.configure(text=f"Failed to allocate contiguous block of size {size}")

    def allocate_linked():
        free_indices = [i for i, b in enumerate(disk_blocks) if b == 0]
        if len(free_indices) >= 4:
            indices = random.sample(free_indices, 4)
            indices.sort()
            
            for idx in indices:
                disk_blocks[idx] = 2
                
            bw = draw_disk()
            
            # Draw Arrows
            for i in range(len(indices)-1):
                x1 = 50 + indices[i]*bw + (bw/2)
                x2 = 50 + indices[i+1]*bw + (bw/2)
                cv.create_line(x1, 130, x2, 130, arrow=tk.LAST, width=2, fill="#D97706")

    def allocate_indexed():
        free_indices = [i for i, b in enumerate(disk_blocks) if b == 0]
        if len(free_indices) >= 4:
            index_block = random.choice(free_indices)
            disk_blocks[index_block] = 4 # Index block color
            
            free_indices.remove(index_block)
            data_blocks = random.sample(free_indices, 3)
            
            for b in data_blocks:
                disk_blocks[b] = 3
                
            bw = draw_disk()
            idx_x = 50 + index_block*bw + (bw/2)
            
            for b in data_blocks:
                target_x = 50 + b*bw + (bw/2)
                cv.create_line(idx_x, 30, idx_x, 15, fill="#2563EB", width=2)
                cv.create_line(idx_x, 15, target_x, 15, fill="#2563EB", width=2)
                cv.create_line(target_x, 15, target_x, 30, arrow=tk.LAST, fill="#2563EB", width=2)

    def reset_disk():
        for i in range(len(disk_blocks)):
            disk_blocks[i] = 0
        draw_disk()

    # Draw initially
    parent_frame.after(100, draw_disk)

    btn_frame = ctk.CTkFrame(card, fg_color="transparent")
    btn_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
    
    ctk.CTkButton(btn_frame, text="Contiguous Allocation", fg_color="#10B981", hover_color="#059669", command=allocate_contiguous).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Linked Allocation", fg_color="#F59E0B", hover_color="#D97706", command=allocate_linked).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Indexed Allocation", fg_color="#3B82F6", hover_color="#2563EB", command=allocate_indexed).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Reset Disk", fg_color="#EF4444", hover_color="#DC2626", command=reset_disk).pack(side="left", padx=20)
