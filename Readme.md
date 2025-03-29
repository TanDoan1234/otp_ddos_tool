# OTP DDoS Tool

**CHỈ SỬ DỤNG CHO MỤC ĐÍCH NGHIÊN CỨU VÀ KHÓA LUẬN BẢO MẬT**

Công cụ mô phỏng tấn công DDoS thông qua các dịch vụ gửi OTP. Đây là một công cụ **DEMO** được phát triển cho nghiên cứu về bảo mật và chỉ nên được sử dụng trong môi trường kiểm thử có kiểm soát.

## Cảnh báo

**CẢNH BÁO**: Công cụ này KHÔNG gửi các request thực đến bất kỳ dịch vụ nào và chỉ mô phỏng quá trình tấn công. Sử dụng công cụ tương tự để tấn công bất kỳ hệ thống nào mà không có sự cho phép rõ ràng là **BẤT HỢP PHÁP** và có thể bị truy tố theo luật pháp.

Tác giả không chịu trách nhiệm về bất kỳ thiệt hại nào gây ra bởi việc sử dụng sai mục đích công cụ này.

## Mô tả

OTP DDoS Tool là một công cụ demo cung cấp giao diện đồ họa để mô phỏng tấn công DDoS thông qua việc spam OTP. Công cụ này được phát triển để giúp nghiên cứu và hiểu rõ hơn về cách thức hoạt động của các cuộc tấn công DDoS thông qua dịch vụ xác thực hai yếu tố.

### Tính năng

- Giao diện đồ họa dễ sử dụng
- Mô phỏng gửi OTP đến nhiều dịch vụ
- Hỗ trợ multi-threading
- Cài đặt proxy và xoay vòng IP
- Thống kê và biểu đồ theo thời gian thực
- Xuất báo cáo kiểm thử

## Cấu trúc dự án

```
otp_ddos_tool/
│
├── main.py                  # File chính để chạy ứng dụng
├── README.md                # Tài liệu hướng dẫn
│
├── gui/
│   ├── __init__.py          # Package marker
│   ├── main_window.py       # Cửa sổ chính của ứng dụng
│   ├── disclaimer.py        # Cửa sổ disclaimer
│   ├── tabs/
│   │   ├── __init__.py      # Package marker
│   │   ├── spam_tab.py      # Tab chính để spam OTP
│   │   ├── ddos_tab.py      # Tab cài đặt DDoS
│   │   └── stats_tab.py     # Tab thống kê
│   └── widgets/
│       ├── __init__.py      # Package marker
│       └── charts.py        # Widget vẽ biểu đồ
│
├── services/
│   ├── __init__.py          # Package marker
│   ├── otp_services.py      # Các dịch vụ OTP
│   └── proxy_manager.py     # Quản lý proxy
│
└── core/
    ├── __init__.py          # Package marker
    ├── ddos_engine.py       # Engine DDoS
    ├── stats_manager.py     # Quản lý thống kê
    ├── utils.py             # Các hàm tiện ích
    └── config.py            # Cấu hình chung
```

## Cài đặt

1. Yêu cầu Python 3.6 hoặc cao hơn
2. Clone repository hoặc tải source code
3. Không cần cài đặt thêm thư viện bên ngoài (chỉ dùng các thư viện tiêu chuẩn của Python)

## Sử dụng

1. Chạy file `main.py`:

   ```
   python main.py
   ```

2. Đọc và đồng ý với disclaimer

3. Nhập số điện thoại mục tiêu và chọn các dịch vụ

4. Cấu hình các tùy chọn DDoS nâng cao (tùy chọn)

5. Nhấn nút "GỬI OTP" để bắt đầu mô phỏng

6. Xem thống kê và kết quả trong tab "Thống kê"

## Lưu ý cho nghiên cứu

Công cụ này được phát triển cho nghiên cứu bảo mật và có thể được sử dụng cho các mục đích sau:

1. Nghiên cứu về cơ chế tấn công DDoS qua OTP
2. Phát triển các biện pháp phòng thủ chống lại tấn công spam OTP
3. Kiểm thử khả năng chịu tải của hệ thống xác thực hai yếu tố
4. Phân tích và đánh giá hiệu quả của các biện pháp rate limiting

## Giấy phép

OTP DDoS Tool được phát hành dưới giấy phép MIT.

## Tác giả

Nguyễn Hoàng - Khóa luận nghiên cứu bảo mật
