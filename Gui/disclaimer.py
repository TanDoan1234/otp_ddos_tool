#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTP DDoS Tool - Disclaimer
Hiển thị thông báo cảnh báo và điều khoản sử dụng
"""

import tkinter as tk
from tkinter import ttk, messagebox

def show_disclaimer(parent):
    """
    Hiển thị disclaimer và yêu cầu người dùng đồng ý
    
    Args:
        parent: Cửa sổ cha
        
    Returns:
        bool: True nếu người dùng đồng ý, False nếu không
    """
    print("Starting show_disclaimer function")
    
    # Biến để theo dõi kết quả
    result = {'agreed': False}
    
    # Tạo cửa sổ disclaimer
    disclaimer = tk.Toplevel(parent)
    disclaimer.title("CẢNH BÁO - CHỈ DÙNG CHO NGHIÊN CỨU")
    disclaimer.geometry("500x300")
    disclaimer.transient(parent)
    
    print("Created disclaimer window")
    
    disclaimer_frame = ttk.Frame(disclaimer, padding=20)
    disclaimer_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(
        disclaimer_frame, 
        text="CÔNG CỤ NGHIÊN CỨU BẢO MẬT",
        font=("Arial", 14, "bold")
    ).pack(pady=(0, 10))
    
    message = """
    CẢNH BÁO: Công cụ này được phát triển CHỈ cho mục đích nghiên cứu học thuật
    về bảo mật và kiểm thử DDoS. Sử dụng công cụ này để tấn công bất kỳ hệ thống
    nào mà không có sự cho phép rõ ràng là BẤT HỢP PHÁP và có thể bị truy tố
    theo luật pháp.
    
    Công cụ này là một phần của khóa luận nghiên cứu học thuật và nên được sử
    dụng CHỈ trong môi trường kiểm thử có kiểm soát.
    """
    
    text_area = tk.Text(
        disclaimer_frame, 
        wrap=tk.WORD, 
        height=10,
        font=("Arial", 10),
        background="#fff8dc"
    )
    text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    text_area.insert(tk.END, message)
    text_area.config(state=tk.DISABLED)
    
    agree_var = tk.BooleanVar()
    ttk.Checkbutton(
        disclaimer_frame,
        text="Tôi hiểu và đồng ý chỉ sử dụng công cụ này cho mục đích nghiên cứu",
        variable=agree_var
    ).pack(pady=(0, 10))
    
    def on_agree():
        """Xử lý khi người dùng nhấn nút đồng ý"""
        print("Agree button clicked")
        if agree_var.get():
            result['agreed'] = True
            disclaimer.destroy()
        else:
            messagebox.showerror("Lỗi", "Bạn phải đồng ý với điều khoản để sử dụng công cụ này!")
    
    def on_close():
        """Xử lý khi người dùng đóng cửa sổ"""
        print("Close button clicked")
        result['agreed'] = False
        disclaimer.destroy()
    
    ttk.Button(
        disclaimer_frame,
        text="Đồng ý và Tiếp tục",
        command=on_agree
    ).pack(fill=tk.X)
    
    # Ngăn người dùng đóng bằng nút X
    disclaimer.protocol("WM_DELETE_WINDOW", on_close)
    
    # Đảm bảo cửa sổ disclaimer hiển thị
    disclaimer.update()
    disclaimer.deiconify()
    
    print("Waiting for user response")
    parent.wait_window(disclaimer)
    print(f"User response: {result['agreed']}")
    
    return result['agreed']