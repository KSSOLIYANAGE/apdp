import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Setup ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Sales Data Upload Interface")
root.geometry("1100x620")
root.configure(fg_color="#eaf4f4")  # Light sky blue background

# --- Oval Decorations ---
bg_canvas = tk.Canvas(root, width=1100, height=620, bg="#eaf4f4", highlightthickness=0)
bg_canvas.place(x=0, y=0)
bg_canvas.create_oval(-150, 400, 300, 800, fill="#36454f", outline="")  # Bottom-left oval
bg_canvas.create_oval(800, -200, 1200, 200, fill="#36454f", outline="")  # Top-right oval

# --- LEFT PANEL ---
left_panel = ctk.CTkFrame(root, width=650, height=550, corner_radius=20, fg_color="#36454f")
left_panel.place(x=20, y=25)

heading = ctk.CTkLabel(left_panel, text="Data Sales Data", font=("Helvetica", 22, "bold"), text_color="white")
heading.place(x=30, y=25)

subtext = ctk.CTkLabel(left_panel, text="Upload and analyze monthly .csv files",
                       font=("Arial", 14), text_color="white")
subtext.place(x=30, y=60)

# --- Preview Box ---
preview_textbox = ctk.CTkTextbox(left_panel, width=580, height=200, fg_color="white", text_color="black",
                                 corner_radius=10, font=("Consolas", 12))
preview_textbox.place(x=30, y=150)
preview_textbox.insert("0.0", "CSV preview will appear here after uploading.")

# --- Chart Frame ---
chart_frame = ctk.CTkFrame(left_panel, width=580, height=200, fg_color="white", corner_radius=10)
chart_frame.place(x=30, y=370)

# --- RIGHT PANEL ---
right_panel = ctk.CTkFrame(root, width=350, height=550, corner_radius=20, fg_color="#dceefb")
right_panel.place(x=700, y=25)

panel_title = ctk.CTkLabel(right_panel, text="Loading CSV: Monthly Sales Data",
                           font=("Helvetica", 16, "bold"), text_color="#2c7873")
panel_title.place(x=20, y=30)

validate_log = ctk.CTkLabel(right_panel, text="\u2713 Validation Log\n-", font=("Arial", 13),
                            text_color="gray", justify="left")
validate_log.place(x=20, y=90)

fail_log = ctk.CTkLabel(right_panel, text="\u2713 Failure Log\n-", font=("Arial", 13),
                        text_color="gray", justify="left")
fail_log.place(x=20, y=160)

success_log = ctk.CTkLabel(right_panel, text="\u2713 Success Log\n-", font=("Arial", 13),
                           text_color="gray", justify="left")
success_log.place(x=20, y=230)

# --- Upload CSV Function ---
def upload_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return

    try:
        df = pd.read_csv(filepath)

        required_cols = {"DateRow", "BranchRow", "ProductRow", "QuantityRow", "UnitPriceRow", "TotalAmountRow", "PaymentMethodRow"}
        if not required_cols.issubset(df.columns):
            raise ValueError("CSV must contain required columns.")

        # Preview
        preview_textbox.delete("0.0", "end")
        preview_textbox.insert("0.0", df.head(10).to_string(index=False))

        # Log
        validate_log.configure(text="\u2713 Validation Log\n✓ All Required Columns Found", text_color="green")
        fail_log.configure(text="\u2713 Failure Log\nNone", text_color="gray")
        success_log.configure(text="\u2713 Success Log\nCSV Imported Successfully", text_color="green")

        # Analysis Bar Chart (Total Sales per Branch)
        branch_sales = df.groupby("BranchRow")["TotalAmountRow"].sum()

        # Plot
        fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
        branch_sales.plot(kind='bar', color='#2c7873', ax=ax)
        ax.set_title("Total Sales per Branch")
        ax.set_ylabel("Rs.")
        ax.set_xlabel("Branch")
        plt.tight_layout()

        # Clear previous chart
        for widget in chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        preview_textbox.delete("0.0", "end")
        fail_log.configure(text="\u2713 Failure Log\nUpload Error", text_color="red")
        validate_log.configure(text="\u2713 Validation Log\nFailed", text_color="red")
        messagebox.showerror("Error", str(e))

# --- Upload Button ---
upload_btn = ctk.CTkButton(left_panel, text="Upload CSV", command=upload_csv,
                           width=160, height=40, corner_radius=12,
                           fg_color="white", text_color="#2c7873")
upload_btn.place(x=30, y=100)

# --- Run ---
root.mainloop()
