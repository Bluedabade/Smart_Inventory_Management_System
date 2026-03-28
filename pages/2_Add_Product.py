import streamlit as st
from modules.ui_helpers import init_app_state, save_all, render_nav_buttons
from modules.inventory_manager import add_product
from modules.category_manager import get_main_categories, get_sub_categories

st.set_page_config(page_title="เพิ่มสินค้า", layout="wide")
init_app_state()

st.title("➕ เพิ่มสินค้า")

with st.sidebar:
    render_nav_buttons()

products = st.session_state.products
categories = st.session_state.categories

main_categories = get_main_categories(categories)

with st.form("add_product_form"):
    product_id = st.text_input(
    "รหัสสินค้า",
    placeholder="เช่น P001"
)
    st.info("กรุณากรอกรหัสสินค้าในรูปแบบ P001, P002, P003 และห้ามซ้ำกับรหัสเดิมในระบบ")
    name = st.text_input("ชื่อสินค้า")
    price = st.number_input("ราคา", min_value=0.0, format="%.2f")
    quantity = st.number_input("จำนวนคงเหลือ", min_value=0, step=1)

    if main_categories:
        selected_main = st.selectbox("เลือกหมวดหลัก", main_categories)

        sub_categories = get_sub_categories(categories, selected_main)

        if sub_categories:
            selected_sub = st.selectbox("เลือกหมวดย่อย", sub_categories)
        else:
            selected_sub = ""
            st.warning("หมวดหลักนี้ยังไม่มีหมวดย่อย")
    else:
        selected_main = ""
        selected_sub = ""
        st.warning("ยังไม่มีหมวดหมู่ในระบบ กรุณาไปเพิ่มหมวดหมู่ก่อน")

    submitted = st.form_submit_button("เพิ่มสินค้า")

if submitted:
    if not all([product_id.strip(), name.strip(), selected_main, selected_sub]):
        st.error("กรุณากรอกข้อมูลให้ครบ")
    else:
        category = f"{selected_main}>{selected_sub}"

        new_product = {
            "product_id": product_id.strip(),
            "name": name.strip(),
            "price": float(price),
            "quantity": int(quantity),
            "category": category
        }

        success, message = add_product(st.session_state.products, new_product)

        if success:
            st.session_state.undo_stack.push({
                "action": "add",
                "product": new_product
            })
            save_all()
            st.success(message)
            st.rerun()
        else:
            st.error(message)