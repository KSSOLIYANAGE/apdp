# main_menu_interface.py
import customtkinter as ctk
import tkinter as tk
import subprocess

# --- Setup ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Main Menu Interface")
root.geometry("960x500")

# Colors
light_bg = "#e6ecf7"
charcoal = "#36454f"
black = "#000000"

root.configure(fg_color=light_bg)

# --- Canvas for Charcoal Ovals ---
canvas = tk.Canvas(root, width=960, height=500, bg=light_bg, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_oval(-300, 350, 400, 900, fill=charcoal, outline="")     # Bottom-left
canvas.create_oval(700, -200, 1200, 300, fill=charcoal, outline="")     # Top-right

# --- Titles ---
title_label = ctk.CTkLabel(
    root,
    text="Main Menu Main Menu",
    font=("Helvetica", 22, "bold"),
    text_color=charcoal,
    bg_color=light_bg
)
title_label.pack(pady=(20, 5))

subtitle_label = ctk.CTkLabel(
    root,
    text="for Admin and Analyst",
    font=("Arial", 13),
    text_color="black",
    bg_color=light_bg
)
subtitle_label.pack(pady=(0, 10))

# --- Open Data Management Interface ---
def open_data_management():
    root.destroy()
    subprocess.Popen(["python", "data_management_interface.py"])

# --- Button Factory ---
def create_menu_button(text, fg, txt_color, command=None):
    return ctk.CTkButton(
        master=grid_frame,
        text=text,
        width=240,
        height=45,
        corner_radius=18,
        fg_color=fg,
        text_color=txt_color,
        font=("Arial", 13, "bold"),
        border_width=0,
        hover_color="#dde3f0",
        command=command
    )

# --- Grid Frame ---
grid_frame = ctk.CTkFrame(root, fg_color=light_bg, bg_color=light_bg)
grid_frame.pack(pady=10)

# --- Button Configuration ---
buttons = [
    ("View Monthly Sales Analysis", black, "white", None),               # ← CHANGED
    ("View Weekly Sales Analysis", black, "white", None),               # ← CHANGED
    ("View Monthly Sales Analysis", black, "white", None),              # ← CHANGED

    ("View Weekly Sales Analysis", "#ffffff", "black", None),
    ("Product Price & Preference Analysis", "#ffffff", "black", None),
    ("Distribution of Total Sales", "#ffffff", "black", None),

    ("Distribution of Total Sales", black, "white", None),              # ← CHANGED
    ("Distribution of Total Sales", "#ffffff", "black", None),
    ("Load/Import Sales Data", black, "white", None),                   # ← CHANGED

    ("Load/Import Sales Data", "#ffffff", "black", None),
    ("Data Management Interface", black, "white", open_data_management),  # ← CHANGED
    ("Exit", "#ffffff", "black", root.destroy)
]

# --- Render Buttons ---
for i in range(4):
    for j in range(3):
        idx = i * 3 + j
        if idx < len(buttons):
            text, fg_color, txt_color, cmd = buttons[idx]
            btn = create_menu_button(text, fg_color, txt_color, cmd)
            btn.grid(row=i, column=j, padx=15, pady=10)

# --- Run ---
root.mainloop()
