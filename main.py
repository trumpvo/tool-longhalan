import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd

def chon_thu_muc():
    folder = filedialog.askdirectory(title="Chọn thư mục chứa các file Excel hóa đơn")
    if folder:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder)

def copy_ket_qua():
    noi_dung = txt_ket_qua.get("1.0", tk.END).strip()
    if noi_dung:
        root.clipboard_clear()
        root.clipboard_append(noi_dung)
        lbl_status.config(text="Đã copy toàn bộ kết quả vào bộ nhớ tạm!", fg="green")

def tim_kiem():
    folder = entry_folder.get().strip()
    mst_can_tim = entry_mst.get().strip()

    if not folder or not os.path.isdir(folder):
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn thư mục chứa file Excel.")
        return
    if not mst_can_tim:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập MST người bán cần tìm.")
        return

    mst_chuan = mst_can_tim.lstrip("0")

    # Xóa kết quả cũ trên màn hình
    txt_ket_qua.delete("1.0", tk.END)
    lbl_status.config(text="Đang quét dữ liệu, vui lòng đợi...", fg="blue")
    root.update()

    tong_so_hd = 0
    so_file_da_quet = 0

    for file_name in os.listdir(folder):
        if file_name.endswith(".xlsx") and not file_name.startswith("~$"):
            file_path = os.path.join(folder, file_name)
            try:
                df_raw = pd.read_excel(file_path, header=None, dtype=str)
                so_file_da_quet += 1

                header_row = None
                col_idx = None

                # Tự dò dòng tiêu đề trong 15 dòng đầu
                for idx, row in df_raw.head(15).iterrows():
                    for c_idx, val in enumerate(row):
                        if pd.notna(val) and "mst người bán" in str(val).lower():
                            header_row = idx
                            col_idx = c_idx
                            break
                    if header_row is not None:
                        break

                if header_row is not None:
                    df = df_raw.iloc[header_row + 1:].copy()
                    df.columns = [str(c).replace("\n", " ").strip() for c in df_raw.iloc[header_row]]
                    cot_mst_thuc_te = df.columns[col_idx]

                    # Chuẩn hóa MST để so sánh (bỏ khoảng trắng, đuôi .0 và số 0 đầu)
                    mst_series = (
                        df[cot_mst_thuc_te]
                        .astype(str)
                        .str.strip()
                        .str.replace(r"\.0$", "", regex=True)
                        .str.lstrip("0")
                    )

                    df_loc = df[mst_series.str.contains(mst_chuan, na=False)]

                    for _, row in df_loc.iterrows():
                        tong_so_hd += 1
                        txt_ket_qua.insert(tk.END, f"=== HÓA ĐƠN #{tong_so_hd} (File: {file_name}) ===\n")
                        for col_name, val in row.items():
                            # Chỉ in các cột có dữ liệu
                            if pd.notna(val) and str(val).strip() != "":
                                txt_ket_qua.insert(tk.END, f"  • {col_name}: {str(val).strip()}\n")
                        txt_ket_qua.insert(tk.END, "\n")
                        root.update()

            except Exception as e:
                txt_ket_qua.insert(tk.END, f"[Lỗi đọc file {file_name}]: {e}\n\n")

    if tong_so_hd == 0:
        lbl_status.config(text=f"Đã quét {so_file_da_quet} file. Không tìm thấy kết quả.", fg="red")
        txt_ket_qua.insert(tk.END, f"Không tìm thấy MST '{mst_can_tim}' trong {so_file_da_quet} file.")
    else:
        lbl_status.config(text=f"Hoàn tất! Tìm thấy {tong_so_hd} hóa đơn trong {so_file_da_quet} file.", fg="green")

# Giao diện người dùng
root = tk.Tk()
root.title("Tra cứu Hóa đơn theo MST")
root.geometry("720x520")

# Khung chọn thư mục
frame_top = tk.Frame(root)
frame_top.pack(fill="x", padx=15, pady=(12, 5))

tk.Label(frame_top, text="Thư mục Excel:", width=14, anchor="w").pack(side="left")
entry_folder = tk.Entry(frame_top)
entry_folder.pack(side="left", expand=True, fill="x", padx=(0, 5))
tk.Button(frame_top, text="Chọn...", command=chon_thu_muc).pack(side="right")

# Khung nhập MST và nút bấm
frame_mid = tk.Frame(root)
frame_mid.pack(fill="x", padx=15, pady=5)

tk.Label(frame_mid, text="MST người bán:", width=14, anchor="w").pack(side="left")
entry_mst = tk.Entry(frame_mid)
entry_mst.pack(side="left", expand=True, fill="x", padx=(0, 5))
entry_mst.bind("<Return>", lambda event: tim_kiem())  # Cho phép bấm Enter để tìm

tk.Button(
    frame_mid, text="Tìm kiếm", command=tim_kiem,
    bg="#0078D7", fg="white", font=("Arial", 9, "bold"), width=10
).pack(side="left", padx=(0, 5))

tk.Button(frame_mid, text="Copy hết", command=copy_ket_qua, width=9).pack(side="right")

# Dòng trạng thái
lbl_status = tk.Label(root, text="Nhập MST và bấm Tìm kiếm (hoặc Enter).", fg="gray", anchor="w")
lbl_status.pack(fill="x", padx=15, pady=(2, 5))

# Khung hiển thị kết quả dạng text có thanh cuộn
txt_ket_qua = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
txt_ket_qua.pack(expand=True, fill="both", padx=15, pady=(0, 15))

root.mainloop()
