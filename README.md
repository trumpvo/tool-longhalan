# tool-longhalan

Tool tra cứu hóa đơn theo MST người bán trong các file Excel (giao diện Tkinter).

## Chạy từ source

```bash
pip install -r requirements.txt
python main.py
```

## Build file .exe (Windows)

GitHub Actions (`.github/workflows/build-exe.yml`) tự build file `.exe` bằng PyInstaller
mỗi khi push lên nhánh `main`/`dev`, hoặc chạy thủ công qua tab **Actions → Build EXE →
Run workflow**.

Sau khi workflow chạy xong, vào tab **Actions**, chọn run tương ứng, tải artifact
**tool-longhalan-exe** để lấy file `tool-longhalan.exe`.

Build thủ công trên máy Windows:

```bash
pip install -r requirements.txt
pyinstaller --onefile --noconsole --name tool-longhalan main.py
```

File exe nằm ở `dist/tool-longhalan.exe`.
