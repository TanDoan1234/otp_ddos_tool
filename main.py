import tkinter as tk
from tkinter import ttk
import sys
import os

# Thêm thư mục gốc vào đường dẫn
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    # Import các module cần thiết
    from Gui.Tabs.spam_tab import SpamTab
    from Gui.Tabs.ddos_tab import DDoSTab
    from Gui.Tabs.stats_tab import StatsTab
    from Gui.disclaimer import show_disclaimer
    
    # Import StatsManager (nếu có)
    try:
        from Core.stats_manager import StatsManager
    except ImportError:
        try:
            from Core.stats_manager import StatsManager
        except ImportError:
            # Tạo StatsManager giả nếu không import được
            class StatsManager:
                def __init__(self):
                    self.stats = {
                        "requests_count": 0,
                        "success_count": 0,
                        "failed_count": 0,
                        "ratelimited_count": 0,
                        "elapsed_time": 0,
                        "success_ratio": 0,
                        "failed_ratio": 0,
                        "ratelimited_ratio": 0
                    }
                
                def get_stats(self):
                    return self.stats
                
                def get_settings(self):
                    return {}
                
                def update_stats(self, **kwargs):
                    for key, value in kwargs.items():
                        if key in self.stats:
                            self.stats[key] = value
                
                def reset_stats(self):
                    self.stats = {
                        "requests_count": 0,
                        "success_count": 0,
                        "failed_count": 0,
                        "ratelimited_count": 0,
                        "elapsed_time": 0,
                        "success_ratio": 0,
                        "failed_ratio": 0,
                        "ratelimited_ratio": 0
                    }
except Exception as e:
    print(f"Lỗi khi import modules: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

class OTPToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OTP TOOL - ĐOÀN MINH TÂN DEV")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Tạo biến status và StatsManager
        self.status_var = tk.StringVar(root, "Sẵn sàng")
        self.stats_manager = StatsManager()
        
        # Kiểm tra disclaimer trước khi hiển thị ứng dụng
        self.show_app()
    
    def show_app(self):
        # Tạo Notebook (TabControl)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tạo các tab
        self.spam_tab = None
        self.ddos_tab = None
        self.stats_tab = None
        
        # Tạo từng tab trong khối try/except riêng
        try:
            # Tạo SpamTab
            self.spam_tab = SpamTab(self.notebook, self.status_var, self.stats_manager)
            self.notebook.add(self.spam_tab.frame, text="Spam OTP")
            print("SpamTab created successfully")
        except Exception as e:
            print(f"Lỗi khi tạo SpamTab: {e}")
            import traceback
            traceback.print_exc()
            
            # Tạo tab thay thế nếu lỗi
            spam_frame = ttk.Frame(self.notebook)
            ttk.Label(spam_frame, text="Không thể tải tab Spam OTP").pack(pady=20)
            self.notebook.add(spam_frame, text="Spam OTP")
        
        try:
            # Tạo DDoSTab 
            self.ddos_tab = DDoSTab(self.notebook)
            self.notebook.add(self.ddos_tab, text="Cài đặt DDoS")
            print("DDoSTab created successfully")
        except Exception as e:
            print(f"Lỗi khi tạo DDoSTab: {e}")
            import traceback
            traceback.print_exc()
            
            # Tạo tab thay thế nếu lỗi
            ddos_frame = ttk.Frame(self.notebook)
            ttk.Label(ddos_frame, text="Không thể tải tab DDoS").pack(pady=20)
            self.notebook.add(ddos_frame, text="Cài đặt DDoS")
        
        try:
            # Tạo StatsTab
            self.stats_tab = StatsTab(self.notebook, self.stats_manager)
            self.notebook.add(self.stats_tab.frame, text="Thống kê")
            print("StatsTab created successfully")
        except Exception as e:
            print(f"Lỗi khi tạo StatsTab: {e}")
            import traceback
            traceback.print_exc()
            
            # Tạo tab thay thế nếu lỗi
            stats_frame = ttk.Frame(self.notebook)
            ttk.Label(stats_frame, text="Không thể tải tab Thống kê").pack(pady=20)
            self.notebook.add(stats_frame, text="Thống kê")
        
        # Thiết lập liên kết giữa các tab
        if self.spam_tab and self.ddos_tab and self.stats_tab:
            try:
                self.spam_tab.set_ddos_tab(self.ddos_tab)
                self.spam_tab.set_stats_tab(self.stats_tab)
            except Exception as e:
                print(f"Lỗi khi thiết lập liên kết giữa các tab: {e}")

def main():
    # Tạo cửa sổ root
    root = tk.Tk()
    
    try:
        # Hiển thị disclaimer
        if show_disclaimer(root):
            app = OTPToolApp(root)
            root.mainloop()
        else:
            root.destroy()
            sys.exit(0)
    except Exception as e:
        print(f"Lỗi khi khởi chạy ứng dụng: {e}")
        import traceback
        traceback.print_exc()
        root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    main()