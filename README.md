# KHTN Math Trainer - Demo

Ứng dụng Windows thử nghiệm dành cho học sinh lớp 8 đang ôn thi chuyên Toán lớp 9.

## Demo hiện có

- 3 bài mẫu: luyện nền, bài KHTN và kỹ năng trình bày.
- Hai cách viết: **Nháp nhanh** và **Trình bày đi thi**.
- Nhận dạng một số cách viết tự nhiên như `chc`, `ntc`, `scp`.
- Hiện cách app đang hiểu câu trả lời.
- Gợi ý nhẹ, kiểm tra từng bước và lưu tiến độ offline.

Đây là bản demo kỹ thuật, chưa phải công cụ chấm mọi lời giải Toán tự do.

## Tải bản Windows

Mở tab **Actions**, chọn workflow **Build Windows demo**, rồi tải artifact
`KHTN-Math-Trainer-Demo-Windows`. Sau khi tạo tag `v0.1.0`, file `.exe` cũng được
đưa vào mục **Releases**.

## Chạy từ mã nguồn

```bash
python app.py
```

Ứng dụng dùng Tkinter có sẵn trong Python và không cần cài thêm thư viện khi chạy từ source.

## Tự build trên Windows

Chạy file:

```text
build_windows.bat
```

File tạo ra nằm tại `dist/KHTN-Math-Trainer-Demo.exe`.

## Kiểm thử

```bash
python -m unittest -v
```

## Phạm vi tiếp theo

1. Mở rộng bộ câu OFFICIAL và INFORMAL.
2. Thêm máy kiểm tra biến đổi đại số.
3. Nhập đầy đủ bài phương trình nghiệm nguyên KHTN đã kiểm duyệt.
4. Sổ lỗi và lịch ôn lại.
