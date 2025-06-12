# 🧩 Hướng Dẫn Sử Dụng Git Cho Nhóm (Dành Cho Người Mới Bắt Đầu)

Hướng dẫn này sẽ giúp bạn hiểu cách làm việc nhóm với Git một cách rõ ràng. Bạn có thể dùng **Git CLI** (gõ lệnh trên máy tính) hoặc **GitHub Desktop** (ứng dụng có nút bấm). Nội dung bao gồm cách tạo nhánh mới, giữ nhánh của bạn cập nhật, lưu tạm thay đổi bằng `stash`, làm cho lịch sử commit gọn gàng, và tránh các vấn đề khi gộp mã.

---

## 🔧 1. Làm Việc Trên Một Nhánh Mới

Khi bạn muốn làm một việc gì đó (như thêm tính năng, sửa lỗi), hãy tạo một **nhánh mới** từ nhánh `main`. Nhánh giống như một bản sao của dự án, để bạn có thể thay đổi mà không làm ảnh hưởng đến bản chính.

### 🖥 Dùng Git CLI

```bash
git checkout main
git pull origin main
git checkout -b feature/task-name
```

- `git checkout main`: Chuyển sang nhánh chính (main).
- `git pull origin main`: Lấy phiên bản mới nhất của nhánh main từ GitHub.
- `git checkout -b feature/task-name`: Tạo nhánh mới (ví dụ: `feature/login-page`) và chuyển sang đó.

### 🪟 Dùng GitHub Desktop

- Nhấn vào "Current Branch" (nhánh hiện tại) → chọn "New Branch" (tạo nhánh mới).
- Chọn nhánh cơ sở là `main`.
- Đặt tên dễ hiểu, ví dụ: `feature/login-page`.

---

## ✍️ 2. Viết Mã Và Lưu Thay Đổi (Commit)

Khi bạn làm việc, hãy **lưu thay đổi thường xuyên** bằng cách "commit". Mỗi lần commit giống như chụp ảnh lại công việc bạn vừa làm, kèm theo lời giải thích ngắn (ví dụ: "Thêm nút đăng nhập").

### 🖥 Dùng Git CLI

```bash
git add .
git commit -m "Thêm nút đăng nhập"
```

- `git add .`: Chuẩn bị tất cả thay đổi để lưu.
- `git commit -m "Thêm nút đăng nhập"`: Lưu thay đổi với lời giải thích.

### 🪟 Dùng GitHub Desktop

- Nhìn thấy các thay đổi bạn vừa làm.
- Chọn những thay đổi muốn lưu.
- Gõ lời giải thích ngắn (ví dụ: "Thêm nút đăng nhập").
- Nhấn nút "Commit to [tên nhánh của bạn]".

---

## 🧳 3. Lưu Tạm Thay Đổi Bằng Stash

**Stash là gì?**  
Stash giống như cất đồ vào balo tạm thời. Nếu bạn đang làm dở và cần chuyển sang việc khác, stash giúp bạn lưu thay đổi mà không cần commit ngay.

### 🖥 Dùng Git CLI

Nếu bạn cần chuyển nhánh mà chưa commit:

```bash
git stash save "Đang làm nút đăng nhập"
git checkout main
```

Khi quay lại làm tiếp:

```bash
git checkout feature/task-name
git stash pop
```

- `git stash save`: Cất thay đổi vào balo với ghi chú.
- `git stash pop`: Lấy thay đổi từ balo ra và xóa khỏi balo.
- Sau khi xong việc, dùng `git stash clear` để dọn sạch balo, tránh nhầm lẫn sau này.

### 🪟 Dùng GitHub Desktop

- Khi chuyển nhánh mà có thay đổi chưa lưu, GitHub Desktop sẽ hỏi bạn có muốn cất tạm không.
- Sau này, bạn có thể lấy lại từ phần "Stashed changes".

---

## 🔄 4. Cập Nhật Nhánh Của Bạn

Trước khi gửi công việc cho nhóm xem, hãy đảm bảo nhánh của bạn có mọi thay đổi mới nhất từ `main`. Điều này giúp tránh lỗi khi gộp mã.

### 🖥 Dùng Git CLI

```bash
git checkout main
git pull origin main
git checkout feature/task-name
git merge main
```

- Chuyển sang `main`, lấy phiên bản mới, rồi gộp nó vào nhánh của bạn.
- Nếu muốn gọn hơn, có thể dùng `git rebase main`, nhưng cách trên đơn giản hơn cho người mới.

### 🪟 Dùng GitHub Desktop

- Chuyển sang nhánh `main` → Nhấn "Fetch origin" để lấy phiên bản mới.
- Quay lại nhánh của bạn.
- Vào menu "Branch" → "Merge into current branch" → chọn `main`.

---

## 🧼 5. Làm Gọn Lịch Sử Commit (Tùy Chọn)

Nếu bạn muốn lịch sử commit (danh sách các lần lưu) trông gọn gàng hơn, bạn có thể gộp nhiều commit thành một. Nhưng điều này hơi khó, nên người mới có thể bỏ qua.

### 🖥 Dùng Git CLI

```bash
git rebase -i HEAD~3
```

- Gộp 3 commit gần nhất thành 1. Chỉ làm nếu bạn chưa gửi nhánh lên GitHub.

---

## 🚀 6. Gửi Nhánh Và Tạo Pull Request

Khi xong việc, bạn cần **gửi nhánh lên GitHub** và tạo **Pull Request** (yêu cầu gộp mã) để nhóm xem xét.

### 🖥 Dùng Git CLI

```bash
git push origin feature/task-name
```

- Sau đó, vào GitHub, nhấn "Create Pull Request".

### 🪟 Dùng GitHub Desktop

- Nhấn "Push origin" để gửi nhánh lên.
- Nhấn "Create Pull Request" (trình duyệt sẽ mở).

---

## ✅ 7. Kiểm Tra Trước Khi Gộp Mã

Trước khi gộp nhánh của bạn vào `main`, hãy kiểm tra:

- Nhánh của bạn đã có mọi thay đổi mới nhất từ `main`.
- Không có lỗi hay xung đột.
- Nếu có bài kiểm tra (test), tất cả phải chạy tốt.
- Có người trong nhóm xem lại mã của bạn.
- Không còn thay đổi nào trong "balo" stash.
- Lời giải thích commit dễ hiểu.

---

## 🔀 8. Gộp Mã Và Dọn Dẹp

Sau khi Pull Request được duyệt và gộp:

- Bạn có thể giữ nhánh của mình trên máy tính để xem lại sau.
- Có thể xóa nhánh trên GitHub để gọn gàng:

```bash
git push origin --delete feature/task-name
```

- Cập nhật nhánh `main` trên máy:

```bash
git checkout main
git pull origin main
```

- Dọn sạch stash (nếu có):

```bash
git stash clear
```

---

## 📌 Tóm Tắt Quy Trình

1. Bắt đầu từ nhánh `main`.
2. Tạo nhánh mới cho việc bạn làm.
3. Lưu thay đổi thường xuyên bằng commit.
4. Nếu cần làm việc khác, cất tạm thay đổi bằng stash.
5. Cập nhật nhánh của bạn với `main`.
6. Sửa lỗi nếu có.
7. Gửi nhánh lên GitHub.
8. Tạo Pull Request để nhóm xem.
9. Sau khi gộp, dọn stash và có thể xóa nhánh trên GitHub.

Cách làm này giúp:

- Lịch sử dự án dễ nhìn.
- Ít lỗi hơn.
- Làm việc nhóm mượt mà hơn.

---
