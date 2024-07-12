import tkinter as tk
from tkinter import ttk
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import time

class SystemMonitor(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("System Monitor")
        self.geometry("1000x800")
        
        self.data_points = 300  # 5 minutes of data (300 seconds)
        self.cpu_data = [0] * self.data_points
        self.memory_data = [0] * self.data_points
        self.disk_data = [0] * self.data_points
        self.sent_data = [0] * self.data_points
        self.recv_data = [0] * self.data_points

        self.create_widgets()
        self.update_stats()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill='both')

        self.create_cpu_memory_disk_tab()
        self.create_network_tab()
        self.create_process_tab()

    def create_cpu_memory_disk_tab(self):
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='CPU/Memory/Disk')

        self.cpu_label = tk.Label(self.tab1, text="CPU Usage: ", font=("Helvetica", 14))
        self.cpu_label.pack(pady=10)

        self.memory_label = tk.Label(self.tab1, text="Memory Usage: ", font=("Helvetica", 14))
        self.memory_label.pack(pady=10)

        self.disk_label = tk.Label(self.tab1, text="Disk Usage: ", font=("Helvetica", 14))
        self.disk_label.pack(pady=10)

        self.process_frame = tk.Frame(self.tab1)
        self.process_frame.pack(pady=10, fill=tk.X)

        self.listbox_frame = tk.Frame(self.process_frame)
        self.listbox_frame.pack(pady=10)

        self.cpu_process_listbox = tk.Listbox(self.listbox_frame, width=50, height=10)
        self.cpu_process_scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.cpu_process_listbox.yview)
        self.cpu_process_listbox.config(yscrollcommand=self.cpu_process_scrollbar.set)
        self.cpu_process_listbox.pack(side=tk.LEFT, padx=5)
        self.cpu_process_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.memory_process_listbox = tk.Listbox(self.listbox_frame, width=50, height=10)
        self.memory_process_scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.memory_process_listbox.yview)
        self.memory_process_listbox.config(yscrollcommand=self.memory_process_scrollbar.set)
        self.memory_process_listbox.pack(side=tk.LEFT, padx=5)
        self.memory_process_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.disk_process_listbox = tk.Listbox(self.listbox_frame, width=50, height=10)
        self.disk_process_scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.disk_process_listbox.yview)
        self.disk_process_listbox.config(yscrollcommand=self.disk_process_scrollbar.set)
        self.disk_process_listbox.pack(side=tk.LEFT, padx=5)
        self.disk_process_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.fig1 = Figure(figsize=(8, 6), dpi=100, constrained_layout=True)
        self.cpu_plot = self.fig1.add_subplot(111)

        self.cpu_canvas = FigureCanvasTkAgg(self.fig1, master=self.tab1)
        self.cpu_canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)

    def create_network_tab(self):
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Network')

        self.network_label = tk.Label(self.tab2, text="Network Usage: Sent: 0 B, Received: 0 B", font=("Helvetica", 14))
        self.network_label.pack(pady=10)

        self.network_frame = tk.Frame(self.tab2)
        self.network_frame.pack(pady=10, fill=tk.X)

        self.inbound_label = tk.Label(self.network_frame, text="Inbound Traffic", font=("Helvetica", 12))
        self.inbound_label.pack(side=tk.LEFT, padx=5)

        self.outbound_label = tk.Label(self.network_frame, text="Outbound Traffic", font=("Helvetica", 12))
        self.outbound_label.pack(side=tk.RIGHT, padx=5)

        self.inbound_listbox = tk.Listbox(self.network_frame, width=50, height=10)
        self.inbound_scrollbar = tk.Scrollbar(self.network_frame, orient=tk.VERTICAL, command=self.inbound_listbox.yview)
        self.inbound_listbox.config(yscrollcommand=self.inbound_scrollbar.set)
        self.inbound_listbox.pack(side=tk.LEFT, padx=5)
        self.inbound_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.outbound_listbox = tk.Listbox(self.network_frame, width=50, height=10)
        self.outbound_scrollbar = tk.Scrollbar(self.network_frame, orient=tk.VERTICAL, command=self.outbound_listbox.yview)
        self.outbound_listbox.config(yscrollcommand=self.outbound_scrollbar.set)
        self.outbound_listbox.pack(side=tk.RIGHT, padx=5)
        self.outbound_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.fig2 = Figure(figsize=(8, 6), dpi=100, constrained_layout=True)
        self.network_plot = self.fig2.add_subplot(111)

        self.network_canvas = FigureCanvasTkAgg(self.fig2, master=self.tab2)
        self.network_canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)

    def create_process_tab(self):
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Processes')

        self.process_label = tk.Label(self.tab3, text="Processes: ", font=("Helvetica", 14))
        self.process_label.pack(pady=10)

        self.process_listbox_tab3 = tk.Listbox(self.tab3, width=80, height=20)
        self.process_scrollbar_tab3 = tk.Scrollbar(self.tab3, orient=tk.VERTICAL, command=self.process_listbox_tab3.yview)
        self.process_listbox_tab3.config(yscrollcommand=self.process_scrollbar_tab3.set)
        self.process_listbox_tab3.pack(pady=10, side=tk.LEFT)
        self.process_scrollbar_tab3.pack(pady=10, side=tk.LEFT, fill=tk.Y)

    def update_stats(self):
        self.update_cpu_memory_disk_stats()
        self.update_network_stats()
        self.update_process_stats()
        self.after(1000, self.update_stats)

    def format_size(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024

    def update_cpu_memory_disk_stats(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.memory_label.config(text=f"Memory Usage: {memory_usage}%")
        self.disk_label.config(text=f"Disk Usage: {disk_usage}%")

        self.cpu_data.append(cpu_usage)
        self.memory_data.append(memory_usage)
        self.disk_data.append(disk_usage)
        self.cpu_data.pop(0)
        self.memory_data.pop(0)
        self.disk_data.pop(0)

        self.cpu_plot.clear()
        x = np.arange(len(self.cpu_data))
        self.cpu_plot.fill_between(x, 0, self.cpu_data, label='CPU', color='blue', alpha=0.5)
        self.cpu_plot.fill_between(x, 0, self.memory_data, label='Memory', color='green', alpha=0.5)
        self.cpu_plot.fill_between(x, 0, self.disk_data, label='Disk', color='red', alpha=0.5)
        self.cpu_plot.set_ylim(0, 100)
        self.cpu_plot.set_title("Usage Over Time")
        self.cpu_plot.set_xlabel("Time (s)")
        self.cpu_plot.set_ylabel("Usage (%)")
        self.cpu_plot.legend(loc="upper right")

        self.cpu_canvas.draw()

        self.cpu_process_listbox.delete(0, tk.END)
        self.memory_process_listbox.delete(0, tk.END)
        self.disk_process_listbox.delete(0, tk.END)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'io_counters']):
            self.cpu_process_listbox.insert(tk.END, f"PID: {proc.info['pid']} - {proc.info['name']} - CPU: {proc.info['cpu_percent']}%")
            self.memory_process_listbox.insert(tk.END, f"PID: {proc.info['pid']} - {proc.info['name']} - Memory: {proc.info['memory_percent']:.2f}%")
            io_counters = proc.info.get('io_counters')
            if io_counters:
                self.disk_process_listbox.insert(tk.END, f"PID: {proc.info['pid']} - {proc.info['name']} - Disk Read: {self.format_size(io_counters.read_bytes)} - Disk Write: {self.format_size(io_counters.write_bytes)}")

    def update_network_stats(self):
        net_io = psutil.net_io_counters()
        self.network_label.config(text=f"Network Usage: Sent: {self.format_size(net_io.bytes_sent)}, Received: {self.format_size(net_io.bytes_recv)}")

        self.sent_data.append(net_io.bytes_sent)
        self.recv_data.append(net_io.bytes_recv)
        self.sent_data.pop(0)
        self.recv_data.pop(0)

        self.network_plot.clear()
        x = np.arange(len(self.sent_data))
        self.network_plot.fill_between(x, 0, self.sent_data, label='Bytes Sent', color='blue', alpha=0.5)
        self.network_plot.fill_between(x, 0, self.recv_data, label='Bytes Received', color='green', alpha=0.5)
        self.network_plot.set_title("Network Usage Over Time")
        self.network_plot.set_xlabel("Time (s)")
        self.network_plot.set_ylabel("Data Transferred")
        self.network_plot.legend(loc="upper right")

        self.network_canvas.draw()

        self.inbound_listbox.delete(0, tk.END)
        self.outbound_listbox.delete(0, tk.END)
        for conn in psutil.net_connections():
            if conn.laddr:
                self.inbound_listbox.insert(tk.END, f"IP: {conn.laddr.ip} Port: {conn.laddr.port} Status: {conn.status}")
            if conn.raddr and isinstance(conn.raddr, tuple):
                self.outbound_listbox.insert(tk.END, f"IP: {conn.raddr.ip} Port: {conn.raddr.port} Status: {conn.status}")

    def update_process_stats(self):
        self.process_listbox_tab3.delete(0, tk.END)
        for proc in psutil.process_iter(['pid', 'name']):
            self.process_listbox_tab3.insert(tk.END, f"PID: {proc.info['pid']} - {proc.info['name']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitor(root)
    root.mainloop()
