# Báo cáo tổng quan dự án Ebook2LateX

## 1. Mục tiêu dự án

Dự án Ebook2LateX là một web application hỗ trợ xử lý PDF sách/tài liệu toán học. Hệ thống cho phép tải lên PDF, trích xuất các dòng có dạng công thức LaTeX, chỉnh sửa công thức bằng trình soạn thảo MathLive, rồi gửi dữ liệu đã sửa vào cơ sở dữ liệu PostgreSQL.

## 2. Kiến trúc tổng thể

Dự án được chia thành 3 phần chính:

- Backend: FastAPI, SQLAlchemy, Alembic
- Frontend: React + Vite + MathLive
- Database: PostgreSQL

Toàn bộ hệ thống được chạy bằng Docker Compose. Khi khởi động, container backend chờ database sẵn sàng, chạy migration rồi mới mở API.

## 3. Cấu trúc thư mục chính

- backend/: mã nguồn API, model, schema, service và migration
- frontend/: giao diện người dùng bằng React
- docker-compose.yml: cấu hình chạy các service bằng Docker
- scripts/: các script hỗ trợ seed dữ liệu và truy vấn
- migrations/: cấu hình Alembic và lịch sử migration
- uploads/: nơi lưu file tải lên và dữ liệu tạm cho backend

## 4. Chức năng chính của hệ thống

### Upload PDF

Người dùng tải lên một file PDF. Backend nhận file, lưu tạm và phân tích nội dung để tìm các dòng có khả năng là công thức.

### Trích xuất công thức

Service xử lý PDF sẽ đọc nội dung từ tài liệu và chuyển các đoạn phù hợp thành dữ liệu công thức theo định dạng LaTeX.

### Chỉnh sửa công thức

Frontend hiển thị danh sách công thức đã trích xuất. Người dùng chọn từng công thức và sửa trực tiếp trong MathLive editor.

### Gửi kết quả vào database

Sau khi chỉnh sửa, người dùng có thể submit toàn bộ công thức đã thay đổi. Backend cập nhật dữ liệu vào PostgreSQL và đánh dấu trạng thái xử lý của tài liệu.

## 5. Backend

Backend dùng FastAPI để xây dựng API. Các thành phần chính gồm:

- app/main.py: tạo ứng dụng FastAPI và đăng ký router
- app/api/routes/documents.py: API liên quan đến upload PDF, liệt kê công thức, submit dữ liệu
- app/api/routes/formulas.py: API cập nhật công thức riêng lẻ
- app/services/pdf_formula_service.py: xử lý PDF và trích xuất công thức
- app/models/entities.py: khai báo entity ORM
- app/schemas/formula.py: schema dữ liệu cho request/response
- app/database.py: cấu hình kết nối database

Migrations được quản lý bằng Alembic trong thư mục migrations/.

## 6. Frontend

Frontend được xây dựng bằng React và Vite. Các phần đáng chú ý:

- App.jsx: điều phối luồng upload, chọn công thức, chỉnh sửa và submit
- components/PDFUploader.jsx: chọn và tải PDF lên backend
- components/FormulaList.jsx: hiển thị danh sách công thức đã trích xuất
- components/MathLiveEditor.jsx: biên tập LaTeX bằng MathLive
- services/api.js: lớp gọi API tới backend

Giao diện hiện tại tập trung vào quy trình làm việc của người dùng: upload file, xem công thức, sửa, rồi submit.

## 7. Docker và cách chạy

Project được đóng gói bằng Docker Compose với 3 service:

- db: PostgreSQL 16
- backend: FastAPI API
- frontend: Vite dev server

Sau khi chỉnh cấu hình, lệnh khởi động đầy đủ là:

```bash
docker compose up --build
```

Lệnh này sẽ dựng toàn bộ stack, bao gồm cả frontend.

## 8. Luồng xử lý dữ liệu

1. Người dùng upload PDF từ frontend.
2. Backend lưu file và phân tích PDF.
3. Hệ thống trích xuất các đoạn giống công thức thành LaTeX.
4. Frontend hiển thị danh sách công thức để người dùng chỉnh sửa.
5. Người dùng submit kết quả.
6. Backend ghi dữ liệu đã sửa vào PostgreSQL.

## 9. Công nghệ sử dụng

- Python 3.12+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- React 18
- Vite
- MathLive
- Docker và Docker Compose

## 10. Điểm cần nhớ khi vấn đáp

- Đây là hệ thống xử lý PDF toán học theo hướng bán tự động, không phải OCR tổng quát.
- Backend chịu trách nhiệm xử lý file, trích xuất công thức và lưu database.
- Frontend tập trung vào trải nghiệm chỉnh sửa LaTeX nhanh bằng MathLive.
- Docker Compose là cách triển khai chính để chạy đồng bộ database, backend và frontend.
- Alembic dùng để quản lý schema database theo version.

## 11. Kết luận

Dự án Ebook2LateX là một ứng dụng web full-stack phục vụ việc chuyển đổi và hiệu chỉnh công thức từ PDF sang LaTeX, giúp người dùng kiểm tra lại công thức trước khi lưu vào cơ sở dữ liệu. Kiến trúc rõ ràng, tách backend - frontend - database, và có thể triển khai đầy đủ bằng Docker.