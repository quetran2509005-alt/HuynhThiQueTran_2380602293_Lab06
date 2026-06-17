import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. LOGIC RAIL FENCE ĐƠN GIẢN (TỐI ƯU CÚ PHÁP)
# ==========================================
def encrypt_rail_fence(text, key):
    if key <= 1: return text
    
    # Tạo các hàng rào trống dạng danh sách chuỗi
    rails = [''] * key
    row = 0
    direction = 1  # 1 là đi xuống, -1 là đi lên

    for char in text:
        rails[row] += char
        row += direction
        
        # Đảo chiều khi chạm đỉnh hoặc đáy rào
        if row == 0 or row == key - 1:
            direction = -direction
            
    return ''.join(rails)

def decrypt_rail_fence(cipher, key):
    if key <= 1: return cipher
    
    # Bước 1: Xác định độ dài chuỗi của từng hàng rào trước
    pattern = [0] * len(cipher)
    row = 0
    direction = 1
    for i in range(len(cipher)):
        pattern[i] = row
        row += direction
        if row == 0 or row == key - 1:
            direction = -direction

    # Bước 2: Tách bản mã ngược lại vào các hàng rào
    rails = [''] * key
    idx = 0
    for r in range(key):
        count = pattern.count(r)
        rails[r] = cipher[idx : idx + count]
        idx += count

    # Bước 3: Đọc lại theo đường zigzag để khôi phục văn bản gốc
    result = []
    rail_indexes = [0] * key
    row = 0
    direction = 1
    for i in range(len(cipher)):
        current_rail = row
        current_char_idx = rail_indexes[current_rail]
        
        result.append(rails[current_rail][current_char_idx])
        rail_indexes[current_rail] += 1
        
        row += direction
        if row == 0 or row == key - 1:
            direction = -direction
            
    return ''.join(result)

# ==========================================
# 2. ĐIỀU KHIỂN GIAO DIỆN UI
# ==========================================
def handle_encrypt():
    text = entry_input.get()
    try:
        key = int(entry_key.get())
        if key <= 1: raise ValueError
    except ValueError:
        messagebox.showerror("Lỗi", "Số hàng (Key) phải là số nguyên lớn hơn 1!")
        return
        
    if not text:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản!")
        return
        
    entry_output.delete(0, tk.END)
    entry_output.insert(0, encrypt_rail_fence(text, key))

def handle_decrypt():
    cipher = entry_input.get()
    try:
        key = int(entry_key.get())
        if key <= 1: raise ValueError
    except ValueError:
        messagebox.showerror("Lỗi", "Số hàng (Key) phải là số nguyên lớn hơn 1!")
        return
        
    if not cipher:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập bản mã!")
        return
        
    entry_output.delete(0, tk.END)
    entry_output.insert(0, decrypt_rail_fence(cipher, key))

# ==========================================
# 3. GIAO DIỆN ĐỒ HỌA
# ==========================================
root = tk.Tk()
root.title("Trân Smartphone - Rail Fence Simple")
root.geometry("480x320")
root.resizable(False, False)

tk.Label(root, text="MẠ VÀ GIẢI MÃ RAIL FENCE ĐƠN GIẢN", font=("Arial", 12, "bold"), fg="#E65100").pack(pady=10)

frame = tk.Frame(root)
frame.pack(padx=20, fill="x")

tk.Label(frame, text="Nhập chuỗi:").grid(row=0, column=0, sticky="w", pady=5)
entry_input = tk.Entry(frame, width=40)
entry_input.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Số hàng (Key):").grid(row=1, column=0, sticky="w", pady=5)
entry_key = tk.Entry(frame, width=10)
entry_key.grid(row=1, column=1, sticky="w", pady=5)
entry_key.insert(0, "3")

tk.Label(frame, text="Kết quả:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="w", pady=15)
entry_output = tk.Entry(frame, width=40, font=("Arial", 9, "bold"), fg="#1B5E20")
entry_output.grid(row=2, column=1, pady=15)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Mã hóa", bg="#4CAF50", fg="white", width=12, font=("Arial", 9, "bold"), command=handle_encrypt).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Giải mã", bg="#FF9800", fg="white", width=12, font=("Arial", 9, "bold"), command=handle_decrypt).grid(row=0, column=1, padx=10)

root.mainloop()