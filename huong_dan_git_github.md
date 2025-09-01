# Hướng dẫn sử dụng Git & GitHub đơn giản

## 1. Cho cá nhân

### Khởi tạo và lưu trữ dự án
```bash
# Khởi tạo repo local
$ git init
# Kết nối với repo trên GitHub
$ git remote add origin https://github.com/<username>/<repo>.git
```

### Quy trình làm việc
1. **Sửa file**
2. <span style="color:red;font-weight:bold">Lưu file (Ctrl+S) — Việc này rất quan trọng! Luôn lưu file sau khi hoàn thành chỉnh sửa trước khi chạy git add, git commit.</span>
> **Lưu ý:**
> - Nên đóng các file không cần thiết trước khi lưu và commit để tránh tạo lại file rác cho dự án.
> - Trước khi lưu và commit, hãy kiểm tra kỹ các thay đổi Undo/Keep, chỉ giữ lại nội dung thực sự cần thiết. Nếu không chắc, hãy Undo để loại bỏ thay đổi không mong muốn.
3. **Thêm thay đổi vào Git**
   ```bash
   git add <ten_file>   # Thêm file chỉ định
   git add .            # Thêm tất cả các file thay đổi
   ```
4. **Tạo commit**
   ```bash
   git commit -m "<loại>: <mô tả ngắn>"   # Tuân thủ Conventional Commits
   # Ví dụ:
   # Conventional Commits: <loại>: <mô tả ngắn>
   # Loại: feat, fix, chore, docs, style, refactor, perf, test
   # Ví dụ:
   # git commit -m "feat: thêm chức năng đăng nhập"
   # git commit -m "fix: sửa lỗi hiển thị trên mobile"
   ```
5. **Đẩy lên GitHub**
   ```bash
   git push origin master
   ```

### Làm việc với branch
```bash
# Tạo branch mới
$ git checkout -b feature-xyz
# Làm việc, commit trên branch
$ git add .
$ git commit -m "Thay đổi trên branch"
$ git push origin feature-xyz
# Gộp branch vào master
$ git checkout master
$ git merge feature-xyz
$ git push origin master
```

---

## 2. Cho team dev 3-5 người

### Quy trình làm việc nhóm
1. **Mỗi dev clone repo về máy**
   ```bash
   git clone https://github.com/<org>/<repo>.git
   ```
2. **Tạo branch cho từng tính năng/bug**
   ```bash
   git checkout -b feature-abc
   ```
3. **Commit và push lên branch cá nhân**
   ```bash
   git add .
   git commit -m "Thay đổi cho feature abc"
   git push origin feature-abc
   ```
4. **Tạo Pull Request (PR) trên GitHub**
   - Đề xuất merge branch vào master/main
   - Thành viên khác review, comment, yêu cầu sửa
   - Leader/Reviewer duyệt và merge PR

### Lưu ý khi làm việc nhóm
- Luôn cập nhật branch master/main mới nhất trước khi làm việc:
  ```bash
  git checkout master
  git pull origin master
  git checkout feature-abc
  git merge master
  ```
- Giải quyết xung đột nếu có, rồi push lại.
- Chỉ leader hoặc người có quyền mới được merge vào master/main.

---

## Một số lệnh hữu ích
```bash
# Xem trạng thái
$ git status
# Xem lịch sử commit
$ git log --oneline --graph --all
# Khôi phục file về trạng thái cũ
$ git checkout <hash> <ten_file>
# Khôi phục toàn bộ repo về commit cũ
$ git reset --hard <hash>
# Quay lại commit cũ nhưng vẫn giữ lịch sử (tạo commit mới revert)
$ git revert <hash>
# Ví dụ:
# git log --oneline   # Xem danh sách commit và lấy hash
# git revert a1b2c3d4 # Quay lại commit có hash a1b2c3d4
# Kiểm tra thay đổi nội dung so với commit trước
$ git diff           # So sánh thay đổi so với commit gần nhất
$ git diff <hash1> <hash2> # So sánh giữa 2 commit bất kỳ
```

---

**Áp dụng đúng quy trình sẽ giúp quản lý code hiệu quả, bảo vệ bản quyền và làm việc nhóm chuyên nghiệp!**
