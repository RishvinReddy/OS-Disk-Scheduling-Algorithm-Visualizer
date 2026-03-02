import customtkinter as ctk

def show_splash(root):
    splash = ctk.CTkToplevel()
    splash.geometry("600x350")
    splash.overrideredirect(True)
    
    # Center splash on screen
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width / 2) - (600 / 2)
    y = (screen_height / 2) - (350 / 2)
    splash.geometry(f"600x350+{int(x)}+{int(y)}")

    frame = ctk.CTkFrame(splash, fg_color="#1F77B4", corner_radius=0)
    frame.pack(fill="both", expand=True)

    ctk.CTkLabel(frame, text="OS Simulation Suite", font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(expand=True, pady=(80, 0))
    ctk.CTkLabel(frame, text="Advanced OS Resource Management Simulator", font=ctk.CTkFont(size=14), text_color="white").pack(pady=(10, 20))
    ctk.CTkLabel(frame, text="Developed by Erolla Rishvin Reddy", font=ctk.CTkFont(size=12, slant="italic"), text_color="#E0E0E0").pack(pady=(0, 40))

    splash.update()
    splash.after(2500, splash.destroy)
    root.wait_window(splash)
