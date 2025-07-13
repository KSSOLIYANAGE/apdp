import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Monthly Sales Analysis Module")
root.geometry("1000x600")
root.configure(fg_color="#dceefb")  # Light sky blue

# Background canvas and ovals
canvas = tk.Canvas(root, width=1000, height=600, bg="#dceefb", highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_oval(-120, 450, 300, 700, fill="#36454f", outline="")  # Bottom left charcoal
canvas.create_oval(750, -100, 1100, 250, fill="#36454f", outline="")  # Top right charcoal

# Title
title_label = ctk.CTkLabel(root, text="Monthly Sales Analysis Module",
                           font=("Helvetica", 22, "bold"), text_color="#36454f")
title_label.place(x=320, y=20)

# Month selector
month_label = ctk.CTkLabel(root, text="Select Month", font=("Arial", 13, "bold"), text_color="black")
month_label.place(x=30, y=80)

month_var = tk.StringVar()
month_dropdown = ctk.CTkComboBox(root, variable=month_var,
                                 values=["January", "February", "March", "April", "May", "June", "July"],
                                 width=150)
month_dropdown.place(x=140, y=80)
month_dropdown.set("February")

# Preview
preview_box = ctk.CTkTextbox(root, width=850, height=180, fg_color="white", text_color="black",
                             font=("Consolas", 11), corner_radius=12)
preview_box.place(x=70, y=130)
preview_box.insert("0.0", "CSV preview will appear here after uploading.")

# Chart frame
chart_frame = ctk.CTkFrame(root, width=850, height=180, fg_color="white", corner_radius=12)
chart_frame.place(x=70, y=340)

# Month map
month_mapping = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

# CSV upload
def upload_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return
    try:
        df = pd.read_csv(filepath)

        # Validate actual CSV column names
        if not {"DateRow", "BranchRow", "TotalAmountRow"}.issubset(df.columns):
            raise ValueError("CSV must contain 'DateRow', 'BranchRow', and 'TotalAmountRow' columns.")

        # Parse date column (DMY format)
        df["DateRow"] = pd.to_datetime(df["DateRow"], format="%d/%m/%Y", errors="coerce")

        # Extract month name
        df["Month"] = df["DateRow"].dt.month.map(month_mapping)
        selected_month = month_var.get()
        df_month = df[df["Month"] == selected_month]

        if df_month.empty:
            raise ValueError(f"No data found for selected month: {selected_month}")

        # Display preview
        preview_box.delete("0.0", "end")
        preview_box.insert("0.0", df_month.head(10).to_string(index=False))

        # Plot bar chart
        sales = df_month.groupby("BranchRow")["TotalAmountRow"].sum()
        fig, ax = plt.subplots(figsize=(6, 2.8), dpi=100)
        sales.plot(kind='bar', color="#36454f", ax=ax)
        ax.set_title(f"Total Sales - {selected_month}")
        ax.set_ylabel("Amount (Rs.)")
        ax.set_xlabel("Branch")
        plt.tight_layout()

        # Display chart
        for widget in chart_frame.winfo_children():
            widget.destroy()

        canvas_chart = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas_chart.draw()
        canvas_chart.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Buttons
upload_btn = ctk.CTkButton(root, text="Upload CSV", command=upload_csv,
                           width=120, height=35, corner_radius=12,
                           fg_color="#36454f", text_color="white")
upload_btn.place(x=320, y=540)

export_btn = ctk.CTkButton(root, text="Export ➝", command=upload_csv,
                           width=120, height=35, corner_radius=12,
                           fg_color="#36454f", text_color="white")
export_btn.place(x=480, y=540)

# Run
root.mainloop()
