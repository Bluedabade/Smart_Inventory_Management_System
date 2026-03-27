import streamlit as st
from modules.ui_helpers import init_app_state

st.set_page_config(page_title="Smart Inventory", layout="wide")
init_app_state()

st.title("📦 Smart Inventory Management System")
st.subheader("ระบบจัดการสต๊อกสินค้าและหมวดหมู่อัจฉริยะ")

st.write("เลือกเมนูที่ต้องการใช้งาน")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.page_link("pages/1_Show_All.py", label="📋 แสดงสินค้าทั้งหมด", use_container_width=True)
    st.page_link("pages/2_Add_Product.py", label="➕ เพิ่มสินค้า", use_container_width=True)

with col2:
    st.page_link("pages/3_Edit_Product.py", label="✏️ แก้ไขสินค้า", use_container_width=True)
    st.page_link("pages/4_Delete_Product.py", label="🗑️ ลบสินค้า", use_container_width=True)

with col3:
    st.page_link("pages/5_Search.py", label="🔍 ค้นหาสินค้า", use_container_width=True)

with col4:
    st.page_link("pages/7_Category.py", label="🌳 หมวดหมู่สินค้า", use_container_width=True)
    st.page_link("pages/8_Undo.py", label="↩️ Undo", use_container_width=True)

st.divider()

products = st.session_state.products
total_items = len(products)
total_quantity = sum(p["quantity"] for p in products)
total_value = sum(p["price"] * p["quantity"] for p in products)

m1, m2, m3 = st.columns(3)
m1.metric("จำนวนรายการสินค้า", total_items)
m2.metric("จำนวนคงเหลือรวม", total_quantity)
m3.metric("มูลค่าสินค้ารวม", f"{total_value:,.2f} บาท")