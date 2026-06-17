import tkinter as tk
from tkinter import messagebox
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

# ==========================================
# 1. LOGIC THUẬT TOÁN RSA
# ==========================================
# Khởi tạo biến toàn cục để lưu khóa
private_key = None
public_key = None

def generate_keys():
    global private_key, public_key
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    
    # Hiển thị thông báo và hiển thị một phần khóa lên giao diện
    entry_pub.delete(0, tk.END)
    entry_pub.insert(0, public_key.export_key().decode()[:50] + "...")
    messagebox.showinfo("Thành công", "Đã tạo cặp khóa Public/Private 2048-bit mới!")

def encrypt_rsa():
    if public_key is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng tạo khóa trước khi mã hóa!")
        return
    
    plaintext = entry_input.get().encode('utf-8')
    if not plaintext:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản cần mã hóa!")
        return

    cipher_rsa = PKCS1_v1_5.new(public_key)
    ciphertext = cipher_rsa.encrypt(plaintext)
    
    # Chuyển sang Base64 để hiển thị được dưới dạng chuỗi văn bản
    encoded_cipher = base64.b64encode(ciphertext).decode('utf-8')
    entry_output.delete(0, tk.END)
    entry_output.insert(0, encoded_cipher)

def decrypt_rsa():
    if private_key is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng tạo khóa trước!")
        return
    
    try:
        encoded_cipher = entry_input.get()
        if not encoded_cipher:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập bản mã cần giải mã!")
            return
            
        ciphertext = base64.b64decode(encoded_cipher)
        cipher_rsa = PKCS1_v1_5.new(private_key)
        
        # sentinel là giá trị trả về nếu giải mã lỗi
        sentinel = b"Giai ma that bai!"
        decrypted_text = cipher_rsa.decrypt(ciphertext, sentinel)
        
        entry_output.delete(0, tk.END)
        entry_output.insert(0, decrypted_text.decode('utf-8'))
    except Exception as e:
        messagebox.showerror("Lỗi", "Bản mã không hợp lệ hoặc sai khóa!")

# ==========================================
# 2. THIẾT KẾ GIAO DIỆN UI
# ==========================================
root = tk.Tk()
root.title(" RSA Security")
root.geometry("600x450")
root.resizable(False, False)

# Tiêu đề
tk.Label(root, text="MÃ HÓA & GIẢI MÃ RSA (2048-BIT)", font=("Arial", 14, "bold"), fg="#1565C0").pack(pady=15)

frame = tk.Frame(root)
frame.pack(padx=30, fill="x")

# Nút tạo khóa
tk.Button(frame, text="1. TẠO CẶP KHÓA (GENERATE KEYS)", bg="#7E57C2", fg="white", font=("Arial", 9, "bold"), command=generate_keys).grid(row=0, column=0, columnspan=2, sticky="we", pady=10)

# Hiển thị Public Key tạm thời
tk.Label(frame, text="Public Key (Rút gọn):").grid(row=1, column=0, sticky="w")
entry_pub = tk.Entry(frame, width=50, fg="grey")
entry_pub.grid(row=1, column=1, pady=5)

# Input
tk.Label(frame, text="Dữ liệu nhập vào:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=15)
entry_input = tk.Entry(frame, width=50, font=("Arial", 10))
entry_input.grid(row=2, column=1, pady=15)

# Output
tk.Label(frame, text="Kết quả trả về:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=15)
entry_output = tk.Entry(frame, width=50, font=("Arial", 10), fg="#2E7D32")
entry_output.grid(row=3, column=1, pady=15)

# Buttons Actions
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="MÃ HÓA (ENCRYPT)", bg="#1E88E5", fg="white", width=20, font=("Arial", 10, "bold"), command=encrypt_rsa).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="GIẢI MÃ (DECRYPT)", bg="#FB8C00", fg="white", width=20, font=("Arial", 10, "bold"), command=decrypt_rsa).grid(row=0, column=1, padx=10)

tk.Label(root, text="Lưu ý: Bạn cần tạo khóa trước khi thực hiện mã hóa.", font=("Arial", 8, "italic"), fg="red").pack()

root.mainloop()