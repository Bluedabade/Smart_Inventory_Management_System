import streamlit as st
from modules.ui_helpers import init_app_state, display_products, render_nav_buttons
from modules.category_tree import (
    get_main_categories,
    get_sub_categories,
    get_products_by_main_and_sub_category
)

st.set_page_config(page_title="หมวดหมู่สินค้า", layout="wide")
init_app_state()

st.title("📂 หมวดหมู่สินค้า")

with st.sidebar:
    render_nav_buttons()

products = st.session_state.products

main_categories = get_main_categories(products)

if main_categories:
    selected_main = st.selectbox("เลือกหมวดหลัก", main_categories)

    sub_categories = get_sub_categories(products, selected_main)

    if sub_categories:
        selected_sub = st.selectbox("เลือกหมวดย่อย", sub_categories)

        if st.button("แสดงสินค้า", type="primary"):
            result = get_products_by_main_and_sub_category(
                products,
                selected_main,
                selected_sub
            )
            display_products(result)
    else:
        st.warning("ไม่พบหมวดย่อยในหมวดหลักนี้")
else:
    st.warning("ยังไม่มีหมวดหมู่สินค้าในระบบ")