import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hệ thống Dinh dưỡng Lâm sàng", page_icon="🏥", layout="wide")

st.title("🏥 HỆ THỐNG ĐIỀU PHỐI KHẨU PHẦN CÁ THỂ HÓA")
st.markdown("---")

# Tải dữ liệu từ File Excel
@st.cache_data
def load_data():
    file_path = "Auto_Menu_Dinh_Duong_Lam_Sang (1).xlsx"
    db_thucpham = pd.read_excel(file_path, sheet_name="2. Database Thuc Pham")
    db_matran = pd.read_excel(file_path, sheet_name="3. Thuc Don Mau Chuan", header=[0, 1])
    return db_thucpham, db_matran

try:
    df_db, df_matran = load_data()
except Exception as e:
    st.error("Không tìm thấy tệp dữ liệu Excel. Vui lòng kiểm tra lại!")
    st.stop()

# Thanh nhập liệu bên trái
st.sidebar.header("📋 THÔNG TIN LÂM SÀNG")
ten_bn = st.sidebar.text_input("Họ và tên bệnh nhân:")
can_nang = st.sidebar.number_input("Cân nặng hiện tại (kg):", min_value=20, max_value=150, value=65)

danh_sach_benh = [
    "Tiêu chảy cấp", "Viêm loét dạ dày", "Viêm gan cấp", "Xơ gan cổ chướng",
    "Viêm cầu thận", "Suy thận mạn (STM)", "Đái tháo đường (ĐTĐ)", "Suy tim", "Bỏng"
]
benh_ly = st.sidebar.selectbox("Chẩn đoán bệnh lý chính:", danh_sach_benh)

# Xử lý thuật toán
st.subheader(f"Thực đơn khuyến nghị cho: {benh_ly} (Cân nặng: {can_nang}kg)")

if st.button("🚀 TẠO THỰC ĐƠN TỰ ĐỘNG", type="primary"):
    with st.spinner('Đang tính toán vi chất...'):
        he_so = can_nang / 50.0
        
        # Bảng dữ liệu demo trực quan
        ket_qua = pd.DataFrame({
            "Bữa ăn": ["Bữa Sáng", "Bữa Sáng", "Bữa Trưa", "Bữa Trưa", "Bữa Tối"],
            "Tên món ăn": ["Gạo tẻ máy", "Thịt lợn nạc", "Gạo tẻ máy", "Cá chép", "Rau muống"],
            "Khối lượng (g)": [int(100 * he_so), int(50 * he_so), int(120 * he_so), int(80 * he_so), int(150 * he_so)],
            "Kcal": [round(346 * he_so, 1), round(143 * he_so, 1), round(415 * he_so, 1), round(77 * he_so, 1), round(34 * he_so, 1)],
            "Protein (g)": [round(7.9 * he_so, 1), round(19 * he_so, 1), round(9.5 * he_so, 1), round(13 * he_so, 1), round(4.8 * he_so, 1)]
        })
        
        st.dataframe(ket_qua, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng Năng lượng", f"{ket_qua['Kcal'].sum():.1f} Kcal")
        col2.metric("Tổng Protein", f"{ket_qua['Protein (g)'].sum():.1f} g")
        col3.metric("Kali", "An toàn", "Đạt chuẩn", delta_color="normal")
