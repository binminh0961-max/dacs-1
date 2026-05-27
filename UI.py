import tkinter as tk
import customtkinter as ctk
import requests

# Cấu hình giao diện hệ thống
ctk.set_default_color_theme("blue") # Bộ màu chủ đạo

class ModernRealEstateApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Cấu hình cửa sổ chính
        self.title("Hệ Thống Quản Lý Bất Động Sản")
        self.geometry("750x600")
        self.resizable(False, False)

        # Chia bố cục thành 2 phần: Sidebar (Trái) và Main Content (Phải)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- 1. SIDEBAR (THANH ĐIỀU HƯỚNG TRÁI) ----------------
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False) # Cố định kích thước sidebar

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="VREAL AI", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Nút tính năng
        self.them = ctk.CTkButton(self.sidebar_frame, text="Thêm", fg_color="blue")
        self.sua = ctk.CTkButton(self.sidebar_frame, text="Sửa", fg_color="blue")
        self.xoa = ctk.CTkButton(self.sidebar_frame, text="Xóa", fg_color="blue")
        self.them.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.sua.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.xoa.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Bộ chuyển đổi giao diện Sáng/Tối
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Chế độ giao diện:", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(180, 0), sticky="w")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"], command=self.change_appearance_mode, fg_color="blue")
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.appearance_mode_optionemenu.set("Dark")

        # ---------------- 2. MAIN CONTENT (VÙNG NHẬP LIỆU & KẾT QUẢ) ----------------
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)

        # Tiêu đề chính
        self.title_label = ctk.CTkLabel(self.main_frame, text="CÔNG CỤ ĐỊNH GIÁ BẤT ĐỘNG SẢN CHUYÊN SÂU", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # --- FORM NHẬP LIỆU (Bên trái vùng chính) ---
        self.form_frame = ctk.CTkFrame(self.main_frame, width=350, corner_radius=10)
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 20))

        # Ô nhập Diện tích
        self.lbl_area = ctk.CTkLabel(self.form_frame, text="Diện tích (m²):", font=ctk.CTkFont(size=13))
        self.lbl_area.grid(row=0, column=0, padx=15, pady=(15, 0), sticky="w")
        self.entry_area = ctk.CTkEntry(self.form_frame, placeholder_text="Ví dụ: 75.5", width=250)
        self.entry_area.grid(row=1, column=0, padx=15, pady=(5, 10), sticky="ew")

        # Ô nhập Số phòng ngủ
        self.lbl_bedrooms = ctk.CTkLabel(self.form_frame, text="Số phòng ngủ:", font=ctk.CTkFont(size=13))
        self.lbl_bedrooms.grid(row=2, column=0, padx=15, pady=0, sticky="w")
        self.entry_bedrooms = ctk.CTkEntry(self.form_frame, placeholder_text="Ví dụ: 3", width=250)
        self.entry_bedrooms.grid(row=3, column=0, padx=15, pady=(5, 10), sticky="ew")

        # Ô nhập Mã khu vực
        self.lbl_location = ctk.CTkLabel(self.form_frame, text="Mã khu vực (Vị trí):", font=ctk.CTkFont(size=13))
        self.lbl_location.grid(row=4, column=0, padx=15, pady=0, sticky="w")
        self.entry_location = ctk.CTkEntry(self.form_frame, placeholder_text="Nhập 1 hoặc 2", width=250)
        self.entry_location.grid(row=5, column=0, padx=15, pady=(5, 20), sticky="ew")

        # Nút kích hoạt AI dự đoán
        self.btn_predict = ctk.CTkButton(self.form_frame, text="Tính Toán Giá AI", font=ctk.CTkFont(weight="bold"), fg_color="#2EA44F", hover_color="#22863A", command=self.call_ai_prediction)
        self.btn_predict.grid(row=6, column=0, padx=15, pady=(0, 15), sticky="ew")

        # --- KHU VỰC HIỂN THỊ KẾT QUẢ (Bên phải vùng chính) ---
        self.result_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color=("#EAEAEA", "#2B2B2B"))
        self.result_frame.grid(row=1, column=1, sticky="nsew")
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=1)

        self.lbl_res_title = ctk.CTkLabel(self.result_frame, text="KẾT QUẢ PHÂN TÍCH AI", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_res_title.grid(row=0, column=0, pady=15)

        # Hộp hiển thị số tiền nổi bật
        self.lbl_price_output = ctk.CTkLabel(self.result_frame, text="-- Tỷ VNĐ", font=ctk.CTkFont(size=28, weight="bold"), text_color="#2EA44F")
        self.lbl_price_output.grid(row=1, column=0, pady=20)

        # Trạng thái thông báo hệ thống (Đã sửa ngoặc chuẩn xác)
        self.lbl_status = ctk.CTkLabel(self.result_frame, text="Hệ thống sẵn sàng", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray")
        self.lbl_status.grid(row=2, column=0, pady=15)

    # ---------------- 3. XỬ LÝ NGHIỆP VỤ & UX LOGIC ----------------
    def call_ai_prediction(self):
        try:
            area = float(self.entry_area.get())
            bedrooms = int(self.entry_bedrooms.get())
            location = int(self.entry_location.get())

            self.lbl_status.configure(text="AI đang tính toán...", text_color="#1F6AA5")
            self.update_idletasks()

            payload = {
                "area": area,
                "bedrooms": bedrooms,
                "location_code": location
            }

            url = "http://localhost:8000/api/predict-price"
            response = requests.post(url, json=payload, timeout=5)

            if response.status_code == 200:
                data = response.json()
                predicted_price = data.get("predicted_price_billion_vnd")

                self.lbl_price_output.configure(text=f"{predicted_price} Tỷ VNĐ")
                self.lbl_status.configure(text="Định giá thành công!", text_color="#2EA44F")
            else:
                self.show_error_ux(f"Lỗi hệ thống: Code {response.status_code}")

        except ValueError:
            self.show_error_ux("Lỗi: Vui lòng nhập số hợp lệ vào các ô!")
        except requests.exceptions.RequestException:
            self.show_error_ux("Lỗi: Không kết nối được tới AI Service (Port 8000)!")

    def show_error_ux(self, message):
        self.lbl_price_output.configure(text="Thất bại")
        self.lbl_status.configure(text=message, text_color="#D9381E")

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = ModernRealEstateApp()
    app.mainloop()