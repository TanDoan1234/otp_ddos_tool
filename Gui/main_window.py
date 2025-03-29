#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - Main Window
Cửa sổ chính của ứng dụng
"""

import tkinter as tk
from tkinter import ttk

from Gui.Tabs.spam_tab import SpamTab
from Gui.Tabs.ddos_tab import DDoSTab
from Gui.Tabs.stats_tab import StatsTab
from Core.stats_manager import StatsManager

class OTPToolApp:
    """Lớp chính quản lý giao diện người dùng"""
    
    def __init__(self, root):
        """
        Khởi tạo ứng dụng
    
        Args:
        root: Cửa sổ gốc Tkinter
        """
        self.root = root
    
        #Thêm dòng này để khởi tạo status_var
        self.status_var = tk.StringVar()
        self.status_var.set("Sẵn sàng")
    
        # Cài đặt style
        self.setup_styles()
    
        # Tạo Stats Manager để chia sẻ dữ liệu giữa các tabs
        self.stats_manager = StatsManager()
    
        # Tạo notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        # Tạo các tab
        self.create_tabs()
    
        # Status bar
        # Thay đổi phần này để sử dụng status_var đã tạo ở trên
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_styles(self):
        """Cài đặt style cho các widget"""
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TCheckbutton', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12, 'bold'))
    
    def create_tabs(self):
        """Tạo các tab cho ứng dụng"""
        # Tab chính
        self.spam_tab = SpamTab(
            self.notebook, 
            self.status_var, 
            self.stats_manager
        )
        self.notebook.add(self.spam_tab.frame, text="Spam OTP")
        
        # Tab cài đặt DDoS nâng cao
        self.ddos_tab = DDoSTab(
            self.notebook,
            self.stats_manager
        )
        self.notebook.add(self.ddos_tab.frame, text="Cài đặt DDoS")
        
        # Tab thống kê
        self.stats_tab = StatsTab(
            self.notebook,
            self.stats_manager
        )
        self.notebook.add(self.stats_tab.frame, text="Thống kê")
        
        # Kết nối các tab lại với nhau
        self.spam_tab.set_ddos_tab(self.ddos_tab)
        self.spam_tab.set_stats_tab(self.stats_tab)