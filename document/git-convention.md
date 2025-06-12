## Quy Tắc Commit và Đặt Tên Branch

Để duy trì một lịch sử mã nguồn rõ ràng và dễ hiểu, chúng ta sẽ tuân theo các quy tắc sau cho commit messages và đặt tên branch.

### Commit Messages

- Sử dụng định dạng **Conventional Commits**: `<type>: <subject>`
- Các loại (**types**):
  - `feat`: Tính năng mới
  - `fix`: Sửa lỗi
  - `docs`: Tài liệu
  - `style`: Định dạng mã (không thay đổi logic)
  - `refactor`: Tái cấu trúc mã
  - `test`: Thêm hoặc sửa test
  - `chore`: Công việc khác (ví dụ: cập nhật dependencies)
- **Subject**: Tóm tắt ngắn gọn, dùng thì hiện tại, không có dấu chấm cuối.
- **Body** (tùy chọn): Giải thích chi tiết hơn về thay đổi, lý do, và cách thực hiện.

**Ví dụ**:
- `feat: add user authentication`
- `fix: resolve login issue on Safari`

**Lợi ích**: Giúp dễ dàng tạo changelog và hiểu rõ lịch sử thay đổi của dự án.

### Đặt Tên Branch

- Sử dụng **tiền tố** để chỉ loại công việc:
  - `feature/`: Cho tính năng mới
  - `bugfix/`: Cho sửa lỗi
  - `hotfix/`: Cho sửa lỗi khẩn cấp
  - `docs/`: Cho cập nhật tài liệu
  - `refactor/`: Cho tái cấu trúc mã
- Theo sau là tên mô tả ngắn gọn, sử dụng dấu gạch nối (`-`) để phân tách các từ.

**Ví dụ**:
- `feature/user-authentication`
- `bugfix/login-safari-issue`

**Lợi ích**: Giúp dễ dàng nhận biết mục đích của mỗi nhánh và quản lý công việc hiệu quả.

**Lưu ý**: Đây là các hướng dẫn và có thể được điều chỉnh theo nhu cầu của nhóm.