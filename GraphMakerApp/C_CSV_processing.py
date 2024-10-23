#!/usr/bin/env python
# coding: utf-8

# In[4]:


# @title Graphic Maker
import pandas as pd
import matplotlib.pyplot as plt

# package to handle GUI application for file upload
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, Tk
from tkinter import ttk


#from IPython.display import display
#from IPython.display import display, clear_output
#import numpy as np
#import zipfile
#import io
#import random

#//////////////////////////////////////////////////////////////////////////////////////////////////////

# define global df variable
df = None

# The number of signals we plot in the sequel
num_signals = 12

# Global lists to store the generated widgets
y_dropdowns = []
y_checkboxes = []
plot_checkboxes = []
subplot_checkboxes = []
float_entries = []

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
            checkbox = tk.Checkbutton(app, text="Second Y-Axis")
            checkbox.grid(row=i+3, column=2, padx=5, pady=5, sticky='nsew')
            y_checkboxes.append(checkbox)

            # Checkbox for plotting the signal (fourth column)
            plot_checkbox = tk.Checkbutton(app, text=f'Plot Signal {i+1}')
            plot_checkbox.grid(row=i+3, column=3, padx=5, pady=5, sticky='nsew')
            plot_checkboxes.append(plot_checkbox)

            # Checkbox for subplot (fifth column)
            subplot_checkbox = tk.Checkbutton(app, text=f'Subplot Signal {i+1}')
            subplot_checkbox.grid(row=i+3, column=4, padx=5, pady=5, sticky='nsew')
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
