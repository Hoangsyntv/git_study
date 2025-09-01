# KiotViet API Tool - PowerShell Quick Start
# Sử dụng: .\run.ps1

Write-Host "🚀 KiotViet API Quick Start" -ForegroundColor Green
Write-Host ""

# Check .env file
if (-not (Test-Path ".env")) {
    Write-Host "❌ File .env không tồn tại!" -ForegroundColor Red
    Write-Host "💡 Tạo file .env từ template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Đã tạo file .env" -ForegroundColor Green
    Write-Host "📝 Hãy chỉnh sửa file .env với thông tin API của bạn" -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
    return
}

# Setup environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "📦 Tạo virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment created and activated" -ForegroundColor Green
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt | Out-Null
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Menu
Write-Host ""
Write-Host "🎯 MENU LỰA CHỌN:" -ForegroundColor Cyan
Write-Host "1. Tool chính (interactive)" -ForegroundColor White
Write-Host "2. Top 10 sản phẩm bán chạy 2024" -ForegroundColor White
Write-Host "3. Top 10 sản phẩm nhiều đơn hàng 2024" -ForegroundColor White
Write-Host "4. Top 10 sản phẩm doanh thu cao 2024" -ForegroundColor White
Write-Host "5. Phân tích sản phẩm tiềm năng marketing" -ForegroundColor White
Write-Host "6. Thoát" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Nhập lựa chọn (1-6)"

switch ($choice) {
    "1" { python API_kiotviet_NTV.py }
    "2" { python -c "from API_kiotviet_NTV import KiotVietAPI; api = KiotVietAPI(); api.answer_question('top 10 sản phẩm bán chạy nhất năm 2024')" }
    "3" { python -c "from API_kiotviet_NTV import KiotVietAPI; api = KiotVietAPI(); api.answer_question('top 10 sản phẩm có nhiều đơn hàng nhất năm 2024')" }
    "4" { python -c "from API_kiotviet_NTV import KiotVietAPI; api = KiotVietAPI(); api.answer_question('top 10 sản phẩm mang lại lợi nhuận cao nhất năm 2024')" }
    "5" { python marketing_potential_analysis.py }
    "6" { Write-Host "👋 Tạm biệt!" -ForegroundColor Green }
    default { Write-Host "❌ Lựa chọn không hợp lệ!" -ForegroundColor Red }
}

Read-Host "Press Enter to exit"
