import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# Constants
VALID_USERNAME = "oma"
VALID_PASSWORD = "123"

# --- Functions ---
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        messagebox.showinfo("Login Successful", "The login is successful!")
        root.destroy()
        subprocess.run([sys.executable, "main_menu_interface.py"])
    elif username != VALID_USERNAME and password != VALID_PASSWORD:
        messagebox.showerror("Login Failed", "Invalid username or password.")
    elif username != VALID_USERNAME:
        messagebox.showwarning("Login Failed", "Incorrect username.")
    elif password != VALID_PASSWORD:
        messagebox.showwarning("Login Failed", "Incorrect password.")

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        messagebox.showinfo("Signup", "Account already exists.")
    elif username == "" or password == "":
        messagebox.showwarning("Signup", "Please fill in all fields.")
    else:
        messagebox.showinfo("Signup Successful", f"Account created for {username}!")

def clear_fields():
    username_entry.delete(0, 'end')
    password_entry.delete(0, 'end')

# --- Setup ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Sales Analysis Login Form")
root.geometry("800x450")

# Colors
charcoal = "#36454f"
sky_blue = "#dceefb"
root.configure(fg_color=sky_blue)

# --- Canvas for Ovals ---
canvas = tk.Canvas(root, width=800, height=450, bg=sky_blue, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_oval(-150, 300, 300, 600, fill=charcoal, outline="")  # Bottom-left
canvas.create_oval(600, -100, 900, 200, fill=charcoal, outline="")  # Top-right

# --- Header (without box) ---
header_label = ctk.CTkLabel(
    root,
    text="Sales Analysis Login Form",
    font=("Helvetica", 22, "bold"),
    text_color=charcoal,
    bg_color=sky_blue
)
header_label.pack(pady=25)

# --- White Form Box ---
form_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=12, bg_color=sky_blue)
form_frame.pack(pady=10, padx=40)

# --- Username ---
username_label = ctk.CTkLabel(form_frame, text="Username:", text_color="black", font=("Arial", 13), bg_color="white")
username_label.grid(row=0, column=0, padx=10, pady=15, sticky="e")
username_entry = ctk.CTkEntry(form_frame, width=250, corner_radius=10)
username_entry.grid(row=0, column=1, padx=10, pady=15)

# --- Password ---
password_label = ctk.CTkLabel(form_frame, text="Password:", text_color="black", font=("Arial", 13), bg_color="white")
password_label.grid(row=1, column=0, padx=10, pady=15, sticky="e")
password_entry = ctk.CTkEntry(form_frame, width=250, show="*", corner_radius=10)
password_entry.grid(row=1, column=1, padx=10, pady=15)

# --- Buttons ---
login_btn = ctk.CTkButton(
    form_frame, text="LOGIN", command=login,
    width=120, corner_radius=20,
    fg_color="#ffffff", text_color="black",
    border_color="black", border_width=1,
    hover_color="#f1f1f1"
)
login_btn.grid(row=2, column=0, pady=20, padx=10)

signup_btn = ctk.CTkButton(
    form_frame, text="SIGNUP", command=signup,
    width=120, corner_radius=20,
    fg_color=charcoal, text_color="white",
    border_color=charcoal, border_width=1,
    hover_color="#2c3e50"
)
signup_btn.grid(row=2, column=1, pady=20, padx=10)

# --- Clear Button ---
clear_btn = ctk.CTkButton(
    root, text="CLEAR", command=clear_fields,
    width=250, corner_radius=20,
    fg_color="#ffffff", text_color="black",
    border_color="black", border_width=1,
    hover_color="#f1f1f1",
    bg_color=sky_blue
)
clear_btn.pack(pady=15)

# --- Run ---
root.mainloop()
