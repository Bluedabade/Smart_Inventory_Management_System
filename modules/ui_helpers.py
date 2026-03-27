import streamlit as st
from modules.file_manager import load_products, save_products
from modules.undo_stack import UndoStack
from modules.category_manager import load_categories, save_categories

FILE_PATH = "data/products.txt"
CATEGORY_FILE_PATH = "data/categories.txt"


def init_app_state():
    if "products" not in st.session_state:
        st.session_state.products = load_products(FILE_PATH)

    if "categories" not in st.session_state:
        st.session_state.categories = load_categories(CATEGORY_FILE_PATH)

    if "undo_stack" not in st.session_state:
        st.session_state.undo_stack = UndoStack()


def save_all():
    save_products(FILE_PATH, st.session_state.products)
    save_categories(CATEGORY_FILE_PATH, st.session_state.categories)


def display_products(products):
    if not products:
        st.warning("ไม่พบข้อมูลสินค้า")
        return
    st.dataframe(products, use_container_width=True)


def render_nav_buttons():
    st.page_link("app.py", label="🏠 หน้าแรก", use_container_width=True)
    st.page_link("pages/1_Show_All.py", label="📋 แสดงสินค้าทั้งหมด", use_container_width=True)
    st.page_link("pages/2_Add_Product.py", label="➕ เพิ่มสินค้า", use_container_width=True)
    st.page_link("pages/3_Edit_Product.py", label="✏️ แก้ไขสินค้า", use_container_width=True)
    st.page_link("pages/4_Delete_Product.py", label="🗑️ ลบสินค้า", use_container_width=True)
    st.page_link("pages/5_Search.py", label="🔍 ค้นหาและเรียงลำดับสินค้า", use_container_width=True)
    st.page_link("pages/7_Category.py", label="📂 จัดการหมวดหมู่สินค้า", use_container_width=True)
    st.page_link("pages/8_Undo.py", label="↩️ Undo", use_container_width=True)