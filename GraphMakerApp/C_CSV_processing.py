#!/usr/bin/env python
# coding: utf-8

# In[4]:


# @title Graphic Maker
import pandas as pd
import numpy as np

import matplotlib
print(matplotlib.get_backend())  # Confirm backend
matplotlib.use('TkAgg')  # Change to an appropriate one for your OS

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.legend import Legend
import matplotlib.colors as mcolors

#import random

#from textwrap import wrap

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

# Initialize the global variable to track the text object
analysis_text_obj = None

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
            checkbox = tk.Checkbutton(app, text="Second Y-axis", variable=y_axis_var)
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
            ("Second Y-axis Min:", 0, "Second Y-axis Max:", 0),
            ("X Divisions:", 10, "Y Divisions:", 10),
        ]
        
        label_fields = [
            ("Y-axis Label:", "Label1", "Second Y-axis Label:", "Label2")
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
    """Function to validate entries and show error if any max values are invalid."""
    try:
        # Convert the entry values to floats
        value_y1_max = float(float_entries[3].get())
        value_y2_max = float(float_entries[5].get())
        
        # Ensure Y1 max is greater than 0
        if value_y1_max <= 0:
            messagebox.showerror("Error", "Entry 'Y-axis Max' must be greater than zero.")
            return False
        
        # Validate Right Y-axis Max only if the checkbox is checked
        for checkbox in y_checkboxes:
            if checkbox.var.get():  # If the checkbox for the second Y-axis is checked
                if value_y2_max <= 0:
                    messagebox.showerror("Error", "Entry 'Second Y-axis Max' must be greater than zero when enabled.")
                    return False
        
    except ValueError:
        messagebox.showerror("Error", "Entries 'Y-axis Max' and 'Second Y-axis Max' contain invalid values.")  # Display error for non-numeric
        return False
    
    return True


def generate_unique_colors(num_colors):
    """Function to define unique colors for plotting"""
    """
    random.seed(5)
    colors = set()
    while len(colors) < num_colors:
        # Generate a random color in hexadecimal format
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        colors.add(color)  
    return list(colors)
    """
    """Generate a list of visually distinct colors."""
    if num_colors <= 12:
        # Use a predefined, high-contrast palette for smaller numbers
        base_colors = [
            "#e6194b", "#3cb44b", "#4363d8", "#f58231",
            "#911eb4", "#46f0f0", "#f032e6", "#808080",
            "#008080", "#e6beff", "#9a6324", "#808000",  
            "#fffac8", "#ffd8b1", "#000075", "#800000"
        ]
        return base_colors[:num_colors]
    else:
        # For larger numbers, generate evenly spaced colors in HSL space
        hues = np.linspace(0, 1, num_colors, endpoint=False)
        colors = [mcolors.hsv_to_rgb((hue, 0.7, 0.8)) for hue in hues]
        hex_colors = [mcolors.rgb2hex(color) for color in colors]
        return hex_colors

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
        ax_right = None  # Initialize the second Y-axis
    
        for i, (signal_name, color) in enumerate(combined_signals):
            if y_checkboxes[i].var.get():  # Check if the second Y-axis is enabled for this signal
                if ax_right is None:  # Create the second Y-axis only once
                    ax_right = ax_combined.twinx()
                    ax_right.set_ylabel(float_entries[9].get())  # Set the label for the second Y-axis
            
                # Plot the signal on the second Y-axis
                ax_right.scatter(df_filtered[time_col], df_filtered[signal_name], color=color, label=f"{signal_name}")
            else:
                # Plot the signal on the primary (left) Y-axis
                ax_combined.scatter(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)
    
        graph_title = title.get()
        ax_combined.set_title(graph_title)
        ax_combined.set_xlabel("Time (s)")
        ax_combined.set_ylabel(float_entries[8].get())  # Y-axis label for combined plot
        ax_combined.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)
        ax_combined.tick_params(axis='x', which='both', labelbottom=True)  # Ensure x-axis numbers are displayed
        
        x_div = int(float_entries[6].get()) + 1
        y_div = int(float_entries[7].get()) + 1
    
        x_ticks = np.linspace(t_min, t_max, num=x_div)
        ax_combined.set_xticks(x_ticks)
        ax_combined.set_xlim([t_min, t_max])
        
        y_ticks = np.linspace(float(float_entries[2].get()), float(float_entries[3].get()), num=y_div)
        ax_combined.set_yticks(y_ticks)
        ax_combined.set_ylim([float(float_entries[2].get()), float(float_entries[3].get())])
        
        # Second y-axis
        right_y_min = float(float_entries[4].get())
        right_y_max = float(float_entries[5].get())
        right_y_div = y_div #int(float_entries[7].get()) + 1
        right_y_ticks = np.linspace(right_y_min, right_y_max, num=right_y_div)

        if ax_right: 
            ax_right.set_yticks(right_y_ticks)
            ax_right.set_ylim(right_y_min, right_y_max)
            
        # legend
        from matplotlib.lines import Line2D  # For creating proxy artists

        # Obtain handles and labels from both axes
        handles1, labels1 = ax_combined.get_legend_handles_labels()
        if ax_right is not None:
            handles2, labels2 = ax_right.get_legend_handles_labels()
        else:
            handles2, labels2 = [], []

        # Create proxy artists for group titles
        group_title_style = Line2D([0], [0], color='none', linestyle='none')  # Invisible marker

        # Prepare custom legend entries
        custom_labels = []
        custom_handles = []
        
        # Add a blank entry for spacing
        custom_labels.append("")  # Empty label
        custom_handles.append(group_title_style)  # Invisible handle for spacing

        # Group for the Y-axis
        if handles1:
            custom_labels.append("Y - AXIS SIGNALS:")
            custom_handles.append(group_title_style)  # Placeholder for the group title
            custom_labels.extend(labels1)
            custom_handles.extend(handles1)
            
        # Add a blank entry for spacing
        custom_labels.append("")  # Empty label
        custom_handles.append(group_title_style)  # Invisible handle for spacing

        # Group for the Second Y-axis
        if handles2:
            custom_labels.append("SECOND Y - AXIS SIGNALS:")
            custom_handles.append(group_title_style)  # Placeholder for the group title
            custom_labels.extend(labels2)
            custom_handles.extend(handles2)

        # Create the legend
        legend = Legend(
            fig, custom_handles, custom_labels,
            loc='upper right',  # Place it to the right of the figure
            #bbox_to_anchor=(0.99, 0.5),  # Adjust for desired placement
            borderaxespad=0,
            frameon=False,
            handletextpad=1,
            fontsize=10,
            title="LEGEND",  
            )
        legend._legend_box.align = "left" 
        
        # Add space by adding a newline before the title
        legend.set_title(f"\nLEGEND") 

        # Add the custom legend to the figure
        ax_combined.add_artist(legend)

        # Adjust layout to leave space for the legend
        fig.tight_layout(rect=[0, 0.2, 0.65, 1])  # Adjust right-side spacing
                
                
    # Plot each signal in its own subplot
    for ax, (signal_name, color) in zip(axes[1:], subplot_signals):
        ax.scatter(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)
        #ax.set_title(f"{signal_name}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(signal_name)
        ax.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)
        ax.tick_params(axis='x', which='both', labelbottom=True) 
        
    
    # Add the figure to the Tkinter canvas
    canvas_widget = FigureCanvasTkAgg(fig, master=scrollable_frame)
    canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Add the Matplotlib navigation toolbar
    toolbar_frame = tk.Frame(scrollable_frame)  # Place toolbar inside the scrollable area
    toolbar_frame.pack(fill=tk.X, padx=10, pady=5)
    toolbar = NavigationToolbar2Tk(canvas_widget, toolbar_frame)
    toolbar.update()

    # Add a Text widget for user input below the plots, also inside the scrollable frame
    analysis_text = tk.Text(scrollable_frame, height=5, width=100)
    analysis_text.pack(side=tk.BOTTOM, padx=10, pady=10)

    def custom_save(*args, **kwargs):
        """Custom save function to include analysis text in the saved figure."""
        global analysis_text_obj  # Keep a reference to the text object
        
        analysis = analysis_text.get("1.0", "end-1c")  # Get the user input
    
        # Remove the old text object if it exists
        if analysis_text_obj is not None:
            try:
                analysis_text_obj.remove()  # Remove the text object from the figure
            except Exception as e:
                print(f"Error while removing old text: {e}")
            finally:
                analysis_text_obj = None
            
        if analysis.strip():  # If there is any text
            # Measure the text length and calculate the required space
            text_length = len(analysis)
            base_space = 0.3  # Base space for the text
            extra_space = 0.015 * (text_length // 50)  # Add extra space for every 50 characters
            reserved_space = base_space + extra_space
        
            # Limit how much space the text can take
            if reserved_space > 0.4:
                reserved_space = 0.4

            # Reserve space below the figure for the analysis text
            fig.subplots_adjust(bottom=reserved_space)

            # Add the text to the figure as a footer
            analysis_text_obj = fig.text(
                0.1, 0.03,  # Adjust the position dynamically
                f"Test report comments:\n {analysis}",  # Single line of text
                ha="left", fontsize=10, color="black"
                )
    
        original_save(*args, **kwargs)  # Call the original save function

    original_save = canvas_widget.print_figure  # Keep a reference to the original save function
    canvas_widget.print_figure = custom_save  # Override with the custom save function

    # Finalize
    canvas_widget.draw()

    plot_window.mainloop()
    
    
"""
# Add the analysis input space below the plots
def update_analysis():
    analysis = analysis_text.get("1.0", "end-1c")  # Get the user input
    print(f"Analysis: {analysis}")
    # You can save the analysis with the plot if needed
    fig.savefig("plot_with_analysis.png")  # Save the plot with the analysis

# Create a Text widget for user input below the plots
analysis_text = tk.Text(plot_window, height=5, width=100)
analysis_text.pack(side=tk.BOTTOM, padx=10, pady=10)

# Create a button to submit analysis
submit_button = tk.Button(plot_window, text="Submit Analysis", command=update_analysis)
submit_button.pack(side=tk.BOTTOM, pady=10)
        

# Add the figure to the Tkinter canvas
canvas_widget = FigureCanvasTkAgg(fig, master=scrollable_frame)
canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas_widget.draw()

# Add the Matplotlib navigation toolbar
toolbar_frame = tk.Frame(plot_window)
toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
toolbar = NavigationToolbar2Tk(canvas_widget, toolbar_frame)
toolbar.update()
"""
    
    
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

