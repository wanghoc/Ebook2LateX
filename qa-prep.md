# Chuẩn bị trả lời (Q&A) — Dự án Ebook2LateX

Tập hợp các câu hỏi thường gặp và câu trả lời ngắn gọn để ôn vấn đáp.

---

## 1. Mục tiêu dự án là gì?
- Mục tiêu: xây dựng web app bán tự động chuyển công thức trong PDF sang LaTeX, cho phép người dùng kiểm tra và chỉnh sửa trước khi lưu.

## 2. Kiến trúc tổng quan?
- 3 thành phần: Frontend (React + Vite + MathLive), Backend (FastAPI + SQLAlchemy + Alembic), Database (PostgreSQL).
- Chạy đồng bộ bằng `docker compose up --build`.

## 3. Luồng xử lý dữ liệu (ngắn gọn)?
1. Người dùng upload PDF.
2. Backend phân tích PDF (text layer hoặc OCR) để tìm candidate công thức.
3. Trả về danh sách candidate cho frontend.
4. Người dùng chỉnh sửa từng công thức trong MathLive.
5. Save từng công thức hoặc `Submit all` để lưu vào DB.

## 4. Những endpoint quan trọng?
- `POST /api/v1/documents/upload` — upload PDF, trả về `document_id` và `formulas`.
- `GET /api/v1/documents/{document_id}/formulas` — lấy danh sách công thức đã lưu cho document.
- `PUT /api/v1/formulas/{id}` — cập nhật 1 formula.
- `DELETE /api/v1/formulas/{id}` — xóa 1 formula.
- `POST /api/v1/documents/{id}/submit` — submit toàn bộ công thức cho document.

## 5. Làm sao hệ thống trích xuất công thức?
- Dùng PyMuPDF (fitz) để đọc text layer và chia thành dòng/khối.
- Áp heuristic: dò dấu hiệu toán học (ký hiệu, dấu ngoặc, backslash `\`, toán tử) để chấm điểm candidate.
- Nếu text layer quá nhiễu, fallback sang OCR (pytesseract + Pillow) để đọc ảnh trang.
- Kết quả kèm `confidence_score` (giá trị trong response) để frontend lọc/ẩn low-confidence.

## 6. Tại sao kết quả có ký tự lạ?
- Vì PDF có text layer không sạch (encoding, ligatures), hoặc là ảnh quét; cần hậu xử lý/chuẩn hóa và đôi khi cần chỉnh tay trong MathLive.

## 7. Cách deploy nhanh trên máy dev?
```bash
cd D:\Ebook2LateX
docker compose up -d --build
```
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/v1

## 8. Cách xem công thức đã lưu?
- Dùng UI: mở `View saved formulas` trong app (sau khi upload sẽ có `document_id`).
- Dùng API: `GET /api/v1/documents/{document_id}/formulas`.
- Dùng SQL: truy vấn bảng `formulas` trong PostgreSQL.

## 9. Cấu trúc DB (tóm tắt)?
- `documents` (id, file_name, created_at, status...)
- `formulas` (id, document_id, latex_content, order_index, confidence_score, created_at, updated_at)

## 10. Migration và schema?
- Dùng Alembic; migration files ở `migrations/versions/`.
- Khi thay model, tạo migration: `alembic revision --autogenerate -m "msg"` rồi `alembic upgrade head`.

## 11. Làm sao kiểm thử chức năng trích xuất?
- Upload một PDF mẫu qua frontend, kiểm tra danh sách candidate, edit rồi Save/Submit.
- Kiểm tra logs backend để thấy pipeline xử lý, hoặc gọi trực tiếp API upload bằng `curl`.

## 12. Các hạn chế & cải tiến tương lai?
- Hạn chế: phương pháp heuristic không hoàn hảo với PDF phức tạp; OCR đơn giản (Tesseract) kém với công thức phức tạp.
- Cải tiến: tích hợp mô hình Im2LaTeX / neural OCR chuyên cho công thức, thêm crowd-sourcing để build training set, refine regex/normalization.

## 13. Bảo mật & dữ liệu?
- Hiện tại không có auth (local dev). Nếu deploy public cần thêm xác thực, rate limiting, và cơ chế xóa an toàn.
- File upload lưu tạm trong `uploads/` — nên làm cleanup định kỳ.

## 14. Câu hỏi kỹ thuật sâu (gợi ý trả lời ngắn)
- "Làm sao chấm điểm candidate?": tính score dựa trên tần suất ký hiệu toán, tồn tại slash/backslash, độ dài hợp lý, và trừ penalty nếu nhiều từ prose.
- "Khi nào dùng OCR?": khi text-layer trả về quá ít chữ/không có ký hiệu toán hoặc khi text chứa nhiều ký tự lạ; hệ thống phát hiện trang noisy và gọi pytesseract.
- "Làm sao sync frontend-backend khi thay response?": cập nhật `app/schemas` (Pydantic) và client API (`frontend/src/services/api.js`), rebuild frontend.

## 15. Demo ngắn (kịch bản 3 bước)
1. Start stack: `docker compose up -d --build`.
2. Mở http://localhost:5173, upload `sample.pdf`.
3. Chọn một candidate, sửa trong editor, nhấn `Save` rồi `Submit all`.

---

Nếu bạn muốn, tôi có thể:
- Tùy chỉnh file này thành slide (PDF) để thuyết trình.
- Thêm mục "câu hỏi hóc búa" và câu trả lời mẫu để luyện trả lời.
- Dịch sang tiếng Anh.

