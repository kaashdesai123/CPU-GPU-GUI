import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import socket
import pandas as pd
import matplotlib.animation as animation

class SystemMonitor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title("System Monitor")

        self.fig, self.ax = plt.subplots(2, 2, figsize=(8, 6))

        self.cpu_data = [0] * 60
        self.mem_data = [0] * 60

        self.create_widgets()

        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000)

    def create_widgets(self):
        nb = ttk.Notebook(self)

        page1 = ttk.Frame(nb)
        nb.add(page1, text='Dashboard')

        cpu_canvas = FigureCanvasTkAgg(self.fig, master=page1)
        cpu_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        page2 = ttk.Frame(nb)
        nb.add(page2, text='System Info')

        tree = ttk.Treeview(page2)
        tree["columns"]=("one","two")
        tree.heading("one", text="Property")
        tree.heading("two", text="Value")

        properties = {
            'Hostname': socket.gethostname(),
            'IP Address': socket.gethostbyname(socket.gethostname())
        }

        for key, value in properties.items():
            tree.insert("", 0, text=key, values=(value,))

        tree.pack()

        page3 = ttk.Frame(nb)
        nb.add(page3, text='Processes')

        self.proc_tree = ttk.Treeview(page3)
        self.proc_tree["columns"]=("one","two")
        self.proc_tree.heading("one", text="PID")
        self.proc_tree.heading("two", text="Name")

        self.proc_tree.pack()

        nb.pack(fill='both', expand='yes')

    def update_plot(self, i):
        self.update_stats()
        self.ax[0, 0].cla()
        self.ax[0, 0].plot(self.cpu_data, label='CPU usage (%)')
        self.ax[0, 0].legend(loc='upper left')

        self.ax[0, 1].cla()
        self.ax[0, 1].plot(self.mem_data, label='Memory usage (%)')
        self.ax[0, 1].legend(loc='upper left')
        
        mem_info = psutil.virtual_memory()
        labels = ['Available', 'Used']
        sizes = [mem_info.available, mem_info.used]
        self.ax[1, 0].cla()
        self.ax[1, 0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        self.ax[1, 0].axis('equal')

        disk_info = psutil.disk_usage('/')
        labels = ['Free', 'Used']
        sizes = [disk_info.free, disk_info.used]
        self.ax[1, 1].cla()
        self.ax[1, 1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        self.ax[1, 1].axis('equal')

    def update_stats(self):
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()

        self.cpu_data.append(cpu_percent)
        self.cpu_data = self.cpu_data[-60:]

        self.mem_data.append(memory_info.percent)
        self.mem_data = self.mem_data[-60:]

        for i in self.proc_tree.get_children():
            self.proc_tree.delete(i)

        for proc in psutil.process_iter(['pid', 'name']):
            self.proc_tree.insert("", "end", text=str(proc.info['pid']), values=(proc.info['name'],))

if __name__ == "__main__":
    app = SystemMonitor()
    app.mainloop()
