import tkinter as tk
import zipfile
import os
import pandas as pd
from tkinter import filedialog
from tkinter import messagebox
import datetime

#----------------- FILE SELECTION -----------------
root = tk.Tk()
root.withdraw()

messagebox.showinfo("File selection", "Select your .zip file.")
file_path = filedialog.askopenfilename()
file_name = os.path.basename(file_path)
#----------------- FILE SELECTION -----------------

#----------------- NEW FILE SELECTION --------------
messagebox.showinfo("New file", "Select the name and the path to save the new file.")

new_file_path = filedialog.asksaveasfilename(defaultextension=".txt")
#----------------- NEW FILE SELECTION --------------

#----------------- FILES MERGE --------------------
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    txt_dir = ''
    for file_name in zip_ref.namelist():
        if file_name.endswith('.txt'):
            txt_dir = os.path.dirname(file_name)
            break

    with open(new_file_path, 'w') as outfile:
        for file_name in zip_ref.namelist():
            if file_name.endswith('.txt'):
                with zip_ref.open(file_name) as infile:
                    outfile.write(infile.read().decode('utf-8'))

messagebox.showinfo("Merge Result", f"The contents of the text files have been merged into {new_file_path}.")
#----------------- FILES MERGE --------------------

#--------------------- FILES METRICS --------------
with open(new_file_path) as f:
    content = f.readlines()
    OS_RST_dates = []
    MRST_dates = []
    BTRC_dates = []
    for line in content:
        if "OS_RST" in line:
            date = line.split(";")[0]
            OS_RST_dates.append(date)
        if "MRST = 1" in line:
            date = line.split(";")[0]
            MRST_dates.append(date)
        if "BTRC lost connection" in line:
            date = line.split(";")[0]
            BTRC_dates.append(date)

    OS_RST_count = len(OS_RST_dates)
    MRST_count = len(MRST_dates)
    BTRC_count = len(BTRC_dates)
#-------------------------- TIME DIFERENCE ----------------------------------

def calculate_time_difference(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    disconnected_time = None
    connected_time = None
    for line in lines:
        if "BTRC lost connection" in line:
            disconnected_time = datetime.datetime.strptime(line[:23], '%d-%m-%Y %H:%M:%S.%f')
        if "BTRC connected" in line:
            connected_time = datetime.datetime.strptime(line[:23], '%d-%m-%Y %H:%M:%S.%f')
        if disconnected_time and connected_time:
            break
    time_difference = abs(connected_time - disconnected_time)
    time_difference_in_minutes = time_difference.total_seconds() / 60
    return time_difference_in_minutes

time_difference = calculate_time_difference(new_file_path)
print("Time difference between BTRC lost connection and connection: {:.2f}".format(time_difference))

# --------------------- METRICS DISPLAY --------------
metrics_window = tk.Tk()
metrics_window.title("Files Metrics")
metrics_window.geometry("800x800")

OS_RST_label = tk.Label(metrics_window, text="OS_RST occurrences:", font=("Arial", 12, "bold"))
OS_RST_count_label = tk.Label(metrics_window, text=OS_RST_count, font=("Arial", 12))
OS_RST_dates_label = tk.Label(metrics_window, text="OS_RST occurrence dates:", font=("Arial", 12, "bold"))

OS_RST_scrollbar = tk.Scrollbar(metrics_window)
OS_RST_dates_text = tk.Text(metrics_window, height=5, width=30, yscrollcommand=OS_RST_scrollbar.set)
OS_RST_dates_text.insert(tk.END, '\n'.join(OS_RST_dates))
OS_RST_scrollbar.config(command=OS_RST_dates_text.yview)

MRST_label = tk.Label(metrics_window, text="MRST occurrences:", font=("Arial", 12, "bold"))
MRST_count_label = tk.Label(metrics_window, text=MRST_count, font=("Arial", 12))
MRST_dates_label = tk.Label(metrics_window, text="MRST occurrence dates:", font=("Arial", 12, "bold"))

MRST_scrollbar = tk.Scrollbar(metrics_window)
MRST_dates_text = tk.Text(metrics_window, height=5, width=30, yscrollcommand=MRST_scrollbar.set)
MRST_dates_text.insert(tk.END, '\n'.join(MRST_dates))
MRST_scrollbar.config(command=MRST_dates_text.yview)

BTRC_label = tk.Label(metrics_window, text="BTRC lost connection occurrences:", font=("Arial", 12, "bold"))
BTRC_count_label = tk.Label(metrics_window, text=BTRC_count, font=("Arial", 12))
BTRC_dates_label = tk.Label(metrics_window, text="BTRC lost connection occurrence dates:", font=("Arial", 12, "bold"))

BTRC_scrollbar = tk.Scrollbar(metrics_window)
BTRC_dates_text = tk.Text(metrics_window, height=5, width=30, yscrollcommand=BTRC_scrollbar.set)
BTRC_dates_text.insert(tk.END, '\n'.join(BTRC_dates))
BTRC_scrollbar.config(command=BTRC_dates_text.yview)

summary_label = tk.Label(metrics_window, text="Summary:", font=("Arial", 12, "bold"))
summary_text = tk.Label(metrics_window, text=f"PM7 had {OS_RST_count + MRST_count} resets, which {OS_RST_count} of them were from Operating System resets, {MRST_count} of them were from APP resets.\nAlso, there were {BTRC_count} BTRC connection losts.", font=("Arial", 12))

OS_RST_label.pack()
OS_RST_count_label.pack()
OS_RST_dates_label.pack()
OS_RST_dates_text.pack()

MRST_label.pack()
MRST_count_label.pack()
MRST_dates_label.pack()
MRST_dates_text.pack()

BTRC_label.pack()
BTRC_count_label.pack()
BTRC_dates_label.pack()
BTRC_dates_text.pack()

summary_label.pack(pady=20)
summary_text.pack()

metrics_window.mainloop()


# --------------------- METRICS DISPLAY --------------