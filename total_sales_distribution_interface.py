import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Setup ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Total Sales Distribution")
root.geometry("1000x650")
root.configure(fg_color="#dceefb")  # light blue

# --- Canvas for charcoal ovals ---
canvas = tk.Canvas(root, width=1000, height=650, bg="#dceefb", highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_oval(-150, 480, 300, 800, fill="#36454f", outline="")  # bottom left
canvas.create_oval(800, -80, 1200, 280, fill="#36454f", outline="")   # top right

# --- Title ---
title = ctk.CTkLabel(root, text="Total Sales Distribution", font=("Helvetica", 24, "bold"),
                     text_color="black", bg_color="#dceefb")
title.place(x=340, y=30)

subtitle = ctk.CTkLabel(root, text="Analyze customer purchase bracket distribution from uploaded sales data.",
                        font=("Arial", 13), text_color="#555555", bg_color="#dceefb")
subtitle.place(x=230, y=70)

# --- Chart Frame ---
chart_card = ctk.CTkFrame(root, width=900, height=350, fg_color="white", corner_radius=18)
chart_card.place(x=50, y=110)

# --- Upload Section ---
button_frame = ctk.CTkFrame(root, width=200, height=60, corner_radius=10, fg_color="white")
button_frame.place(x=60, y=490)

upload_label = ctk.CTkLabel(button_frame, text="Bar Chart", font=("Arial", 13, "bold"), text_color="black")
upload_label.place(x=10, y=5)

def upload_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path)

        # Correct column name from your CSV
        if "TotalAmountRow" not in df.columns:
            raise ValueError("CSV must contain 'TotalAmountRow' column.")

        brackets = ['Under 1000', '1000-5000', '5000-10000', '10000+']
        def categorize(amount):
            if amount < 1000:
                return 'Under 1000'
            elif amount <= 5000:
                return '1000-5000'
            elif amount <= 10000:
                return '5000-10000'
            else:
                return '10000+'

        df['Bracket'] = df['TotalAmountRow'].apply(categorize)
        summary = df['Bracket'].value_counts().reindex(brackets, fill_value=0)

        # Clear chart frame
        for widget in chart_card.winfo_children():
            widget.destroy()

        # Plot chart
        fig, ax = plt.subplots(figsize=(7.5, 3), dpi=100)
        summary.plot(kind='barh', color=['#83b7e0', '#ecb3e1', '#ffd470', '#f3c1e9'], ax=ax)
        ax.set_title("Sales Distribution by Amount Bracket")
        ax.set_xlabel("Number of Orders")
        ax.set_ylabel("Amount Bracket")
        plt.tight_layout()

        canvas_chart = FigureCanvasTkAgg(fig, master=chart_card)
        canvas_chart.draw()
        canvas_chart.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Upload Button ---
upload_button = ctk.CTkButton(button_frame, text="Upload CSV", command=upload_csv,
                              fg_color="#3b7dd8", text_color="white", width=140, height=32, corner_radius=8)
upload_button.place(x=10, y=30)

# --- Run App ---
root.mainloop()
