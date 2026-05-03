1. Yêu cầu hệ thống
1.1 Sơ đồ hệ thống


1.2 Mô tả yêu cầu
[FR1] Hệ thống đọc tài liệu Ebook toán học dạng PDF, chỉ đọc các công thức toán học, đưa lên Giao diện

[FR2] Trên Giao diện: chuyển công thức toán từ ebook sang dạng LateX và dạng biểu thức toán học tương ứng, cho phép người dùng sửa nội dung trên giao diện. Khi sửa nội dung bên LateX thì bên Mathlive Symbol sẽ cập nhật theo, và ngược lại, sửa bên Mathlive Symbol thì bên LateX cũng cập nhật 

[FR3] Khi người dùng bấm nút Submit, nội dung LateX sẽ được lưu xuống Database

1.3 Lựa chọn công nghệ
- Loại ứng dụng: Web app

- Back-end: Python (FastAPI)

- Front-end: React

- Database: PostgreSQL

1.4 Bài tập và câu hỏi

Bài tập

Trả lời các câu hỏi sau, ghi lại vào trong sổ tay môn học.

Câu 1a. Tài liệu dạng PDF là gì? Tại sao được sử dụng nhiều?

Câu 1b. Tài liệu dạng LateX là gì? Dùng để làm gì?

Câu 1c. Mathlive symbol là gì? Dùng để làm gì? Tại sao lại phải chuyển đổi qua lại giữa PDF - LateX; LateX - Mathlive symbol?

Câu 1d. Ứng dụng trên làm bằng Desktop app hay Web app thì tốt hơn? Giải thích tại sao?

Câu 1e. Phân tích ưu và nhược điểm khi lựa chọn giải pháp CSR (client-side rendering) và SSR (server-side rendering)

Câu hỏi ôn tập

Câu 1.1 Bạn có thể sử dụng các hệ quản trị cơ sở dữ liệu sau để lưu trữ dữ liệu? Đáp án nào không đúng?

A. React

B. PostgreSQL

C. MongoDB

D. SQLite

Câu 1.2 Bạn có thể sử dụng các công nghệ sau đây để xây dựng phần Backend của hệ thống, đáp án nào không đúng?

A. Node.js (Express)

B. PHP (Laravel)

C. Python (FastAPI)

D. JavaScript (ReactJS)

Câu 1.3 Giả sử bạn đang xây dựng ứng dụng OCR toán học cho các giáo viên ở vùng sâu vùng xa, nơi kết nối Internet rất chập chờn nhưng họ cần xử lý hàng trăm trang tài liệu mỗi ngày. Lựa chọn nào sau đây là tối ưu nhất về mặt kỹ thuật?

A. Xây dựng ứng dụng chạy trên nền tảng Cloud (SaaS)

B. Xây dựng Web App với giải pháp Server-Side Rendering (SSR)

C. Xây dựng Web App sử dụng Client-Side Rendering (CSR)

D. Xây dựng Desktop App chạy offline hoàn toàn trên máy tính

Câu 1.4 Nếu ưu tiên quan trọng nhất của dự án là tối ưu hóa SEO để các công thức toán học lưu trong Database có thể được tìm thấy dễ dàng trên Google, bạn nên áp dụng chiến lược nào cho phần Front-end?

A. Sử dụng React với Client-Side Rendering (CSR) thuần túy

B. Chỉ sử dụng Desktop App và không cần làm bản Web

C. Sử dụng Server-Side Rendering (SSR) để trả về nội dung HTML hoàn chỉnh

D. Lưu tất cả công thức dưới dạng hình ảnh thay vì LaTeX

Ebook2LateX (2) - Phân tích hệ thống
Bài trước: Ebook2LateX (1) - Hiểu yêu cầu và chọn công nghệ
-----

2. Phân tích hệ thống
2.1 Cấu trúc thư mục dự án
Ebook2LateX/

├── .git/                   # Thư mục ẩn của Git

├── .gitignore              # Khai báo các tập không đưa vào Git

├── docker-compose.yml       # File điều phối toàn bộ hệ thống Docker

├── backend/                # Python (FastAPI)

│   ├── Dockerfile          # Cách đóng gói Backend

│   ├── app/

│   │   ├── main.py         # Điểm khởi đầu của API

│   │   ├── api/            # Các endpoint (upload, process, save)

│   │   ├── core/           # Cấu hình hệ thống, OCR model loading

│   │   ├── models/         # Định nghĩa bảng database (SQLAlchemy)

│   │   ├── services/       # Logic xử lý PDF & OCR (Parse tool)

│   │   └── schemas/        # Pydantic models (Validation dữ liệu)

│   ├── uploads/            # Lưu tạm file PDF người dùng gửi lên

│   ├── requirements.txt

│   └── .env                # Biến môi trường (DB_URL, API_KEY)

├── frontend/               # React (Vite)

│   ├── Dockerfile          # Cách đóng gói Frontend

│   ├── src/

│   │   ├── components/     # MathLiveEditor, PDFUploader, Preview

│   │   ├── hooks/          # Custom hooks xử lý logic LaTeX

│   │   ├── services/       # Kết nối API tới Backend

│   │   └── App.jsx

│   ├── package.json

│   └── public/

2.2 Các thành phần logic chính
A. Backend: Bộ máy Parse tool

Đây là phần quan trọng nhất để giải quyết yêu cầu [FR1]

- Xử lý PDF: Dùng thư viện PyMuPDF (fitz) để trích xuất hình ảnh từ PDF

- OCR Toán học: Để chuyển hình ảnh công thức sang LaTeX, sử dụng mô hình pix2tex (LaTeX-OCR)

- API: Khi nhận tập tin PDF, Backend sẽ cắt các vùng chứa công thức, chạy qua model OCR và trả về chuỗi LaTeX cho Frontend

B. Frontend: Trình soạn thảo hai chiều (React + MathLive)

Để giải quyết yêu cầu [FR2] (sửa bên này cập nhật bên kia):

- MathLive: Sử dụng thư viện mathlive (JavaScript). Thư viện này cung cấp một <math-field> có thể lắng nghe sự kiện thay đổi

- Logic đồng bộ: Tạo một State trong React (ví dụ: latexContent)

    + Khi người dùng gõ vào ô Textarea (LaTeX): Cập nhật State -> MathField render lại

    + Khi người dùng sửa trên MathField: Lấy giá trị .value (dạng latex) -> Cập nhật State -> Textarea cập nhật theo

C. Database: Lưu trữ (PostgreSQL)

Giải quyết yêu cầu [FR3]:

- Bảng dữ liệu cơ bản: Documents, FormulaEntries, Users, Logs

2.3 Công nghệ chi tiết
- Backend Framework: FastAPI. Framework này chạy nhanh, hỗ trợ xử lý bất đồng bộ tốt khi gọi các model AI nặng

- OCR Library: pix2tex hoặc sử dụng API của Mathpix (nếu muốn độ chính xác tuyệt đối mà không cần tự train model)

- Frontend UI: Tailwind CSS (để dàn trang giao diện chỉnh sửa nhanh chóng)

- Frontend Framework: React.js — Dùng để quản lý trạng thái (State) của công thức toán học và điều khiển luồng dữ liệu giữa các thành phần

- Math Library: MathLive — Thư viện chuyên biệt nhúng vào React để hiển thị và chỉnh sửa ký hiệu toán học trực quan

- ORM: SQLAlchemy (để làm việc với PostgreSQL một cách chuyên nghiệp)

2.4 Bài tập và câu hỏi
Bài tập

Bài 2a. Dựa vào nội dung phân tích hệ thống của dự án, hoàn thành bảng sau:

Chức năng hệ thống

Công cụ thực hiện

Quản lý phiên bản mã nguồn


Đóng gói môi trường phát triển


Framework phía front-end


Framework phía back-end


Trích xuất hình ảnh từ PDF


Chuyển từ hình ảnh sang LateX


ORM


Hệ quản trị cơ sở dữ liệu




Câu hỏi



Câu 2.1 Trong dự án Ebook2LateX, thư viện nào được sử dụng ở Backend để thực hiện nhiệm vụ trích xuất hình ảnh từ tập tin PDF?



A. MathLive



B. PyMuPDF (fitz)



C. Tailwind CSS



D. Pydantic



Câu 2.2 Tại sao hệ thống Ebook2LateX lại sử dụng React State (ví dụ: latexContent) để quản lý dữ liệu trong trình soạn thảo hai chiều?



A. Để lưu trữ vĩnh viễn công thức vào cơ sở dữ liệu PostgreSQL ngay khi người dùng vừa gõ phím



B. Để đóng gói ứng dụng vào Docker container giúp triển khai lên server dễ dàng hơn



C. Giúp đồng bộ tức thời dữ liệu giữa ô nhập liệu LaTeX và hiển thị của MathLive



D. Để thay thế hoàn toàn thư viện MathLive trong việc nhận diện các ký hiệu toán học phức tạp



Câu 2.3 Một nhóm phát triển muốn triển khai dự án Ebook2LateX sao cho môi trường chạy ứng dụng của tất cả các thành viên (từ máy của lập trình viên đến máy chủ) đều giống hệt nhau, tránh lỗi "chạy được trên máy tôi nhưng không chạy được trên máy bạn". Dựa vào cấu trúc dự án, họ nên sử dụng các tập tin nào để thực hiện việc này?



A. .gitignore và .git



B. requirements.txt và package.json



C. main.py và App.jsx



D. Dockerfile và docker-compose.yml

-----
Bài sau: Ebook2LateX (3) - Các giai đoạn thực hiện

Ebook2LateX (3) - Các giai đoạn thực hiện
Bài trước: Ebook2LateX (2) - Phân tích hệ thống
-----
3. Các giai đoạn thực hiện

3.1 Thiết lập nền tảng và Cơ sở dữ liệu

Giai đoạn này chuẩn bị môi trường để thực hiện yêu cầu [FR3]

Khởi tạo dự án

- Tạo thư mục dự án Ebook2LateX

- Khởi tạo Git

- Tạo file: .gitignore

- Tạo repo trên Github

Cài đặt cơ sở dữ liệu

- Cài đặt PostgreSQL

- Tạo database

- Cấu hình chuỗi kết nối trong tập tin .env

- Tạo các bảng dữ liệu

- Nhập dữ liệu mẫu

Cấu hình Backend

- Cài đặt FastAPI và SQLAlchemy. Kết nối thành công từ Python đến PostgreSQL để sẵn sàng ghi dữ liệu

Cấu hình Frontend



Docker hóa môi trường phát triển

- Tạo Dockerfile cho Backend: Định nghĩa môi trường chạy Python, cài đặt các thư viện OCR và FastAPI

- Tạo Dockerfile cho Frontend: Định nghĩa môi trường chạy Node.js để build ứng dụng React

- Tạo docker-compose.yml: Đây là "nhạc trưởng" điều phối 3 dịch vụ: db: Chạy hình ảnh của PostgreSQL; backend: Chạy mã FastAPI; frontend: Chạy mã React


3.2 Xây dựng "Parse tool" (Xử lý PDF & OCR)
Giai đoạn này tập trung vào việc giải quyết yêu cầu [FR1]

[GD2.1] Trích xuất hình ảnh từ PDF: Sử dụng thư viện PyMuPDF để đọc tập tin PDF và cắt ra các vùng chứa công thức toán học

[GD2.2] Tích hợp Model OCR: Cài đặt mô hình pix2tex (LaTeX-OCR) vào thư mục services/

[GD2.3] Tạo API xử lý: Viết endpoint trong FastAPI để nhận tập tin PDF từ người dùng, chạy qua quy trình OCR và trả về chuỗi ký tự LaTeX

3.3 Phát triển Giao diện và Logic đồng bộ

Giai đoạn này hiện thực hóa yêu cầu [FR2] về tính tương tác

[GD3.1] Khởi tạo Frontend: Sử dụng React (Vite) và Tailwind CSS để dựng giao diện cơ bản gồm khu vực tải tập tin và khu vực biên tập

[GD3.2] Tích hợp MathLive: Nhúng thành phần <math-field> vào ứng dụng để hiển thị công thức trực quan

[GD3.3] Lập trình đồng bộ hai chiều:

    + Tạo State latexContent trong React

    + Viết logic để khi sửa ô văn bản (LaTeX raw), công thức trong MathLive tự động cập nhật

    + Ngược lại, khi sửa bằng biểu tượng trong MathLive, nội dung text LaTeX cũng thay đổi tương ứng

3.4 Hoàn thiện quy trình dữ liệu (Submit)

Kết nối các thành phần lại để hoàn tất yêu cầu [FR3]

[GD4.1] Kết nối Front-End và Back-End: Sử dụng thư viện axios để gửi nội dung LaTeX cuối cùng từ giao diện về API của FastAPI

[GD4.2] Xử lý lưu trữ: Backend nhận dữ liệu và sử dụng SQLAlchemy để lưu bản ghi vào PostgreSQL

3.5 Kiểm thử và Triển khai

[GD5.1] Kiểm thử (Testing): Thử nghiệm với các tập tin PDF toán học có độ phức tạp khác nhau để tinh chỉnh model OCR

[GD5.1] Đóng gói dự án: Viết tập tin docker-compose.yml để có thể chạy toàn bộ hệ thống (Web, API, DB) chỉ bằng một câu lệnh

3.6 Bài tập và câu hỏi

Bài tập 1. Các công cụ sau đây được dùng để làm gì?

- Git

- Github

- .gitignore

- PostgreSQL

- SQLAlchemy

- FastAPI

- React

- Docker

Câu hỏi 3.1 Trong lập trình, công cụ Git được sử dụng để làm gì? 

A. Để thiết kế giao diện người dùng cho trang web

B. Để quản lý các phiên bản mã nguồn và theo dõi lịch sử thay đổi của dự án

C. Để chạy các ứng dụng Python trên môi trường đám mây

D. Để lưu trữ dữ liệu người dùng dưới dạng bảng

Câu 2: Docker là công cụ được dùng với mục đích gì? 

A. Dùng để viết mã nguồn Python nhanh hơn

B. Dùng để tạo ra các "container" giúp đóng gói ứng dụng và môi trường chạy một cách nhất quán

C. Dùng để quản lý các câu hỏi trắc nghiệm trong cơ sở dữ liệu

D. Dùng để kết nối máy tính với mạng Internet toàn cầu

Câu 3: PostgreSQL thuộc loại công cụ nào dưới đây? 

A. Một thư viện dùng để tạo giao diện

B. Một khung làm việc (Framework) để xây dựng API

C. Một hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) dùng để lưu trữ dữ liệu

D. Một công cụ dùng để đẩy mã nguồn lên mạng cho người khác xem

-----

Bài sau: Ebook2LateX (4) - Khởi tạo dự án

Ebook2LateX (4) - Khởi tạo dự án
Bài trước: Ebook2LateX (3) - Các giai đoạn thực hiện
-----
4. Khởi tạo dự án
Giai đoạn này chuẩn bị môi trường để thực hiện yêu cầu [FR3]

4.1 Tạo thư mục và cấu hình Git, Github

Bước 1. Tạo thư mục dự án

- Trong ổ đĩa D, tạo thư mục Ebook2LateX

Bước 2. Khởi tạo Git

- Tải và cài đặt phần mềm Git vào máy tính

- Sau khi cài đặt xong, mở cửa sổ dòng lệnh (CMD), gõ lệnh: git -v, nếu có thông tin về phiên bản là Git đã sẵn sàng để làm việc. Ví dụ:

C:\Users\VIET HOANG - VTS>git -v

git version 2.52.0.windows.1

- Nhúng Git vào trong thư mục dự án: Trong cửa sổ CMD, di chuyển dấu nhắc lệnh vào trong thư mục Ebook2LateX. Chạy lệnh git init

D:\DuAn\Ebook2LateX>git init

Initialized empty Git repository in D:/DuAn/Ebook2LateX/.git/

- Tạo tập tin: .gitignore

Tập tin .gitignore dùng để loại trừ các tập tin và thư mục mà bạn không muốn lưu vào kho chứa .git, nhằm tăng tốc độ lưu trạng thái và giảm dung lượng của kho chứa. Các tập tin và thư mục không cần thiết sẽ không cần phải lưu trạng thái. Ngoài ra, các tập tin lưu thông tin quan trọng (ví dụ tập tin .env chứa mật khẩu Database) cũng không nên lưu vào kho chứa, vì bạn có thể vô tình đẩy lên Github và mọi người sẽ thấy được thông tin này.

Bạn nên tham khảo trên mạng về cách tạo nội dung cho tập tin .gitignore, hoặc sử dụng một số tập tin .gitignore tạo sẵn, phù hợp với dự án của bạn.

Ví dụ, cách tạo tập tin .gitignore:

    + Truy cập trang web gitignore.io

    + Nhập các từ khóa công nghệ bạn đang dùng cho dự án: Python, Node, React, Windows VisualStudioCode

    + Bấm Create. Trang web sẽ tạo ra một danh sách đầy đủ các tập tin/thư mục cần loại bỏ. Bạn chỉ cần chép và dán vào tập tin .gitignore. Bạn cần tạo tập tin .gitignore (không có phần mở rộng) trong thư mục gốc của dự án (Book2LateX) (nếu bạn chưa tạo).

Bước 3. Thực hiện commit lần đầu cho dự án

Để thực hiện “commit lần đầu” cho dự án Ebook2LateX, bạn cần thực hiện theo các bước sau đây, tại cửa sổ dòng lệnh (CMD).

Việc này giúp ghi lại trạng thái đầu tiên của dự án và thực hành với Git.

- Đảm bảo dấu nhắc lệnh của bạn đang nằm ở thư mục gốc của dự án:

D:\DuAn\Ebook2LateX>

- Kiểm tra trạng thái hiện tại. Trước khi lưu, bạn nên xem Git đang nhận diện những gì:

git status

Lúc này, bạn sẽ thấy tập tin .gitignore hiện lên với màu đỏ (Untracked files - chưa được theo dõi)

- Đưa tập tin vào "Vùng chờ" (Staging Area). Sử dụng lệnh sau để nói với Git rằng bạn muốn lưu tất tất cả các tập tin hiện có:

git add .

(Dấu chấm tượng trưng cho tất cả các tập tin trong thư mục hiện tại)

- Thực hiện lệnh Commit (Ghi lại lịch sử). Đây là bước quan trọng nhất để tạo một "điểm khôi phục" đầu tiên cho dự án:

git commit -m "Initial commit: Khoi tao cau truc thu muc backend va frontend cho Ebook2LateX"

-m: Viết tắt của "message" (thông điệp)

Nội dung trong ngoặc kép: Là mô tả ngắn gọn về những gì bạn đã làm. Điều này giúp các thành viên khác hoặc chính bạn sau này biết được bản commit này chứa thay đổi gì

- Kiểm tra kết quả. Sau khi commit xong, bạn gõ lệnh:

git log

Màn hình sẽ hiển thị thông tin về bản commit bạn vừa tạo, bao gồm: Mã định danh (Hash), Tác giả (Author), Ngày giờ và nội dung thông điệp bạn vừa viết.

Bước 4. Tạo repo trên Github

Mục đích: để bạn chia sẻ mã nguồn cho các thành viên khác.

    + Bạn cần tạo tài khoản trên Github

    + Khi đăng nhập vào tài khoản, Github yêu cầu bạn chứng thực 2FA (Two-Factor Authentication), đây là kiểu chứng thực giúp bạn bảo vệ tài khoản Github, tránh việc bị mất tài khoản. Bạn có thể sử dụng công cụ Authy.

    + Ý tưởng của chứng thực 2FA: khi bạn đăng nhập vào Github > Github sẽ kích hoạt ứng dụng Authy > ứng dụng Authy sẽ sinh ra 6 số > bạn nhập 6 số này vào Github. Ý tưởng giống khi bạn nhập mã OTP khi chuyển khoản ngân hàng.

Các bước để tạo repo trên Github:

    + Đảm bảo bạn đã đăng nhập vào tài khoản Github

    + Tại trang chủ hoặc trang cá nhân, nhấn vào biểu tượng dấu + ở góc trên cùng bên phải và chọn New repository

    + Điền các thông tin sau:

Repository name: Nhập tên dự án (ví dụ: Ebook2LateX)

Public/Private: Trong mục Configuration > Choose visibility > chọn Public nếu bạn muốn chia sẻ công khai, hoặc Private nếu chỉ muốn các thành viên được mời mới thấy được mã nguồn

Initialize this repository with: Vì bạn đã khởi tạo Git ở máy cục bộ (local) rồi, nên không tích vào các mục Add a README file, Add .gitignore hay Choose a license để tránh xung đột khi đẩy mã nguồn lên lần đầu

- Nhấn nút Create repository

Bước 5. Kết nối máy tính với GitHub (Dùng dòng lệnh CMD)

Sau khi tạo xong, GitHub sẽ hiện ra một trang hướng dẫn. Bạn đọc để có thêm thông tin.

Bạn mở cửa sổ CMD, di chuyển dấu nhắc lệnh vào thư mục dự án (ví dụ: thư mục D:\DuAn\Ebook2LateX) và chạy các lệnh sau:

- Thêm địa chỉ Remote (kết nối thư mục trên máy tính với Github):

git remote add origin https://github.com/ten-tai-khoan-cua-ban/Ebook2LateX.git

(Thay link trên bằng link thực tế mà Github cung cấp cho bạn)

Bước 6. Đặt tên nhánh chính

git branch -M main

(Github hiện nay ưu tiên tên nhánh chính là main thay vì master).

Bước 7. Đẩy kho chứa cục bộ lên Github (Push)

git push -u origin main

Trong đó,

- git push: Là lệnh yêu cầu Git đẩy các bản ghi (commits) từ kho chứa cục bộ lên một kho chứa ở xa

- origin: Đây là tên hiệu (alias) đại diện cho địa chỉ URL của kho chứa trên Github. Thay vì phải gõ một đường dẫn dài như https://github.com/user/Ebook2LateX.git, bạn chỉ cần gọi tên origin. (Tên này thường được thiết lập ở bước git remote add origin...)

- main: Đây là tên của nhánh (branch) mà bạn muốn đẩy lên. Hiện nay, main là tên nhánh chính mặc định trên Github

- u (viết tắt của --set-upstream): Đây là phần quan trọng nhất cho lần đẩy đầu tiên. Nó thiết lập một mối liên kết theo dõi giữa nhánh main ở máy bạn và nhánh main trên Github

Bước 8: Kiểm tra kết quả

Sau khi chạy lệnh git push thành công, bạn quay lại trình duyệt và tải lại (F5) trang Repository trên Github. Cấu trúc thư mục dự án của bạn sẽ xuất hiện trên đó.

Bây giờ bạn có thể gửi đường liên kết URL của Repo này cho các thành viên khác để họ có thể git clone hoặc phối hợp làm việc chung. (Ví dụ: https://github.com/legiacong/Ebook2LateX.git)

4.2 Bài tập và câu hỏi

Bài tập

Bài tập 4a. Thực hiện cài đặt các nội dung trong bài học.

Câu hỏi

Câu 4.1 Trong quy trình khởi tạo dự án, tập tin nào được sử dụng để không đưa các thư mục không cần thiết hoặc các thông tin bảo mật vào kho chứa Git?

A. .gitconfig

B. git.ignore

C. .gitignore

D. .gitgnore

Câu 4.2 Trong quá trình khởi tạo dự án tại máy cục bộ, lệnh nào được sử dụng để bắt đầu nhúng Git vào thư mục dự án?

A. git status

B. git init

C. git commit

D. git push

4.3 Sau khi đã tạo thành công Repository trên Github, bạn cần thực hiện chuỗi lệnh nào dưới đây tại cửa sổ dòng lệnh (CMD) để kết nối và đẩy bản commit đầu tiên từ thư mục dự án lên nhánh chính của Github?

A.

git remote add origin <URL>

git branch -M main

git push -u origin main

B.

git init

git add .

git commit -m "Initial commit"

C.

git clone <URL>

git status

git log

D.

git remote add origin <URL>

git branch -M master

git pull origin master

-----
Bài sau: Ebook2LateX (5) - Cài đặt hệ quản trị cơ sở dữ liệu

Ebook2LateX (5) - Cài đặt hệ quản trị cơ sở dữ liệu
Bài trước: Ebook2LateX (4) - Khởi tạo dự án
-----
5. Cài đặt hệ quản trị cơ sở dữ liệu
Phần này sẽ cài đặt hệ quản trị cơ sở dữ liệu để lưu trữ thông tin cho dự án.


5.1 PostgreSQL
Bước 1. Cài đặt PostgreSQL

- Tải phần mềm: Truy cập trang chủ PostgreSQL (https://www.postgresql.org/) và tải bản cài đặt phù hợp với hệ điều hành bạn đang sử dụng (Windows/Linux/macOS)

- Thực hiện cài đặt như một chương trình bình thường

- Cấu hình ban đầu: Thiết lập mật khẩu cho tài khoản quản trị mặc định (tài khoản: postgres; mật khẩu: p@ssword1)

- Ghi nhớ cổng kết nối mặc định (thường là 5432)

- Sau khi cài đặt PostgreSQL thành công, sử dụng công cụ pgAdmin4 (được cài đặt tự động với quá trình cài đặt PostgreSQL) để đăng nhập vào hệ thống

Bước 2. Tạo Database cho dự án

(sử dụng pgAdmin4)

- Mở pgAdmin4 và đăng nhập với mật khẩu đã tạo ở bước cài đặt (postgres - p@ssword1)

- Chuột phải vào mục Databases -> chọn Create -> Database…

- Tại ô Database, nhập tên: ebook2latex_db

- Nhấn Save

Bước 3: Cấu hình chuỗi kết nối trong tập tin .env

Để ứng dụng Backend (FastAPI) có thể giao tiếp với cơ sở dữ liệu mà vẫn đảm bảo tính bảo mật, chúng ta lưu thông tin cấu hình trong tập tin môi trường.

- Trong thư mục gốc của dự án (Ebook2LateX), tạo thư mục backend

- Truy cập vào thư mục backend/

- Tạo một tập tin mới tên là .env (nếu chưa có)

- Thêm nội dung cấu hình chuỗi kết nối theo định dạng của SQLAlchemy như sau:

[.env]

# Định dạng: postgresql://[user]:[password]@[host]:[port]/[database_name]

DATABASE_URL=postgresql://postgres:mat_khau_cua_ban@localhost:5432/ebook2latex_db

Giải thích các thành phần của đoạn mã trên:

- postgres: Tên người dùng mặc định

- mat_khau_cua_ban: Thay bằng mật khẩu bạn đã thiết lập ở bước cài đặt

- localhost: Chạy trên máy cục bộ (hoặc db nếu bạn chạy trong Docker)

- 5432: Cổng mặc định của PostgreSQL

- ebook2latex_db: Tên cơ sở dữ liệu vừa tạo

Việc tách và lưu thông tin cấu hình ra tập tin .env giúp bạn dễ dàng thay đổi môi trường (từ máy cá nhân sang Docker hoặc Cloud) mà không cần sửa mã nguồn ứng dụng.

5.2 Bài tập và câu hỏi

Bài tập

Bài tập 5a. Thực hiện cài đặt các nội dung trong bài học.

Câu hỏi

Câu 5.1 Tại sao thông tin kết nối cơ sở dữ liệu nên được lưu trữ trong tập tin .env thay vì viết trực tiếp vào mã nguồn của ứng dụng Backend?

A. Để giúp cơ sở dữ liệu PostgreSQL chạy nhanh hơn

B. Để đảm bảo tính bảo mật và giúp dễ dàng thay đổi cấu hình khi chuyển đổi môi trường (như từ máy cá nhân lên Cloud) mà không cần sửa mã nguồn

C. Vì tập tin .env là nơi duy nhất mà công cụ pgAdmin4 có thể đọc được tên cơ sở dữ liệu

D. Để hệ điều hành Windows/Linux tự động cài đặt PostgreSQL khi ứng dụng khởi chạy

Câu 5.2 Trong chuỗi kết nối postgresql://postgres:p@ssword1@localhost:5432/ebook2latex_db, thành phần "5432" đóng vai trò gì?

A. Là mã định danh (ID) của tài khoản người dùng quản trị

B. Là mật khẩu truy cập vào hệ quản trị cơ sở dữ liệu

C. Là cổng kết nối (port) mặc định để ứng dụng giao tiếp với PostgreSQL

D. Là phiên bản của hệ quản trị cơ sở dữ liệu PostgreSQL đang sử dụng

Câu 5.3 Giả sử bạn đã cài đặt PostgreSQL với mật khẩu là 123456 và tạo một database tên là project_math. Bạn cần cấu hình tập tin .env trong thư mục backend như thế nào để ứng dụng kết nối đúng (giả sử các thông số khác để mặc định)?

A. DATABASE_URL=postgresql://admin:123456@localhost:5432/project_math

B. DATABASE_URL=postgresql://postgres:123456@localhost:5432/project_math

C. DATABASE_URL=postgresql://123456:postgres@localhost:5432/project_math

D. DATABASE_URL=postgresql://postgres:123456@localhost:8000/project_math

-----

Bài sau: Ebook2LateX (6) - Phân tích và thiết kế các bảng

Ebook2LateX (6) - Phân tích và thiết kế các bảng
Bài trước: Ebook2LateX (5) - Cài đặt hệ quản trị cơ sở dữ liệu
-----
6. Phân tích và thiết kế các bảng
Để giải quyết yêu cầu [FR3], chúng ta cần tạo hai bảng dữ liệu chính với mối quan hệ một-nhiều (một tài liệu có nhiều mục công thức).

Ngoài ra, chúng ta cũng tạo thêm 2 bảng để quản lý việc đăng nhập; theo dõi hiệu suất và lỗi khi thực hiện OCR của mô hình AI.

6.1 Danh sách các bảng

[1] Bảng lưu trữ tài liệu (ví dụ: Documents)

Bảng này dùng để quản lý các tập tin PDF mà người dùng tải lên hệ thống. Các trường thông tin cần thiết bao gồm:

- ID: Khóa chính (Primary Key), định danh duy nhất cho mỗi tài liệu

- FileName: Tên tập tin gốc khi tải lên

- FilePath/URL: Đường dẫn lưu trữ tập tin trên máy chủ hoặc Cloud để có thể mở lại khi cần

- UploadDate: Thời gian tài liệu được tải lên hệ thống

- Status: Trạng thái xử lý của tài liệu (ví dụ: Đang chờ, Đã xử lý, Lỗi)

[2] Bảng lưu trữ công thức (ví dụ: FormulaEntries)

Đây là bảng quan trọng nhất để thực hiện yêu cầu [FR3] (Lưu dữ liệu dạng LateX vào Database). Theo thiết kế dự án, mỗi tài liệu sẽ có nhiều mục công thức, bao gồm:

- ID: Khóa chính của mục công thức

- DocumentID: Khóa ngoại (Foreign Key) liên kết với bảng Documents (quan hệ 1-nhiều)

- RawImage/ImagePath: Lưu ảnh vùng công thức đã được cắt ra từ tập tin PDF (hoặc đường dẫn tới ảnh đó) để đối chiếu

- LatexContent: Nội dung mã LaTeX đã được mô hình pix2tex trích xuất hoặc người dùng đã chỉnh sửa thủ công

- OrderIndex: Thứ tự của công thức trong tài liệu để hiển thị lại đúng cấu trúc ban đầu

- CreatedAt/UpdatedAt: Thời gian tạo và lần cuối cùng chỉnh sửa công thức

[3] Bảng thông tin người dùng (ví dụ: Users)

Bảng này dùng để quản lý định danh, quyền truy cập

- UserID: Khóa chính (Primary Key), mã định danh duy nhất cho mỗi người dùng

- Username/Email: Tên đăng nhập hoặc địa chỉ email dùng để xác thực và liên lạc

- PasswordHash: Lưu trữ mật khẩu đã được mã hóa (không lưu mật khẩu thô, bảo mật theo chuẩn OAuth2/JWT)

- FullName: Họ và tên đầy đủ của người dùng để hiển thị trên giao diện

- Role: Vai trò của người dùng (ví dụ: Admin, Editor, Viewer) để phân quyền

- LastLogin: Thời gian cuối cùng người dùng đăng nhập vào hệ thống

- IsActive: Trạng thái tài khoản (Đang hoạt động hoặc Đã khóa)

[4] Bảng theo dõi hiệu suất và lỗi khi thực hiện OCR của mô hình AI (ví dụ: Logs)

Bảng này dùng để giám sát chất lượng của mô hình AI (pix2tex/Mathpix), giúp lập trình viên phát hiện lỗi kỹ thuật và cải thiện độ chính xác của việc trích xuất công thức.

- LogID: Khóa chính, định danh duy nhất cho mỗi bản ghi nhật ký

- FormulaID: Khóa ngoại liên kết với bảng FormulaEntries, giúp biết lỗi hoặc hiệu suất này thuộc về công thức cụ thể nào

- ProcessingTime: Thời gian (tính bằng mili giây hoặc giây) mà mô hình AI cần để chuyển đổi từ ảnh sang LaTeX. Chỉ số này giúp đánh giá tốc độ hệ thống

- ConfidenceScore: Độ tin cậy của kết quả OCR do mô hình trả về (thường từ 0 đến 1). Nếu điểm quá thấp, hệ thống có thể đánh dấu để người dùng kiểm tra kỹ hơn

- ErrorType: Loại lỗi phát sinh nếu quá trình OCR thất bại (ví dụ: Timeout, InvalidImageFormat, ModelCrash)

- ErrorMessage: Nội dung chi tiết thông báo lỗi kỹ thuật để phục vụ việc sửa lỗi (debugging)

- Timestamp: Thời điểm chính xác sự kiện xảy ra

- EnvironmentInfo: Thông tin về môi trường chạy (ví dụ: Docker_Container_ID, CPU/GPU_Usage) để phân tích tải hệ thống

6.2 Bài tập và câu hỏi

Bài tập

Bài tập 6a. Đọc hiểu nội dung phân tích và thiết kế các bảng.


-----
Bài sau: Ebook2LateX (7) - Tạo các bảng


Ebook2LateX (7) - Tạo các bảng
Bài trước: Ebook2LateX (6) - Phân tích và thiết kế các bảng
-----

7. Tạo các bảng
7.1 Giải pháp
Tới phần này, bạn đã có tài liệu thiết kế của các bảng, các ràng buộc, mối quan hệ giữa các bảng. Công việc tiếp theo là tạo các bảng, tạo các ràng buộc, tạo các quan hệ giữa các bảng trên Hệ quản trị cơ sở dữ liệu (PostgreSQL).

Để thao tác với PostgreSQL, chúng ta có một số cách:

- Sử dụng giao diện dòng lệnh (CMD)

- Sử dụng giao diện đồ họa (pgAdmin4)

- Sử dụng ngôn ngữ lập trình

Một vài câu hỏi đặt ra là:

- Làm sao để việc tạo bảng, nhập dữ liệu mẫu được nhanh nhất

- Những người cùng nhóm có thể tải dự án và phát triển tiếp một cách tiện lợi

Vậy, giải pháp để tạo cơ sở dữ liệu nên được tiến hành như thế nào?

Bạn có thể trao đổi thêm với AI để có giải pháp phù hợp.

Trong phần này, chúng ta sẽ làm việc với Hệ quản trị cơ sở dữ liệu bằng ngôn ngữ Python và Công cụ di chuyển cơ sở dữ liệu (database migration).

Sau đây là các bước thực hiện:

[1] Sử dụng công cụ Database Migration (Alembic)

Thay vì tạo bảng thủ công bằng CMD hay pgAdmin4, bạn nên sử dụng Alembic kết hợp với SQLAlchemy trong môi trường Python.

Cách làm này có vài điểm lợi:

- Mọi thay đổi về cấu trúc bảng (thêm cột, đổi kiểu dữ liệu, tạo ràng buộc) được ghi lại thành các tập tin mã nguồn (scripts). Khi người khác tải dự án về, họ chỉ cần chạy một câu lệnh để đồng bộ hóa cấu trúc database mà không cần thực hiện thủ công

- Giúp theo dõi lịch sử thay đổi của cơ sở dữ liệu tương tự như cách Git quản lý mã nguồn

[2] Định nghĩa Schema bằng Object-Relational Mapping (ORM)

Chúng ta sẽ định nghĩa các bảng (Users, Documents, FormulaEntries, Logs) dưới dạng các Class trong Python sử dụng SQLAlchemy.

Việc sử dụng Snake Case (user_id, file_name) trong định nghĩa bảng giúp ánh xạ tự động và tự nhiên sang các đối tượng Python, giúp viết mã xử lý dữ liệu nhanh hơn.

Các ràng buộc phức tạp như CASCADE (tự động xóa dữ liệu liên quan) và các Trigger (tự động cập nhật thời gian updated_at) được thiết lập ngay trong mã nguồn, đảm bảo tính toàn vẹn dữ liệu một cách có hệ thống.

7.2 Cài đặt
Để triển khai giải pháp quản lý cơ sở dữ liệu chuyên nghiệp bằng Python, SQLAlchemy và Alembic, bạn hãy thực hiện theo các bước chi tiết dưới đây. Cách tiếp cận này giúp bạn đồng bộ hóa database giữa các thành viên trong nhóm một cách tự động.

Bước 1: Thiết lập môi trường và Cài đặt thư viện

Trước tiên, bạn cần cài đặt các thư viện cần thiết để Python có thể giao tiếp với PostgreSQL và quản lý việc di chuyển cơ sở dữ liệu (migration).

Tạo môi trường ảo:

Để thực hiện các cài đặt, phải đảm bảo trên máy của bạn đã cài trình dịch lệnh Python. Trong cửa sổ dòng lệnh, nhập lệnh sau để xem trên máy có Python hay chưa (nhớ viết hoa chữ V):

python -V

# Python 3.14.0

Trong cửa sổ dòng lệnh (CMD), di chuyển dấu nhắc lệnh vào thư mục dự án, nhập lệnh sau:

python -m venv venv

Ý nghĩa của lệnh:

- python -m venv: Gọi module tạo môi trường ảo

- venv (cái tên cuối cùng): Là tên thư mục sẽ chứa môi trường ảo. Bạn có thể đặt tên khác, nhưng venv là tên phổ biến nhất

Sau khi chạy lệnh trên, bạn vào thư mục dự án, thấy xuất hiện thư mục venv là đã tạo được môi trường ảo.

Môi trường ảo là một thư mục, chứa phiên bản Python riêng biệt và các thư viện riêng dành cho một dự án cụ thể.

Môi trường ảo giúp:

- Giữ thư viện của dự án không làm ảnh hưởng (xung đột) đến dự án khác hoặc hệ thống máy tính

- Đảm bảo dự án luôn chạy đúng các phiên bản thư viện đã cài đặt

- Giúp người khác tải dự án của bạn về và cài đặt mọi thứ đồng bộ một cách dễ dàng thông qua tập tin danh sách thư viện (requirements.txt).

Bạn chạy tiếp lệnh sau để kích hoạt môi trường ảo

venv\Scripts\activate     # Windows

Khi bạn chạy lệnh này, các thay đổi sau sẽ xảy ra:

- Máy tính sẽ tạm thời "quên" phiên bản Python chung của hệ thống. Thay vào đó, nó sẽ ưu tiên sử dụng trình thông dịch Python và các thư viện nằm bên trong thư mục venv của dự án

- Bạn sẽ thấy tên môi trường (ví dụ: (venv)) xuất hiện ở đầu dòng lệnh trong Terminal/CMD. Điều này báo hiệu rằng bạn đang đứng "bên trong" chiếc hộp cách ly của dự án. Ví dụ:

D:\DuAn\Ebook2LateX>venv\scripts\activate

(venv) D:\DuAn\Ebook2LateX>

- Từ thời điểm này, bất kỳ thư viện nào bạn cài đặt bằng lệnh pip install sẽ chỉ được lưu vào thư mục venv đó, không ảnh hưởng đến các dự án khác hay cài đặt gốc của máy tính

Cài đặt các thư viện:

pip install sqlalchemy alembic psycopg2-binary python-dotenv

Mục đích của các thư viện:

- SQLAlchemy giúp bạn làm việc với cơ sở dữ liệu bằng ngôn ngữ Python

- Alembic theo dõi và quản lý những thay đổi của các bảng dữ liệu theo thời gian

- psycopg2-binary chuyển lệnh xuống cho PostgreSQL thực hiện

- python-dotenv lấy mật khẩu để mở cổng kết nối

Sau khi quá trình cài đặt thành công, bạn vào thư mục của dự án, vào “...\venv\Lib\site-packages” để kiểm tra, các gói vừa được cài đặt sẽ có tại đây (ví dụ: D:\DuAn\Ebook2LateX\venv\Lib\site-packages)

Sau khi kiểm tra các gói đã xuất hiện trong site-packages, bước cuối cùng là trích xuất danh sách này ra tập tin cấu hình bằng lệnh: 

(lưu ý: dấu nhắc lệnh phải nằm ở thư mục \backend)

pip freeze > requirements.txt

Tại sao bước này là bắt buộc?

- Để Docker làm việc: Tập tin này chính là "thực đơn" mà Docker sẽ đọc để tự động cài đặt môi trường bên trong Container. Thiếu nó, Docker sẽ không thể vận hành Backend

- Đảm bảo tính nhất quán: Nó lưu lại chính xác phiên bản của các thư viện bạn đang dùng. Điều này giúp dự án của bạn không bị lỗi khi các thư viện này cập nhật phiên bản mới trong tương lai

- Thay thế cho venv: Thay vì phải gửi cả thư mục venv nặng nề cho người khác, bạn chỉ cần gửi tập tin requirements.txt nhỏ gọn này.

Bạn mở tập tin requirement.txt để đảm bảo đã có tên của các gói bạn vừa cài đặt.

Bước 2: Cấu hình Alembic (Khởi tạo Migration)

Alembic sẽ giúp bạn quản lý các phiên bản của database (giống như Git quản lý mã nguồn).

Khởi tạo Alembic trong thư mục backend/:

- Vào cửa sổ dòng lệnh, di chuyển dấu nhắc lệnh vào thư mục backend, gõ lệnh sau:

alembic init migrations

- Lệnh này tạo ra thư mục migrations/ và tập tin alembic.ini. (trong thư mục backend)

- Cấu hình kết nối: Mở tệp migrations/env.py, tìm và chỉnh sửa dòng target_metadata để Alembic biết các Model của bạn nằm ở đâu:

[Mã python]

from models import Base  # Import Base từ file models.py của bạn

target_metadata = Base.metadata  # Thiết lập metadata để Alembic theo dõi

Giải thích dòng mã trên:

Dòng mã trên đóng vai trò là "trạm kết nối" giữa các định nghĩa bảng trong mã Python và công cụ quản lý cơ sở dữ liệu Alembic. Đây là bước quan trọng nhất để Alembic có thể hiểu được cấu trúc Database của bạn.

from models import Base

- Dòng này thực hiện nạp đối tượng Base từ tập tin định nghĩa dữ liệu của bạn (thường là models.py)

- Tại sao cần Base? Trong SQLAlchemy, tất cả các Class (như User, Document, FormulaEntry, Log) đều phải kế thừa từ một lớp cha chung gọi là Base (thường được tạo bằng hàm declarative_base()). Khi các Class này kế thừa Base, chúng sẽ tự động đăng ký cấu trúc của mình (tên bảng, các cột, kiểu dữ liệu) vào một "sổ cái" chung nằm bên trong Base.

target_metadata = Base.metadata

- Base.metadata là bản thiết kế (Schema) tổng thể của toàn bộ cơ sở dữ liệu. Nó chứa danh sách tất cả các bảng, các ràng buộc (constraints), và mối quan hệ mà bạn đã khai báo trong mã nguồn Python

- target_metadata là một biến đặc biệt mà Alembic sẽ tham chiếu tới

Luồng hoạt động của 2 dòng mã trên:

Khi bạn chạy lệnh tạo phiên bản database mới (ví dụ: alembic revision --autogenerate), Alembic sẽ thực hiện các bước sau:

- Tham chiếu tới biến target_metadata: Xem trong mã Python bạn đang khai báo những bảng nào, cột nào (Dựa trên thông tin từ Base.metadata)

- Nhìn vào Database thực tế: Kết nối xuống PostgreSQL để xem cấu trúc bảng hiện tại ở đó

- So sánh (Diff): Nếu trong mã nguồn có bảng mới mà dưới Database chưa có, Alembic sẽ tự động viết một tập tin script để tạo bảng đó

Nếu không có hai dòng mã này, Alembic sẽ bị "mù". Nó sẽ không biết bạn đã định nghĩa những gì trong Python và không thể tự động tạo ra các tập tin cập nhật cấu trúc cơ sở dữ liệu cho bạn và đồng nghiệp.

Bước 3: Định nghĩa Schema bằng SQLAlchemy (ORM)

Thay vì viết SQL, bạn định nghĩa các bảng bằng cách tạo các Class trong Python.

Trong thư mục backend của dự án, tạo tập tin models.py và nhập vào đoạn mã sau:

[models.py]

import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Text, Numeric

from sqlalchemy.dialects.postgresql import UUID, JSONB

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func


# Khởi tạo lớp Base để các Model kế thừa

Base = declarative_base()


class User(Base):

    __tablename__ = 'users'

    

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username_email = Column(String(255), unique=True, nullable=False)

    password_hash = Column(Text, nullable=False)

    full_name = Column(String(100))

    role = Column(String(20), default='Editor') # Admin, Editor, Viewer

    last_login = Column(DateTime(timezone=True))

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


    # Quan hệ: Một người dùng có thể tải lên nhiều tài liệu

    documents = relationship("Document", back_populates="owner")


class Document(Base):

    __tablename__ = 'documents'

    

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='SET NULL'))

    file_name = Column(Text, nullable=False)

    file_path_url = Column(Text, nullable=False)

    upload_date = Column(DateTime(timezone=True), server_default=func.now())

    status = Column(String(50), default='Pending') # Pending, Processed, Error


    # Quan hệ ngược lại với User

    owner = relationship("User", back_populates="documents")

    # Quan hệ: Một tài liệu có nhiều mục công thức

    formulas = relationship("FormulaEntry", back_populates="document", cascade="all, delete-orphan")


class FormulaEntry(Base):

    __tablename__ = 'formula_entries'

    

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id', ondelete='CASCADE'), nullable=False)

    raw_image_path = Column(Text)

    latex_content = Column(Text)

    order_index = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    # Quan hệ ngược lại với Document

    document = relationship("Document", back_populates="formulas")

    # Quan hệ: Một công thức có thể có nhiều log (nếu chạy OCR nhiều lần)

    logs = relationship("Log", back_populates="formula", cascade="all, delete-orphan")


class Log(Base):

    __tablename__ = 'logs'

    

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    formula_id = Column(UUID(as_uuid=True), ForeignKey('formula_entries.id', ondelete='CASCADE'))

    processing_time_ms = Column(Integer)

    confidence_score = Column(Numeric(3, 2))

    error_type = Column(String(100))

    error_message = Column(Text)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    environment_info = Column(JSONB) # Lưu trữ thông số CPU/GPU dưới dạng JSON


    # Quan hệ ngược lại với FormulaEntry

    formula = relationship("FormulaEntry", back_populates="logs")

Các điểm lưu ý trong mã nguồn trên:

- UUID: Sử dụng uuid.uuid4 để tự động tạo ID duy nhất cho mỗi bản ghi ngay từ phía Python nếu PostgreSQL chưa hỗ trợ

- Mối quan hệ (Relationship):

    + relationship() giúp bạn truy xuất dữ liệu dễ dàng. Ví dụ: từ một đối tượng document, bạn có thể gọi document.formulas để lấy danh sách tất cả công thức của nó

    + cascade="all, delete-orphan": Khi bạn xóa một tài liệu, tất cả các công thức và log liên quan sẽ tự động bị xóa theo, giúp database sạch sẽ

- Tự động cập nhật thời gian: server_default=func.now(): Tự lấy thời gian hiện tại khi tạo mới bản ghi

- onupdate=func.now(): Tự cập nhật lại thời gian vào cột updated_at mỗi khi bạn sửa nội dung công thức

- JSONB: Cột environment_info trong bảng Log sử dụng kiểu dữ liệu JSONB của PostgreSQL, cho phép bạn lưu trữ các bộ tham số không cố định một cách linh hoạt

Bước 4: Thực hiện Migration (Tạo bảng tự động)

Sau khi đã có tập tin định nghĩa cơ sở dữ liệu models.py, chúng ta sẽ sử dụng Alembic để chuyển đổi các Class Python này thành các bảng thực tế trong cơ sở dữ liệu PostgreSQL mà không cần viết lệnh CREATE TABLE, hoặc dùng giao diện pgAdmin 4 thủ công.

Ở phần trên, chúng ta đã tạo ra môi trường Alembic: đã tạo ra thư mục Migrations, tạo tập tin alembic.ini.

Chúng ta sẽ cấu hình để kết nối tới Database: 

- Mở tập tin alembic.ini và tìm dòng sqlalchemy.url. Hãy cập nhật thông tin kết nối PostgreSQL của bạn theo định dạng (nhớ lưu lại tập tin sau khi cập nhật thông tin):

sqlalchemy.url = postgresql://user:password@localhost:5432/ebook2latex_db

# ví dụ: sqlalchemy.url = postgresql://postgres:p@ssword1@localhost:5432/ebook2latex_db

Ở phần trên, bạn cũng đã thực hiện liên kết Alembic với Model của bạn.

Để chắc chắn, bạn có thể kiểm tra lại, bằng cách vào tập tin migrations/env.py:

Đảm bảo đã có 2 dòng cấu hình sau:

from models import Base  # Import Base từ file models.py của bạn

target_metadata = Base.metadata  # Thiết lập metadata để Alembic theo dõi

(Lưu ý: Đảm bảo đường dẫn import models chính xác với cấu trúc thư mục của bạn).

Tạo bản thảo Migration (Autogenerate):

- Bây giờ, hãy để Alembic tự động so sánh sự khác biệt giữa các Class trong Python và Database hiện tại:

Gõ lệnh sau vào cửa sổ dòng lệnh. Lưu ý: dấu nhắc lệnh phải đang nằm ở thư mục của dự án mà có chứa tập tin alembic.ini (ví dụ: D:\DuAn\Ebook2LateX\backend)

alembic revision --autogenerate -m "Tao cac bang ban dau cho Ebook2LateX"

Lưu ý: (có thể) chạy lệnh trên bạn sẽ gặp thông báo lỗi vì ký tự “@” trong chuỗi kết nối của tập tin alembic.ini gây ra hiểu lầm về đường dẫn. Bạn hãy vào tập tin alembic.ini, tìm tới dòng kết nối và sửa lại: thay chữ “@” bằng “%%40”.

Ví dụ: 

sqlalchemy.url = postgresql://postgres:p%%40ssword1@localhost:5432/ebook2latex_db

Alembic sẽ tạo ra một tập tin mới trong thư mục migrations/versions/. Tập tin này chứa mã Python mô tả việc tạo các bảng users, documents, formula_entries, và logs.

Thực thi tạo bảng (Upgrade)

Cuối cùng, chạy lệnh sau để áp dụng các thay đổi vào PostgreSQL:

Trong cửa sổ dòng lệnh, gõ lệnh sau (dấu nhắc lệnh đang ở (venv) D:\DuAn\Ebook2LateX\backend>):

alembic upgrade head

Kiểm tra kết quả

Sau khi chạy xong, bạn có thể vào công cụ quản lý database (như pgAdmin hoặc DBeaver) để kiểm tra:

- Các bảng đã được tạo đầy đủ với đúng kiểu dữ liệu (UUID, JSONB, TIMESTAMP...)

- Các khóa ngoại (Foreign Keys) đã được thiết lập đúng mối quan hệ

- Cột updated_at sẽ có Trigger tự động cập nhật thời gian mỗi khi dữ liệu thay đổi

Tại sao chúng ta làm cách này?

- An toàn dữ liệu: Sau này nếu bạn thêm cột accuracy_score vào bảng logs, bạn chỉ cần sửa models.py, chạy lại lệnh ở bước Tạo bản thảo Migration và Thực thi tạo bảng. Alembic sẽ chỉ thêm cột mới mà không xóa dữ liệu cũ của bạn

- Đồng bộ nhóm: Khi làm việc nhóm, bạn chỉ cần gửi tập tin migration này cho thành viên khác, họ chỉ cần chạy lệnh upgrade là database sẽ giống hệt của bạn


Vậy là chúng ta đã tạo được bảng dữ liệu bằng ORM có tên là SQLAlchemy và công cụ di chuyển dữ liệu (database migration) Alembic. Chúng ta sẽ thực hiện commit vào Git để lưu lại trạng thái của hệ thống, phòng khi làm các bước tiếp theo có bị lỗi thì có mốc để khôi phục lại dự án.

- Trong chương trình cửa sổ dòng lệnh (CMD), dấu nhắc đang ở thư mục dự án (Ebook2LateX), nhập lệnh sau

- Kiểm tra để biết được các tập tin mới nào đã được tạo/sửa trong dự án và sẽ được commit

git status

- Chuyển các tập tin sang Vùng tạm (staging area):

git add .

- Commit 

git commit -m "feat: tao cac bang du lieu"


7.3 Bài tập và Câu hỏi
Bài tập

Bài tập 7a. Thực hiện các cài đặt, cấu hình trong phần lý thuyết.

Bài tập 7b. Gạch đầu dòng một số bước, một số lệnh quan trọng, khi bạn làm việc với các công cụ: ORM Alchemy, Database migration Alembic.

Câu hỏi

Câu 7.1 Môi trường ảo (venv) trong dự án Python được hiểu là gì? 

A. Là một trang web dùng để lưu trữ mã nguồn trực tuyến

B. Là một thư mục chứa phiên bản Python và các thư viện riêng biệt, giúp dự án không bị xung đột với các thư viện khác trong hệ thống

C. Là một phần mềm dùng để vẽ sơ đồ thiết kế cơ sở dữ liệu

D. Là một câu lệnh dùng để xóa toàn bộ các bảng trong PostgreSQL

Câu 7.2 Trong quy trình làm việc với Alembic, lệnh nào được dùng để thực thi các thay đổi từ tập tin bản thảo (script) vào cơ sở dữ liệu thực tế? 

A. alembic init migrations 

B. alembic revision --autogenerate 

C. alembic upgrade head 

D. pip freeze > requirements.txt

Câu 7.3 Tại sao chúng ta nên định nghĩa các bảng dưới dạng các Class trong Python bằng SQLAlchemy thay vì viết lệnh SQL trực tiếp? 

A. Vì SQLAlchemy sẽ giúp việc truy xuất dữ liệu dễ dàng hơn thông qua các đối tượng Python và hỗ trợ quản lý các mối quan hệ phức tạp

B. Vì sử dụng SQLAlchemy sẽ giúp ứng dụng chạy nhanh gấp 10 lần so với SQL thông thường

C. Vì SQLAlchemy là công cụ duy nhất có thể kết nối được với PostgreSQL

D. Vì viết mã Python ngắn hơn và không cần phải quan tâm đến kiểu dữ liệu của các cột

Câu 7.4 Lợi ích quan trọng nhất của việc sử dụng Database Migration (Alembic) khi làm việc nhóm là gì? 

A. Giúp mã nguồn chạy nhanh hơn trên máy tính của các thành viên khác

B. Giúp ghi lại lịch sử thay đổi cấu trúc bảng, cho phép các thành viên đồng bộ cơ sở dữ liệu chỉ bằng một câu lệnh mà không cần làm thủ công

C. Giúp bảo mật mật khẩu của cơ sở dữ liệu khi gửi qua Internet

D. Giúp tự động sửa các lỗi cú pháp trong tập tin models.py.

Câu 7.5 Giả sử bạn đã định nghĩa xong model User và Document trong tập tin models.py. Để Alembic có thể "nhìn thấy" các định nghĩa này và tự động tạo tập tin script cập nhật, bạn bắt buộc phải thực hiện thao tác nào trong tập tin migrations/env.py? 

A. Chèn mật khẩu của PostgreSQL vào dòng target_metadata

B. Cài đặt lại thư viện psycopg2-binary

C. Import biến Base từ models.py và gán cho target_metadata = Base.metadata

D. Xóa bỏ thư mục venv và tạo lại từ đầu
-----
Bài sau: Ebook2LateX (8) - Nhập dữ liệu tự động

Ebook2LateX (8) - Nhập dữ liệu tự động
Bài trước: Ebook2LateX (7) - Tạo các bảng
-----
8. Nhập dữ liệu tự động
8.1 Nhập dữ liệu tự động
Sau các bài học trước, chúng ta đã thực hiện:

- Tạo cơ dữ liệu cho dự án

- Tạo các bảng dữ liệu

- Thiết lập quan hệ giữa các bảng

- Lưu lại trạng thái dự án vào hệ thống Git

- Đẩy dự án lên Github

- Biết sử dụng ORM (SQLAlchemy)

- Biết sử dụng data migration (Alembic)

Tuy nhiên, trong các bảng chưa có dữ liệu. Việc nhập dữ liệu thủ công vào các bảng sẽ mất nhiều thời gian.

Trong phần này chúng ta sẽ viết script để tự động nhập dữ liệu mẫu vào các bảng. 

Quá trình tự động nhập dữ liệu vào các bảng được gọi là seeding. Seeding có nghĩa thông thường là “gieo hạt”. Trong cơ sở dữ liệu nó là quá trình “gieo dữ liệu” vào các bảng.

Tại sao cần nhập dữ liệu tự động?

- Để tối ưu hóa thời gian và nguồn lực: Thay vì tiêu tốn hàng giờ để nhập liệu thủ công từng bản ghi qua pgAdmin, một script tự động có thể tạo ra hàng nghìn dữ liệu chuẩn xác chỉ trong vài giây, giúp lập trình viên tập trung vào việc viết mã logic

- Kiểm thử giao diện và trải nghiệm người dùng (UI/UX): Dữ liệu mẫu giúp mô phỏng "hình hài" thực tế của ứng dụng. Ví dụ, cho phép kiểm tra xem các công thức toán học dài có làm vỡ khung giao diện không, hay các tính năng phân trang, tìm kiếm và cuộn trang có hoạt động mượt mà hay không

- Đảm bảo tính nhất quán trong làm việc nhóm: Cung cấp một bộ dữ liệu chuẩn duy nhất cho tất cả thành viên. Điều này giúp loại bỏ tình trạng sai lệch dữ liệu giữa các máy tính cá nhân, giúp việc tái hiện lỗi (debug) và phối hợp phát triển trở nên đồng bộ

- Xác thực cấu trúc và các ràng buộc hệ thống: Quá trình đổ dữ liệu tự động là cách nhanh nhất để kiểm tra tính đúng đắn của thiết kế cơ sở dữ liệu, đảm bảo các mối quan hệ khóa ngoại và các ràng buộc dữ liệu hoạt động đúng như mong đợi

Các bước để tạo dữ liệu

Để thực hiện tạo dữ liệu, chúng ta sẽ xây dựng các script Python sử dụng chính các Model (Users, Documents, FormulaEntries, Logs) đã định nghĩa bằng SQLAlchemy.

- Bước 1: Khởi tạo kết nối Database, chúng ta sử dụng đối tượng Session từ SQLAlchemy để giao tiếp với PostgreSQL thông qua chuỗi kết nối đã cấu hình trong tập tin .env.

Bạn cần đảm bảo: trong tập tin /Ebook2LateX/backend/.evn, đã có chuỗi kết nối, ví dụ: DATABASE_URL=postgresql://postgres:p%40ssword1@localhost:5432/ebook2latex_db

(Lưu ý: Khác với khi làm việc với Alembic, Python sẽ báo lỗi nếu chúng ta mã hóa “@” thành “%%40”, nên chúng ta sẽ mã hóa “@” thành “%40”).

Bạn cũng cần đảm bảo đã cài đặt thư viện python-dotenv để đọc thông tin từ .evn. (Xem lại phần 7.2 Cài đặt). Nếu chưa cài đặt, bạn chạy lệnh sau:

pip install python-dotenv

Viết mã khởi tạo trong database.py

Trong thư mục backend, tạo thư mục app. Trong app tạo tập tin database.py với nội dung sau:

[database.py]

import os

from dotenv import load_dotenv

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base


# Tải các biến môi trường từ tập tin .env

load_dotenv()


# 1. Lấy chuỗi kết nối từ biến môi trường

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")


# 2. Tạo Engine: Đây là "nguồn" kết nối chính tới Database

engine = create_engine(SQLALCHEMY_DATABASE_URL)


# 3. Tạo SessionLocal: Mỗi thực thể của lớp này sẽ là một phiên làm việc database

# autocommit=False: Đảm bảo dữ liệu chỉ được lưu khi ta ra lệnh commit()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 4. Tạo Base class: Các models (User, Document...) sẽ kế thừa từ đây

Base = declarative_base()

Giải thích thêm về đoạn mã trên

- load_dotenv(): Hàm này đọc tập tin .env và đưa các cấu hình vào hệ thống, để Python có thể đọc được qua os.getenv

- create_engine: Đóng vai trò là trung tâm điều khiển. Nó giữ các kết nối thực tế tới PostgreSQL. Bạn chỉ nên tạo một Engine duy nhất cho toàn bộ ứng dụng

- sessionmaker: Đây là thành phần tạo ra các đối tượng Session. Mỗi khi Backend nhận được một yêu cầu (request) từ người dùng, chúng ta sẽ mở một Session từ thành phần này để truy vấn dữ liệu

- bind=engine: Kết nối thành phần tạo session này với Engine đã tạo ở trên

Liên kết Models với cấu trúc thư mục mới

Vì bạn vừa đưa tập tin database.py vào thư mục app, bạn cần đảm bảo tập tin models.py (nơi định nghĩa các bảng Users, Documents...) cũng nằm trong thư mục app này để đồng bộ.

Di chuyển tập tin models.py vào thư mục /backend/app/.

Mở tập tin models.py, tìm dòng from database import Base và sửa thành (nếu chưa có thì thêm):

from .database import Base  # Dấu chấm đại diện cho việc import cùng thư mục

[models.py]

import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Text, Numeric

from sqlalchemy.dialects.postgresql import UUID, JSONB

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from .database import Base



# Khởi tạo lớp Base để các Model kế thừa

Base = declarative_base()

...

Viết Script để tạo dữ liệu (seed.py)

Bây giờ chúng ta sẽ viết một tập tin Python để tự động tạo dữ liệu. Hãy tạo tập tin seed.py nằm trong thư mục /backend/ (cùng cấp với thư mục app).

Nội dung cho tập tin seed.py:

[seed.py]

import uuid

from app.database import SessionLocal

from app.models import User, Document, FormulaEntry


def seed_data():

    # 1. Khởi tạo phiên làm việc (Session)

    db = SessionLocal()

    

    try:

        print("Đang tạo dữ liệu...")


        # 2. Tạo dữ liệu cho bảng User

        # Lưu ý: Trong thực tế mật khẩu cần được băm (hash), ở đây ta nhập mật khẩu tượng trưng

        test_user = User(

            user_id=uuid.uuid4(),

            username_email="teo@dalat.edu.vn",

            password_hash="hashed_password_here",

            full_name="Lê Văn Tèo",

            role="Admin"

        )

        db.add(test_user)

        db.flush() # Đẩy dữ liệu tạm thời để lấy user_id cho bảng sau


        # 3. Tạo dữ liệu mẫu cho bảng Documents

        test_doc = Document(

            id=uuid.uuid4(),

            user_id=test_user.user_id,

            file_name="Giao_trinh_Toan_12.pdf",

            file_path_url="/uploads/toan12.pdf",

            status="Completed"

        )

        db.add(test_doc)

        db.flush()


        # 4. Tạo dữ liệu mẫu cho bảng FormulaEntries (Công thức LaTeX)

        formula = FormulaEntry(

            id=uuid.uuid4(),

            document_id=test_doc.id,

            latex_content=r"\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",

            order_index=1

        )

        db.add(formula)


        # 5. Xác nhận lưu toàn bộ thay đổi vào Database

        db.commit()

        print("Tạo dữ liệu thành công! Kiểm tra pgAdmin4 để xem kết quả.")


    except Exception as e:

        print(f"Có lỗi xảy ra: {e}")

        db.rollback() # Hoàn tác nếu có lỗi để tránh rác dữ liệu

    finally:

        db.close() # Luôn đóng kết nối sau khi xong


if __name__ == "__main__":

    seed_data()

Chạy lệnh Seeding

Sau khi viết xong tập tin seed.py, bạn mở Terminal tại thư mục /backend/ và chạy lệnh sau:

python seed.py

Sau bước này, bạn có thể mở pgAdmin 4, chuột phải vào các bảng và chọn View Data để xem kết quả là những dòng dữ liệu mẫu đầu tiên.


Cập nhật Git

Thực hiện commit vào Git để lưu lại trạng thái.

- Trong cửa sổ dòng lệnh (CMD), dấu nhắc lệnh đang ở thư mục gốc dự án (Ebook2LateX), nhập các lệnh sau:

(venv) D:\DuAn\Ebook2LateX>git status

HEAD detached at 4766c6a

Changes not staged for commit:

  (use "git add/rm <file>..." to update what will be committed)

  (use "git restore <file>..." to discard changes in working directory)

        deleted:    backend/models.py


Untracked files:

  (use "git add <file>..." to include in what will be committed)

        backend/app/

        backend/seed.py


no changes added to commit (use "git add" and/or "git commit -a")

(venv) D:\DuAn\Ebook2LateX>git add .

(venv) D:\DuAn\Ebook2LateX>git commit -m "feat: tao du lieu tu dong"

Cập nhật dự án lên Github

Kiểm tra kết nối giữa máy local với kho chứa ở xa?

Mở chương trình dòng lệnh, dấu nhắc tại thư mục dự án, gõ lệnh sau:

(venv) D:\DuAn\Ebook2LateX>git remote -v

origin  https://github.com/legiacong/Ebook2LateX.git (fetch)

origin  https://github.com/legiacong/Ebook2LateX.git (push)

Vậy là yên tâm để đẩy dự án lên Github:

(venv) D:\DuAn\Ebook2LateX>git push origin main

Ý nghĩa lệnh trên: Đẩy dự án lên repo có tên gọi tắt là origin, đẩy vào nhánh main.

8.2 Bài tập và câu hỏi
Bài tập

Bài tập 8a. Lập trình và cài đặt các nội dung trong phần lý thuyết.

Khi làm các bài tập, các bạn đừng sợ làm hỏng Database. Nếu làm sai, bạn có thể xóa database, tạo lại và chạy lệnh upgrade head cùng seed.py. Đó chính là sức mạnh của các công cụ bạn vừa học.

Bài tập 8b. Mở rộng cấu trúc (Schema Expansion)

Mục tiêu: Giúp người học hiểu cách thay đổi cấu trúc Database mà không làm mất dữ liệu hiện có.

Yêu cầu 1: Thêm tính năng "Yêu thích" (Likes/Stars):

- Yêu cầu: Thêm một bảng mới tên là UserFavorites để lưu việc người dùng đánh dấu các công thức (FormulaEntry) họ quan tâm

- Thao tác: Định nghĩa Model mới > Chạy alembic revision --autogenerate > alembic upgrade head

Yêu cầu 2: Quản lý phiên bản tài liệu:

- Yêu cầu: Thêm một cột version (kiểu Integer, mặc định là 1) vào bảng Documents

- Thao tác: Cập nhật models.py > Thực hiện migration để cập nhật database thực tế

Bài 8c: Truy vấn Nâng cao

Mục tiêu: Sử dụng Session và Relationship để lấy dữ liệu phức tạp.

Yêu cầu 1: Thống kê báo cáo (Reporting):

- Yêu cầu: Viết một script Python sử dụng SessionLocal để in ra danh sách tất cả các User, kèm theo số lượng tài liệu mà mỗi người đã tải lên

- Gợi ý: Sử dụng hàm func.count() trong SQLAlchemy

Yêu cầu 2: Tìm kiếm công thức:

- Yêu cầu: Viết một hàm nhận vào một từ khóa (ví dụ: "sqrt") và trả về tất cả các FormulaEntry có chứa từ khóa đó trong cột latex_content

Bài tập 8d. Seeding thực tế 

Mục tiêu: Làm quen với việc tạo dữ liệu mẫu số lượng lớn và ngẫu nhiên.

Yêu cầu 1: "Gieo dữ liệu" số lượng lớn với thư viện Faker:

- Thay vì nhập tay từng dòng như seed.py, hãy cài đặt thư viện Faker (pip install faker)

- Viết script tự động tạo ra 50 người dùng với tên và email ngẫu nhiên, mỗi người dùng có từ 2-5 tài liệu mẫu

Yêu cầu 2: Seeding từ tệp JSON:

- Tạo một tệp data.json chứa danh sách 10 công thức toán học

- Viết script seed_from_json.py đọc dữ liệu từ tập tin này và nạp vào bảng FormulaEntries

Câu hỏi

Câu 8.1 Trong dự án Python, thư viện python-dotenv được cài đặt và sử dụng nhằm mục đích chính là gì? 

A. Để tự động vẽ sơ đồ cơ sở dữ liệu cho dự án

B. Để nạp các biến môi trường (như chuỗi kết nối Database) từ tập tin .env vào hệ thống

C. Để mã hóa các tập tin hình ảnh thành định dạng LaTeX

D. Để gửi email thông báo cho người dùng khi có dữ liệu mới

Câu 8.2 Trong tập tin database.py, đối tượng engine được tạo ra bằng hàm create_engine đóng vai trò gì trong hệ thống?

A. Là nơi chứa các câu lệnh SQL dùng để tạo bảng

B. Là giao diện người dùng để nhập liệu thủ công vào PostgreSQL

C. Là "trung tâm điều khiển" giữ kết nối thực tế và quản lý việc giao tiếp giữa ứng dụng Python với PostgreSQL

D. Là một thư mục dùng để lưu trữ các tập tin PDF được tải lên

Câu 8.3 Tại sao chúng ta nên sử dụng SessionLocal (phiên làm việc) thay vì kết nối trực tiếp vào Database mỗi khi cần thao tác dữ liệu?

A. Để tăng tốc độ mạng Internet của máy tính

B. Để SQLAlchemy có thể quản lý các thay đổi một cách có hệ thống, cho phép xác nhận lưu (commit) hoặc hoàn tác (rollback) khi có lỗi xảy ra

C. Vì PostgreSQL không cho phép kết nối trực tiếp từ ngôn ngữ Python

D. Để tự động sao lưu dữ liệu lên hệ thống đám mây Github

Câu 8.4 Trong tập tin seed.py, nếu bạn muốn tạo một bản ghi cho bảng Document mà bảng này có khóa ngoại liên kết với bảng User, bạn cần phải thực hiện bước nào dưới đây để đảm bảo tính toàn vẹn dữ liệu? 

A. Phải tạo và lưu thông tin User trước, sau đó lấy user_id của người dùng đó để gán vào thuộc tính user_id của đối tượng Document

B. Chỉ cần nhập một tên người dùng bất kỳ vào bảng Document mà không cần quan tâm bảng User

C. Xóa bỏ ràng buộc khóa ngoại trong models.py trước khi chạy lệnh seeding

D. Phải chạy lệnh alembic upgrade head ngay bên trong tập tin seed.py

-----
Bài sau: Ebook2LateX (9) - Web services

Ebook2LateX (9) - Web services
Bài trước: Ebook2LateX (8) - Nhập dữ liệu tự động
-----
9. Web services
Tới phần này, chúng ta đã thực hiện được các việc sau:

- Thiết lập môi trường quản lý mã nguồn với Git

- Thiết lập hệ thống cơ sở dữ liệu

Trước khi bắt tay vào làm phần backend, chúng ta sẽ tìm hiểu về Dịch vụ web (web services).

9.1 Web services là gì?
Dịch vụ web (tiếng Anh là web services hay web service), để tiện trình bày sẽ dùng luôn từ gốc là web services.

Web services:

- Là một dịch vụ, do thiết bị điện tử này cung cấp cho một thiết bị điện tử khác, quá trình trao đổi được thực hiện trên môi trường web (world wide web, WWW, Internet, HTTP)

- Một máy server trên mạng sẽ luôn lắng nghe các yêu cầu từ một cổng cụ thể, để cung cấp các tài nguyên web như HTML, JSON, XML, images và tạo ra các dịch vụ cho các ứng dụng có sử dụng web services

Xem hình minh họa về web services,



So sánh trang web và web services

Ở một góc nhìn khác, kết quả trả về của một web services khá giống một trang web, tuy nhiên có một số khác biệt sau:

 

Trang web

Kết quả trả về của web services

Đối tượng sử dụng

Con người

Chương trình

Kiểu dữ liệu

Thông tin, dữ liệu

Thông tin, dữ liệu

Kiểu hiển thị

Thông tin con người có thể đọc được

Dữ liệu dạng XML, JSON

Một số định nghĩa khác về web service

- Web services là một hệ thống phần mềm, được thiết kế để hỗ trợ khả năng tương tác giữa các ứng dụng trên các máy tính khác nhau, thông qua mạng Internet, giao diện chung và sự gắn kết của nó được mô tả bằng XML

- Là tài nguyên phần mềm có thể xác định bằng địa chỉ URL

- Thực hiện các chức năng và đưa ra các thông tin người dùng yêu cầu

- Ứng dụng cơ bản của web services là tích hợp các hệ thống

- Các ứng dụng được tích hợp với cơ sở dữ liệu và các ứng dụng khác, người sử dụng sẽ giao tiếp với cơ sở dữ liệu để tiến hành phân tích và lấy dữ liệu

Xem hình minh họa,



- Web services là một tập hợp các giao thức và tiêu chuẩn mở được sử dụng để trao đổi dữ liệu giữa các ứng dụng hoặc giữa các hệ thống

- Các ứng dụng phần mềm được viết bằng các ngôn ngữ lập trình khác nhau hoặc chạy trên các nền tảng khác nhau, chúng có thể sử dụng các web services để trao đổi dữ liệu qua lại theo cách tương tự như liên lạc giữa các quá trình trên một máy tính

Xem hình minh họa,



Cơ chế hoạt động của Web services

Hệ thống web services cũng hoạt động dựa trên mô hình client-server. Hoạt động của web services được thể hiện ở hình sau:



Trong đó,

- Một hệ thống web services gồm hai thành phần chính là client (service consumer) và server (service provider). Chúng giao tiếp với nhau bằng giao thức HTTP, lấy hạ tầng Internet làm môi trường truyền. Lưu ý, client trong web services không phải là trình duyệt mà là ứng dụng web do lập trình viên đang xây dựng

- Server luôn ở trạng thái sẵn sàng đáp ứng các yêu cầu từ phía client

- Client gửi yêu cầu thông qua HTTP request tới server

- Server xử lý và gửi kết quả về client, thông qua HTTP response

- Có hai loại công nghệ web services được sử dụng là SOAP và REST. Hiện nay, REST được sử dụng phổ biến hơn

- Định dạng dữ liệu dùng để giao tiếp giữa client và server có thể ở dạng XML, JSON, text…v.v

9.2 Triển khai Web services trong Ebook2LateX
Để hiểu rõ hơn về Web services, chúng ta sẽ triển khai trong dự án Ebook2LateX.

Ứng dụng Ebook2LateX gồm 2 thành phần: Frontend và Backend.

Trong đó, thành phần Backend sẽ cung cấp các dịch vụ dưới dạng các Web services cho phần Frontend.

Thành phần Frontend và Backend sẽ giao tiếp với nhau thông qua Web services.

- Frontend sẽ sử dụng framework React

- Backend sẽ sử dụng framework FastAPI

Như vậy, React sẽ kết nối với FastAPI để trao đổi dữ liệu. Nghĩa là React sẽ sử dụng các dịch vụ web mà FastAPI cung cấp.

Cài đặt FastAPI

Như bạn đã biết, để làm ứng dụng web phía backend, bạn có thể lập trình từ đầu, có thể dùng CMS, hoặc có thể dùng framework.

Trong phần này chúng ta sẽ sử dụng framework FastAPI.

FastAPI là một web framework dựa trên Python, hỗ trợ lập trình bất đồng bộ mạnh mẽ.

FastAPI là framework mã nguồn mở, được Sebastián Ramírez người Colombia phát hành lần đầu 2018.

Để cài đặt và chạy được FastAPI, bạn cần có Python (phiên bản 3.8 trở lên) đã được cài đặt trên máy tính. Bạn có thể kiểm tra bằng lệnh: 

python -V

Ví dụ:

C:\Users\VIET HOANG - VTS>python -V

Python 3.14.0

Chúng ta đã có thư mục dự án là Ebook2LateX, đã có thư mục “môi trường ảo” là venv. Xem hình minh họa:



Chúng ta sẽ cài đặt FastAPI vào thư mục “môi trường ảo” (venv). Việc sử dụng môi trường ảo giúp cô lập các thư viện của dự án này, tránh xung đột với các dự án khác trên máy tính.

- Tại cửa sổ dòng lệnh (CMD), di chuyển dấu nhắc lệnh vào thư mục Ebook2LateX, kích hoạt môi trường ảo:

D:\DuAn\Ebook2LateX>venv\scripts\activate

(venv) D:\DuAn\Ebook2LateX>

- Gõ lệnh sau để cài đặt FastAPI: pip install "fastapi[all]"

(venv) D:\DuAn\Ebook2LateX>pip install "fastapi[all]"

Tham số “all” sẽ cài đặt luôn các thư viện bổ trợ cần thiết như uvicorn, pydantic, và các công cụ hỗ trợ xử lý dữ liệu form.

Uvicorn là gì?

Uvicorn là phần mềm web server, dùng để chạy các ứng dụng web viết bằng Python, hỗ trợ xử lý bất đồng bộ (ASGI - Asynchronous Server Gateway Interface).

Pydantic là gì?

Pydantic là một thư viện Python dùng để kiểm tra dữ liệu (validation) và xác thực dữ liệu (parsing) dựa trên các gợi ý kiểu (type hints).

Sau khi cài đặt xong, bạn nên chạy lệnh pip freeze > requirements.txt ở thư mục gốc để ghi lại danh sách các thư viện, giúp việc triển khai lên Docker sau này được đồng bộ. Như vậy trong dự án sẽ có 2 tập tin requirements.txt, một tập tin trong thư mục backend và một trong thư mục gốc. Bạn nên đọc thêm về mục đích của 2 tập tin requirements.txt này.

Viết đoạn mã nguồn đầu tiên (Hello World)

Trong thư mục backend, tạo tập tin có tên main.py và nhập vào đoạn mã sau (bạn nên tự tay gõ lại để nhớ và hiểu mã nguồn):

[main.py]

# Goi thu vien FastAPI

from fastapi import FastAPI

# Tao doi tuong app tu class FastAPI

app = FastAPI()

# Tao decorator cho app.get(“/”) 

@app.get("/")

# khi nguoi dung truy cap vao web root, goi ham sau

def read_root():

    return {"message": "Chao mung ban den voi Ebook2LateX!"}

Khởi chạy ứng dụng

Trở lại chương trình dòng lệnh (CMD), chạy lệnh sau để khởi động phần mềm web server:

uvicorn main:app --reload

Trong đó,

- main: là tên tập tin (main.py)

- app: là biến được khởi tạo trong code (app = FastAPI())

- --reload: Chế độ tự động tải lại server khi bạn thay đổi mã nguồn (rất hữu ích khi đang phát triển)

Nếu cửa sổ dòng lệnh xuất các thông tin sau là web server đã khởi chạy thành công:

…

←[32mINFO←[0m:     Started server process [←[36m62384←[0m]

←[32mINFO←[0m:     Waiting for application startup.

←[32mINFO←[0m:     Application startup complete.

(Đừng tắt cửa sổ dòng lệnh này, nếu tắt là tắt web server).

Kiểm tra kết quả

Sau khi khởi chạy ứng dụng thành công, bạn có thể mở trình duyệt web, truy cập vào địa chỉ sau:

http://127.0.0.1:8000

Bạn sẽ thấy câu chào mừng trên trình duyệt:

["Chao mung ban den voi Ebook2LateX!"]

Thực hiện commit trạng thái của dự án vào Git

D:\DuAn\Ebook2LateX>git status

        backend/main.py

        requirements.txt

D:\DuAn\Ebook2LateX>git add .

D:\DuAn\Ebook2LateX>git commit -m "feat: cai dat FastAPI"

9.3 Bài tập và câu hỏi
Bài tập

Bài tập 9a. Cài đặt các nội dung trong phần lý thuyết.

Bài tập 9b. Sử dụng File Explorer, tìm trong thư mục dự án (Ebook2LateX) và cho biết: sau khi cài đặt, mã nguồn của framework FastAPI được lưu ở đâu?

Câu hỏi

Câu 9.1 Web services là gì?

A. Là một loại phần cứng dùng để lưu trữ dữ liệu trên Internet

B. Là dịch vụ do thiết bị điện tử này cung cấp cho thiết bị điện tử khác thông qua môi trường mạng (WWW, HTTP)

C. Là một ngôn ngữ lập trình mới dùng để xây dựng giao diện người dùng

D. Là một hệ điều hành dành riêng cho các máy chủ lưu trữ tập tin PDF

Câu 9.2 Tại sao trong một dự án web, Backend và Frontend lại cần trao đổi dữ liệu thông qua định dạng JSON hoặc XML?

A. Vì đây là các định dạng giúp tăng dung lượng lưu trữ của ổ cứng

B. Vì đây là các ngôn ngữ lập trình có thể thực hiện các phép toán phức tạp

C. Vì đây là các định dạng dữ liệu chuẩn giúp các hệ thống khác nhau (như Python và React) có thể hiểu và làm việc với nhau

D. Vì các định dạng này giúp mã hóa dữ liệu để không ai có thể đọc được

Câu 9.3 Ai là người đã phát hành phiên bản đầu tiên của FastAPI vào năm 2018?

A. Guido van Rossum

B. Sebastián Ramírez

C. Mark Zuckerberg

D. Brendan Eich

Câu 9.4 Đặc điểm nào sau đây giúp FastAPI đạt được hiệu suất cao tương đương với Go hoặc Node.js?

A. Sử dụng giao thức SOAP để truyền tin

B. Dựa trên nền tảng Starlette, Pydantic và hỗ trợ lập trình bất đồng bộ (async)

C. Chỉ chạy được trên các máy chủ có cấu hình phần cứng cực mạnh

D. Không cần sử dụng bất kỳ thư viện hỗ trợ nào từ bên thứ ba

Câu 9.5 ASGI (Asynchronous Server Gateway Interface) là gì?

A. Là một thư viện dùng để vẽ biểu đồ toán học trong Python

B. Là chuẩn giao diện hỗ trợ lập trình bất đồng bộ cho các web server và ứng dụng Python

C. Là một hệ quản trị cơ sở dữ liệu thay thế cho PostgreSQL

D. Là một công cụ dùng để đóng gói ứng dụng vào Docker

Câu 9.6 Uvicorn đóng vai trò gì trong dự án web viết bằng Python?

A. Là một framework để viết mã nguồn Frontend

B. Là một hệ quản trị cơ sở dữ liệu quan hệ

C. Là một máy chủ Web (Web Server) chuẩn ASGI dùng để chạy ứng dụng FastAPI

D. Là trình soạn thảo mã nguồn chuyên dụng cho Python

Câu 9.7 Khi bạn thực hiện lệnh uvicorn main:app --reload trong terminal, tham số --reload có tác dụng gì đối với quá trình phát triển dự án?

A. Tự động cài đặt lại toàn bộ thư viện trong requirements.txt

B. Tự động sao lưu dữ liệu từ PostgreSQL sang một tập tin khác

C. Tự động phát hiện thay đổi trong mã nguồn và khởi động lại server để áp dụng thay đổi ngay lập tức

D. Xóa bỏ các tập tin rác trong thư mục venv/

Câu 9.8 Trong Python, "Decorator" thường được nhận diện bằng ký hiệu nào đặt ngay phía trên định nghĩa hàm?

A. Dấu #

B. Dấu $

C. Dấu &

D. Dấu @

-----
Bài sau: Ebook2LateX (10) - Lập trình Web services

Ebook2LateX (10) - Lập trình Web services
Bài trước: Ebook2LateX (9) - Web services
-----
10. Lập trình Web services
Tới bài học này, bạn đã thực hiện được các việc sau:

- Đã tạo môi trường ảo venv, cài đặt các thư viện cần thiết như FastAPI, Sqlalchemy, Alembic, và Python-dotenv

- Đã thiết lập kết nối với PostgreSQL, định nghĩa các bảng dữ liệu (Users, Documents, FormulaEntries, Logs) trong models.py và thực hiện migration để tạo bảng tự động

- Đã tạo tập tin main.py với mã nguồn "Hello World" và khởi chạy thành công Web server bằng Uvicorn

- Đã viết script seed.py để tự động nạp dữ liệu vào database

- Đã thực hiện commit các thay đổi và đẩy dự án lên GitHub

Trong phần này, chúng ta sẽ tìm hiểu một số nội dung sau:

- Hệ thống lại hoạt động của ứng dụng web trên nền tảng Python

- Lập trình minh họa để hiểu sâu về hoạt động của hệ thống

- Làm quen với việc tạo ra các services với kỹ thuật RESTful API

10.1 Mô hình client-server
Các ứng dụng web hoạt động dựa trên mô hình client-server.

Ý tưởng của mô hình client-server, đơn giản chỉ là: máy khách (client) gửi một yêu cầu (request) đến máy chủ (server), máy chủ sẽ xử lý và trả kết quả về cho máy khách.

Xem hình minh họa về mô hình client-server:



Mô hình client-server gồm một số thành phần:

- Client: khởi phát yêu cầu, gửi yêu cầu tới server, nhận kết quả từ server trả về. Client có thể là trình duyệt, ứng dụng viết bằng python/javascript hoặc bất kỳ ứng dụng nào mà có phát sinh ra HTTP request

- Server: có vai trò cung cấp dịch vụ, xử lý và trả về kết quả cho máy client

- Môi trường truyền thông tin: hạ tầng mạng (LAN, Internet), bao gồm cả phần cứng và phần mềm

- Giao thức truyền thông tin: các chuẩn công nghệ giúp giao tiếp và truyền thông tin giữa server-client. Ví dụ HTTP, HTTPS

Trong mô hình client-server, khi môi trường truyền đã được kết nối và sẵn sàng, thì client luôn là nơi khởi phát của ứng dụng. Client sẽ gửi một HTTP request tới server. Khi server nhận được request, nó sẽ xử lý và trả kết quả về cho client bằng một HTTP response

Client là thành phần chủ động. Server là thành phần bị động.

Chúng ta sẽ thấy cách hoạt động của một ứng dụng web rất khác so với cách hoạt động của chương trình trên máy cục bộ (ví dụ Microsoft Word). Trong Microsoft Word, mọi thao tác đều được thực hiện ngay trên máy người dùng, từ việc ra lệnh, xử lý và trả về kết quả. Cũng là chương trình xử lý văn bản, nhưng Google Docs là một ứng dụng hoạt động theo mô hình client-server. Nếu không có kết nối mạng thì Google Docs sẽ không hoạt động được.

Để hiểu rõ hơn về mô hình client-server, chúng ta sẽ cùng quan sát các bước của quá trình mở một ứng dụng web:

Do ứng dụng web hoạt động theo mô hình client-server, nên để có trang web trên trình duyệt, cần trải qua các bước sau:

Bước 1: Người dùng nhập địa chỉ trang web (URL) vào thanh địa chỉ. Ví dụ: http://example.com/hello.php

Bước 2: Trình duyệt dựa vào URL trong thanh địa chỉ, kết nối tới máy web server, gửi yêu cầu tới web server (ví dụ yêu cầu: gửi cho nội dung trang web hello.php)

Bước 3: Web server xử lý yêu cầu, gửi trả kết quả về cho trình duyệt (ví dụ nội dung trang web dưới dạng mã nguồn HTML, CSS và JavaScript)

Bước 4: Trình duyệt thực thi mã HTML, CSS, JavaScript và hiển thị trang web ra màn hình

Xem hình minh họa:



Chúng ta cùng thực hành, quan sát trình duyệt mở một ứng dụng web trên máy tính:

Bước 1. Mở trình duyệt web. Ví dụ Chrome

Bước 2. Nhập vào đường dẫn của trình duyệt địa chỉ một trang web, bấm Enter để trình duyệt lấy trang web từ máy server, và hiển thị nội dung ra màn hình. Ví dụ thanhnien.vn

Bước 3. Mở Developer tools của trình duyệt bằng một số cách sau:

- Bấm tổ hợp ba phím Ctrl+Shift+I

- hoặc bấm phím F12

- hoặc vào menu của trình duyệt tìm tới mục Developer tools

- hoặc bấm chuột phải vào trang web, chọn Inspect

Bước 4. Trong cửa sổ của Developer tools, bấm chuột vào mục Network

Bước 5. Quan sát sẽ thấy các tập tin HTML (thanhnien.vn), CSS (các tập tin có phần mở rộng là css), JavaScript (các tập tin có phần mở rộng là js) được server gửi về cho client

Bước 6. Bấm chuột vào các tập tin do server gửi về và quan sát nội dung của nó ở cửa sổ bên phải. Nhớ chọn mục Response

10.2 Hoạt động của ứng dụng web trên Python
Để trải nghiệm với ứng dụng web trên Python, chúng ta cùng thực hành và quan sát cách hệ thống này hoạt động.

Hình minh họa các thành phần của hệ thống:



Mô tả hoạt động của hệ thống:

- [Bước 1] Khởi chạy phần mềm Uvicorn, đây chính là phần mềm web server

- [Bước 2] Mở trình duyệt, gõ vào thanh địa chỉ: http://localhost:8000/ để gửi request tới Uvicorn, gửi tới cổng 8000, chuyển tới hàm get() của FastAPI.

- [Bước 3] Hàm get() của FastAPI sẽ xử lý yêu cầu từ client

- [Bước 4] FastAPI trả kết quả về cho trình duyệt

10.3 Bài tập và câu hỏi
Bài tập

Bài tập 10a. Hãy viết một chương trình đơn giản, để thực hiện việc sau:

- Mở trình duyệt, gửi một số qua thanh địa chỉ

- FastAPI nhận số từ trình duyệt, nhân với 10 rồi gửi trả lại cho trình duyệt

Bài tập 10b. Hãy viết một chương trình đơn giản, để thực hiện việc sau:

- Mở trình duyệt, gửi nhãn hiệu (brand) và kích thước (size) đôi giày bạn muốn mua (qua thanh địa chỉ), ví dụ hiệu Nike, kích thước 42

- FastAPI nhận brand và size từ trình duyệt, xử lý và trả về chuỗi: Bạn muốn mua giày [brand] kích thước [size] đúng không?

Câu hỏi

Câu 10.1 Trong mô hình client-server, thành phần nào đóng vai trò là nơi khởi phát yêu cầu (request)? 

A. Server 

B. Client 

C. Môi trường truyền tin 

D. Cơ sở dữ liệu

Câu 10.2 Đâu là các ví dụ về giao thức truyền thông tin dùng để kết nối giữa máy khách và máy chủ trong ứng dụng web? 

A. CPU và RAM 

B. LAN và Internet 

C. HTTP và HTTPS 

D. HTML và CSS

Câu 10.3 Phần mềm nào được sử dụng làm Web server chuẩn ASGI để chạy các ứng dụng FastAPI trong dự án web Python?

A. PostgreSQL 

B. React 

C. Uvicorn 

D. SQLAlchemy

Câu 10.4 Thứ tự các bước cơ bản để một ứng dụng web Python xử lý yêu cầu là gì? 

A. FastAPI trả kết quả -> Uvicorn nhận request -> Hàm xử lý thực thi

B. Khởi chạy Uvicorn -> Nhận request từ trình duyệt -> FastAPI xử lý -> Trả kết quả về trình duyệt

C. Mở trình duyệt -> FastAPI xử lý -> Khởi chạy Uvicorn -> Nhận kết quả

D. FastAPI nhận request trực tiếp từ trình duyệt -> Trả kết quả cho Uvicorn

Câu 10.5 Tại sao FastAPI được coi là một framework phù hợp cho các dịch vụ web hiện đại đòi hỏi hiệu suất cao? 

A. Vì nó chỉ chạy được trên hệ điều hành Windows

B. Vì nó hỗ trợ lập trình bất đồng bộ (async) mạnh mẽ và dựa trên nền tảng Starlette, Pydantic

C. Vì nó không cần cài đặt Python

D. Vì nó tự động kết nối với tất cả các loại cơ sở dữ liệu mà không cần cấu hình

Câu 10.6 Trong mã nguồn FastAPI, ký hiệu @app.get("/") (Decorator) có ý nghĩa gì? 

A. Khai báo một biến số nguyên cho ứng dụng

B. Định nghĩa một ghi chú (comment) không có giá trị thực thi

C. Điều hướng yêu cầu (routing) từ người dùng truy cập vào trang chủ (web root) để gọi hàm xử lý tương ứng

D. Dùng để cài đặt thư viện FastAPI vào máy tính

Câu 10.7 Khi đang phát triển ứng dụng, lệnh nào sau đây giúp bạn khởi chạy server sao cho mọi thay đổi trong mã nguồn main.py sẽ được tự động cập nhật ngay lập tức mà không cần khởi động lại thủ công? 

A. python main.py 

B. uvicorn main:app 

C. uvicorn main:app --reload 

D. pip install fastapi

Câu 10.8 Giả sử bạn có tập tin mã nguồn tên là api_service.py và biến khởi tạo ứng dụng là my_web_app = FastAPI(). Lệnh đúng để khởi chạy server này bằng Uvicorn là: 

A. uvicorn api_service:my_web_app 

B. uvicorn my_web_app:api_service 

C. python api_service.py 

D. run uvicorn api_service