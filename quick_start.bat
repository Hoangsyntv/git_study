@echo off
REM Quick Start Script for KiotViet API Tool

echo 🚀 KiotViet API Quick Start
echo.

REM Check if .env exists
if not exist .env (
    echo ❌ File .env không tồn tại!
    echo 💡 Copy .env.example thành .env và điền thông tin API
    echo.
    copy .env.example .env
    echo ✅ Đã tạo file .env từ template
    echo 📝 Hãy chỉnh sửa file .env với thông tin API của bạn
    pause
    exit
)

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate
    echo ✅ Đã kích hoạt virtual environment
) else (
    echo 💡 Tạo virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    echo ✅ Đã tạo và kích hoạt virtual environment
)

REM Install dependencies
echo 📦 Cài đặt dependencies...
pip install -r requirements.txt

echo.
echo 🎯 MENU LỰA CHỌN:
echo 1. Chạy tool chính (interactive)
echo 2. Top 10 sản phẩm bán chạy 2024
echo 3. Top 10 sản phẩm nhiều đơn hàng 2024  
echo 4. Top 10 sản phẩm doanh thu cao 2024
echo 5. Phân tích sản phẩm tiềm năng marketing
echo 6. Thoát
echo.

set /p choice="Nhập lựa chọn (1-6): "

if %choice%==1 (
    python API_kiotviet_NTV.py
) else if %choice%==2 (
    python -c "from API_kiotviet_NTV import KiotVietAPI; api = KiotVietAPI(); api.answer_question('top 10 sản phẩm bán chạy nhất năm 2024')"
) else if %choice%==3 (
    python -c "from API_kiotviet_NTV import KiotVietAPI; api = KiotVietAPI(); api.answer_question('top 10 sản phẩm có nhiều đơn hàng nhất năm 2024')"
) else if %choice%==4 (
    python -c "from API_kiotviet_NTV import KiotVietAPI; api = KiotVietAPI(); api.answer_question('top 10 sản phẩm mang lại lợi nhuận cao nhất năm 2024')"
) else if %choice%==5 (
    python marketing_potential_analysis.py
) else if %choice%==6 (
    echo 👋 Tạm biệt!
) else (
    echo ❌ Lựa chọn không hợp lệ!
)

pause
