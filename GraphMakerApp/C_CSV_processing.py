#!/usr/bin/env python
# coding: utf-8

# In[4]:


# @title Graphic Maker
import pandas as pd

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib
print(matplotlib.get_backend())  # Confirm backend
matplotlib.use('TkAgg')  # Change to an appropriate one for your OS

import matplotlib.pyplot as plt

import random

# package to handle GUI application for file upload
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, Tk
from tkinter import ttk

#//////////////////////////////////////////////////////////////////////////////////////////////////////

# define global df variable
df = None

# The number of signals we plot in the sequel
num_signals = 12

# define global lists to store the generated widgets
y_dropdowns = []
y_checkboxes = []
plot_checkboxes = []
subplot_checkboxes = []
float_entries = []
title = None

# file upload button
def upload_file():
    global df
    # Open file dialog for the user to select the CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if file_path:
        # Read the CSV file into a DataFrame using pandas
        try:
            df = pd.read_csv(file_path, encoding='latin-1')
            print("File uploaded successfully!")
            print("Available columns:", df.columns.tolist())
            messagebox.showinfo("Success", "File uploaded successfully!")
            
            # Call generate_widgets after a successful upload
            generate_widgets()

        except Exception as e:
            print(f"Error reading file: {e}")
            messagebox.showerror("Error", f"Failed to read file: {e}")
            df = None  # Reset df if there's an error
    else:
        print("No file selected.")
        messagebox.showwarning("Warning", "No file selected.")
        df = None

def generate_widgets():
    if df is not None:
        # Clear previous widgets if they exist
        clear_widgets()

        # Get the columns from the dataframe (except the first column)
        columns = df.columns.tolist()
        
        # Title
        global title
        tk.Label(app, text='Graph Title:').grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        entry_t = tk.Entry(app, width=8)
        entry_t.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        entry_t.insert(0, 'Title')
        title = entry_t

        # Header row for the grid
        headers = ['Signal', 'Select Signal', 'Second Y-Axis', 'Plot Signal', 'Subplot Signal']
        for col, text in enumerate(headers):
            header_label = tk.Label(app, text=text, font=('Arial', 10, 'bold'))
            header_label.grid(row=2, column=col, padx=5, pady=5, sticky='nsew')  # Start at row=2 (below the button)

        # Dynamically create widgets based on the number of signals
        for i in range(num_signals):
            # Label for each signal (first column)
            label = tk.Label(app, text=f'Signal {i+1}:')
            label.grid(row=i+3, column=0, padx=5, pady=5, sticky='nsew')  # Start from row 3

            # Dropdown menu for each signal (second column)
            dropdown = ttk.Combobox(app, values=columns[1:], state="readonly", width=35)
            dropdown.set("Select Signal")
            dropdown.grid(row=i+3, column=1, padx=5, pady=5, sticky='nsew')
            y_dropdowns.append(dropdown)

            # Checkbox for second Y-axis (third column)
            y_axis_var = tk.IntVar()
            checkbox = tk.Checkbutton(app, text="Second Y-Axis", variable=y_axis_var)
            checkbox.grid(row=i+3, column=2, padx=5, pady=5, sticky='nsew')
            checkbox.var = y_axis_var
            y_checkboxes.append(checkbox)

            # Checkbox for plotting the signal (fourth column)
            plot_var = tk.IntVar()
            plot_checkbox = tk.Checkbutton(app, text=f'Plot Signal {i+1}', variable=plot_var)
            plot_checkbox.grid(row=i+3, column=3, padx=5, pady=5, sticky='nsew')
            plot_checkbox.var = plot_var
            plot_checkboxes.append(plot_checkbox)

            # Checkbox for subplot (fifth column)
            subplot_var = tk.IntVar()
            subplot_checkbox = tk.Checkbutton(app, text=f'Subplot Signal {i+1}', variable=subplot_var)
            subplot_checkbox.grid(row=i+3, column=4, padx=5, pady=5, sticky='nsew')
            subplot_checkbox.var = subplot_var
            subplot_checkboxes.append(subplot_checkbox)
            
            
        # Take minimum and maximu of the time column
        time_min = df[df.columns[0]].min()
        time_max = df[df.columns[0]].max()
        
        def validate_float(value_if_allowed):
            if value_if_allowed == "":  # Allow empty input
                return True
            try:
                float(value_if_allowed)  # Try to convert to float
                return True
            except ValueError:
                return False

        # Define a validation command that points to the validate_float function
        vcmd = (app.register(validate_float), '%P')  # '%P' is the value after the change 
        
        numeric_fields = [  
            ("Time Min (s):", time_min, "Time Max (s):", time_max),
            ("Y-axis Min:", 0, "Y-axis Max:", 0),
            ("Right Y-axis Min:", 0, "Right Y-axis Max:", 0),
            ("X Divisions:", 10, "Y Divisions:", 10),
        ]
        
        label_fields = [
            ("Y-axis Label:", "Label1", "Right Y-axis Label:", "Label2")
        ]
        
        for i, (label1, val1, label2, val2) in enumerate(numeric_fields):
            tk.Label(app, text=label1).grid(row=num_signals + 6 + i, column=2, padx=5, pady=5, sticky='nsew')
            entry1 = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
            entry1.grid(row=num_signals + 6 + i, column=3, padx=5, pady=5, sticky='nsew')
            entry1.insert(0, val1)
            float_entries.append(entry1)

            tk.Label(app, text=label2).grid(row=num_signals + 6 + i, column=4, padx=5, pady=5, sticky='nsew')
            entry2 = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
            entry2.grid(row=num_signals + 6 + i, column=5, padx=5, pady=5, sticky='nsew')
            entry2.insert(0, val2)
            float_entries.append(entry2)
            
        for i, (label1, val1, label2, val2) in enumerate(label_fields):
            row_index = num_signals + 6 + len(numeric_fields) + i  # Offset by numeric fields count
            tk.Label(app, text=label1).grid(row=row_index, column=2, padx=5, pady=5, sticky='nsew')
            entry1 = tk.Entry(app, width=12)
            entry1.grid(row=row_index, column=3, padx=5, pady=5, sticky='nsew')
            entry1.insert(0, val1)
            float_entries.append(entry1)

            tk.Label(app, text=label2).grid(row=row_index, column=4, padx=5, pady=5, sticky='nsew')
            entry2 = tk.Entry(app, width=12)
            entry2.grid(row=row_index, column=5, padx=5, pady=5, sticky='nsew')
            entry2.insert(0, val2)
            float_entries.append(entry2)
        
        # Add a button to trigger plotting after the fields
        plot_button = tk.Button(app, text="Plot Signals", command=plot_signals, font=("Arial", 12))
        plot_button.grid(row=num_signals + 6 + len(numeric_fields) + len(label_fields), column=2, columnspan=4, pady=20, sticky='nsew')
        
        
    else:
        messagebox.showwarning("Warning", "Please upload a file first!")


def clear_widgets():
    """Clear the previous dropdowns and checkboxes if they exist."""
    global y_dropdowns, y_checkboxes, plot_checkboxes, subplot_checkboxes, float_entries

    # Destroy existing widgets before creating new ones
    for widget_list in [y_dropdowns, y_checkboxes, plot_checkboxes, subplot_checkboxes, float_entries]:
        for widget in widget_list:
            widget.destroy()

    # Clear the lists to reset them
    y_dropdowns.clear()
    y_checkboxes.clear()
    plot_checkboxes.clear()
    subplot_checkboxes.clear()
    float_entries.clear()


def validate_ymax_entries():
    """Function to validate entries and show error if any value max values are nonzero"""
    try:
        value_y1_max = float(float_entries[3].get())  # Convert the entry value to float
        value_y2_max = float(float_entries[7].get()) 
            
        if value_y1_max == 0 or value_y2_max == 0:
            messagebox.showerror("Error", "Entries 'Y1 Max' and 'Y2 Max' have to be greater than zero.")  # Display error message
            return False    
    except ValueError:
        messagebox.showerror("Error", "Entries 'Y1 Max' and 'Y2 Max' contain an invalid value.")  # Display error for non-numeric
        return False
    return True


def generate_unique_colors(num_colors):
    """Function to define unique colors for plotting"""
    random.seed(5)
    colors = set()
    while len(colors) < num_colors:
        # Generate a random color in hexadecimal format
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        colors.add(color)  
    return list(colors)

unique_colors = generate_unique_colors(num_signals)

def plot_signals():
    """Plot the graph with combined plots and subplots in a single matplotlib window."""
    if df is None:
        messagebox.showerror("Error", "No data available to plot. Please upload a file.")
        return
    
    # Validate Y max values
    if not validate_ymax_entries():
        return
    
    # Extract and validate the time range
    t_min = float(float_entries[0].get())
    t_max = float(float_entries[1].get())
    time_col = df.columns[0]  # Assuming the first column is the time column
    df_filtered = df[(df[time_col] >= t_min) & (df[time_col] <= t_max)]
    
    # Separate signals into combined plot and subplot groups
    combined_signals = []
    subplot_signals = []

    for i, dropdown in enumerate(y_dropdowns):
        signal_name = dropdown.get()
        if plot_checkboxes[i].var.get() and signal_name in df_filtered.columns:
            if subplot_checkboxes[i].var.get():  # Check if 'Subplot Signal' is checked
                subplot_signals.append((signal_name, unique_colors[i]))
            else:
                combined_signals.append((signal_name, unique_colors[i]))
    
    # Ensure at least one signal is selected for plotting
    if not combined_signals and not subplot_signals:
        messagebox.showwarning("Warning", "No valid signal selected for plotting. Please check your selections.")
        return
    
    
    # Create a new tkinter window for the plots
    plot_window = tk.Toplevel()
    plot_window.title("Signals")
    plot_window.geometry("1200x800")
    plot_window.resizable(True, True)

    # Create a canvas for the figure and add scrollbars
    canvas_frame = tk.Frame(plot_window)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(canvas_frame)
    scrollbar_y = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)

    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create the Matplotlib figure
    num_plots = 1 + len(subplot_signals)  # Combined plot + individual subplots
    fig = Figure(figsize=(12, 5 * num_plots), tight_layout=True)
    axes = fig.subplots(num_plots, 1, sharex=True)
    
    # Add mouse wheel scrolling support for the canvas
    def _on_mouse_wheel(event):
        """Scroll the canvas with the mouse wheel."""
        if event.delta:  # Handles macOS and Windows
            delta = event.delta
            if delta > 0:  # Positive scroll
                canvas.yview_scroll(-1, "units")
            elif delta < 0:  # Negative scroll
                canvas.yview_scroll(1, "units")
        else:  # Handles Linux (where delta is absent)
            delta = -1 if event.num == 4 else 1
            canvas.yview_scroll(delta, "units")

    # Bind the mouse wheel events to the canvas
    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)  # macOS and Windows
    canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))  # Scroll up (Linux)
    canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))   # Scroll down (Linux)

    if num_plots == 1:
        axes = [axes]

    # Plot combined signals on the first axes
    if combined_signals:
        ax_combined = axes[0]
        for signal_name, color in combined_signals:
            ax_combined.scatter(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)
        graph_title = title.get()
        ax_combined.set_title(graph_title)
        ax_combined.set_xlabel("Time (s)")
        ax_combined.set_ylabel(float_entries[8].get())  # Y-axis label for combined plot
        ax_combined.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
        ax_combined.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)
        ax_combined.tick_params(axis='x', which='both', labelbottom=True)  # Ensure x-axis numbers are displayed

    # Plot each signal in its own subplot
    for ax, (signal_name, color) in zip(axes[1:], subplot_signals):
        ax.scatter(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)
        ax.set_title(f"{signal_name}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(signal_name)
        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
        ax.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)
        ax.tick_params(axis='x', which='both', labelbottom=True)  # Ensure x-axis numbers are displayed

    # Set x-label on the last subplot
    #axes[-1].set_xlabel("Time (s)")

    # Add the figure to the Tkinter canvas
    canvas_widget = FigureCanvasTkAgg(fig, master=scrollable_frame)
    canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas_widget.draw()
    
    # Add the Matplotlib navigation toolbar
    toolbar_frame = tk.Frame(plot_window)
    toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
    toolbar = NavigationToolbar2Tk(canvas_widget, toolbar_frame)
    toolbar.update()

    plot_window.mainloop()
    
    
    
#//////////////////////////////////////////////////////////////////////////////////////////////////
# Building the app 'Graph Maker'

# Create the main application window
app = tk.Tk()
app.title("Graph Maker")
app.geometry("1000x1000")  # Set window size

# Add a button for file upload using grid(), placing it at the top (row=0)
upload_button = tk.Button(app, text="Upload File", command=upload_file, font=("Arial", 12))
upload_button.grid(row=0, column=0, columnspan=5, padx=10, pady=20)  # Button in row 0

# Spacer row to avoid overlapping between upload button and the headers
spacer = tk.Label(app, text="")
spacer.grid(row=1, column=0, columnspan=5, pady=10)  # Spacer in row 1 for extra space

# Run the main application loop
app.mainloop()

"""
# Determine the total number of subplots
num_plots = 1 + len(subplot_signals)  # 1 for the combined plot, plus one for each subplot
#fig, axes = plt.subplots(num_plots, 1, figsize=(14, 5 * num_plots), sharex=True)
fig = Figure(figsize=(14, 6 * num_plots), dpi=100)

# Create subplots
axes = fig.subplots(num_plots, 1, sharex=True)

# Ensure axes is always iterable
if num_plots == 1:
    axes = [axes]


# Plot combined signals on the first axes
if combined_signals:
    ax_combined = axes[0]
    for signal_name, color in combined_signals:
        print(f"Plotting {signal_name} in combined plot with color {color}")
        ax_combined.scatter(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)
    graph_title = title.get()
    ax_combined.set_title(graph_title)
    ax_combined.set_xlabel('Time (s)')
    ax_combined.set_ylabel(float_entries[8].get())  # Y-axis label for combined plot
    ax_combined.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)  # Add grid to combined plot
    ax_combined.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
    ax_combined.tick_params(axis='x', which='both', labelbottom=True)  # Ensure x-axis numbers are displayed
else:
    print("No signals selected for the combined plot.")

# Plot each signal in its own subplot
for ax, (signal_name, color) in zip(axes[1:], subplot_signals):
    print(f"Plotting {signal_name} in its own subplot with color {color}")
    ax.scatter(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)
    ax.set_title(f"{signal_name}")
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(signal_name)
    ax.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)  # Add grid to each subplot
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
    ax.tick_params(axis='x', which='both', labelbottom=True)  # Ensure x-axis numbers are displayed

# Set the shared x-label for all plots
#axes[-1].set_xlabel('Time (s)')


# Apply tight layout
plt.tight_layout()#(rect=[0, 0, 0.9, 1], h_pad=2.0)
plt.show(block=True)
"""


"""
        # ////////////////////////////////////////////////////////////////////////////////
        # Label for float entry fields section
        float_label = tk.Label(app, text="Axis customization", font=('Arial', 10, 'bold'))
        float_label.grid(row=num_signals+4, column=0, columnspan=5, padx=5, pady=10, sticky='nsew')

        # Generate float entry fields 
        # Label for float entry - time min 
        t_min_label = tk.Label(app, text='Time Min (s):')
        t_min_label.grid(row=num_signals+5+1, column=2, padx=5, pady=5, sticky='nsew')

        # Float entry widget - time min
        t_min_entry = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
        t_min_entry.grid(row=num_signals+5+1, column=3, padx=5, pady=5, sticky='nsew')
        t_min_entry.insert(0, time_min)
        float_entries.append(t_min_entry)
        
        # Label for float entry - time max
        t_max_label = tk.Label(app, text='Time Max (s):')
        t_max_label.grid(row=num_signals+5+1, column=4, padx=5, pady=5, sticky='nsew')

        # Float entry widget - time max
        t_max_entry = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
        t_max_entry.grid(row=num_signals+5+1, column=5, padx=5, pady=5, sticky='nsew')
        t_max_entry.insert(0, time_max)
        float_entries.append(t_max_entry)
        
        # Y1 min
        y1_min_label = tk.Label(app, text='Y1 Min:')
        y1_min_label.grid(row=num_signals+5+2, column=2, padx=5, pady=5, sticky='nsew')
        
        y1_min_entry = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
        y1_min_entry.grid(row=num_signals+5+2, column=3, padx=5, pady=5, sticky='nsew')
        y1_min_entry.insert(0, 0)
        float_entries.append(y1_min_entry)
        
        # Y1 max
        y1_max_label = tk.Label(app, text='Y1 Max:')
        y1_max_label.grid(row=num_signals+5+2, column=4, padx=5, pady=5, sticky='nsew')
        
        y1_max_entry = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
        y1_max_entry.grid(row=num_signals+5+2, column=5, padx=5, pady=5, sticky='nsew')
        y1_max_entry.insert(0, 0)
        float_entries.append(y1_max_entry)
        
        # Y2 min
        y2_min_label = tk.Label(app, text='Y2 Min:')
        y2_min_label.grid(row=num_signals+5+3, column=2, padx=5, pady=5, sticky='nsew')
        
        y2_min_entry = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
        y2_min_entry.grid(row=num_signals+5+3, column=3, padx=5, pady=5, sticky='nsew')
        y2_min_entry.insert(0, 0)
        float_entries.append(y2_min_entry)
        
        # Y2 max
        y2_max_label = tk.Label(app, text='Y2 Max:')
        y2_max_label.grid(row=num_signals+5+3, column=4, padx=5, pady=5, sticky='nsew')
        
        y2_max_entry = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
        y2_max_entry.grid(row=num_signals+5+3, column=5, padx=5, pady=5, sticky='nsew')
        y2_max_entry.insert(0, 0)
        float_entries.append(y2_max_entry)
        
        # X division
        x_div_label = tk.Label(app, text='X Divisions:')
        x_div_label.grid(row=num_signals+5+4, column=2, padx=5, pady=5, sticky='nsew')
        
        x_div_entry = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
        x_div_entry.grid(row=num_signals+5+4, column=3, padx=5, pady=5, sticky='nsew')
        x_div_entry.insert(0, 10)
        float_entries.append(x_div_entry)
        
        # Y division
        y_div_label = tk.Label(app, text='Y Divisions:')
        y_div_label.grid(row=num_signals+5+4, column=4, padx=5, pady=5, sticky='nsew')
        
        y_div_entry = tk.Entry(app, validate="key", validatecommand=vcmd, width=12)
        y_div_entry.grid(row=num_signals+5+4, column=5, padx=5, pady=5, sticky='nsew')
        y_div_entry.insert(0, 10)
        float_entries.append(y_div_entry)
        
        # Y1-axis 
        y1_axis_label = tk.Label(app, text='Y1-axis:')
        y1_axis_label.grid(row=num_signals+5+5, column=2, padx=5, pady=5, sticky='nsew')
        
        y1_axis_entry = tk.Entry(app, validate="key", width=12)
        y1_axis_entry.grid(row=num_signals+5+5, column=3, padx=5, pady=5, sticky='nsew')
        y1_axis_entry.insert(0, 'Label1')
        float_entries.append(y1_axis_entry)
        
        # Y2-axis
        y2_axis_label = tk.Label(app, text='Y2-axis:')
        y2_axis_label.grid(row=num_signals+5+5, column=4, padx=5, pady=5, sticky='nsew')
        
        y2_axis_entry = tk.Entry(app, validate="key", width=12)
        y2_axis_entry.grid(row=num_signals+5+5, column=5, padx=5, pady=5, sticky='nsew')
        y2_axis_entry.insert(0, 'Label2')
        float_entries.append(y2_axis_entry)
"""

