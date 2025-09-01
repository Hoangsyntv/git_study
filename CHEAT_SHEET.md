# 🚀 KiotViet API Tool - CHEAT SHEET

## ⚡ QUICK COMMANDS

### 🎯 Chạy nhanh (Windows)
```cmd
# Chạy tool với menu
.\quick_start.bat

# Hoặc PowerShell
.\run.ps1
```

### 📊 One-liner Commands
```powershell
# Top 10 bán chạy 2024
python -c "from API_kiotviet_NTV import KiotVietAPI; api = KiotVietAPI(); api.answer_question('top 10 sản phẩm bán chạy nhất năm 2024')"

# Top 10 nhiều đơn hàng 2024  
python -c "from API_kiotviet_NTV import KiotVietAPI; api = KiotVietAPI(); api.answer_question('top 10 sản phẩm có nhiều đơn hàng nhất năm 2024')"

# Top 10 doanh thu cao 2024
python -c "from API_kiotviet_NTV import KiotVietAPI; api = KiotVietAPI(); api.answer_question('top 10 sản phẩm mang lại lợi nhuận cao nhất năm 2024')"

# Phân tích marketing
python marketing_potential_analysis.py
```

### 🔧 Setup Commands
```cmd
# Tạo virtual environment
python -m venv venv
venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Copy config template
copy .env.example .env
```

### 📝 Git Commands
```cmd
# Save all changes
git add -A
git commit -m "feat: your message here"
git push origin master

# Quick save
git add -A && git commit -m "update" && git push
```

## 🎯 ANALYSIS TYPES

| Command | Description | Use Case |
|---------|-------------|----------|
| `bán chạy` | Theo số lượng | Sản phẩm phổ biến |
| `nhiều đơn hàng` | Theo tần suất | Sản phẩm được tin tưởng |
| `doanh thu cao` | Theo giá trị | Sản phẩm sinh lời |
| `marketing potential` | Tiềm năng | Cần đẩy mạnh quảng cáo |

## 🗂️ PROJECT STRUCTURE
```
├── API_kiotviet_NTV.py          # Main tool
├── config.py                    # Configuration  
├── marketing_potential_analysis.py # Marketing analysis
├── .env                         # API credentials (SECRET)
├── quick_start.bat             # Windows quick start
├── run.ps1                     # PowerShell script
├── README.md                   # Documentation
└── requirements.txt            # Dependencies
```

## 🛡️ SECURITY NOTES
- ✅ `.env` chứa API credentials
- ❌ NEVER commit `.env` to Git
- ✅ Use `.env.example` for templates
- ✅ Check `.gitignore` includes `.env`

## 🔧 TROUBLESHOOTING

### ❌ "Configuration Error"
```cmd
# Check .env file exists and has content
type .env
```

### ❌ "Import error"  
```cmd
# Reinstall dependencies
pip install -r requirements.txt
```

### ❌ "API 401 Unauthorized"
```cmd
# Check API credentials in .env
# Ensure CLIENT_ID and CLIENT_SECRET are correct
```

## 🚀 QUICK SETUP (New Machine)
```cmd
git clone <repo-url>
cd git_study
copy .env.example .env
# Edit .env with your API credentials
.\quick_start.bat
```

---
*Save this file as bookmark for quick reference! 📚*
