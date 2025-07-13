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
root.title("Product Price & Preference Analysis")
root.geometry("1150x720")
root.configure(fg_color="#eaf1f8")  # Light sky blue

# --- Background Design ---
canvas = tk.Canvas(root, width=1150, height=720, bg="#eaf1f8", highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_arc(-400, 500, 600, 1300, fill="#36454f", outline="")  # Charcoal C-wave
canvas.create_oval(880, -150, 1300, 250, fill="#dceefb", outline="")  # Light blue oval top-right

# --- Header ---
header = ctk.CTkLabel(root, text="Product Price & Preference Analysis",
                      font=("Helvetica", 24, "bold"), text_color="#23395d")
header.place(x=60, y=30)

# --- Chart Frames ---
def create_chart_frame(x, y):
    outer = ctk.CTkFrame(root, width=502, height=242, fg_color="#23395d", corner_radius=18)
    outer.place(x=x, y=y)
    inner = ctk.CTkFrame(outer, width=490, height=230, fg_color="white", corner_radius=15)
    inner.place(x=6, y=6)
    return inner

frame1 = create_chart_frame(50, 100)
frame2 = create_chart_frame(600, 100)
frame3 = create_chart_frame(50, 370)
frame4 = create_chart_frame(600, 370)

# --- Clear Frames ---
def clear_frames():
    for frame in [frame1, frame2, frame3, frame4]:
        for widget in frame.winfo_children():
            widget.destroy()

# --- Upload CSV + Generate Charts ---
def upload_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    try:
        df = pd.read_csv(file_path)

        # Rename columns to match expected names
        df.rename(columns={
            "ProductRow": "Product",
            "BranchRow": "Branch",
            "QuantityRow": "Quantity",
            "UnitPriceRow": "UnitPrice",
            "TotalAmountRow": "TotalAmount"
        }, inplace=True)

        # Check if expected columns are now present
        required_cols = {"Product", "Branch", "Quantity", "UnitPrice", "TotalAmount"}
        if not required_cols.issubset(df.columns):
            raise ValueError("CSV must contain: Product, Branch, Quantity, UnitPrice, TotalAmount")

        clear_frames()

        # Chart 1: Sales Count
        fig1, ax1 = plt.subplots(figsize=(3.2, 2.2), dpi=100)
        df.groupby("Branch")["Quantity"].sum().plot(kind='bar', color='#3b7dd8', ax=ax1)
        ax1.set_title("Sales Count per Branch")
        ax1.set_ylabel("Quantity")
        ax1.set_xlabel("Branch")
        canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack()

        # Chart 2: Avg Revenue
        fig2, ax2 = plt.subplots(figsize=(3.2, 2.2), dpi=100)
        df.groupby("Branch")["TotalAmount"].mean().plot(kind='bar', color='#73b3f2', ax=ax2)
        ax2.set_title("Average Revenue per Branch")
        ax2.set_ylabel("Revenue (Rs.)")
        ax2.set_xlabel("Branch")
        canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack()

        # Chart 3: Most Preferred Products
        fig3, ax3 = plt.subplots(figsize=(3.2, 2.2), dpi=100)
        df.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(5).plot(kind='bar', color='#437fd1', ax=ax3)
        ax3.set_title("Most Preferred Products")
        ax3.set_ylabel("Quantity")
        ax3.set_xlabel("Product")
        canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
        canvas3.draw()
        canvas3.get_tk_widget().pack()

        # Chart 4: Most Overgoing Products
        fig4, ax4 = plt.subplots(figsize=(3.2, 2.2), dpi=100)
        df.groupby("Product")["UnitPrice"].mean().sort_values(ascending=False).head(5).plot(kind='bar', color='#5ba3c6', ax=ax4)
        ax4.set_title("Most Overgoing Products")
        ax4.set_ylabel("Unit Price")
        ax4.set_xlabel("Product")
        canvas4 = FigureCanvasTkAgg(fig4, master=frame4)
        canvas4.draw()
        canvas4.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Upload Button ---
upload_btn = ctk.CTkButton(root, text="Upload CSV", command=upload_csv,
                           width=160, height=40, corner_radius=12,
                           fg_color="#2c6d91", text_color="white",
                           font=("Arial", 13, "bold"))
upload_btn.place(x=900, y=30)

# --- Run ---
root.mainloop()
