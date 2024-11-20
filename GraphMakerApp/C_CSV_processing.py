#!/usr/bin/env python
# coding: utf-8

# In[4]:


# @title Graphic Maker
import pandas as pd

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
        
        fields = [  
            ("Time Min (s):", time_min, "Time Max (s):", time_max),
            ("Y1 Min:", 0, "Y1 Max:", 0),
            ("Y2 Min:", 0, "Y2 Max:", 0),
            ("X Divisions:", 10, "Y Divisions:", 10),
            ("Y1-axis:", "Label1", "Y2-axis:", "Label2")
        ]
        
        
        # define widgets for graph setup
        for i, (label1, val1, label2, val2) in enumerate(fields):
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

        # Add a button to trigger plotting after the fields
        plot_button = tk.Button(app, text="Plot Signals", command=plot_signals, font=("Arial", 12))
        plot_button.grid(row=num_signals + 6 + len(fields), column=2, columnspan=4, pady=20, sticky='nsew')
        
        
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
    colors = set()
    while len(colors) < num_colors:
        # Generate a random color in hexadecimal format
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        colors.add(color)  
    return list(colors)

unique_colors = generate_unique_colors(num_signals)

def plot_signals():
    """Plot the graph based on selected signals and settings."""
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
    
    # Debug filtered data
    print(f"Filtered DataFrame shape: {df_filtered.shape}")
    print(f"Available columns: {df_filtered.columns.tolist()}")
    
    # Initialize plot with primary and secondary y-axes
    fig, ax = plt.subplots(figsize=(10, 6))
    secondary_ax = None  

    # Track if any signal was successfully plotted
    any_signal_plotted = False

    # Debug signal selection
    for i, dropdown in enumerate(y_dropdowns):
        print(f"Signal {i+1}: {dropdown.get()} (Plot: {plot_checkboxes[i].var.get()}, Second Y: {y_checkboxes[i].var.get()})")


    for i, dropdown in enumerate(y_dropdowns):
        # Check if a signal is selected for plotting
        if plot_checkboxes[i].var.get():
            signal_name = dropdown.get()
            
            # Validate that the selected signal exists in the DataFrame
            if signal_name in df_filtered.columns:
                color = unique_colors[i]
                any_signal_plotted = True  # At least one valid signal will be plotted
                print(f"Plotting {signal_name} with color {color}")


                # Check if it should be plotted on the secondary y-axis
                if y_checkboxes[i].var.get():
                    if secondary_ax is None:
                        secondary_ax = ax.twinx()
                    #secondary_ax.plot(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)
                    secondary_ax.scatter(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)
                    secondary_ax.set_ylabel(float_entries[9].get())  # Y2-axis label
                else:
                    print(f"Plotting {signal_name} on primary Y-axis.")
                    #ax.plot(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)
                    ax.scatter(df_filtered[time_col], df_filtered[signal_name], color=color, label=signal_name)

                    
    # Finalize and display the plot
    if any_signal_plotted:
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(float_entries[8].get())  # Y1-axis label
        ax.legend(loc='upper left')

        if secondary_ax:
            secondary_ax.legend(loc='upper right')
            
        print(f"Figure has {len(fig.axes)} axes.")
        for i, ax in enumerate(fig.axes, start=1):
            print(f"Axes {i}: {len(ax.lines)} line(s) plotted.")
        
        plt.show(block=True)
    else:
        messagebox.showwarning("Warning", "No valid signal selected for plotting. Please check your selections.")
    


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


#//////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////


# # Función para graficar
# def plot_signals(y_columns, second_axes, plot_signals_list, subplot_signals_list, title, y1_label, y2_label, time_min, time_max):



    # # Contar cuántas señales se deben graficar como subplots
    # num_subplots = sum(subplot_signals_list)

    # # Definir la figura, con subplots si es necesario
    # if num_subplots > 0:
    #     fig, axs = plt.subplots(nrows=num_subplots + 1, ncols=1, figsize=(12, 6 + 4*num_subplots))  # +1 para el gráfico principal
    # else:
    #     fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(12, 6))

    # # Si solo hay un subplot, convertir axs en una lista para consistencia
    # if num_subplots == 0:
    #     axs = [axs]
    # elif num_subplots == 1:
    #     axs = [axs[0], axs[1]]  # Asegurarse de tener una lista para manejar múltiples subplots

#//////////////////////////////////////////////////////////////////////////////////////////////////////

    # ax1 = axs[0]  # Primer gráfico será el principal
    # ax2 = None    # Almacenar el eje secundario si es necesario

    # # Listas para guardar las etiquetas de leyenda
    # y1_labels = []
    # y2_labels = []
    # handles1, handles2 = [], []
    # subplot_idx = 1

#//////////////////////////////////////////////////////////////////////////////////////////////////////

    # Graficar cada señal seleccionada
    # for i, (y_col, second_axis, plot_signal, subplot_signal) in enumerate(zip(y_columns, second_axes, plot_signals_list, subplot_signals_list)):
    #     if plot_signal:  # Solo graficar si el checkbox de 'Plot Signal' está activado
    #         if subplot_signal:  # Graficar en un subplot
    #             ax_subplot = axs[subplot_idx]  # Obtener el subplot correspondiente
    #             ax_subplot.scatter(df[x_column], df[y_col], color=unique_colors[i], alpha=0.7, label=y_col)
    #             ax_subplot.set_ylabel(y_col)
    #             ax_subplot.grid(True)

    #             # Aplicar divisiones personalizadas para el eje X en cada subplot
    #             if x_div_box.value is not None:
    #                 ax_subplot.xaxis.set_major_locator(plt.MaxNLocator(x_div_box.value))  # Aplicar divisiones en el eje X del subplot

    #             # **Aplicar los mismos límites de tiempo que en el gráfico principal**
    #             ax_subplot.set_xlim([time_min, time_max])

    #             subplot_idx += 1
    #         else:
    #             if second_axis:
    #                 if ax2 is None:  # Si no se ha creado el segundo eje, se crea
    #                     ax2 = ax1.twinx()

    #                 # Graficar en el segundo eje Y
    #                 sc = ax2.scatter(df[x_column], df[y_col], color=unique_colors[i], alpha=0.7, label=y_col)
    #                 y2_labels.append(y_col)  # Agregar a la lista de leyendas para Y2
    #                 handles2.append(sc)  # Almacenar el handle del gráfico
    #                 ax2.set_ylabel(y2_label)
    #                 #ax2.grid(True)  # Asegurarse de que el grid de Y2 esté activado
    #             else:
    #                 # Graficar en el eje Y primario
    #                 sc = ax1.scatter(df[x_column], df[y_col], color=unique_colors[i], alpha=0.7, label=y_col)
    #                 y1_labels.append(y_col)  # Agregar a la lista de leyendas para Y1
    #                 handles1.append(sc)  # Almacenar el handle del gráfico
    #                 ax1.set_ylabel(y1_label)
    #                 ax1.grid(True)  # Asegurarse de que el grid de Y2 esté activado

#//////////////////////////////////////////////////////////////////////////////////////////////////////

    # ax1.set_xlabel(x_column)
    # ax1.set_title(title)
    # ax1.set_xlim([time_min, time_max])

#//////////////////////////////////////////////////////////////////////////////////////////////////////

    # # Obtener las posiciones de los ejes en la figura
    # pos1 = ax1.get_position()  # Coordenadas del eje 1

    # # Verificación de si existe el segundo eje (ax2)
    # if ax2 is not None:
    #     pos2 = ax2.get_position()  # Coordenadas del eje 2, si existe

    # # Leyenda fuera del gráfico para el eje 1 (izquierda)
    # if y1_labels:
    #     ax1.legend(handles1, y1_labels, loc='center',
    #               bbox_to_anchor=(pos1.x0 - 0.4, pos1.y0))  # A la izquierda del eje y1

    # # Leyenda fuera del gráfico para el eje 2 (derecha), si ax2 existe
    # if y2_labels and ax2 is not None:
    #     ax2.legend(handles2, y2_labels, loc='center',
    #               bbox_to_anchor=(pos2.x1 + 0.4, pos2.y0))  # A la derecha del eje y2

#//////////////////////////////////////////////////////////////////////////////////////////////////////

    # # Aplicar divisiones personalizadas para el eje X
    # if x_div_box.value is not None:
    #     ax1.xaxis.set_major_locator(plt.MaxNLocator(x_div_box.value))  # Aplicar divisiones en el eje X

    # # Aplicar límites y divisiones personalizadas para el eje Y1
    # if y1_min_box.value is not None and y1_max_box.value is not None:
    #     if y1_min_box.value != y1_max_box.value:  # Evitar límites idénticos en Y1
    #         ax1.set_ylim([y1_min_box.value, y1_max_box.value])
    #     else:
    #         print("Error: 'Y1 Min' y 'Y1 Max' no pueden ser iguales.")

    # # Aplicar divisiones personalizadas para ambos ejes (major ticks)
    # if y_div_box.value is not None:
    #     ax1.yaxis.set_major_locator(plt.MaxNLocator(y_div_box.value))  # Aplicar divisiones principales en Y1
    #     if ax2:
    #         ax2.yaxis.set_major_locator(plt.MaxNLocator(y_div_box.value))  # Aplicar divisiones principales en Y2

    # # Aplicar límites personalizados para el eje Y2 (si existe)
    # if ax2:
    #     if y2_min_box.value is not None and y2_max_box.value is not None:
    #         if y2_min_box.value != y2_max_box.value:  # Evitar límites idénticos en Y2
    #             ax2.set_ylim([y2_min_box.value, y2_max_box.value])
    #         else:
    #             print("Error: 'Y2 Min' y 'Y2 Max' no pueden ser iguales.")

#//////////////////////////////////////////////////////////////////////////////////////////////////////

#    plt.show()

#//////////////////////////////////////////////////////////////////////////////////////////////////////

# # Crear un botón para graficar
# button = widgets.Button(description='Plot')
# output = widgets.Output()

#//////////////////////////////////////////////////////////////////////////////////////////////////////

# def on_button_clicked(b):
#     with output:
#         output.clear_output()  # Limpiar el área de salida antes de graficar

#         # Obtener las señales seleccionadas y si deben ir al segundo eje Y
#         y_columns = [dropdown.value for dropdown in y_dropdowns]
#         second_axes = [checkbox.value for checkbox in y_checkboxes]
#         plot_signals_list = [checkbox.value for checkbox in plot_checkboxes]
#         subplot_signals_list = [checkbox.value for checkbox in subplot_checkboxes]

#         # Obtener los textos de los text boxes
#         title = title_box.value
#         y1_label = y1_label_box.value
#         y2_label = y2_label_box.value

#         # Obtener los valores de los TextBoxes de tiempo
#         time_min = time_min_box.value
#         time_max = time_max_box.value

#         # Llamar a la función para graficar
#         plot_signals(y_columns, second_axes, plot_signals_list, subplot_signals_list, title, y1_label, y2_label, time_min, time_max)

# button.on_click(on_button_clicked)

#//////////////////////////////////////////////////////////////////////////////////////////////////////

# # Alinear los dropdowns, checkboxes y subplots dinámicamente usando HBox
# # Cada fila contiene un dropdown, sus respectivos checkboxes, y el checkbox para subplot
# boxes =  [widgets.HBox([y_dropdowns[i], y_checkboxes[i], subplot_checkboxes[i], plot_checkboxes[i]]) for i in range(num_signals)]
# y1_controls = widgets.HBox([y1_label_box, y1_min_box, y1_max_box, y_div_box])  # Fila para Y1: Axis, Min, Max
# y2_controls = widgets.HBox([y2_label_box, y2_min_box, y2_max_box])  # Fila para Y2: Axis, Min, Max
# time_controls = widgets.HBox([widgets.Label(layout=widgets.Layout(width='300px')),time_min_box, time_max_box, x_div_box])  # Fila para time: Min, Max

#//////////////////////////////////////////////////////////////////////////////////////////////////////

# # Mostrar los widgets y el botón
# controls = widgets.VBox([*boxes, y1_controls, y2_controls, time_controls])
# display(title_box, controls, button, output)


# # Obtener el nombre del archivo cargado
# filename = next(iter(uploaded))

# # Comprobar si el archivo es un archivo ZIP
# if filename.endswith('.zip'):
#     with zipfile.ZipFile(io.BytesIO(uploaded[filename]), 'r') as zip_ref:
#         # Descomprimir el archivo ZIP
#         zip_ref.extractall('/content/')  # Extrae todos los archivos a la carpeta /content/
#         # Obtener el primer archivo CSV dentro del ZIP
#         csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
#         if len(csv_files) > 0:
#             filename = csv_files[0]  # Usar el primer archivo CSV encontrado
#         else:
#             print("No se encontró ningún archivo CSV en el ZIP.")
# else:
#     # Si no es un archivo ZIP, asumir que es un archivo CSV
#     pass


# # Leer el archivo CSV
# df = pd.read_csv(filename, encoding='latin1')


# buttons

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

