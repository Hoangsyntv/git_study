# 🚀 KiotViet API Tool

Tool phân tích dữ liệu bán hàng từ KiotViet API với báo cáo chi tiết.

## 📋 Tính năng

- ✅ Kết nối KiotViet API với OAuth 2.0
- ✅ Phân tích top sản phẩm theo số lượng bán
- ✅ Phân tích top sản phẩm theo số đơn hàng
- ✅ Phân tích top sản phẩm theo doanh thu
- ✅ Báo cáo tổng hợp và so sánh
- ✅ Xuất báo cáo HTML và console

## 🛠️ Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/Hoangsyntv/git_study.git
cd git_study
```

### 2. Tạo virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

### 3. Cài đặt dependencies
```bash
pip install requests python-dotenv
```

### 4. Cấu hình API credentials

#### Tạo file .env từ template:
```bash
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux
```

#### Chỉnh sửa file .env:
```env
KIOTVIET_RETAILER=your_retailer_name
KIOTVIET_CLIENT_ID=your_client_id_here
KIOTVIET_CLIENT_SECRET=your_client_secret_here
```

⚠️ **QUAN TRỌNG**: Không bao giờ commit file `.env` lên Git!

## 🔑 Lấy API Credentials

1. Đăng nhập vào [KiotViet Developer](https://developer.kiotviet.vn)
2. Tạo ứng dụng mới
3. Copy `Client ID` và `Client Secret`
4. Thêm vào file `.env`

## 🚀 Sử dụng

### Chạy tool chính:
```bash
python API_kiotviet_NTV.py
```

### Chạy các test cụ thể:
```bash
# Test top sản phẩm theo số đơn hàng
python test_invoice_count.py

# Test top sản phẩm theo doanh thu
python test_revenue_analysis.py

# Phân tích tổng hợp
python comprehensive_analysis_2024.py
```

## 📊 Các loại báo cáo

1. **Top sản phẩm bán chạy** (theo số lượng)
2. **Top sản phẩm nhiều đơn hàng** (theo tần suất)
3. **Top sản phẩm doanh thu cao** (theo giá trị)
4. **Báo cáo tổng hợp** (so sánh đa chiều)

## 🔧 Cấu hình nâng cao

Chỉnh sửa file `.env` để tùy chỉnh:

```env
# Debugging
DEBUG=True

# Caching
CACHE_ENABLED=True

# Logging
LOG_LEVEL=INFO
```

## 🛡️ Bảo mật

- ✅ API credentials được lưu trong file `.env`
- ✅ File `.env` được ignore bởi Git
- ✅ Không hardcode sensitive data
- ✅ Template `.env.example` cho setup

## 📁 Cấu trúc project

```
├── API_kiotviet_NTV.py          # Main API client
├── config.py                    # Configuration management
├── comprehensive_analysis_2024.py # Comprehensive analysis
├── test_invoice_count.py        # Test invoice count analysis
├── test_revenue_analysis.py     # Test revenue analysis
├── .env                         # Environment variables (DO NOT COMMIT)
├── .env.example                 # Template for .env
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## 🐛 Troubleshooting

### Lỗi "Configuration Error"
```
❌ Configuration Error: Missing required environment variables
```
**Giải pháp**: Kiểm tra file `.env` có đầy đủ thông tin không.

### Lỗi "Import dotenv could not be resolved"
```bash
pip install python-dotenv
```

### Lỗi API 401 Unauthorized
- Kiểm tra `CLIENT_ID` và `CLIENT_SECRET` trong `.env`
- Đảm bảo credentials còn hiệu lực

## 📚 Tài liệu

- [KiotViet API Documentation](https://documenter.getpostman.com/view/10806036/UVRA9mU6)
- [Hướng dẫn chi tiết](huong_dan_API_va_bao_cao.md)
- [Quick Start Template](quick_start_template.md)

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

---

*Made with ❤️ for business intelligence and data analysis*
