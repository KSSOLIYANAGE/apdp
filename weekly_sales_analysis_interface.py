import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Appearance setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Weekly Sales Analysis")
root.geometry("1000x620")
root.configure(fg_color="#dceefb")  # Sky blue background

# Canvas design for curves
canvas = tk.Canvas(root, width=1000, height=620, bg="#dceefb", highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_oval(-100, 420, 280, 700, fill="#36454f", outline="")  # Bottom-left charcoal oval
canvas.create_oval(720, -120, 1080, 240, fill="#36454f", outline="")  # Top-right charcoal oval

# Title
title = ctk.CTkLabel(root, text="Weekly Sales Analysis", font=("Helvetica", 22, "bold"), text_color="#36454f")
title.place(x=30, y=20)

# Week selector
week_label = ctk.CTkLabel(root, text="Select Week", font=("Arial", 13, "bold"), text_color="black")
week_label.place(x=30, y=70)

week_var = tk.StringVar()
week_dropdown = ctk.CTkComboBox(root, variable=week_var, width=150)
week_dropdown.place(x=140, y=70)

# CSV preview
preview = ctk.CTkTextbox(root, width=880, height=180, fg_color="white", text_color="black",
                         font=("Consolas", 11), corner_radius=10)
preview.place(x=50, y=110)
preview.insert("0.0", "CSV preview will appear here after uploading.")

# Chart area
chart_frame = ctk.CTkFrame(root, width=880, height=200, fg_color="white", corner_radius=10)
chart_frame.place(x=50, y=310)

# --- Upload CSV ---
def upload_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return
    try:
        df = pd.read_csv(filepath)

        # ✅ Adjusted to match uploaded column names
        if not {"DateRow", "BranchRow", "TotalAmountRow"}.issubset(df.columns):
            raise ValueError("CSV must contain 'DateRow', 'BranchRow', and 'TotalAmountRow' columns.")

        df["DateRow"] = pd.to_datetime(df["DateRow"], format="%d/%m/%Y", errors='coerce')
        df.dropna(subset=["DateRow"], inplace=True)
        df["Week"] = df["DateRow"].dt.isocalendar().week
        df["Day"] = df["DateRow"].dt.day_name()
        df["Sales"] = df["TotalAmountRow"]

        # Dropdown values
        unique_weeks = sorted(df["Week"].unique())
        week_dropdown.configure(values=[f"Week {w}" for w in unique_weeks])
        week_dropdown.set(f"Week {unique_weeks[0]}")

        root.df_data = df  # store for later use

        preview.delete("0.0", "end")
        preview.insert("0.0", df.head(10).to_string(index=False))

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Analyze Selected Week ---
def analyze_week():
    try:
        df = root.df_data
        selected = week_var.get()
        if not selected.startswith("Week "):
            raise ValueError("Please select a valid week.")

        week_num = int(selected.split()[-1])
        week_data = df[df["Week"] == week_num]

        if week_data.empty:
            raise ValueError(f"No data for week {week_num}.")

        summary = week_data.groupby("Day")["Sales"].sum().reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        ).fillna(0)

        # Clear chart
        for widget in chart_frame.winfo_children():
            widget.destroy()

        # Bar chart
        fig, ax = plt.subplots(figsize=(6, 2.8), dpi=100)
        summary.plot(kind="bar", ax=ax, color="#36454f")
        ax.set_title(f"Weekly Sales - Week {week_num}")
        ax.set_ylabel("Sales (Rs.)")
        ax.set_xlabel("Day")
        plt.tight_layout()

        canvas_chart = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas_chart.draw()
        canvas_chart.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Buttons
upload_btn = ctk.CTkButton(root, text="Upload CSV", command=upload_csv,
                           width=130, height=35, fg_color="#36454f", text_color="white")
upload_btn.place(x=320, y=550)

analyze_btn = ctk.CTkButton(root, text="Analyze ➝", command=analyze_week,
                            width=130, height=35, fg_color="#36454f", text_color="white")
analyze_btn.place(x=480, y=550)

# Run
root.mainloop()
